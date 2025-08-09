import time
from playwright.sync_api import Playwright, sync_playwright, TimeoutError
def scroll_to_bottom(page, max_scrolls=100):
    last_height = 0
    for i in range(max_scrolls):
        print(f"Scrolling ({i+1}/{max_scrolls})...")
        page.mouse.wheel(0, 10000)  # simulate scrolling
        time.sleep(2)  # wait for new content

        # check if more content was loaded
        new_height = page.evaluate("() => document.documentElement.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom — all videos are loaded.")
            break
        last_height = new_height


def skip_ads(page):
    try:
        if page.locator(".ad-showing").is_visible():
            print("Ad is playing...")
            try:
                page.wait_for_selector("button:has(span.ytp-skip-ad-button__icon)", timeout=10000)
                skip_btn = page.locator("button:has(span.ytp-skip-ad-button__icon)")
                if skip_btn.is_visible():
                    print("Ad detected. Skipping...")
                    skip_btn.click()
                    time.sleep(1)
            except TimeoutError:
                print("Ad playing but no skip button appeared.")

            while page.locator(".ad-showing").is_visible():
                print("Waiting for ad to finish...")
                time.sleep(1)
        else:
            print("No ad is playing.")
    except Exception as e:
        print(f"Ad error: {e}")


def try_get_transcript(page, retries=3):
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} to open transcript...")
        try:
            time.sleep(2)
            try:
                page.get_by_role("button", name="...more").click(timeout=3000)
            except:
                page.locator("tp-yt-paper-button#expand").click(timeout=3000)
            time.sleep(1)

            transcript_btn = page.get_by_role("button", name="Show transcript")
            if transcript_btn.is_visible():
                transcript_btn.click()
                time.sleep(2)

                if page.get_by_title("Transcript").is_visible():
                    print("Transcript panel opened.")
                    return True

        except Exception as e:
            print(f"Transcript attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    print("Transcript not found.")
    return False

def safe_goto(page, url, timeout=60000, retries=10):
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Navigating to {url}...")
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            return True
        except TimeoutError:
            print(f"Timeout on attempt {attempt + 1}")
            time.sleep(2)
    return False

def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    print("Navigating to MrBeastGaming videos...")
    if not safe_goto(page, "https://www.youtube.com/@MrBeastGaming/videos"):
        print("Failed to open channel page.")
        context.close()
        browser.close()
        return []
    scroll_to_bottom(page)
    time.sleep(5)

    video_links = page.locator('a[href^="/watch?v="]').all()
    print(f"Found {len(video_links)} video links.")
    seen = set()
    results = []

    print(f"Found {len(video_links)} video links.")
    for link in video_links:
        href = link.get_attribute("href")
        if not href or href in seen:
            continue
        seen.add(href)
        video_url = f"https://www.youtube.com{href}"
        print(f"\nOpening {video_url}")
        page.goto(video_url)
        time.sleep(4)

        skip_ads(page)

        try:
            if page.get_by_role("button", name="Play").is_visible():
                print("Video is paused. Clicking play...")
                page.get_by_role("button", name="Play").click()
                time.sleep(1)
        except:
            pass

        success = try_get_transcript(page)
        if success:
            print("Transcript available.")
            title = page.title()
            lines = page.locator("ytd-transcript-segment-renderer").all_inner_texts()
            transcript = "\n".join(lines)

            # ✅ Just print out the result as you requested
            print("\nTITLE:", title)
            print("URL:", video_url)
            print("TRANSCRIPT:\n", transcript[:1000], "\n...")  # trimmed for readability

            results.append({
                "title": title,
                "url": video_url,
                "transcript": transcript
            })
        else:
            print("Skipping video. No transcript.")

        print("Returning to channel...")
        page.goto("https://www.youtube.com/@MrBeastGaming/videos")
        time.sleep(5)

    context.close()
    browser.close()
    return results



from playwright.sync_api import sync_playwright, TimeoutError
import time

def scrape_transcripts(channel_url, max_videos=5, max_attempts=2):
    results = []  # to store dictionaries of scraped videos

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to channel...")
        page.goto(channel_url)
        page.wait_for_load_state("networkidle")
        time.sleep(14)  # increased pause

        # Scroll to load more videos
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            time.sleep(3)  # increased pause

        print("Finding video links...")
        video_elements = page.locator('ytd-rich-grid-media a#thumbnail')
        count = video_elements.count()
        print(f"Found {count} videos, processing {min(count, max_videos)}...")

        for i in range(min(count, max_videos)):
            href = video_elements.nth(i).get_attribute('href')
            if not href:
                continue
            video_url = f"https://www.youtube.com{href}"
            print(f"\nStarting: {video_url}")

            # Prepare retry loop
            for attempt in range(1, max_attempts + 1):
                print(f"Attempt {attempt}...")
                attempt_failed = False
                transcript = ""
                title = ""
                video_page = None

                try:
                    video_page = context.new_page()
                    video_page.goto(video_url)
                    video_page.wait_for_load_state("networkidle")
                    time.sleep(5)  # pause after load

                    # get title
                    try:
                        title = video_page.locator("h1.title yt-formatted-string").inner_text(timeout=5000)
                    except Exception:
                        title = "Unknown Title"

                    # open transcript
                    video_page.get_by_role("button", name="...more").click(timeout=7000)
                    time.sleep(1)
                    video_page.get_by_role("button", name="Show transcript").click(timeout=7000)
                    time.sleep(3)

                    transcript = video_page.locator("ytd-transcript-renderer").inner_text(timeout=7000)
                    print(f"Transcript captured (length {len(transcript)} chars).")
                except TimeoutError as e:
                    print(f"Timeout/Element not found: {e}")
                    attempt_failed = True
                except Exception as e:
                    print(f"Error: {e}")
                    attempt_failed = True
                finally:
                    if video_page:
                        video_page.close()

                if not attempt_failed:
                    break  # success, skip further retries
                else:
                    print("Retrying...")

            # save result
            results.append({
                "title": title,
                "url": video_url,
                "transcript": transcript or "Transcript not available."
            })

        context.close()
        browser.close()

    return results



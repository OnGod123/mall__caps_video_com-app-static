import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # or directly: openai.api_key = "sk-..."

def analyze_video_with_openai(title, transcript):
    prompt = f"""
You are an expert video content analyst. Below is the title and transcript of a YouTube video.

Your task:
1. Analyze what this video is about.
2. Provide a short summary.
3. List 3-5 bullet points on key ideas or scenes.
4. Guess what type of video it is (tutorial, vlog, gaming, entertainment, etc).
5. Mention the intended audience (kids, gamers, entrepreneurs, etc).
6. Output must be JSON.

Title: {title}

Transcript:
{transcript[:4000]}  # truncate if too long
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You analyze YouTube video content for insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"OpenAI Error: {str(e)}"

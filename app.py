import os
import streamlit as st
import google.generativeai as genai
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi


from dotenv import load_dotenv
load_dotenv() ### Loading all env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
You are a Youtube video summarizer. You will be taking the transcript text \
and summarizing the entire video and providing summary in points within \
300 words.
Do not provide anything out of the transcript.

Transcript : """

### Getting summary from google gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

### Getting transcript data
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract.video_id(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages = ["en", "hi"])
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

st.title("VidScribe")
youtube_link = st.text_input('Enter YouTube Video link:')

if youtube_link:
    video_id = extract.video_id(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width = True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("### Detailed Notes")
        st.write(summary)
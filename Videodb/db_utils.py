import streamlit as st
from videodb import connect
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

openai_api_key = os.getenv("openai_api_key")
videodb_api_key = os.getenv("videodb_api_key")

client = OpenAI(api_key = openai_api_key)

conn = connect(api_key=videodb_api_key)
coll = conn.get_collection()

# Function to upload videos
def upload_videos_to_database():
    for link in st.session_state.youtube_links:
        try:
            coll.upload(url=link)
            print(f"Video: {link} uploaded successfully")
            for video in coll.get_videos():
                video.index_spoken_words()
                print(f"Indexed {video.name}")
        except Exception as e:
            print(f"Exception occured for video {link} as {e}")

def getanswer(query):
    result = coll.search(query = query)
    print("Type: ")
    first_shot = result.get_shots()[0]
    video_title = first_shot.video_title
    text = first_shot.text
    print("Video Title:", video_title)
    print("Text:", text)
    answer = ""
    answer = get_openai_ans(query=query, text=text)
    matching_video = {
        "video_title": video_title,
        "text": text
    }
    return answer, matching_video

def get_openai_ans(query, text):
    messages = [
        {
            "role": "assistant",
            "content": f"""You are an helpful AI chatbot, who answers questions based on the generated transcript of a video. Remember to be precise and to the point while answering questions.
            You need to output the query only based on the below context provided, if you don't find answer in the context, output 'Information to the query is not in the provided video context' 
            The context to answer query is: {text} 
            
            Now answer the queries given by user"""
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
    )

    answer = response.choices[0].message.content
    return answer
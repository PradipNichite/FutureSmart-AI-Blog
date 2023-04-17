# file name youtube_subtitle_gen.py
import openai
import tempfile
import numpy as np
import pandas as pd
from pytube import YouTube, Search
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("openai_key")

video_dict = {
    "url": [],
    "title": [],
    "content": []
}


def video_to_audio(video_URL):
    # Get the video
    video = YouTube(video_URL)
    video_dict["url"].append(video_URL)
    try:
        video_dict["title"].append(video.title)
    except:
        video_dict["title"].append("Title not found")


    # Convert video to Audio
    audio = video.streams.filter(only_audio=True).first()

    temp_dir = tempfile.mkdtemp()
    variable = np.random.randint(1111, 1111111)
    file_name = f'recording{variable}.mp3'
    temp_path = os.path.join(temp_dir, file_name)
    # audio_in = AudioSegment.from_file(uploaded_file.name, format="m4a")
    # with open(temp_path, "wb") as f:
    #     f.write(uploaded_file.getvalue())

    # Save to destination
    output = audio.download(output_path=temp_path)

    audio_file = open(output, "rb")
    textt = openai.Audio.translate("whisper-1", audio_file)["text"]

    return textt


def create_dataframe(data):
    df = pd.DataFrame(data)
    df.to_csv("history.csv")


s = Search("history lessons under 4 minutes")
print(len(s.results))

for ele in s.results[0:5:1]:
    transcription = video_to_audio(ele.watch_url)
    print(transcription)
    print("\n\n\n")
    video_dict["content"].append(transcription)

create_dataframe(video_dict)

print("Created Dataframe")

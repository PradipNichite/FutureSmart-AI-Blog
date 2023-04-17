import pinecone
import pandas as pd
import openai
import os

pinecone.init(api_key=os.getenv("pinecone_key"), environment="us-east-1-aws")

index = pinecone.Index("demo-youtube-app")
print(index.describe_index_stats())

df = pd.read_csv("history.csv")
print(df.head())
openai.api_key = ""


def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )

    return response['data'][0]['embedding']


def addData(index,url, title,context):
    my_id = index.describe_index_stats()['total_vector_count']

    chunkInfo = (str(my_id),
                 get_embedding(context),
                 {'video_url': url, 'title':title,'context':context})

    index.upsert(vectors=[chunkInfo])


for indexx, row in df.iterrows():
    addData(index,row["url"],row["title"],row["content"])


print("Completed")
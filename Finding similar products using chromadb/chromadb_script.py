import os
import csv
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()
product_collection = client.create_collection("product_collection")

csv_file_path = r"C:\Users\Admin\Desktop\FutureAI\FutureSmart-AI-Blog\Finding similar products using chromadb\products.csv"

documents = []
metadatas = []
ids = []

with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    next(csv_reader) 
    for row in csv_reader:
        metadata = {
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': float(row[3]),
            'quantity': int(row[4]),
            'description': row[5]
        }
        documents.append(row[5])
        metadatas.append(metadata)
        ids.append(row[0])

product_collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)


query = "wireless mouse with RGB lighting and programmable buttons"

query_results = product_collection.query(
    query_texts=[query],
    n_results=5,
    where={
        '$and': [
            {'category': {'$eq': 'Electronics'}},
            {'price': {'$gte': 100}},
            {'price': {'$lte': 500}}
        ]
    }
)

metadata = query_results.get('metadatas', [])[0]

print(metadata)
import os
import csv
import chromadb
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

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

def find_top_similar_products(query: str, min_price=None, max_price=None, category=None):
    try:
        query_embedding = model.encode([query])[0]

        # Query the product collection
        results = product_collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=5
        )
        # Filtering metadata based on criteria
        filtered_results = []
        for metadata, distance in zip(results.get('metadatas', [[]])[0], results.get('distances', [[]])[0]):
            if (min_price is None or metadata['price'] >= min_price) and \
               (max_price is None or metadata['price'] <= max_price) and \
               (category is None or metadata['category'] == category):
                filtered_results.append((metadata, distance))

        # Initialize a list to store similar products along with their similarity scores
        similar_products = []
        for metadata, distance in filtered_results:
            # Encode the description of the product from metadata and calculate similarity score
            description_embedding = model.encode([metadata["description"].lower()])[0]

            similarity_score = round(cos_sim(query_embedding, description_embedding)[0].item(), 2)

            # Append metadata and similarity score to the list of similar products
            similar_products.append({
                "metadata": metadata,
                "similarity_score": similarity_score
            })

        # Sort the list of similar products based on similarity score in descending order
        sorted_similar_products = sorted(similar_products, key=lambda x: x["similarity_score"], reverse=True)

        return sorted_similar_products

    except Exception as e:
        return [{"error": str(e)}]

query = "wireless mouse with RGB lighting and programmable buttons"
min_price = 100
max_price = 500
category = "Electronics"
similar_products = find_top_similar_products(query, min_price=min_price, max_price=max_price, category=category)

for product in similar_products:
    if "error" in product:
        print("Error:", product["error"])
    else:
        print("Similarity Score:", product["similarity_score"])
        print("Metadata:", product["metadata"])

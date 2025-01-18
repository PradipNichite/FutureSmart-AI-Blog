# General Imports
import os
import time
from dotenv import load_dotenv
from uuid import uuid4 
import asyncio

# Langchain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

# Qdrant imports
from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams


from services.logger import logger
from uuid import uuid4

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
qdrant_db_path=os.getenv("qdrant_db_path")





class DocumentIndexer:
    def __init__(self, qdrant_db_path):
        self.db_path = qdrant_db_path
        self.embedding_function = OpenAIEmbeddings(model="text-embedding-3-large",api_key=OPENAI_API_KEY)

        self.vectors = None
        self.client = AsyncQdrantClient(self.db_path)


    async def index_in_qdrantdb(self, extracted_text, file_name, doc_type, chunk_size):
        """
        Index extracted text in ChromaDB with batch processing to handle large documents.
        """
        try:
            # Create a Document object
            doc = Document(
                page_content=extracted_text,
                metadata={
                    "file_name": file_name,
                    "doc_type": doc_type
                }
            )

            # Use default chunk size if none provided
            if chunk_size is None:
                # Calculate dynamic chunk size based on text length
                text_length = len(extracted_text)
                if text_length < 10000:
                    chunk_size = int(os.getenv("chunk_size"))
                elif text_length < 50000:
                    chunk_size = 1500
                else:
                    chunk_size = 2000
                logger.info(f"Using dynamic chunk size: {chunk_size}")

            # Split the document
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', ','],
                chunk_size=chunk_size,
                chunk_overlap=200
            )
            docus = text_splitter.split_documents([doc])


            # Generate UUIDs for all chunks
            uuids = [f"{str(uuid4())}" for _ in range(len(docus))]
            collection = "rag_demo_collection"

            
            collections = await self.client.get_collections()

            if collection in [collection_name.name for collection_name in collections.collections]:
                logger.info(f"Collection {collection} already exists in QdrantDB")
            else:
                await self.client.create_collection(
                                        collection_name=collection,
                                        vectors_config=VectorParams(size=3072, distance=Distance.COSINE))

            # self.vectors = QdrantVectorStore(
            #     client=self.client,
            #     collection_name=collection,
            #     embedding=self.embedding_function,
            # )

            print(collection)
            self.vectors =  QdrantVectorStore.from_existing_collection(collection_name=collection, embedding=self.embedding_function, url=self.db_path)

            await self.vectors.aadd_documents(documents=docus, ids=uuids)

            logger.info(f"Successfully indexed document  in QdrantDB")
            return True

        except Exception as e:
            logger.error(f"Error indexing document  in QdrantDB: {e}")
            raise

    async def get_retriever(self, top_k):
        """Get a retriever for querying the indexed documents."""
        try:
            collection = "rag_demo_collection"
            if self.vectors is None:
                # self.vectors = QdrantVectorStore(client=self.client,collection_name=collection,embedding=self.embedding_function)
                self.vectors =  QdrantVectorStore.from_existing_collection(collection_name=collection, embedding=self.embedding_function, url=self.db_path)
            
            return self.vectors.as_retriever(search_type="similarity",search_kwargs={"k": top_k})
        except Exception as e:
            logger.error(f"Error creating retriever: {e}")
            raise

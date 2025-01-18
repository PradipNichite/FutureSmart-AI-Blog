from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional,List
import uuid
import logging
from fastapi import  HTTPException, APIRouter
import logging
import uuid,time
from fastapi.responses import JSONResponse
from typing import List
from fastapi import Depends
import langsmith as ls
import nest_asyncio
import os
from datetime import *
from services.pydantic_models import ChatRequest,ChatResponse
from services.logger import logger
import langsmith  as ls
from langsmith.wrappers import wrap_openai
from fastapi.openapi.models import Response
from typing import AsyncGenerator
from uuid import uuid4 
import asyncio
from utils.db_utils import get_past_conversation_async,add_conversation_async
from utils.langchain_utils import generate_chatbot_response, index_documents
from utils.utils import extract_text_from_file
import uvicorn
import aiomonitor
nest_asyncio.apply()



app = FastAPI()

@app.post("/upload-knowledge")
async def upload_knwoledge(
    username: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        extracted_text = ""
        if file:
            logger.info(f"File uploaded: {file.filename}")
            file_content = await file.read()
            file_extension = file.filename.split('.')[-1].lower()
            extracted_text = await extract_text_from_file(file_content, file_extension)
            logger.info(f"File content size: {len(file_content)} bytes")
            logger.info(f"Extracted text from file: {extracted_text}")

            logger.info(f"Indexing documents in QdrantDB")
            await index_documents(username,extracted_text,file.filename,file_extension)
        return {'response':'Indexed Documents Successfully','extracted_text':extracted_text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing indexing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while indexing documents {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest
):
    try:
        start_time = datetime.now()
        logger.info(f"Request started at {start_time}")
        logger.info(f"Received request from {request.username} for question: {request.query}")
        if request.session_id is not None:
            logger.info(f"Fetching past messages")
            past_messages = await get_past_conversation_async(request.session_id)

            logger.info(f"Fetched past messages: {past_messages}")
        elif request.session_id is None:
            request.session_id = str(uuid4())
            past_messages = []

    
        logger.info(f"Generating chatbot response")
        response, response_time, input_tokens, output_tokens, total_tokens, final_context, refined_query, extracted_documents = await generate_chatbot_response(request.query, past_messages,request.no_of_chunks,request.username)
        logger.info(f"Response generated for User question: {request.query}")

        logger.info(f"Adding conversation to chat history")
        await add_conversation_async(request.session_id, request.query, response)
        logger.info(f"Added conversation to chat history")
        

        debug_info = {
                "sources": [{"file_name": doc.metadata["file_name"], "context": doc.page_content} for doc in extracted_documents]
            }
        
        end_time = datetime.now()
        logger.info(f"Request ended at {end_time}")
        return {"username": request.username,"query": request.query,"refine_query": refined_query,"response": response,"session_id": request.session_id,"debug_info": debug_info}


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while generating chatbot response {e}")
    



# if __name__ == "__main__":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     with aiomonitor.start_monitor(loop=asyncio.get_event_loop()):
#         uvicorn.run(app, host="0.0.0.0", port=8000)
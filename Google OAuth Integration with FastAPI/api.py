import os
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from apis import chatbot, authentication
import logging as logger
import time


from dotenv import load_dotenv
load_dotenv(override=True)

config = Config(".env")


expected_api_secret = os.getenv("FASTAPI_SECRET_KEY")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Add Session middleware
app.add_middleware(SessionMiddleware, secret_key=config("SECRET_KEY"))

# # Logging time taken for each api request
@app.middleware("http")
async def log_response_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.url.path} completed in {process_time:.4f} seconds")
    return response 

app.include_router(chatbot.router, tags=["Chatbot"])
app.include_router(authentication.router, tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


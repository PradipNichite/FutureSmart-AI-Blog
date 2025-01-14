from fastapi import  APIRouter
import logging
from fastapi import Depends
import os
from datetime import *
from apis.authentication import get_current_user


router = APIRouter()

@router.get("/chat")
async def get_response(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome!", "user": current_user}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8000)

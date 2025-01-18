from fastapi import Form, UploadFile, File
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List, ClassVar
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv
import os
import re
load_dotenv(override=True)



class ChatRequest(BaseModel):
    username: str
    query: str
    session_id: Optional[str] = None
    no_of_chunks: Optional[int] = 3



class ChatResponse(BaseModel):
    username: str
    query: str
    refine_query: str
    response: str
    session_id: str
    debug_info: Optional[dict] = None
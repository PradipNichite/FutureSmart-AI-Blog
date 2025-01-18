import sqlite3
import time
import aiosqlite
import asyncio
from typing import List
from services.logger import logger


def get_db_connection():
    """Simulate getting a connection to an in-memory SQLite DB."""
    connection = sqlite3.connect(":memory:")  # This creates a new in-memory database
    return connection, connection.cursor()

async def get_past_conversation_async(session_id: str) -> List[dict]:
    start_time = asyncio.get_event_loop().time()
    messages = []

    try:
        # Open an async SQLite connection
        async with aiosqlite.connect("chat_log.db") as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
                session_id TEXT,
                user_query TEXT,
                gpt_response TEXT
            )''')
            logger.info("Database schema ensured.")
            
            # Fetch chat logs for the given session_id
            async with connection.execute(
                "SELECT user_query, gpt_response FROM chat_logs WHERE session_id=?", (session_id,)
            ) as cursor:
                async for row in cursor:
                    message_user = {"role": "user", "content": row[0]}
                    message_assistant = {"role": "assistant", "content": row[1]}
                    messages.extend([message_user, message_assistant])
        
        elapsed_time = asyncio.get_event_loop().time() - start_time
        logger.info(f"History For Context (get_conversation): {messages} in {elapsed_time:.2f}s")
        return messages

    except Exception as e:
        logger.exception(f"Error occurred: {str(e)}")
        raise e


async def add_conversation_async(session_id, user_query, gpt_response):
    try:
        # Open an async SQLite connection
        async with aiosqlite.connect(":memory:") as connection:
            cursor = await connection.cursor()

            # Create table if it doesn't exist
            await cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
                                        session_id TEXT,
                                        user_query TEXT,
                                        gpt_response TEXT)''')

            # Insert new conversation
            await cursor.execute("INSERT INTO chat_logs (session_id, user_query, gpt_response) VALUES (?, ?, ?)",
                                 (session_id, user_query, gpt_response))

            await connection.commit()
            logger.info(f"Conversation added for session {session_id}")

    except Exception as e:
        logger.exception(f"Error occurred while adding conversation: {str(e)}")
        raise e

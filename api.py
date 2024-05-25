import sys
import pandas as pd
from typing import Annotated, List
import asyncpg
import uvicorn
from fastapi import FastAPI, Path, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import CONFIG, DB_URI
from exception_handler import (
    validation_exception_handler,
    python_exception_handler,
    errors_dict,
)
# from security import router as security_router, get_current_user
from models import User, Comment, UserCredentials, Summary

# origins = ["http://localhost:5173"]

# Initialize API
app = FastAPI(
    title="Endpoints for analysis calls for Smrt Media Monitor",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, python_exception_handler)

# Load security api calls
# app.include_router(security_router)


# Retrieve comments from the database
async def fetch_comments(label: str = None) -> List[Comment]:
    conn = await asyncpg.connect(DB_URI)
    try:
        if label:
            query = "SELECT * FROM comments WHERE Label = $1"
            records = await conn.fetch(query, label)
        else:
            query = "SELECT * FROM comments"
            records = await conn.fetch(query)

        comments = [
            Comment(
                id=row['id'],
                name=row['name'],
                comment=row['comment'],
                likes=row['likes'],
                time=row['time'],
                reply_count=row['reply_count'],
                label=row['label'],
                label_score=row['label_score'],
                video_id=row['video_id'],
                comment_id=row['comment_id']
            )
            for row in records
        ]

        return comments
    finally:
        await conn.close()


# Retrieve summaries from the database
async def fetch_summaries(label: str) -> Summary:
    conn = await asyncpg.connect(DB_URI)
    try:
        query = "SELECT * FROM summaries WHERE label = $1"
        record = await conn.fetchrow(query, label)
        if record:
            return Summary(
                id=record['id'],
                label=record['label'],
                summary=record['summary']
            )
        else:
            return None
    finally:
        await conn.close()


@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and add variables
    """
    pass


async def create_user(username: str, channel_id: str, password: str) -> None:
    conn = await asyncpg.connect(DB_URI)
    try:
        await conn.execute(
            "INSERT INTO users (username, channel_id, password) VALUES ($1, $2, $3)",
            username,
            channel_id,
            password
        )
    finally:
        await conn.close()


async def authenticate_user(username: str, password: str) -> bool:
    conn = await asyncpg.connect(DB_URI)
    try:
        # Execute the query to check user credentials
        query = "SELECT COUNT(*) FROM users WHERE username = $1 AND password = $2"
        count = await conn.fetchval(query, username, password)
    finally:
        # Close the database connection
        await conn.close()

    # If count is greater than 0, the user with the provided credentials exists
    return count > 0


@app.post("/signup/")
async def signup(user_data: User):
    await create_user(user_data.username, user_data.channel_id, user_data.password)
    return {"message": "User created successfully"}


@app.post("/login/")
async def login(user_data: UserCredentials):
    user_authenticated = await authenticate_user(user_data.username, user_data.password)
    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}


@app.get("/comments/", response_model=List[Comment])
async def get_comments(label: str = Query(None)):
    comments = await fetch_comments(label)
    return comments


@app.get("/summaries/", response_model=Summary)
async def get_summary(label: str = Query(...)):
    summary = await fetch_summaries(label)
    if summary:
        return summary
    else:
        return {"error": "Summary not found"}


@app.get("/query/")
async def query_chatgpt(query: str = Query(..., description="The user query to be processed by ChatGPT")):
    try:
        # Import the function from chatgpt.py
        from chatgpt import get_chatgpt_response

        # Call the function with the user query
        response = get_chatgpt_response(query)

        # Return the response
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/script/")
async def script_generator(topic: str = Query(..., description="The user query to be processed by ChatGPT")):
    try:
        # Import the function from chatgpt.py
        from chatgpt import get_chatgpt_script
        
        query = "Imagine you're a Youtuber and you run a Youtube channel. Write me detailed script for a youtube video on " + topic + ". It's the script which the youtuber will speak during the video. If you do not know anything make suitable assumptions."

        # Call the function with the user query
        response = get_chatgpt_script(query)

        # Return the response
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    """
    Dummy call
    """
    return {"Use the correct API call brosky"}


if __name__ == "__main__":
    # start api
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

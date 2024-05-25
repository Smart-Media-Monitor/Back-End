from pydantic import BaseModel, Field
from config import CONFIG
import numpy as np
from datetime import datetime


class Comment(BaseModel):
    id: int
    name: str
    comment: str
    likes: int
    time: datetime
    reply_count: int
    label: str
    label_score: float
    video_id: str
    comment_id: int


class Summary(BaseModel):
    id: int
    label: str
    summary: str


class User(BaseModel):
    """
    User Object
    """

    username: str
    channel_id : str
    password: str


class UserCredentials(BaseModel):
    """
    User Credentials Object
    """

    username: str
    password: str


class ErrorResponse(BaseModel):
    """
    Error response for the API
    """

    error: bool = Field(example=True, title="Whether there is error")
    message: str = Field(example="", title="Error message")
    traceback: str = Field(example="", title="Detailed traceback of the error")

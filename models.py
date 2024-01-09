from pydantic import BaseModel, Field
from config import CONFIG
import numpy as np


class User(BaseModel):
    """
    User Object
    """

    username: str
    password: str


class Comment(BaseModel):
    comment_id: int
    name: str
    comment: str
    likes: int
    time: str  # Modify this based on your timestamp format
    reply_count: float
    label: str
    label_score: float
    video_id: str


class ErrorResponse(BaseModel):
    """
    Error response for the API
    """

    error: bool = Field(example=True, title="Whether there is error")
    message: str = Field(example="", title="Error message")
    traceback: str = Field(example="", title="Detailed traceback of the error")

#!/usr/bin/python3
"""It defines class Review"""
from models.base_model import BaseModel


class Review(BaseModel):
    """It represent a review"""

    place_id = ""
    user_id = ""
    text = ""

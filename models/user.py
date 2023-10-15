#!/usr/bin/python3
"""Dedines a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """It represent a user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

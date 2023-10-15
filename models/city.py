#!/usr/bin/python3
"""It defines a class City"""
from models.base_model import BaseModel


class City(BaseModel):
    """It represents a city.
    Attributes:
    state_id(str): state id
    name(str): name of city
    """
    state_id = ""
    name = ""

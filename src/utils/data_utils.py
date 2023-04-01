"""
Module for data utilities such as dataclasses sctructures saved in sqlalchemy database
"""
from dataclasses import dataclass
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

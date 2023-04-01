"""
Module for data utilities such as dataclasses sctructures saved in sqlalchemy database
"""
from dataclasses import dataclass
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


@dataclass
class User(SQLAlchemy.Model):
    _id: Column("id", Integer, primary_key=True)
    name: Column(String(100))
    email: Column(String(100))

    def __repr__(self):
        return f"User {self.name} with email {self.email}"

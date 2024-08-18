#!/usr/bin/env python3
"""
User model for SQLAlchemy
"""

from sqlalchemy import Colum, Integer, String, create_engine
fron sqlalchemy.ext.declarative import declarative_base

Base = dclarative_base()


class User(Base):
    """User model for the users table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

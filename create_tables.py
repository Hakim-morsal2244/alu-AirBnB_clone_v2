#!/usr/bin/python3
"""
This script creates all tables in the database using SQLAlchemy
"""
from models import storage
from models.base_model import Base
from models.state import State
from models.city import City

# Create all tables in the database
Base.metadata.create_all(storage._DBStorage__engine)

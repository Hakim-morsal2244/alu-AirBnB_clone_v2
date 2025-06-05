#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental """
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of objects in the database"""
        dic = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dic[key] = obj
        else:
            for model_class in [State, City, User, Place, Review, Amenity]:
                query = self.__session.query(model_class)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dic[key] = obj
        return dic

    def new(self, obj):
        """Add a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Save all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize a session"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """Close the current SQLAlchemy session"""
        self.__session.remove()

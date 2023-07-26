from sqlalchemy.orm._orm_constructors import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from storage import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    time = Column(DateTime)
    character = Column(Integer, ForeignKey('characters.id'))


class Characters(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    open_ai_description = Column(String)
    img_path = Column(String)


class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    character_id = Column(Integer, ForeignKey('characters.id'))
    user_message = Column(String)
    answer = Column(String)

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from datetime import datetime

Base = declarative_base()

class Category(Base):
  __tablename__ = 'categories'

  id   = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name'         : self.name,
      'id'           : self.id,
    }

class Item(Base):
  __tablename__ = 'items'

  id          = Column(Integer, primary_key = True)
  name        = Column(String(80), nullable = False)
  description = Column(String(250))
  image       = Column(String(250))
  category_id = Column(Integer,ForeignKey('categories.id'))
  created     = Column(DateTime, default=datetime.now)
  updated     = Column(DateTime)

  category    = relationship(Category)

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'id'           : self.id,
      'name'         : self.name,
      'description'  : self.description,
      'category_id'  : self.category_id,
      'image'        : self.image
    }

class User(Base):
  __tablename__ = 'user'

  id           = Column(Integer, primary_key=True)
  name         = Column(String(250), nullable=False)
  email        = Column(String(80), nullable=False)
  picture      = Column(String(80))
  google_id    = Column(String(80))
  facebook_id  = Column(String(80))
  created      = Column(DateTime, default=datetime.now)
  last_login   = Column(DateTime)

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)

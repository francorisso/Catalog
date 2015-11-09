from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base

#Connect to Database and create database session
def getConnection():
  engine = create_engine('sqlite:///catalog.db')
  Base.metadata.bind = engine

  DBSession = sessionmaker(bind=engine)
  session = DBSession()

  return session
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Item

import datetime
import requests
import random
import string

from flask import session as login_session

from modules.database import database

session = database.getConnection()

def get(category_id=0):
  items = session.query(Item).order_by(desc(Item.created))
  if(category_id>0):
    items = items.filter(Item.category_id==category_id)

  return items

def create():
  now  = datetime.datetime.now()
  item = Item(
    name = request.form['name'],
    description = request.form['description'],
    category_id = request.form['category_id'],
    created = now,
    updated = now
  )
  session.add(item)
  flash('New Item %s Successfully Created' % item.name)
  session.commit()

  return item

def update(item_id):
  item = session.query(Item).filter_by(id = item_id).one()
  now  = datetime.datetime.now()
  item.name = request.form['name']
  item.description = request.form['description']
  item.category_id = request.form['category_id']
  item.updated = now
  session.add(item)
  flash('Item %s Successfully Updated' % item.name)
  session.commit()

def delete(item_id):
  item = session.query(Item).filter_by(id = item_id).one()

  session.delete(item)
  flash('Item %s Successfully Deleted' % item.name)
  session.commit()
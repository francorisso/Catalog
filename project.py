from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Category, Item, User

import datetime
import requests
import random
import string

from flask import session as login_session

from modules.google_auth import main as google_auth
from modules.item import itemModel
from modules.database import database

session = database.getConnection()

#check if user exists
def getLoggedUser():
  user = None
  if 'userId' in login_session and login_session['userId']:
    user = session.query(User).filter_by(id=login_session['userId']).one()
  return user

@app.route('/connect', methods=['POST'])
def connect():
  if request.args.get('service') == 'google':
    userInfo  = google_auth.connect()
    user      = getOrCreateUser(userInfo)
    login_session['userId'] = user.id
    return 'logged in'
  else:
    print 'Wrong service'

@app.route('/logout')
def logout():
  login_session.pop('userId', None)
  return redirect(url_for('homepage'));

def getOrCreateUser (userInfo):
  now  = datetime.datetime.now()
  try:
    user = session.query(User).filter_by(email=userInfo['email']).one()

    if userInfo['google_id'] is not None:
      user.google_id = userInfo['google_id']

    if userInfo['facebook_id'] is not None:
      user.facebook_id = userInfo['facebook_id']

    user.picture    = userInfo['picture']
    user.last_login = now

  except NoResultFound as e:
    user = User(
      name          = userInfo['name'],
      picture       = userInfo['picture'],
      email         = userInfo['email'],
      google_id     = userInfo['google_id'],
      facebook_id   = userInfo['facebook_id'],
      created       = now,
      last_login    = now
    )

  session.add(user)
  session.commit()

  return user


# Create anti-forgery state token
@app.route('/login')
def showLogin():
  state = ''.join(
    random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32)
  )
  login_session['state'] = state

  return render_template('login.html', googleClientId=google_auth.CLIENT_ID, STATE=state)

# Homepage
@app.route('/')
@app.route('/category/<int:category_id>')
def homepage(category_id=0):
  paramsForTemplate = {}
  paramsForTemplate['items'] = itemModel.get(category_id)
  return renderTemplate('index.html', paramsForTemplate)


###############  ITEMS  ###############
@app.route('/item/create', methods=['GET','POST'])
def create():
  if (request.method=='POST'):
    itemModel.create()
    return redirect(url_for('homepage'));
  else:
    categories = getCategories()
    return render_template('items/create.html', categories = categories)

@app.route('/item/edit/<int:item_id>', methods=['GET','POST'])
def edit(item_id):
  if (request.method=='POST'):
    itemModel.update(item_id)
    return redirect(url_for('edit',item_id=item_id));
  else:
    item = session.query(Item).filter_by(id = item_id).one()
    categories = getCategories()
    return render_template('items/edit.html', categories = categories, item=item)

@app.route('/item/details/<int:item_id>', methods=['GET'])
def details(item_id):
  item = session.query(Item).filter_by(id = item_id).one()
  categories = getCategories()
  return render_template('items/details.html', categories = categories, item=item)

@app.route('/item/delete/<int:item_id>', methods=['GET','POST'])
def delete(item_id):
  if (request.method=='POST'):
    itemModel.delete(item_id)
    return redirect(url_for('homepage'));
  else:
    item = session.query(Item).filter_by(id = item_id).one()
    categories = getCategories()
    return render_template('items/delete.html', categories = categories, item=item)

@app.route('/catalog.json')
def catalogJSON():
  items = session.query(Item).all()
  return jsonify(items=[i.serialize for i in items])


##### Utilities ####
def getCategories():
  return session.query(Category).order_by(asc(Category.name))

def renderTemplate(templateName, params):
  if not params:
    params = {}

  params['user'] = getLoggedUser()
  params['categories'] = getCategories()

  return render_template('index.html', **params)


if __name__ == '__main__':
  app.secret_key = ']|3\xc9\xc2\x19\x88\x8e4\xa6\xb7\x7fx\x8d\xb3n\xf4%\xea-\xbd\xdf\xa0.'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)

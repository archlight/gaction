from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata

class User(ndb.Model):
    username = ndb.StringProperty()
    gender = ndb.StringProperty()
    age = ndb.IntegerProperty()

class Account(ndb.Model):
    accountid = ndb.IntegerProperty()
    accountowner = ndb.StringProperty()
    accountname = ndb.StringProperty()
    currency = ndb.StringProperty()
    balance = ndb.IntegerProperty()
    asset = ndb.StringProperty()
    
class EquityPortfolio(ndb.Model):
    accountid = ndb.IntegerProperty()
    stock = ndb.StringProperty()
    symbol = ndb.StringProperty()
    buyprice = ndb.FloatProperty()
    amount = ndb.IntegerProperty()
    
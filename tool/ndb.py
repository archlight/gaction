from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata

meta = {'User':['username', 'gender', 'age'],
        'Account':['accountid', 'accountowner', 'currency', 'balance', 'asset'],
        'EquityPortfolio':['accountid', 'stock', 'symbol', 'buyprice', 'amount']}

data = [{
        'User':[['archlight', 'male', 34]],
        'Account':[[8762, 'archlight', 'saving', 'EUR', 500000, 'cash'],
                    [7281, 'archlight', 'current', 'USD', 200000, 'cash'],
                    [2812, 'archlight', 'etrade', 'USD', 200, 'equity']],
        'EquityPortfolio':[[2812, 'Apple Inc', 'AAPL', 110.6, 200],
                           [2812, 'Twitter Inc', 'TWTR', 30.5, 1000]]
         }]

for t in data:
    for k, v in t.items():
        for item in v:
            m = eval(k)(**dict(zip(meta[k], item)))
            m.put()

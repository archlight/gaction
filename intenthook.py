import os
import json
import urllib2

from model import *
        
class AccountHandler():
    input_contexts = []
    ouput_contexts = []
    
    def __init__(self, _intent):
        self.intent = _intent
        self.username = 'archlight'
        self.intentname = self.intent.name.split('-')[0].strip()
        self.action = self.intentname.split('.')[-1] if len(self.intentname.split('.'))>1 else ''
        self.accounts = [t for t in Account.query(Account.accountowner == self.username).fetch()]
    
    def get_accounts(self, _id, _asset):
        if _id:
            return [ t for t in self.accounts if t.accountid == int(_id)]
        else:
            return [ t for t in self.accounts if t.asset == _asset.lower()]
                    
    
    def get_portfolio_by_id(self, _id):
        return EquityPortfolio.query(EquityPortfolio.accountid == int(_id)).fetch()
    
    
    def get_parameter(self, k):        
        v = self.intent.parameters[k] if k in self.intent.parameters else None
        if v:
            return v
        else:
            return self.get_parameter_in_context(k)

    def get_parameter_in_context(self, k):
        if len(self.intent.contexts):
            return self.intent.contexts[0]['parameters'][k] if k in self.intent.contexts[0]['parameters'] else None
        else:
            return None
        
    
    def get_portfolio_return(self, _ptf):
        _latest = {'AAPL':150, 'TWTR':13}
        cost = sum([t.buyprice * t.amount for t in _ptf])
        value = sum([_latest[t.symbol] * t.amount for t in _ptf])
        return value, value/cost - 1
    
    def list_portfolio(self, _ptf):
        d = []
        _latest = {'AAPL':150, 'TWTR':13}
        for t in _ptf:
            d += ['stock %s (%s) shares %d buyprice %.2f lastprice %.2f' % 
                  (t.stock, t.symbol, t.amount, t.buyprice, _latest[t.symbol])]
        return d
        
    
    def handle_response(self, act):
        if act[0].asset == 'cash':
            d = ["Cash Balance: "]
            for t in act:
                d += ["%d %s in account %d" % (t.balance, t.currency, t.accountid)]
            text = ";".join(d)
        elif act[0].asset == 'equity':
            d = ['Equity Portfolio: ']
            for t in act:
                portfolio = self.get_portfolio_by_id(t.accountid)
                if self.action == 'breakdown':
                    d += self.list_portfolio(portfolio)
                else:
                    mtm, returns = self.get_portfolio_return(portfolio)
                    d += ['account: %d, mtm: %.0f (%s), return %.2f percent' % (t.accountid, mtm, t.currency, returns)]
            text = ";".join(d)
        return text
    
    def run(self):
        
        actid = self.get_parameter('account-number')
        asset = self.get_parameter('asset-class')
        
        print(actid)
        print(asset)
        
        text = "default response"
        
        if actid or asset:
            act = self.get_accounts(actid, asset)
            if len(act):
                text = self.handle_response(act)
            else:
                text = "no account found"
        else:
            text = self.handle_response(self.get_accounts('', 'cash'))
            text += self.handle_response(self.get_accounts('', 'equity'))
                
        response = {
            "speech": "account",
            "displayText": text 
            }
        return response
    
class NewsHandler():
    
    NEWS_API_KEY = '00a055304b3e4b6fb73e75203a604938'
    NEWS_BASE_URL = 'https://newsapi.org/v1/articles?'

    input_contexts = []
    ouput_contexts = []
    
    def __init__(self, _intent):
        self.intent = _intent
        self.source = self._get_source_id(_intent.parameters['source'])
        
    def _get_news_headline(self, params):
        print(self.NEWS_BASE_URL+'&'.join(params))

        req = urllib2.urlopen(self.NEWS_BASE_URL+'&'.join(params))
        d = json.loads(req.read())
        if len(d['articles']):
            return d['articles'][0]['title']
        else:
            return 'No Headline'

    def _get_source_id(self, k):
        d = json.load(urllib2.urlopen('https://g-action.appspot.com/json/news.json'))
        
        for t in d['sources']:
            if k.lower() in t['name'].lower():
                return t['id']
        return 'bloomberg'
                
    def run(self):
        
        params = ['apiKey=%s' % self.NEWS_API_KEY]
        params += ['source=%s' % self.source]

        headline = self._get_news_headline(params)
        self.response = {
            "speech": "%s headline" % self.source,
            "displayText": headline
            }
        return self.response

class Intent():
    IntentMap = {
        'news': NewsHandler,
        'portfolio': AccountHandler
        }
    
    def __init__(self, _request):
        self.request = _request
        self.sessionId = _request['sessionId']
        self.name = _request['result']['metadata']['intentName']
        self.parameters = _request['result']['parameters']
        self.contexts = _request['result']['contexts']
    
    def get_context(self, name, **kwargs):
        for t in self.contexts:
            if t['name'] == name:
                for k, v in kwargs.items():
                    t['parameters'][k] = v
                return t
        return {}
                
    def webhook(self):
        return self.IntentMap[self.name.split('.')[0]](self).run()
    
import os
import urllib2
import logging
import json
from datetime import date, datetime

import webapp2
import jinja2

from intenthook import Intent

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)




class BaseHandler(webapp2.RequestHandler):
     
    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = JINJA_ENVIRONMENT.get_template(view_filename)
        self.response.write(template.render(params))

class MainPage(BaseHandler):
    def get(self):
        self.render_template('welcome.html')

class ChatBot(BaseHandler):
    def get(self):
        self.render_template('chatbot.html')    
        
class ApiAiTest(BaseHandler):
    def get(self):
        self.render_template('apiai.html')
        
class WebHook(BaseHandler):


    def post(self):
        logging.info('webhook')
        
        d = json.loads(self.request.body)
        response = Intent(d).webhook()
            
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/webhook', WebHook),
    ('/apiai', ApiAiTest),
    ('/chatbot', ChatBot)
], debug=True)

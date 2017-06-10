import urllib2
import json

base_url = 'https://language.googleapis.com'
sentiment_url = base_url + '/v1/documents:analyzeSentiment'

data = {
  "document":{
    "type":"PLAIN_TEXT",
    "content":"I am a bit worried about current market"
  },
  "encodingType":"UTF8"
}

req = urllib2.Request(sentiment_url)
req.add_header('Content-Type', 'application/json')

d = urllib2.urlopen(req, json.dumps(data))

print(d)


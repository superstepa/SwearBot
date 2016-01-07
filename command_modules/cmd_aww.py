import urllib2
import json
import random


def command_aww(self, command, user):
    hdr = {'User-Agent': 'Grabbing a random awwducational post'}
    url = "http://www.reddit.com/r/awwducational/new.json"
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req).read()
    data = json.loads(response)
    post = random.choice(data['data']['children'])
    title = post['data']['title'].encode('utf-8')
    self.send_message(self.CHAN, title)

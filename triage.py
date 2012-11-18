import tornado.ioloop
import tornado.web
from datetime import datetime
import urlparse
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import pymongo
from pymongo import Connection
import logging

class Home(tornado.web.RequestHandler):

    def initialize(self, connection):
        self.db = connection['triage']
        self.catastrophes = self.db['catastrophes']
        self.victims = self.db['victims']

    def output_victims(self, victims):
        for v in victims:
            del(v["_id"])
	    v["timestamp"] = str(v["timestamp"])
            del(v["catastrophe_id"])
        self.write(json.dumps(victims, ensure_ascii=True))

class Catastrophe(Home):

    def get(self, catastrophe_id):
        catastrophe = self.catastrophes.find_one({"_id": ObjectId(catastrophe_id)})
	if not catastrophe:
		raise tornado.web.HTTPError(404)

        self.set_header('Content-Type', 'application/json')
	catastrophe["_id"] = str(catastrophe["_id"])
	catastrophe["timestamp"] = str(catastrophe["timestamp"])
        self.write(dumps(catastrophe, ensure_ascii = True))

class AllCatastrophes(Home):

    def get(self):
        catastrophes = list(self.catastrophes.find())
        self.set_header('Content-Type', 'application/json')

	for c in catastrophes:
		c["_id"] = str(c["_id"])
		c["timestamp"] = str(c["timestamp"])
		c["active"] = False

	catastrophes[len(catastrophes)-1]["active"] = True
        self.write(dumps(catastrophes, ensure_ascii = True))

    def post(self):
        timestamp = datetime.now()
	catastrophe = None
	try:
		catastrophe = json.loads(self.request.body)
	except:
		raise tornado.web.HTTPError(400)
	catastrophe["timestamp"] = timestamp
	self.catastrophes.insert(catastrophe)


class AllVictims(Home):

    def get(self):
        victims = self.victims.find()
        self.set_header('Content-Type', 'application/json')
        self.output_victims(list(victims))

    def post(self):
        timestamp = datetime.now()
	victim = None
	try:
        	victim = json.loads(self.request.body)
	except:
		print "problem parsing", self.request.body
		raise tornado.web.HTTPError(400)

	if not self.catastrophes.find({"catastrophe_id": ObjectId(victim["catastrophe_id"])}).count():
		print "can't find catastrophe", victim["catastrophe_id"]
		raise tornado.web.HTTPError(404)

	victim["catastrophe_id"] = ObjectId(victim["catastrophe_id"])
	victim["timestamp"] = timestamp
       	self.victims.insert(victim)

class Victims(Home):

    def get(self, catastrophe_id):
        victims = self.victims.find({"catastrophe_id":ObjectId(catastrophe_id)})
	if not victims.count():
		raise tornado.web.HTTPError(404)
        self.set_header('Content-Type', 'application/json')
        self.output_victims(list(victims))

application = tornado.web.Application([
    (r"/catastrophes/([a-f0-9]+)", Catastrophe, dict(connection =  Connection()) ),
    (r"/catastrophes/?", AllCatastrophes, dict(connection =  Connection()) ),
    (r"/victims/([a-f0-9]+)", Victims, dict(connection =  Connection()) ),
    (r"/victims/?", AllVictims, dict(connection =  Connection()) ),
])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()

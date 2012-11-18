import tornado.ioloop
import tornado.web
from datetime import datetime
import urlparse
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import pymongo
from pymongo import Connection


class Home(tornado.web.RequestHandler):

    def initialize(self, connection):
        self.conn = connection
        self.db = self.conn['triage']
        # self.collection = self.db['events']
        self.catastrophes = self.db['catastrophes']
        self.victims = self.db['victims']

        ## sample event
        timestamp = str(datetime.now())

        catastrophe = {
                "description": "Demo Earthquake",
                "timestamp": timestamp
        }

        # catastrophe_id = self.db.ctastrophes.insert(catastrophe)

        # for num in range(0,5):
        #     victim = {
        #         "user_name": "John Doe",
        #         "catastrophe_id": catastrophe_id, 
        #         "latitude": 0.0,
        #         "longitude": 0.0,
        #         "precision": 0.0, 
        #         "timestamp": timestamp,
        #         "color_code" : 'red'
        #     }

        #     self.db.victims.insert(victim)

    def outputVictims(self, victims):
        for v in victims:
            del(v["_id"])
            del(v["catastrophe_id"])
        self.write(json.dumps(victims, ensure_ascii=True))





class Catastrophes(Home):

    def get(self, catastrophe_id):
        catastrophe = self.db.catastrophes.find_one({"_id":int(catastrophe_id)})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(catastrophe))

    def post(self):
        timestamp = datetime.now()
        catastrophe_dto = json.loads(self.request.body)
        catastrophe = {
                "description": catastrophe_dto['description'],
                "timestamp" : timestamp
        }

        _id = self.db.catastrophes.insert(catastrophe)
        location = "/catastrophe/"+ str(_id)
        self.set_header('Content-Type', 'application/json')
        self.set_header('Location', location)
        self.set_status(201)
        self.write(dumps(catastrophe))

    # def put(self, eventid):
    #     ## Convert unicode to int
    #     _id = int(eventid)
    #     timestamp = datetime.now()
    #     body = urlparse.parse_qs(self.request.body)
    #     for key in body:
    #             body[key] = body[key][0]
    #     event = {
    #             "title": body['title'],
    #             "tags": body['tags'],
    #             "category": body['category'],
    #             "timestamp": timestamp
    #     }
    #     self.db.events.update({"_id":_id}, {"$set":event})
    #     self.set_header('Content-Type', 'application/json')
    #     self.write(dumps(event))

    # def delete(self,eventid):
    #     ## Convert unicode to int
    #     _id = int(eventid)
    #     event = {
    #             "title": None,
    #             "tags": [],
    #             "category": [],
    #             "timestamp": None,
    #     }
    #     self.db.events.update({"_id":_id}, {"$set":event})
    #     self.set_header('Content-Type', 'application/json')
    #     self.write(dumps(event))

class AllVictims(Home):

    def get(self):
        # victims = str(list(self.db.victims.find()))
        victims = list(self.db.victims.find())
        # victims_utf8 = [str(s).encode('utf-8') for s in victims]
        self.set_header('Content-Type', 'application/json')
        # self.write(dumps(victims))
        self.outputVictims(victims)
        # for v in victims:
        #     del(v["_id"])
        #     del(v["catastrophe_id"])

        # self.write(json.dumps(victims, ensure_ascii=True))


class Victims(Home):

    def get(self, catastrophe_id):
        victims = list(self.db.victims.find({"catastrophe_id":ObjectId(catastrophe_id)}))
        self.set_header('Content-Type', 'application/json')
        self.outputVictims(victims)

    def post(self):
        # _id = self.db.events.count() + 1
        timestamp = datetime.now()
        #body = urlparse.parse_qs(self.request.body)
        victim_dto = json.loads(self.request.body)
        # for key in body:
        #       body[key] = body[key][0]
        
        victim = {
                "user_name": victim_dto['user_name'],
                "catastrophe_id": victim_dto['catastrophe_id'],
                "latitude": victim_dto['latitude'],
                "longitude": victim_dto['longitude'],
                "precision": victim_dto['precision'],
                "color_code" : victim_dto['color_code'],
                "timestamp": timestamp
        }


    # def delete(self):
    #     events = str(list(self.db.events.find()))
    #     self.set_header('Content-Type', 'application/json')
    #     self.db.events.drop()
    #     self.write(dumps(events))

application = tornado.web.Application([
    (r"/", Home),
    # (r"/catastrophe/([A-Za-z0-9]+)", Catastrophes, dict(connection = Connection()) ),
    (r"/catastrophe/", Catastrophes, dict(connection =  Connection()) ),
    (r"/victim/([a-f0-9]+)", Victims, dict(connection =  Connection()) ),
    (r"/victim/", AllVictims, dict(connection =  Connection()) ),
],debug=True)

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()

# 50a82d9bfba662391c3379b0

#!/usr/bin/python3.8

from pymongo import MongoClient
import redis

HOST_MONGO = "172.17.0.3"
DBNAME = "tumindb"

HOST_REDIS = "172.17.0.2"
r = redis.Redis(host=HOST_REDIS)

mongo = MongoClient(HOST_MONGO)
mongo.drop_database(DBNAME)

db = mongo[DBNAME]

rbooks = [key.decode("ascii").split(":")[1] for key in r.keys("students:rbook_*")]
rbooks.sort(key = lambda key: int(key.split("_")[1]))

for i in range(1, 6):
  group = {
    "name": "Group_" + str(i),
    "departament": "Dep_" + str(i),
    "students": rbooks[20*(i-1):20*i]
  }

  db["groups"].insert_one(group)


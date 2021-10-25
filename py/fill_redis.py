#!/usr/bin/python3.8

import json
import redis

HOST = "172.17.0.2"

r = redis.Redis(host=HOST)
r.flushdb()

for i in range(1, 101):
  key = "rbook_" + str(i)
  data = {
    "surname": "Surname" + str(i),
    "name": "Name" + str(i),
    "patronymic": "Patronymic" + str(i)
  }

  r.set("students:" + key, json.dumps(data))


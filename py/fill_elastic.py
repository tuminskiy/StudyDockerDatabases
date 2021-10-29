#!/usr/bin/python3.8

from elasticsearch import Elasticsearch

HOST = "172.17.0.5"
INDEX = "tumindb"

es = Elasticsearch(host=HOST)

if es.indices.exists(index=INDEX):
  es.indices.delete(index=INDEX)

es.indices.create(index=INDEX)

for i in range(1, 101):
  n = 8 if i % 2 == 0 else 16

  data = {
    "lesson": "lesson No. " + str(i),
    "discription": "description No. " + str(i),
    "n_lecture": n,
    "n_practice": n 
  }

  es.index(index=INDEX, document=data)


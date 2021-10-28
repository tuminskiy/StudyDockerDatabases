#!/usr/bin/python3.8

from elasticsearch import Elasticsearch
from neo4j import GraphDatabase

def clear_database(ctx):
  ctx.run("MATCH (s:Student) DELETE s")
  ctx.run("MATCH (g:Group) DELETE g")
  ctx.run("MATCH (l:Lesson) DELETE l")

def create_student(ctx, rbook):
  ctx.run("CREATE (s:Student) SET s.rbook = $rbook", rbook=rbook)

def create_lesson(ctx, lesson_id):
  ctx.run("CREATE (l:Lesson) SET l.id = $lesson_id", lesson_id=lesson_id)


HOST_ELASTIC = "172.17.0.6"
INDEX = "tumindb"

HOST_NEO4J = 'bolt://172.17.0.4:7687'
AUTH = ('neo4j', 'zx3021')

driver = GraphDatabase.driver(HOST_NEO4J, auth=AUTH)

with driver.session() as session:
  session.write_transaction(clear_database)

es = Elasticsearch(HOST_ELASTIC)

with driver.session() as session:
  for i in range(1, 101):
    session.write_transaction(create_student, "rbook_" + str(i))

  response = es.search(index=INDEX, query={"match_all": {}}, size=1000)
  for item in response["hits"]["hits"]:
    session.write_transaction(create_lesson, item["_id"])

driver.close()

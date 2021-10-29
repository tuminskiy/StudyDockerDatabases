#!/usr/bin/python3.8

import redis
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from neo4j import GraphDatabase


def clear_database(ctx):
  ctx.run("MATCH (s)-[r1:PARTOF]->(g) DELETE r1")
  ctx.run("MATCH (g)-[r2:LEARN]->(l) DELETE r2")
  ctx.run("MATCH (s:Student) DELETE s")
  ctx.run("MATCH (g:Group) DELETE g")
  ctx.run("MATCH (l:Lesson) DELETE l")

def create_student(ctx, rbook):
  ctx.run("CREATE (s:Student) SET s.rbook = $rbook", rbook=rbook)

def create_lesson(ctx, lesson_id):
  ctx.run("CREATE (l:Lesson) SET l.id = $lesson_id", lesson_id=lesson_id)

def create_group(ctx, group_id):
  ctx.run("CREATE (g:Group) SET g.id = $group_id", group_id=group_id)

def create_sg_rel(ctx, rbooks, group_id):
  ctx.run("MATCH (s:Student) WHERE s.rbook in $rbooks "
          "MATCH (g:Group) WHERE g.id = $group_id "
          "CREATE (s)-[:PARTOF]->(g)",
          rbooks=rbooks, group_id=group_id)

def create_gl_rel(ctx, group_id, lessons):
  ctx.run("MATCH (g:Group) WHERE g.id = $group_id "
          "MATCH (l:Lesson) WHERE l.id in $lessons "
          "CREATE (g)-[:LEARN]->(l)",
          group_id=group_id, lessons=lessons)

HOST_ELASTIC = "172.17.0.5"
INDEX = "tumindb"

HOST_MONGO = "172.17.0.3"
DBNAME = "tumindb"

HOST_REDIS = "172.17.0.2"

HOST_NEO4J = 'bolt://172.17.0.4:7687'
AUTH = ('neo4j', 'zx3021')

driver = GraphDatabase.driver(HOST_NEO4J, auth=AUTH)

with driver.session() as session:
  session.write_transaction(clear_database)

r = redis.Redis(host=HOST_REDIS)
es = Elasticsearch(HOST_ELASTIC)
mongo = MongoClient(HOST_MONGO)[DBNAME]

with driver.session() as session:
  rbooks = [key.decode("ascii").split(":")[1] for key in r.keys("students:rbook_*")]
  for rbook in rbooks:
    session.write_transaction(create_student, rbook)

  lessons = es.search(index=INDEX, query={"match_all": {}}, size=1000)["hits"]["hits"]
  for lesson in lessons:
    session.write_transaction(create_lesson, lesson["_id"])

  groups = mongo["groups"].find({})
  index = 0
  for group in groups:
    g_id = str(group["_id"])

    session.write_transaction(create_group, g_id)

    start_index = 20*index
    end_index = 20*(index+1)
    index = index+1
    
    c_rbooks = rbooks[start_index:end_index]
    c_lessons = [lesson["_id"] for lesson in lessons[start_index:end_index]]

    session.write_transaction(create_sg_rel, c_rbooks, g_id)
    session.write_transaction(create_gl_rel, g_id, c_lessons)

driver.close()

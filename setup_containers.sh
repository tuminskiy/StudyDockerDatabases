#!/bin/bash

printf "Creating Redis container . . .\n"
docker rm -f c_redis || true
docker run -d --name "c_redis" redis

printf "\nCreating MongoDB container . . .\n"
docker rm -f c_mongo || true
docker run -d --name "c_mongo" mongo

printf "\nCreating Neo4j container . . .\n"
docker rm -f c_neo4j || true
docker run -d --name "c_neo4j" --env NEO4J_AUTH=neo4j/zx3021 neo4j

printf "\nCreating ElasticSearch 6.5.0 container . . .\n"
docker rm -f c_elastic || true
docker network rm elastic_net || true
docker network create elastic_net
docker run -d --name "c_elastic" --net elastic_net elasticsearch:6.5.0

printf "\nCreating PostgreSQL container . . .\n"
docker rm -f c_psql || true
docker run -d --name "c_psql" -e POSTGRES_PASSWORD=zx3021 postgres

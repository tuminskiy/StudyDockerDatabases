#!/usr/bin/python3.8

import psycopg2
import datetime
import calendar

conn = psycopg2.connect(user="postgres", password="zx3021", host="172.17.0.6", port="5432")
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS tumindb");
cursor.execute("CREATE DATABASE tumindb");

cursor.close()
conn.close()

conn = psycopg2.connect(user="postgres", password="zx3021", host="172.17.0.6", port="5432", database="tumindb")
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("CREATE TABLE visit ( "
               #"  id SERIAL NOT NULL PRIMARY KEY, "
               "  rbook VARCHAR(255) NOT NULL, "
               "  datetime TIMESTAMP NOT NULL, "
               "  lesson VARCHAR(255) NOT NULL"
               ") PARTITION BY RANGE (datetime);")

current_year = datetime.datetime.now().year
n_weeks = datetime.date(current_year, 12, 28).isocalendar()[1]

for week in range(1, n_weeks+1):
  str_date = "{year}-W{week}".format(year=current_year, week=week)
  from_date = datetime.datetime.strptime(str_date + "-1", "%Y-W%W-%w")

  str_date = "{year}-W{week}".format(year=current_year, week=week+1)
  to_date = datetime.datetime.strptime(str_date + "-1", "%Y-W%W-%w")

  query = "CREATE TABLE visit_{year}_{week} PARTITION OF visit FOR VALUES FROM ('{from_date}') TO ('{to_date}');" \
          .format(year=current_year, week=week, from_date=from_date, to_date=to_date)
  cursor.execute(query)

cursor.close()
conn.close()

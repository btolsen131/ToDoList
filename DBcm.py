#setting up database

dbconfig = {'host': '127.0.0.1',
            'user':'to_do_login',
            'password': 'password'}

import mysql.connector

conn = mysql.connector.connect(**dbconfig)

cursor = conn.cursor()

cursor.execute("CREATE database to_do")

_SQL="""create table login(
    id integer primary key,
    username varchar(20),
    password varchar(20));"""

#cursor.execute(_SQL)
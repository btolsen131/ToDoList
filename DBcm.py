#setting up database
import mysql.connector

dbconfig = {'host': '127.0.0.1',
            'user':'root',
            'password': 'fuzzbutt',
            'database': 'do_it_already'}



conn = mysql.connector.connect(**dbconfig)

cursor = conn.cursor()

cursor.execute("drop table login;")

_SQL="""create table login(
    id integer primary key auto_increment,
    username varchar(20),
    password varchar(20),
    email varchar(30));"""

#cursor.execute(_SQL)

_SQLinsert= """ insert into login (username, password, email)
                values('bto131','password','Brian@gmail.com');"""
#cursor.execute(_SQLinsert)

#conn.commit()
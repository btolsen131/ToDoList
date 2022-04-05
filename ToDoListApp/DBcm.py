#setting up database
import mysql.connector

_SQL="""create table login(
    id integer primary key auto_increment,
    username varchar(20),
    password varchar(256),
    email varchar(50));"""

#cursor.execute(_SQL)

_SQLinsert= """ insert into login (username, password, email)
                values('bto131','password','Brian@gmail.com');"""
#cursor.execute(_SQLinsert)

class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass


class UseDatabase:

    def __init__(self, config:dict) -> None:
        self.configuration = config

    def __enter__(self) -> 'Cursor':
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError 
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError

    def __exit__(self, exc_type, exc_value, exe_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
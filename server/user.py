
from flask import Flask
from flask_login import UserMixin
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Chiru1998$'
app.config['MYSQL_DB'] = 'knock_knock'
 
mysql = MySQL(app)

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE id = %s', [user_id])
        user = cursor.fetchone()
        if not user:
            return None

        user = User(
            id_=user["id"], name=user["name"], email=user["email"]
        )
        return user

    @staticmethod
    def create(id_, name, email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO User (id, name, email) VALUES (%s, %s, %s)', (id_, name, email))
        mysql.connection.commit()

class WebUser(UserMixin):
    def __init__(self, id_, name, email, H_pass):
        self.id = id_
        self.name = name
        self.email = email
        self.H_pass = H_pass

    @staticmethod
    def check(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE email = %s', [email])
        user = cursor.fetchone()

        if not user:
            return None

        cursor.execute('SELECT * FROM UserLogins WHERE user_id = %s', [user["user_id"]])
        cred = cursor.fetchone()

        user = WebUser(
            id_=user["user_id"], name=user["user_name"], email=user["email"], H_pass=cred["user_passkey"]
        )
        return user

    @staticmethod
    def create(name, email, H_pass, mobile, addr1, city, state, zip):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Users (user_name, email, mobile, address_line1, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, email, mobile, addr1, city, state, zip))
        cursor.execute('SELECT user_id FROM Users WHERE email = %s', [email])
        user = cursor.fetchone()
        cursor.execute('Insert INTO userlogins (user_id,user_passkey, is_active) VALUES (%s, %s, %s)', (user["user_id"], H_pass, 1))
        mysql.connection.commit()

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE user_id = %s', [user_id])
        user = cursor.fetchone()
        if not user:
            return None

        cursor.execute('SELECT * FROM UserLogins WHERE user_id = %s', [user["user_id"]])
        cred = cursor.fetchone()

        user = WebUser(
            id_=user["user_id"], name=user["user_name"], email=user["email"], H_pass=cred["user_passkey"]
        )
        return user

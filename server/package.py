from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootROOT1'
app.config['MYSQL_DB'] = 'knock_knock'
 
mysql = MySQL(app)

class Package():
    def __init__(self, user_id, tracking, addr_to, addr_from):
        self.user_id = user_id
        self.tracking = tracking
        self.addr_to = addr_to
        self.addr_from = addr_from

    def create(user_id, tracking, addr_from, addr_to):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Orders (user_id, tracking_id, order_status) VALUES (%s, %s, "Order Placed")', (user_id, tracking))
        cursor.execute('SELECT order_id FROM Orders WHERE tracking_id = %s', [tracking])
        package = cursor.fetchone()
        cursor.execute('Insert INTO OrderDetails (order_id, from_line1, from_line2, from_city, from_state, from_zip, to_line1, to_line2, to_city, to_state, to_zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (package["order_id"], addr_from["street1"], addr_from["street2"], addr_from["city"], addr_from["state"], addr_from["zip"], addr_to["street1"], addr_to["street2"], addr_to["city"], addr_to["state"], addr_to["zip"]))
        mysql.connection.commit()

    def get_location(tracking):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT order_id FROM Orders WHERE tracking_id = %s', [tracking])
        package = cursor.fetchone()

        if not package:
            return None
         
        cursor.execute('SELECT * FROM OrderDetails WHERE order_id = %s', [package['order_id']])
        package = cursor.fetchone()
        
        addr_curr = {
            "line1": package['from_line1'],
            "line2": package['from_line2'],
            "city": package['from_city'],
            "state": package['from_state'],
            "zip": package['from_zip']
        }

        return addr_curr

    def set_location(tracking, addr):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT order_id FROM Orders WHERE tracking_id = %s', [tracking])
        package = cursor.fetchone()

        if not package:
            return False
         
        cursor.execute('UPDATE OrderDetails SET from_line1 = %s, from_line2 = %s, from_city = %s, from_state = %s, from_zip = %s WHERE order_id = %s', (addr["street1"], addr["street2"], addr["city"], addr["state"], addr["zip"], package['order_id']))
        mysql.connection.commit()

        return True

    def get_status(tracking):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT order_status FROM Orders WHERE tracking_id = %s', [tracking])
        package = cursor.fetchone()

        if not package:
            return None

        return package['order_status']
    
    def set_status(tracking, status):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT order_id FROM Orders WHERE tracking_id = %s', [tracking])
        package = cursor.fetchone()

        if not package:
            return False

        cursor.execute('UPDATE Orders SET order_status = %s  WHERE order_id = %s', (status, package['order_id']))
        mysql.connection.commit()

        return True

        

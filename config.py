from flask import Flask
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'alfredlaw',        # change to your user name
    'password': '2302638',      # change to your password
    'database': 'infmaindb',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection
from flask import request, jsonify
import mysql.connector

from config import app, get_db_connection

## ROUTES ##
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Execute raw SQL query to fetch all users
        cursor.execute("create or replace table test (test_col text)")
        cursor.execute("insert into test values ('This is working')")
        cursor.execute("SELECT * FROM test")
        
        users = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return users as JSON response
        return jsonify(users)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500




## MAIN ##
if __name__ == '__main__':
    app.run(debug=True)
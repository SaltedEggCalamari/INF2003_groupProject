#############
## IMPORTS ##
#############

from flask import request, jsonify
from config import app, get_db_connection
import mysql.connector
from datetime import datetime

############
## ROUTES ##
############

## TEST CONNECTION TO DATABASE
##############################
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Execute queries
        cursor.execute("create or replace table test (test_col text)")
        cursor.execute("insert into test values ('This is working')")
        cursor.execute("SELECT * FROM test")
        
        data = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return as JSON response
        return jsonify(data)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

## CREATE
#########
@app.route('/insert/<string:table_name>', methods=['POST'])
def insert_to_table_name(table_name):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Send a request for data from frontend
        data = request.json
        
        # Get columns fields of table
        query = "show columns from " + table_name
        cursor.execute(query)
        table_info = cursor.fetchall()

        # Loops through table columns to get info on field name and data type
        new_insert = {}
        for column in table_info:
            Field = column.get("Field")
            Type = column.get("Type")

            # Excludes fields that have a default value
            if ('ID' not in Field and 'DateTime' not in Field):

                # Data type matching between request data and table fields
                if ('int' in Type):
                    new_insert.update({Field: int(data.get(Field))})
                
                elif ('decimal' in Type):
                    new_insert.update({Field: float(data.get(Field))})
                
                elif ('varchar' in Type or 'text' in Type):
                    new_insert.update({Field: data.get(Field)})
                
                elif ('date' in Type):
                    date_obj = datetime.strptime(data.get(Field), '%Y-%m-%d')
                    sql_date = date_obj.strftime('%Y-%m-%d')
                    new_insert.update({Field: sql_date})

        # Execute and commit query
        if (table_name == 'inventory'):
            cursor.execute('''INSERT INTO inventory 
                           (Name, Description, SKU, Model, Qty, Location, RawProd)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           [new_insert.get('Name'),
                            new_insert.get('Description'),
                            new_insert.get('SKU'),
                            new_insert.get('Model'),
                            new_insert.get('Qty'),
                            new_insert.get('Location'),
                            new_insert.get('RawProd')])
            
        if (table_name == 'purchasing'):
            cursor.execute('''INSERT INTO purchasing 
                           (PurchasingInvoiceNum, ProductName, Price, Model, SKU, Qty, PurchasingDate)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           [new_insert.get('PurchasingInvoiceNum'),
                            new_insert.get('ProductName'),
                            new_insert.get('Price'),
                            new_insert.get('Model'),
                            new_insert.get('SKU'),
                            new_insert.get('Qty'),
                            new_insert.get('PurchasingDate')])
        connection.commit()
            
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return as JSON response
        return
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


## READ
#######
@app.route('/table', methods=['GET'])
def get_table_names():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        query = "show tables"
        cursor.execute(query)
        
        data = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return as JSON response
        return jsonify(data)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/table/<string:table_name>', methods=['GET'])
def get_table_data(table_name):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        query = "SELECT * FROM " + table_name
        cursor.execute(query)
        
        data = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return as JSON response
        return jsonify(data)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    

## UPDATE
#########



## DELETE
#########


##########
## MAIN ##
##########
if __name__ == '__main__':
    app.run(debug=True)

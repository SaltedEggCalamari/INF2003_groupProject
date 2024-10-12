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

## TEST CONNECTION TO DATABASE ##

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


## ROUTE --> CREATE ##
# Sample response.json
# {
#   value: [v1, v2, v3, ..., vN], 
# }
@app.route('/insert/<string:table_name>', methods=['POST'])
def insert_to_table_name(table_name):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Send a request for data from frontend
        data = request.json
        value = data.get("value")
        
        # Get columns fields of table
        query = "SHOW COLUMNS FROM " + table_name
        cursor.execute(query)
        table_info = cursor.fetchall()

        # Loops through table columns to get info on field name and data type
        column_fields = []
        column_types = []
        for column in table_info:
            column_fields.append(column.get("Field"))
            column_types.append(column.get("Type"))

        # Match set_value to correct data type
        # sample set_value = [v1, v2, NA, v4, ..., vN]
        for i in range(len(column_types)):
            if (value[i] != 'NA'):
                if ('int' in column_types[i]):
                    value[i] = int(value[i])
                elif ('text' in column_types[i] or 'char' in column_types[i]):
                    value[i] = str(value[i])
                elif ('date' in column_types[i]):
                    date_obj = datetime.strptime(value[i], '%Y-%m-%d')
                    sql_date = date_obj.strftime('%Y-%m-%d')
                    value[i] = sql_date

        # Generate and execute query
        query = f"INSERT INTO {table_name} (" + ", ".join([f"{field}" for field in column_fields]) + f") VALUES (" + ", ".join([f"{val}" for val in value]) + ")"
        print(query)
        cursor.execute(query)
        
        connection.commit()
            
        # Close the connection and return
        cursor.close()
        connection.close()
        return (query)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


## ROUTE --> READ ##

@app.route('/table', methods=['GET'])       # Get name of all tables in database as JSON
def get_table_names():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        cursor.execute("show tables")
        data = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Return as JSON response
        return jsonify(data)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/table/<string:table_name>', methods=['GET']) # Get all data from table as JSON
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
    

## ROUTE --> UPDATE ##

# Sample response.json
# {
#   value: [v1, v2, v3, ..., vN], 
#   condition: "fN = x"
# }
@app.route('/update/<string:table_name>', methods=['UPDATE'])
def update_to_table_name(table_name):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Send a request for data from frontend
        data = request.json
        set_value = data.get("value")
        condition_value = data.get("condition")
        
        # Get Field and Type of table columns
        query = "show columns from " + table_name
        cursor.execute(query)
        table_info = cursor.fetchall()
        column_fields = []
        column_types = []

        for column in table_info:
            column_fields.append(column.get("Field"))
            column_types.append(column.get("Type"))

        table_info = {
            "Field": column_fields,
            "Type": column_types
        }

        # Match set_value to correct data type
        # sample set_value = [v1, v2, NA, v4, ..., vN]
        for i in range(len(column_types)):
            if (set_value[i] != 'NA'):
                if ('int' in column_types[i]):
                    set_value[i] = int(set_value[i])
                elif ('text' in column_types[i] or 'char' in column_types[i]):
                    set_value[i] = str(set_value[i])
                elif ('date' in column_types[i]):
                    date_obj = datetime.strptime(set_value[i], '%Y-%m-%d')
                    sql_date = date_obj.strftime('%Y-%m-%d')
                    set_value[i] = sql_date

            # Match NA value to field and type
            if (set_value[i] == 'NA'):
                column_fields[i] = 'NA'
                column_types[i] = 'NA'

        # Clear any NA from all arrays
        set_value = [item for item in set_value if item != 'NA']
        column_fields = [item for item in column_fields if item != 'NA']
        column_types = [item for item in column_types if item != 'NA']

        query = f"UPDATE {table_name} SET " + ", ".join([f"{field} = %s" for field in column_fields]) + f" WHERE {condition_value}"
        print(query)
        cursor.execute(query, set_value)

        connection.commit()
            
        # Close the connectione and return
        cursor.close()
        connection.close()
        return
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


## ROUTE --> DELETE ##
# Sample response.json
# {
#   condition: "fN = x"
# }
@app.route('/delete/<string:table_name>', methods=['DELETE'])
def delete_from_table_name(table_name):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Send a request for data from frontend
        data = request.json
        condition_value = data.get("condition")

        # Generate and execute query
        query = f"DELETE FROM {table_name} WHERE {condition_value}"
        print(query)
        cursor.execute(query)

        connection.commit()
            
        # Close the connectione and return
        cursor.close()
        connection.close()
        return
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500



## ROUTE --> BUILD ##

@app.route('/build/<string:product_name>/<int:qty>', methods=['UPDATE'])
def build_product(table_name):
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
            
        # Close the connectione and return
        cursor.close()
        connection.close()
        return
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


## ROUTE --> CHECK ##

@app.route('/check/<string:product_name>', methods=['GET'])
def check_product(table_name):
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
            
        # Close the connectione and return
        cursor.close()
        connection.close()
        return
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


##########
## MAIN ##
##########
if __name__ == '__main__':

    # Start application
    app.run(debug=True)

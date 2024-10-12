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
        cursor.execute("CREATE OR REPLACE TABLE test (test_col text)")
        cursor.execute("INSERT INTO test VALUES ('This is working')")
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
        cursor.execute("SHOW TABLES")
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
        query = "SHOW COLUMNS FROM " + table_name
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
# Sample response.json
# {
#     Model: "x",
#     Qty: y
# }
@app.route('/build', methods=['UPDATE'])
def build_product():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Send a request for data from frontend
        data = request.json
        product_model = data.get('Model')
        build_qty = data.get('Qty')

        # Building recipe for products {Product model: [ [component_model], [no. of components] ]}
        recipe = {
            'BS-400': [['SD-100', 'SC-700', 'PCB-11', 'PC-300', 'CCB-500', 'BAT-5000'], [1,1,1,1,1,1]],
            'BS-600': [['SD-200', 'SC-700', 'PCB-11', 'PC-300', 'CCB-500', 'BAT-5000'], [1,2,1,1,1,1]],
            'BS-650': [['SD-300', 'SC-800', 'PCB-12', 'PC-300', 'CCB-700', 'BAT-5000'], [2,2,1,1,1,2]],
            'PC-5000': [['BAT-5000', 'CCB-500', 'PC-200'], [1,1,1]],
            'PC-10000': [['BAT-10K', 'CCB-700', 'PC-200'], [1,1,1]],
        }

        # Generate and execute query
        components, recipe_qty = recipe[product_model]
        conditions = []
        for component, qty in zip(components, recipe_qty):
            conditions.append(f"(Model = '{component}' AND Qty >= {build_qty*qty})")

        condition_query = " OR ".join(conditions)
        query = f"SELECT Model, Qty FROM inventory WHERE {condition_query}"

        cursor.execute(query)
        fetch = cursor.fetchall()

        # Check if components are sufficient for build
        if(len(fetch) == len(components)): check = True
        else: check = False

        # Update inventory
        if(check):

            # Get original qty of product from inventory
            query = f"SELECT qty FROM inventory WHERE Model = '{product_model}'"
            cursor.execute(query)
            fetch = cursor.fetchall()[0]
            original_qty = fetch.get("qty")

            # Update qty of product to new quantity
            query = f"UPDATE inventory SET Qty = {original_qty+build_qty} WHERE Model = '{product_model}'"
            cursor.execute(query)

            # Get original qty of components    
            conditions = []
            for component in components:
                conditions.append(f"Model = '{component}'")
            condition_query = " OR ".join(conditions)

            query = f"SELECT Model, qty FROM inventory WHERE ({condition_query})"
            cursor.execute(query)
            fetch = cursor.fetchall()

            # Update qty of components to new quantity            
            conditions = []
            models = []
            for component in fetch:
                model = component.get("Model")
                qty = component.get("qty") - build_qty

                conditions.append(f"WHEN Model = '{model}' THEN {qty}")
                models.append(f"'{model}'")

            condition_query = " ".join(conditions)
            model_query = ", ".join(models)
            
            query = f"UPDATE inventory SET Qty = CASE {condition_query} END WHERE Model IN ({model_query})"
            cursor.execute(query)

        # Execute and commit query
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

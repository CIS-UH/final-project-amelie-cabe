# Amelie Cabergas ID: 2079648
import flask
from flask import jsonify
from flask import request
import mysql.connector
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up application
app.config["DEBUG"] = True #allows to show errors in browser

conn = create_connection("cis2368fall.c1ai8ok8u443.us-east-1.rds.amazonaws.com", "admin", "cis2368123", "cis2368falldb")
cursor = conn.cursor(dictionary = True)

sql = "SELECT * FROM investor"
cursor.execute(sql)
investor_tb = cursor.fetchall()

@app.route('/api/investor', methods=['GET'])
def api_all():
    call_investor = "SELECT * FROM investor"
    investor_list = execute_read_query(conn, call_investor)
    return jsonify(investor_list)

#returns one investor from ID
@app.route('/api/single_investor', methods=['GET'])
def api_id():
    request_data = request.get_json()
    fetch_id = request_data["id"]
    for i in range(len(investor_tb)):
        if investor_tb[i]['ID'] == fetch_id:
            query = f"""SELECT * FROM investor 
            WHERE id = {fetch_id} """
            result = execute_read_query(conn, query)
            return jsonify(result)
    return "no match found"

# add users
@app.route('/api/add_investor', methods =['POST'])
def api_add():
    request_data = request.get_json()
    new_fname = request_data["firstname"]
    new_lname = request_data["lastname"]
    query = """INSERT INTO investor (firstname, lastname)
    VALUES ('%s','%s');""" %(new_fname, new_lname)
    execute_query(conn, query) 
    return "add request successful"

#deletes user
@app.route('/api/delete_investor', methods=['DELETE'])
def api_delete():
    request_data = request.get_json()
    idToDelete = request_data['id']
    for i in range(len(investor_tb) -1, -1, -1):
        if investor_tb[i]["ID"] == idToDelete:
            #query to delete where the id matches
            query = "DELETE FROM investor WHERE ID = %s" %(idToDelete)
            execute_query(conn, query)
            return "delete request successful"



app.run()
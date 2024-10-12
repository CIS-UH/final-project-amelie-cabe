# Amelie Cabergas ID: 2079648
import flask
from flask import jsonify
from flask import request
import mysql.connector
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up application
app.config["DEBUG"] = True #allows to show errors in browser

conn = create_connection("cis2368fall.c1ai8ok8u443.us-east-1.rds.amazonaws.com", "admin", "cis2368123", "cis2368falldb")
cursor = conn.cursor(dictionary = True)

# all return for testing CRUD operations
@app.route('/api/investor', methods=['GET'])
def api_all():
    call_investor = "SELECT * FROM investor"
    investor_list = execute_read_query(conn, call_investor)
    return jsonify(investor_list)

@app.route('/api/stock', methods=['GET'])
def api_all_stock():
    call_stock = "SELECT * FROM stock"
    stock_list = execute_read_query(conn, call_stock)
    return jsonify(stock_list)

@app.route('/api/bond', methods=['GET'])
def api_all_bond():
    call_bond = "SELECT * FROM bond"
    bond_list = execute_read_query(conn, call_bond)
    return jsonify(bond_list)

#returns one investor from ID
@app.route('/api/single_investor', methods=['GET'])
def api_investor_id():
    request_data = request.get_json()
    fetch_id = request_data["ID"]
    query = f"""SELECT * FROM investor 
    WHERE id = {fetch_id} """
    result = execute_read_query(conn, query)
    if result:
        return jsonify(result)
    return "no match found"

# add users
@app.route('/api/add_investor', methods =['POST'])
def api_add_investor():
    request_data = request.get_json()
    new_fname = request_data["firstname"]
    new_lname = request_data["lastname"]
    query = f"""INSERT INTO investor (firstname, lastname)
    VALUES ('{new_fname}','{new_lname}');"""
    execute_query(conn, query) 
    return "investor add request successful"

#edit users - edits all values code similar to homework 2 extra credit
@app.route('/api/edit_investor', methods=['PUT'])
def api_update_user():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newfname = request_data["firstname"]
    newlname = request_data["lastname"]
    query = f"""UPDATE investor
    SET firstname = '{newfname}', lastname = '{newlname}' 
    WHERE id = {idToUpdate}"""
    execute_query(conn,query)
    return "edit request successful"

#deletes user
@app.route('/api/delete_investor', methods=['DELETE'])
def api_delete_user():
    request_data = request.get_json()
    idToDelete = request_data['ID']

    # checks from the table investors to throw correct return message in postman
    check_investor = "SELECT * FROM investor"
    investor_list = execute_read_query(conn, check_investor)

    #code reused from class to match given id to id in table
    for i in range(len(investor_list)-1,-1,-1):
        if investor_list[i]["ID"] == idToDelete :
            #query to delete where the id matches
            query = f"DELETE FROM investor WHERE ID = {idToDelete}" 
            execute_query(conn, query)
            return "delete request successful"
    return "ID not found delete request unsuccessful"

#add stock
@app.route('/api/add_stock', methods=['POST'])
def api_add_stock():
    request_data = request.get_json()
    new_stockname = request_data['stockname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = f'''INSERT INTO stock (stockname, abbreviation, currentprice)
    VALUES ('{new_stockname}','{new_abbr}', {new_price} )'''
    execute_query(conn,query)
    return "add request successful"

#edit stock
@app.route('/api/edit_stock', methods=['PUT'])
def api_edit_stock():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newsname = request_data["stockname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    query = f"""UPDATE stock 
    SET stockname = '{newsname}', abbreviation = '{newabb}', currentprice = {newprice}
    WHERE id = {idToUpdate}""" 
    execute_query(conn, query)
    return "stock edit was successful"

#delete stock
@app.route('/api/delete_stock', methods=['DELETE'])
def api_delete_stock():
    request_data = request.get_json()
    idToDelete = request_data['ID']

    check_stock = "SELECT * FROM stock"
    stock_list = execute_read_query(conn, check_stock)

    for i in range(len(stock_list)-1,-1,-1):
        if stock_list[i]["ID"] == idToDelete :
            #query to delete where the id matches
            query = f"DELETE FROM stock WHERE ID = {idToDelete}" 
            execute_query(conn, query)
            return "delete request successful"
    return "ID not found delete request unsuccessful"

#add bond
@app.route('/api/add_bond', methods=['POST'])
def api_add_bond():
    request_data = request.get_json()
    new_bondname = request_data['bondname']
    new_abbr = request_data['abbreviation']
    new_price = request_data['currentprice']
    query = f'''INSERT INTO bond (bondname, abbreviation, currentprice)
    VALUES ('{new_bondname}','{new_abbr}', {new_price} )'''
    execute_query(conn,query)
    return "bond add request successful"

#edit bond
@app.route('/api/edit_bond', methods=['PUT'])
def api_edit_bond():
    request_data = request.get_json()
    idToUpdate = request_data["ID"]
    newbname = request_data["bondname"]
    newabb = request_data["abbreviation"]
    newprice = request_data["currentprice"]
    query = f"""UPDATE bond 
    SET bondname = '{newbname}', abbreviation = '{newabb}', currentprice = {newprice}
    WHERE id = {idToUpdate}"""
    result = execute_query(conn, query)
    return "bond edit was successful"


#delete bond
@app.route('/api/delete_bond', methods=['DELETE'])
def api_edit_delete():
    request_data = request.get_json()
    idToDelete = request_data['ID']

    call_bond = "SELECT * FROM bond"
    bond_list = execute_read_query(conn, call_bond)

    for i in range(len(bond_list) -1, -1, -1):
        if bond_list[i]["ID"] == idToDelete:
            #query to delete where the id matches
            query = f"DELETE FROM bond WHERE ID = {idToDelete}" 
            execute_query(conn, query)
            return "delete request successful"
    return "ID not found delete request not sucessful"
        
app.run()
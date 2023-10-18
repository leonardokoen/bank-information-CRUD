from flask import Flask
from flask import request, render_template, redirect, url_for, flash
import pyodbc
from conf_dbconnection import *

#Initialising app
app = Flask(__name__)

# Connecting to MS SQL Server and Database using odbc driver.
conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};Encrypt=no'

# This function creates the connection to the database
def get_db_conn():
    conn = pyodbc.connect(conn_str)   
    return conn

#Insertion View: Inserts to the database, utilizes forms. 
@app.route("/insert", methods=["POST", "GET"])
def insert():
    # If the HTTP Request is Post 
    if request.method == "POST":
        # Create SQL command 
        sqlcommand = """INSERT INTO information.banks(name, country, state, city, address, number)
                        VALUES
                        (?,?,?,?,?,?)"""
        # Use the data from the form
        data = request.form
        # Connect to the database
        conn = get_db_conn()
        cursor = conn.cursor()
        # Execute the SQL command for the insertion in the database
        try:
            cursor.execute(sqlcommand,data["banksname"], data["country"], data["state"], data["city"], data["address"], data["number"])
        except:
            return redirect(url_for("insert"))

        # Commiting the changes
        conn.commit()
        # Close the connection
        conn.close()
        # Redirect the url to a success route passing argument bank
        return (redirect(url_for("success", bank = data['banksname'])))
    else:
        # This is the HTTP GET method    
        return render_template("insert.html")
      
# Success View : Prints Successful Insertion
@app.route("/insert/<bank>/success")
def success(bank):
    return f"<h1>You have successfully inserted {bank} in the database.<h1>"

# List View : Reads all distinct banks' names from the database
@app.route('/list')
def list():
    # Exactly the same procedure as described before
    sqlcommand = """SELECT DISTINCT(name) AS banks FROM information.banks ORDER BY name"""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(sqlcommand)
    # Load data in memory
    data = cursor.fetchall()
    conn.close()
    return render_template("list.html", data=[tuple[0] for tuple in data])

# Search View: Redirects To a new route based on the name given in the form
@app.route('/info',  methods=["POST","GET"])
def search():
    if request.method == "POST":
        data = request.form
        return (redirect(url_for("info", name = data['banksname'])))
    else:    
        return render_template("search.html")

# Information View: Prints the information for the bank given
@app.route("/info/<name>")
def info(name):
    sqlcommand = """SELECT name, country + ', ' + state + ', ' + city + ', ' + address + ' ' + number AS location FROM information.banks
                    WHERE name = ?"""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(sqlcommand,name)
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return redirect(url_for("search"))
    return render_template("info.html", location = data[0][1], name =data[0][0])

#Update Search View: Searches if the name of the bank exists   
@app.route("/update" , methods = ["POST", "GET"])
def search_update():
    if request.method == "POST":
        data = request.form
        return (redirect(url_for("update", name = data['banksname'])))
    else:    
        return render_template("search.html")

# Update View: Update fields
@app.route("/update/<name>", methods = ["POST","GET"])
def update(name):
    if request.method == "POST":
        sqlcommand = """UPDATE information.banks SET name=?, country=?, state=?, city=?, address = ?, number = ?
                        WHERE name = ?"""
        data = request.form
        # Connect to the database
        conn = get_db_conn()
        cursor = conn.cursor()
        # Execute the SQL command for the updating in the database
        try:
            cursor.execute(sqlcommand,data["banksname"], data["country"], data["state"], data["city"], data["address"], data["number"], name)
        except:
            return redirect(url_for("update", name = name))

        # Commiting the changes
        conn.commit()
        # Close the connection
        conn.close()
        # Redirect the url to a success route passing argument bank
        return redirect(url_for("update_success", name = name))
    
    else: 
        sqlcommand = """SELECT name, country, state, city, address, number FROM information.banks WHERE name = ?"""
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(sqlcommand,name)
        data = cursor.fetchall()
        conn.close()
        # Check if data exists
        if len(data) == 0:
            return redirect(url_for("search_update"))
        
        return render_template("update.html", name = data[0][0], country = data[0][1], state = data[0][2], city = data[0][3], address = data[0][4], number = data[0][5])

# Success Update View 
@app.route("/update/<name>/success")
def update_success(name):
    return f"<h1>You have successfully updated {name} in the database.<h1>"

# Delete Search View
@app.route("/delete", methods = ["POST", "GET"])
def search_delete():
    if request.method == "POST":
        data = request.form
        return (redirect(url_for("delete", name = data['banksname'])))
    else:    
        return render_template("search.html")

# Delete View
@app.route("/delete/<name>", methods = ["POST", "GET"])
def delete(name):
    if request.method == "POST":
        data = request.form
        if data["answer"] == "I want to delete " + name:
            conn = get_db_conn()
            cursor = conn.cursor()
            # Execute the SQL command for the insertion in the database
            sqlcommand = """DELETE FROM information.banks WHERE name = ?"""
            try:
                cursor.execute(sqlcommand, name)
            except:
                return redirect(url_for("index"))

            # Commiting the changes
            conn.commit()
            # Close the connection
            conn.close()
            # Redirect the url to a success route passing argument name
            return redirect(url_for("delete_success", name = name))
        else:
            # If the data['answer'] is not the one prefedined redirect to /
            return redirect(url_for("index"))
    else:
        sqlcommand = """SELECT * FROM information.banks WHERE name = ?"""
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(sqlcommand,name)
        data = cursor.fetchall()
        conn.close()
        # Check if data exists
        if len(data) == 0:
            return redirect(url_for("search_delete"))    
        return render_template("delete.html", name = name)

#Successful Delete View
@app.route("/delete/<name>/success")
def delete_success(name):
    return f"<h1>You have successfully deleted {name} from the database.<h1>"

#Index View: The homepage
@app.route("/")
def index():
    return render_template("index.html")

# Run server
if __name__== "__main__" :
      app.run(debug=True) 
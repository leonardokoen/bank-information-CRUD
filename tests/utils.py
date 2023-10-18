import pyodbc
from conf_dbconnection import *
from app import app

def del_by_names(names):
    conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};Encrypt=no'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    for name in names:
        cursor.execute("""DELETE FROM information.banks WHERE name = ?""", name)
    conn.commit()
    conn.close()


def create_dummy_banks(names) :
    for name in names:
        app.test_client().post ("/insert", data= {
        "banksname" : name,
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })

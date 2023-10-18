from utils import *

def test_connection():
    conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};Encrypt=no'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM information.banks')
    rows = cursor.fetchall()
    assert len(rows) > 0
    conn.close()
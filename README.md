# Banks-CRUD-Application

This is a small CRUD application using Flask and Microsoft SQL Server to manage a table in the database that contains information about banks(name, location).

## Installation

1) Clone Repository
    
    ```cmd
    git clone https://github.com/leonardokoen/bank-information-CRUD.git
    ```

2) Create python environment

    ```cmd
    python -m venv c:\path\to\myenv\.bank_crud
    ```

3) Activate environment

    ``` cmd
    c:\path\to\myenv\.bank_crud\Scripts\activate
    ```

4) Download requirements.txt

    ```cmd
    cd c:\project\directory
    ```

    ```cmd
    pip install --upgrade pip
    ```

    ```cmd
    pip install -r requirements.txt
    ```

5) Download MS SQL SERVER & SSMS

    ```link
    https://www.microsoft.com/en-us/sql-server/sql-server-downloads
    ```

    ```link
    https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16
    ```

6) Download ODBC Driver 18

    ```link
    https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
    ```

7) Connect in sqlcmd as admin and run the following queries.

    ```sql
    CREATE DATABASE banks;
    GO
    ```

    ```sql
    USE banks;
    GO
    ```

    ```sql
    CREATE SCHEMA information;
    GO
    ```

    ```sql
    CREATE TABLE information.banks (
        id INT IDENTITY (1,1) PRIMARY KEY,
        name VARCHAR (63) NOT NULL UNIQUE, 
        country VARCHAR(63) NOT NULL,
        state VARCHAR(63) NOT NULL,
        city VARCHAR(63) NOT NULL,
        address VARCHAR(63) NOT NULL,
        number VARCHAR(8) NOT NULL
    );
    GO
    ```

8) Create a new Log In and User to connect via SQL Server Authentication and grand SELECT INSERT DELETE UPDATE access to the user for the banks database. (Mandatory if you have only Windows Authentication access to your SQL Server).

9) Insert in conf_dbconnection.py your User credentials and save the file.

    ```python
    DRIVER = "ODBC Driver 18 for SQL Server"
    SERVER = "localhost"
    DATABASE = "banks"
    UID = "test"
    PWD = "test"
    ```

10) Run the following command to start the application

    ```cmd
    python app.py
    ```

11) In a web browser visit http://127.0.0.1:5000/

## Routes

1) / : It redirects user to all the routes that perform the basic CRUD functionallity.

2) /insert : User can insert a bank in the database, all the fields are required and the name should not exist in the database. If the name exists it redirects user to /insert.

    ```python
    POST("/insert", data = {
        "banksname" : "new bank",
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817"
    })
    ```

3) /insert/name_of_bank/success : User will be redirected in this route when user has successfully inserted a row in the database.

4) /list : This route display all the names of the banks in the database.

5) /info : This route redirects user to /info/name_of_bank

    ```python
        POST("/info", data = {
            "banksname" : "new bank"
        })
    ```

6) /info/name_of_bank : This route checks if name_of_bank exists in the database. If it exists it displays the name and the location of the bank. If it doesn't exists it redirects user to /info.

7) /update :  This route redirects you to /update/name_of_bank

    ```python
        POST("/update", data = {
            "banksname" : "new bank"
        })
    ```

8) /update/name_of_bank : This route checks if name_of_bank exists in the database. If it exists user can update the bank's information. If it does not exists it redirects user to /update.
If user is missing a field or the updated name already exists in the database it redirects user to /update without updating the information.

    ```python
        POST("/update/new%20bank", data = {
            "banksname" : "new bank",
            "country" : "USA",
            "state" : "Florida", 
            "city" : "Tallahassee", 
            "address" : "Belair Rd",
            "number" : "8"
        })
    ```

9) /update/name_of_bank/success : User will be redirected in this route when user has successfully updated a row in the database.

10) /delete : This route redirects user to /delete/name_of_bank

    ```python
        POST("/delete", data = {
            "banksname" : "new bank"
        })
    ```

11) /delete/name_of_bank : This route checks if name_of_bank exists in the database. If it exists user should type "I want to delete name_of_bank" to delete the bank from database. If it doesn't exist it redirects user to /delete. In case user does not type exactly "I want to delete name_of_bank" the application redirects user to /

    ```python
        POST("/delete/new%20bank", data = {
            "answer" : "I want to delete new bank"
        })
    ```

12) /delete/name_of_bank/success : User will be redirected in this route, when user has successfully deleted a row in the database.

## Testing

I have prepared 23 tests for some situations that I could think of:

- 1-test for database connectivity.

- 6-tests for deletion(Test Redirections, Responses)

- 4-tests for insertion(Test Redirections, Responses)

- 1-test for listing

- 4-tests for providing information(Test Redirections, Responses)

- 7-tests for updating(Test Redirections, Responses)

```cmd
cd c:\project\directory
```

```cmd
python -m pytest
```

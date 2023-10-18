from utils import *

# Test GET method of Insert View
def test_insert_route_get():
    response = app.test_client().get('/insert')
    assert response.status_code == 200


def test_insert_route_post_and_redirection():

    del_by_names(['new bank'])
    response = app.test_client().post ("/insert", data= {
        "banksname" : 'new bank',
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })

    assert response.status_code == 302
    assert response.headers['Location'] == '/insert/' + "new%20bank" + '/success'
    del_by_names(['new bank'])

def test_already_existing_bank():

    del_by_names(['new bank'])
    response = app.test_client().post ("/insert", data= {
        "banksname" : 'new bank',
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })
    
    response = app.test_client().post ("/insert", data= {
        "banksname" : 'new bank',
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })
    assert response.status_code == 302
    assert response.headers['Location'] == '/insert'
    del_by_names(['new bank'])


def test_missing_fields():

    del_by_names(['new bank'])
    response = app.test_client().post ("/insert", data= {
        "banksname" : "new bank", 
        "city" : "Austin", 
        "address" : "Circle Drive"
        })
    
    assert response.status_code == 302
    assert response.headers['Location'] == '/insert'
    del_by_names(['new bank'])

from utils import *

def test_search_update():
    response = app.test_client().get("/update")
    assert response.status_code == 200

def test_update_search_not_existing_bank():
    del_by_names(["new bank"])
    response = app.test_client().post ("/update", data= {
        "banksname" : "new bank",
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/update/' + 'new%20bank'

def test_update_route_get_existing_bank():
    del_by_names(["new bank"])
    create_dummy_banks(["new bank"])
    response = app.test_client().get ("/update/new%20bank")
    assert response.status_code == 200
    del_by_names(["new bank"])

def test_update_route_get_non_existing_bank():
    del_by_names(["new bank"])
    response = app.test_client().get ("/update/new%20bank")
    assert response.status_code == 302
    assert response.headers['Location'] == '/update'

def test_updating_same_name_different_location():
    del_by_names(["new bank", "new bank 1"])
    create_dummy_banks(["new bank" , "new bank 1"])
    response = app.test_client().post('/update/new%20bank',data = {
        "banksname" : "new bank",
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })
    assert response.status_code == 302
    assert response.headers['Location'] == '/update/new%20bank/success'
    del_by_names(["new bank", "new bank 1"])

def test_updating_different_name_not_existing():
    del_by_names(["new bank", "new bank 1"])
    create_dummy_banks(["new bank" , "new bank 1"])
    response = app.test_client().post('/update/new%20bank',data= {
        "banksname" : 'new bank 2',
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })

    assert response.status_code == 302
    assert response.headers['Location'] == '/update/new%20bank/success'
    del_by_names(["new bank 1", "new bank 2"])

def test_updating_different_name_existing():
    del_by_names(["new bank", "new bank 1"])
    create_dummy_banks(["new bank" , "new bank 1"])
    response = app.test_client().post('/update/new%20bank',data= {
        "banksname" : 'new bank 1',
        "country" : "USA",
        "state" : "Texas", 
        "city" : "Austin", 
        "address" : "Circle Drive",
        "number" : "9817" })

    assert response.status_code == 302
    assert response.headers['Location'] == '/update/new%20bank'
    del_by_names(["new bank", "new bank 1"])
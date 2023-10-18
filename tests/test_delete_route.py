from utils import *

def test_search_delete():
    response = app.test_client().get("/delete")
    assert response.status_code == 200

def test_delete_search_not_existing_bank():
    del_by_names(["new bank"])
    response = app.test_client().post ("/delete", data= {
        "banksname" : "new bank",
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/delete/' + 'new%20bank'

def test_delete_route_get_existing_bank():
    del_by_names(["new bank"])
    create_dummy_banks(["new bank"])
    response = app.test_client().get ("/delete/new%20bank")
    assert response.status_code == 200
    del_by_names(["new bank"])

def test_delete_route_get_non_existing_bank():
    del_by_names(["new bank"])
    response = app.test_client().get ("/delete/new%20bank")
    assert response.status_code == 302
    assert response.headers['Location'] == '/delete'

def test_deleting_correct_message():
    del_by_names(["new bank"])
    create_dummy_banks(["new bank"])
    response = app.test_client().post('/delete/new%20bank',data = {
        "answer" : "I want to delete new bank",
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/delete/new%20bank/success'
    del_by_names(["new bank"])

def test_deleting_wrong_message():
    del_by_names(["new bank"])
    create_dummy_banks(["new bank"])
    response = app.test_client().post('/delete/new%20bank',data = {
        "answer" : "I want to delete new",
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    del_by_names(["new bank"])
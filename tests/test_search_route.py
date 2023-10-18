from utils import *

def test_search_route_get():
    response = app.test_client().get("/info")
    assert response.status_code == 200

def test_search_route_post():
    del_by_names(["new bank"])
    response = app.test_client().post ("/info", data= {
        "banksname" : "new bank",
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/info/' + 'new%20bank'

def test_info_route_get_existing_bank():
    del_by_names(["new bank"])
    create_dummy_banks(["new bank"])
    response = app.test_client().get ("/info/new%20bank")
    assert response.status_code == 200
    del_by_names(["new bank"])

def test_info_route_get_non_existing_bank():
    del_by_names(["new bank"])
    response = app.test_client().get ("/info/new%20bank")
    assert response.status_code == 302
    assert response.headers['Location'] == '/info'







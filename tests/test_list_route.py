from utils import *

def test_list_route():

    names = ['new bank 0', 'new bank 1', 'new bank 2', 'new bank 3']
    del_by_names(names)
    create_dummy_banks(names)
    
    response = app.test_client().get('/list')
    assert response.status_code == 200
    del_by_names(names)
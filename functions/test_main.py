import os
from main import on_request_example

def test_on_request_example():
    os.environ["OURA_API_KEY"] = 'oura123456'
    resp = on_request_example(None)

    assert(resp.status_code == 200)
    assert(resp.status == '200 OK')
    assert(resp.get_data(True) == 'OURA_VARIABLE=oura123456')

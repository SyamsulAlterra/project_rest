import pytest,json, logging
from flask import Flask, request

from blueprints import app
from app import cache

def call_client(request):
    client=app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token_internal():
    token = cache.get('test-token-internal')
    if token is None:
        data={
            'id' : '1'
        }

        req = call_client(request)
        res = req.get('/token',query_string=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_non_internal():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'id' : '0',
        }

        req = call_client(request)
        res = req.get('/token',query_string=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-non-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token
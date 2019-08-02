import json
from . import app,client, cache, create_token_internal,create_token_non_internal


class TestEvent():
    def test_event_get(self,client):
        token = create_token_internal()
        res = client.get('/user/get_event/1',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_event_get_invalid_id(self,client):
        token = create_token_internal()
        res = client.get('/user/get_event/0',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_event_get_invalid_token(self,client):
        res = client.get('/user/get_event/1',headers={'Authorization':'Bearer abc'})
        res_json = json.loads(res.data)
        assert res.status_code == 500


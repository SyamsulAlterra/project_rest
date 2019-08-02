import json
from . import app,client, cache, create_token_internal


class TestEvent():
    tempclient=0
    def test_event_get(self,client):
        token = create_token_internal()
        res = client.get('/client/list',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
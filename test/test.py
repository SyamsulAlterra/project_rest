import json
from . import app,client, cache, create_token_internal, create_token_non_internal

class TestEvent():
    #internal user get all event
    def test_valid_get_internal_user(self, client):
        token = create_token_internal()
        res = client.get('/user/event', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200
        
    #internal user post an event
    def test_valid_post_event(self, client):
        token = create_token_internal()
        data = {
            'nama': 'Hore hore',
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.post('/user/event', headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')
        assert res.status_code == 200

    #invalid post from non internal user
    def test_invalid_post_event(self,client):
        token = create_token_non_internal()
        data = {
            'nama': 'Hore hore',
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.post('/user/event', headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')
        assert res.status_code == 403

    #valid delete post from internal user
    def test_valid_delete_event(self, client):
        token = create_token_internal()
        res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    def test_invalid_delete_event(self, client):
        token = create_token_non_internal()
        res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 403


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

# dari nada
import json
from . import app,client, cache, create_token_internal, create_token_non_internal

<<<<<<< HEAD

class TestEventEndpoint():
=======
class TestEvent():
    tempevent=0
>>>>>>> 3c825b871a26c489ad64f7e36971311fe1441501
    #internal user get all event
    def test_valid_get_internal_user(self, client):
        token = create_token_internal()
        res = client.get('/user/event', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200
<<<<<<< HEAD

    #internal user post an event
    # def test_valid_post_event(self, client):
    #     token = create_token_internal()
    #     data = {
    #         'nama': 'Hore hore',
    #         'ip': '138.68.161.14',
    #         'waktu': '2010-10-10 14:00:00'
    #     }

    #     res = client.post('/user/event', headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')

    #     assert res.status_code == 200
=======
        

    #internal user post an event
    def test_valid_post_event(self, client):
        token = create_token_internal()
        data = {
            'nama': 'Hore hore',
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.post('/user/event', headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')
        res_json = json.loads(res.data)
        TestEvent.tempevent=29
        # self.tempevent=res_json['id']
        assert res.status_code == 200
>>>>>>> 3c825b871a26c489ad64f7e36971311fe1441501

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

<<<<<<< HEAD
    #valid delete post from internal user
    # def test_valid_delete_event(self, client):
    #     token = create_token_internal()

    #     res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})

    #     assert res.status_code == 200

    #invalid delete from non internal user
    def test_invalid_delete_event(self, client):
        token = create_token_non_internal()
=======

    #valid put post from internal user
    def test_valid_put_event(self, client):
        token = create_token_internal()
        data = {
            'nama': 'Hore hore hore',
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.put('/user/event/'+str(TestEvent.tempevent), headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')
        assert res.status_code == 200

    #invalid put missing one argument
    def test_invalid_put_event(self, client):
        token = create_token_internal()
        data = {
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.put('/user/event/'+str(TestEvent.tempevent), headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')
        assert res.status_code == 400
>>>>>>> 3c825b871a26c489ad64f7e36971311fe1441501

        res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})

<<<<<<< HEAD
        assert res.status_code == 403

    #valid put from internal user
    def test_invalid_put_event(self,client):
        token = create_token_non_internal()
        data = {
            'nama': 'Hore hore',
            'ip': '138.68.161.14',
            'waktu': '2010-10-10 14:00:00'
        }
        res = client.post('/user/event', headers={'Authorization': 'Bearer '+token}, data=json.dumps(data), content_type='application/json')

<<<<<<< HEAD
        assert res.status_code == 403
    
=======
# dari nada
>>>>>>> ca64a26dbc544f4f55a19741d291c95387094d29
=======
    #valid get event
    def test_event_get(self,client):
        token = create_token_internal()
        res = client.get('/user/get_event/'+str(TestEvent.tempevent), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    #invalid get_event, invalid event
    def test_event_get_invalid_id(self,client):
        token = create_token_internal()
        res = client.get('/user/get_event/0',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    #invalid get_event dont have token
    def test_event_get_invalid_token(self,client):
        res = client.get('/user/get_event'+str(TestEvent.tempevent),headers={'Authorization':'Bearer abc'})
        res_json = json.loads(res.data)
        assert res.status_code == 404


    #valid delete post from internal user
    def test_valid_delete_event(self, client):
        token = create_token_internal()
        res = client.delete('/user/event/'+str(TestEvent.tempevent), headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    #invalid delete post from non internal user
    def test_invalid_delete_event(self, client):
        token = create_token_non_internal()
        res = client.delete('/user/event/'+str(TestEvent.tempevent), headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 403
>>>>>>> 3c825b871a26c489ad64f7e36971311fe1441501

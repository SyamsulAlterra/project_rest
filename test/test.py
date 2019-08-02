import json
from . import app,client, cache, create_token_internal, create_token_non_internal


class TestEventEndpoint():
    #internal user get all event
    def test_valid_get_internal_user(self, client):
        token = create_token_internal()
        res = client.get('/user/event', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

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
    # def test_valid_delete_event(self, client):
    #     token = create_token_internal()

    #     res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})

    #     assert res.status_code == 200

    #invalid delete from non internal user
    def test_invalid_delete_event(self, client):
        token = create_token_non_internal()

        res = client.delete('/user/event/8', headers={'Authorization': 'Bearer '+token})

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

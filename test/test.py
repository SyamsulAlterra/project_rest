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






# class TestClientCrud():
#     tempclient=0
#     def test_client_get(self,client):
#         token = create_token_internal()
#         res = client.get('/client/list',headers={'Authorization':'Bearer '+token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_client_get_invalid_token(self,client):
#         res = client.get('/client/list',headers={'Authorization':'Bearer abc'})
#         res_json = json.loads(res.data)
#         assert res.status_code == 500

#     def test_client_post(self,client):
#         token = create_token_internal()
#         data = {
#             "client_key": "SECRET00",
#             "client_secret": "internalreal",
#             "status": False
#         }
#         res = client.post('/client',headers={'Authorization':'Bearer '+token}, data=json.dumps(data),content_type='application/json')
#         res_json = json.loads(res.data)
#         TestClientCrud.tempclient=res_json['client_id']
#         assert res.status_code == 200

#     def test_client_post_invalid_status(self,client):
#         token = create_token_internal()
#         data = {
#             "client_key": "SECRET00",
#             "client_secret": "internalreal"
#         }
#         res = client.post('/client',headers={'Authorization':'Bearer '+token},data=json.dumps(data), content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def test_client_put(self,client):
#         token = create_token_internal()
#         data = {
#             "client_key": "SECRET00",
#             "client_secret": "internalreall",
#             "status": False
#         }
#         res = client.put('/client/'+str(TestClientCrud.tempclient),headers={'Authorization':'Bearer '+token}, data=json.dumps(data),content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_client_put_invalid_status(self,client):
#         token = create_token_internal()
#         data = {
#             "client_key": "SECRET00",
#             "client_secret": "internalreall"
#         }
#         res = client.put('/client/'+str(TestClientCrud.tempclient),headers={'Authorization':'Bearer '+token}, data=json.dumps(data),content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def test_client_delete(self,client):
#         token = create_token_internal()
#         res = client.delete('/client/'+str(TestClientCrud.tempclient),headers={'Authorization':'Bearer '+token}, content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_client_delete_invalid_id(self,client):
#         token = create_token_internal()
#         res = client.delete('/client/0',headers={'Authorization':'Bearer '+token}, content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

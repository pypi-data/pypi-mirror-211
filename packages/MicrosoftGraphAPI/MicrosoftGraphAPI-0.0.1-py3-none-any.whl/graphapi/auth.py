import requests


def GenerateToken(client_id, scope, client_secret, grant_type, tenant_id):
    endpoint = 'https://login.microsoftonline.com/'+tenant_id+'/oauth2/v2.0/token'
    data = {'client_id': client_id, 'scope': scope,
            'client_secret': client_secret, 'grant_type': grant_type}
    response = requests.post(endpoint, data=data)
    return response.json()['access_token']

import requests
import adal
import json

'''Vaste variabelen'''
TENNANT_ID = "<YOUR TENNANT ID>"
AUTHORITY_URL = 'https://login.microsoftonline.com/'+TENNANT_ID+'/'
RESOURCE_URL = 'https://analysis.windows.net/powerbi/api'
ENV_FILE = '.env.json'

def get_environment_settings(ENV_FILE):
    with open(ENV_FILE) as f:
        environment = json.load(f)
        return environment

def get_access_token(client_id, client_token):
    context = adal.AuthenticationContext(authority=AUTHORITY_URL, validate_authority=True, api_version=None)
    token = context.acquire_token_with_client_credentials(RESOURCE_URL, client_id, client_token)
    access_token = token.get('accessToken')
    if not access_token:
        return print("Geen token kunnen verkrijgen!")
    else:
        return access_token

def get_dataset_id_in_workspace_by_name(workspace_id, dataset_name, client_id, client_token):
    access_token = get_access_token(client_id, client_token)
    dataset_url = 'https://api.powerbi.com/v1.0/myorg/groups/'+workspace_id+'/datasets'
    header = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
    r = requests.get(url=dataset_url, headers=header)
    result = r.raise_for_status()
    if not result:
        data = r.json()
        len1 = len(data['value'])
        for i in range(len1):
            if data['value'][i]['name'] == dataset_name:
                print('Dataset ID van ' + dataset_name + ' gevonden; \'' + data['value'][i]['id'] + '\'')
                return data['value'][i]['id']
    else:
        print('Er is wat fout gegaan; ' + str(result))

def get_dataset_in_workspace_by_id(workspace_id, dataset_id, client_id, client_token):
    access_token = get_access_token(client_id, client_token)
    dataset_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspace_id + '/datasets/' + dataset_id 
    header = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
    r = requests.get(url=dataset_url, headers=header)
    result = r.raise_for_status()
    if not result:
        return r.json()
    else:
        print('Er is wat fout gegaan; ' + str(result))

def get_workspace_id_by_name(workspace_name,client_id, client_token):
    access_token = get_access_token(client_id, client_token)
    workspace_url = 'https://api.powerbi.com/v1.0/myorg/groups/'
    header = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
    r = requests.get(url=workspace_url, headers=header)
    result = r.raise_for_status()
    if not result:
        data = r.json()
        len1 = len(data['value'])
        for i in range(len1):
            if data['value'][i]['name'] == workspace_name:
                print('Workspace ID van \'' + workspace_name + '\' gevonden; \'' + data['value'][i]['id'] + '\'')
                return data['value'][i]['id']

def refresh_dataset(workspace_id, dataset_id, client_id, client_token):
    access_token = get_access_token(client_id,client_token)
    dataset_refresh_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspace_id + '/datasets/' + dataset_id + '/refreshes'
    header = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
    print('Dataset ' + dataset_id + ' in workspace ' + workspace_id + ' wordt ververst.')
    r = requests.post(url=dataset_refresh_url, headers=header)
    result = r.raise_for_status()
    if not result:
        print('Succesvol dataset \'' + dataset_id + '\' ververst!')
    else:
        print('Er is wat fout gegaan; ' + str(result))

def refresh_dataset_by_names(workspace_name, dataset_name, client_id, client_token):
    access_token = get_access_token(client_id,client_token)
    workspace_id = get_workspace_id_by_name(workspace_name, client_id, client_token)
    dataset_id = get_dataset_id_in_workspace_by_name(workspace_id, dataset_name, client_id, client_token)
    dataset_refresh_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspace_id + '/datasets/' + dataset_id + '/refreshes'
    header = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
    print('Dataset ' + dataset_name + ' in workspace ' + '\'' + workspace_name + '\'' + ' wordt ververst.')
    r = requests.post(url=dataset_refresh_url, headers=header)
    result = r.raise_for_status()
    if not result:
        print('Succesvol dataset \'' + dataset_name + '\' ververst!')
    else:
        print('Er is wat fout gegaan; ' + str(result))
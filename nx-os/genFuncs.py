import yaml
import requests
import json
from requests.auth import HTTPBasicAuth
from decouple import config
from jinja2 import Environment, FileSystemLoader




def cli_conf_payload():

    '''
    opens configuration file to read request payload format for cli_conf command type
    returns the payload
    '''

    # api cli command request payload
    with open('yaml-configs/cli-conf.yaml') as payload_file:
        payload = yaml.full_load(payload_file)
    return payload




def login_config(device, verify=False):

    '''
    takes a device and logs into the device
    returns the request session for the device
    '''

    # setup the login template
    template_env = Environment(loader=FileSystemLoader('./templates/'))
    template_obj = template_env.get_template('login-config.j2')

    # authentication data
    username = config('USERNAME')
    password = config('PASSWORD')
    auth = HTTPBasicAuth(username, password)

    # login configuration data
    with open('yaml-configs/login-config.yaml') as login_file:
        login_commands = yaml.full_load(login_file)

    # api cli command request payload
    payload = cli_conf_payload()

    # setup request
    session = requests.Session()
    port = config('PORT')
    url = f'https://{device}:{port}/ins'
    headers = {'content-type': 'application/json'}
    payload['ins_api']['input'] = login_commands[0]

    #########################################################################################
    if not verify:
        requests.packages.urllib3.disable_warnings()
    #########################################################################################
    
    # request
    response = session.post(url, auth=auth, headers=headers, data=json.dumps(payload), verify=False)

    # output
    reply = json.loads(response.text)
    output = reply['ins_api']['outputs']['output']

    # render template
    login_device = template_obj.render(device=device, login_commands=login_commands, output=output)
    print(login_device)

    # return
    return session




def save_config(device, session):

    '''
    takes a device and a session object and saves configurations the device
    '''
    
    # setup save template
    template_env = Environment(loader=FileSystemLoader('./templates/'))
    template_obj = template_env.get_template('save-config.j2')

    # save configuration data
    with open('yaml-configs/save-config.yaml') as save_file:
        save_commands = yaml.full_load(save_file)
    
    # api cli command request payload
    payload = cli_conf_payload()

    # setup request
    port = config('PORT')
    url = f'https://{device}:{port}/ins'
    payload['ins_api']['input'] = save_commands[0]

    # request
    response = session.post(url, data=json.dumps(payload))

    #output
    reply = json.loads(response.text)       
    output = reply['ins_api']['outputs']['output']['msg']
    
    #render template
    save_config = template_obj.render(device=device, save_commands=save_commands, output=output)
    print(f'\n{save_config}\n')
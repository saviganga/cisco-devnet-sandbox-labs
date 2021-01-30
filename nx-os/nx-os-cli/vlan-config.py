import requests
import json
import yaml
import genFuncs
from requests.auth import HTTPBasicAuth
from decouple import config
from jinja2 import Environment, FileSystemLoader


def config_valn(device, session):

    '''
    takes a device and a session object and configures vlan for the device
    '''

    # set up vlan configuration template
    template_env = Environment(loader=FileSystemLoader('./templates'))
    template_obj = template_env.get_template('vlan-conf.j2')

    # vlan configuration data from configuration file
    with open('yaml-configs/vlan-config.yaml') as vlan_config_file:
        vlans = yaml.full_load(vlan_config_file)
    len_vlans = len(vlans)

    # api cli command request payload
    payload = genFuncs.cli_conf_payload()

    # setup request
    port = config('PORT')    

    # save all responses in a list to be displayed in the template
    output_list = []

    # send the commands
    for vlan in vlans:

        # request
        url = f'https://{device}:{port}/ins'
        payload['ins_api']['input'] = f'vlan {vlan["id"]}  ;  name {vlan["name"]}'
        response = session.post(url, data=json.dumps(payload))
        
        # output
        reply = json.loads(response.text)       
        output = reply['ins_api']['outputs']['output']
        output_list.append(output)
            
    # render the template
    vlan_config = template_obj.render(device=device, vlans=vlans, len_vlans=len_vlans, output_list=output_list)
    print(f'\n{vlan_config}')




def connect_device():

    ''' 
    gets number of devices to connect to from user
    returns a list of selected devices
    '''
    
    # get number of devices to configure
    numb_devices = int(input('Enter the number of devices to configure: '))

    # user enters selected devices (using id)
    selected_devices = []
    for numb in range(1, numb_devices+1):
        device_id = int(input(f'\nEnter device id for device {numb}: '))
        selected_devices.append(device_id)

    # connect to devices
    try:
        connected_devices = []
        for device in selected_devices:
            connected_device = switches[device-1]
            connected_devices.append(connected_device)
       
    except Exception as connect_device_error:
        print('invalid input') 
        connect_device()

    #return connected devices
    return connected_devices




if __name__ == "__main__":

    # get available switches from configuration file
    with open('yaml-configs/switches.yaml') as switches_file:
        switches = yaml.full_load(switches_file)
        
    # display available switches to user
    print('\nSELECT AN ID TO CONNECT TO A SWITCH\n'.center(15, ' '))
    print(f'SWITCHES\n'.center(15, ' '))
    #accepted_input = []
    print(f'id |'.ljust(5, ' ') + 'Switch'.ljust(5, ' ') + '\n')
    for idd, switch in enumerate(switches,start=1):
        print( (str(idd) + ' |').ljust(5, ' ') + switch.ljust(5, ' ') + '\n' )
        #accepted_input.append(idd)

    # connect to the switches
    connected_devices = connect_device()

    # configure vlans on each device
    for device in connected_devices:
        
        # login to device
        login = genFuncs.login_config(device)

        # configure vlan for device
        config_valn(device, login)

        # save configurations for the device
        genFuncs.save_config(device, login)        
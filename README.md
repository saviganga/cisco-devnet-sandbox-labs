# cisco-devnet-sandbox-labs

In this repository, we configure and run commands on the cisco devnet sandboxes using the APIs for the sandbox devices

OVERVIEW
--------

1. nx-os

   - templates :
     directory that holds all template files for the different configuration models
   
   - yaml-configs :
     directory that holds all configuration files to be read from the program and sent to the device
   
   - .env.example :
     file that contains format to set up .env file
   
   - genFuncs.py (general functions) :
     python file that contains general functions used by multiple configuration scripts in the repository
   
   - vlan-config.py :
     python script that selects devices, logs into the devices, configures vlan based on commands from configuration files and saves the new configurations to startup        configurations
   
QUESTIONS
---------

1. How do I enable the self signed certificate on the switch to avoid the warning messages when i set verify=False to bypass using certificates

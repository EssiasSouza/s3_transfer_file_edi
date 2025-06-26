version = "3.0.0"
import sys
import os
import json
import platform

def get_os_type():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Linux':
        return 'Linux'
    else:
        return 'Outro: ' + os_name

def get_app_and_settings_full_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path, os.path.join(base_path, "settings.json")

def read_settings(settings_full_path):
    with open(settings_full_path, 'r') as file:
        data = json.load(file)
    return data

def defining_values(variable_name, settings_full_path):
    parameters = read_settings(settings_full_path)
    if variable_name in parameters:
        return parameters[variable_name]
    return None

def checking_settings_file(settings_full_path):
    message = ""
    settings_content = '''{
        "common_settings": {
            "logs_path": "./logs",
            "log_name": "New_Application.log"
        },
        "app_parameters": {
            "polling_interval": "10"
        }
    }'''

    check_settings_file = os.path.exists(settings_full_path)
    if check_settings_file is False:
        with open(settings_full_path, 'w', encoding='utf-8') as file:
            file.write(settings_content)
        message = "There is no settings.json file. Creating a sample file. Please, set it up as you need."
    return message
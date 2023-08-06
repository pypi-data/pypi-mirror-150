import os
import sys
import logging
import requests
import json

from Config.settings import slack_log_channel_url

def initialise_logger(log_file_path):
    """
    This function initialises a logger object that outputs the logs to the log_file_path provided and returns
    a logger object that can then be passed around (hopefully this approach works)
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def send_log_to_slack(log_message, service, log_topic):
    """
    This function takes a log message, its title and its topic and sends to the designated slack channel
    based on 
    """
    
    slack_data = {
        "username": f'{service}',
        "attachments": [
            {
                "color":  "#9733EE",
                "fields": [
                    {
                        "title": log_topic,
                        "value": log_message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(slack_log_channel_url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
        
    return None
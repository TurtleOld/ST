import json
import os
from schedtrans.logger.log import logger


class SentMessage:
    send_message: list = []


@logger.catch
def prepare_json_file_route():
    current_directory = os.path.dirname(__file__)
    file_name = 'routes.json'
    file_path = os.path.abspath(os.path.join(current_directory, file_name))
    with open(file_path, 'r') as route_file:
        return json.load(route_file)


@logger.catch
def save_file(file_name, data):
    try:
        with open(file_name, 'w+') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as error:
        logger.error(error)


@logger.catch
def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            json_data = json.load(file)
            return json_data
    except Exception as error:
        logger.error(error)

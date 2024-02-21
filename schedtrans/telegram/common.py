import json
import os


class SentMessage:
    send_message: list = []


def prepare_json_file_route():
    current_directory = os.path.dirname(__file__)
    file_name = 'routes.json'
    file_path = os.path.abspath(os.path.join(current_directory, file_name))
    with open(file_path, 'r') as route_file:
        return json.load(route_file)

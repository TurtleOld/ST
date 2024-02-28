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


def save_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def open_file(file_name):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data

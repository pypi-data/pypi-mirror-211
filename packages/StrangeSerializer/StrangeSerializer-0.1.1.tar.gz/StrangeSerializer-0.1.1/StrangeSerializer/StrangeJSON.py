import json


def dump(data_list, file_name):
    with open(file_name, 'w') as file:
        json.dump(data_list, file)


def load(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

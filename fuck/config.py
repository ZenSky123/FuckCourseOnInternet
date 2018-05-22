import os
import json


def mkdir(path):
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        mkdir(parent_dir)
    if not os.path.exists(path):
        os.mkdir(path)


def get_config_path():
    user_dir = os.path.expanduser('~')
    program_name = 'fuckCourseOnInternet'
    config_filename = 'config.json'

    config_path = os.path.join(user_dir, program_name, config_filename)

    return config_path


def init_config(config_json):
    config_path = get_config_path()
    config_dirname = os.path.dirname(config_path)
    mkdir(config_dirname)

    json.dump(config_json, open(config_path, 'w'))


def load_config():
    config_path = get_config_path()
    return json.load(open(config_path))

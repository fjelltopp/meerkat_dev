#!/usr/bin/env python2

import os
from os.path import expanduser

aws_config = """[default]
output = json
region = eu-west-1
"""
aws_credentials = """[default]
aws_secret_access_key = dummy_secret_kay
aws_access_key_id = dummy_id
"""
home = expanduser("~")
default_config_directory = '{}/.aws'.format(home)
confirmation_message = 'Would you like to create dummy aws credentials in {}? (Y/n) '


def create_dummy_aws_config(config_directory=default_config_directory):
    if not os.path.exists(config_directory):
        if raw_input(confirmation_message.format(config_directory)) not in ['n', 'N', 'No', 'no', 'NO']:
            os.makedirs(config_directory)
            with file('{}/config'.format(config_directory), mode='w') as config_file:
                config_file.write(aws_config)
            with file('{}/credentials'.format(config_directory), mode='w') as credentials_file:
                credentials_file.write(aws_credentials)


if __name__ == '__main__':
    create_dummy_aws_config('{}/.aws'.format(home))

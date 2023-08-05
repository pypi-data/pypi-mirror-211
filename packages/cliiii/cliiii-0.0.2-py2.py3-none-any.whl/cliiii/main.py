import platform
import subprocess
import time

import boto3
from importlib_metadata import version as get_version
import requests
from .utils import *


def get_os_and_architecture():
    operating_system = platform.system().lower()
    arch = platform.machine().lower()
    return operating_system, arch


def check_for_cli_updates(current_version, package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    latest_version = response.json()['info']['version']

    if current_version != latest_version:
        print(f"Update available, updating to latest version: {latest_version}")
        subprocess.call(f"pip3 install --upgrade {package_name}", shell=True)
        print(f"Updated cli to latest version: {latest_version}")
    else:
        print("No updates available")


def download_binary(binary, version):
    print(f"Downloading binary for version: {version}")
    time.sleep(1)


def execute_binary(package_name, binary_name):
    current_version = get_version(package_name)
    print(f"Executed binary for version: {current_version}")


def pre_execution_workflow(package_name, binary_name):
    try:
        current_version = get_version(package_name)
        check_for_cli_updates(current_version, package_name)

        current_version = get_version(package_name)
        download_binary(binary_name, current_version)

    except Exception as e:
        print(e)


def run_cli():
    try:
        package_name = "piicli"
        binary_name = "secrets"
        pre_execution_workflow(package_name, binary_name)
        print("Running main cli, version: 0.0.2")
        execute_binary(package_name, binary_name)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_cli()

#!/usr/bin/python
import subprocess
import sys
import json
import argparse
from docker import Client

DOCKER_SOCK='unix://var/run/docker.sock'

def parse_args():
    parser = argparse.ArgumentParser(description="Docker inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def get_docker_client():
    return Client(base_url=DOCKER_SOCK)


def get_host_details(host):
    client = get_docker_client()
    info = client.inspect_container(host)
    return {'ansible_ssh_host': info['NetworkSettings']['IPAddress'],
            'ansible_ssh_port': 22,
            'ansible_ssh_user': 'root'}


def get_docker_vm_list():
    client = get_docker_client()
    info = {'docker_vm': []}
    for container in client.containers():
        if container['Image'] == 'ndphu/ubuntu-ssh':
            info['docker_vm'].append(container['Names'][0][1:])
    return info


def main():
    args = parse_args()
    if args.list:
        details = get_docker_vm_list()
        json.dump(details, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()


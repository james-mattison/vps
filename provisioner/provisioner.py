import requests
import json
import os
import argparse

API_KEY=os.environ['VULTR_API_KEY']

def make_request(*endpoints, blob: dict, kind = "get"):
    if not hasattr(requests, kind):
        raise Exception(f"{kind} not a valid HTTP request type")
    url = "https://api.vultr.com/v2"
    for endpoint in endpoints:
        url += "/" + endpoint
    print(f"URL: {url}")
    headers = {
            "Authorization": f"Bearer {API_KEY}"
            }

    ret = requests.get(url, json = blob, headers = headers)
    print(json.dumps(ret.json(), indent = 4))
    return ret.json()


def list_dns_entries(domain_name: str):
    req = make_request("domains", domain_name, "records", blob = {})
    return req


def create_record(domain_name,
                  record_kind,
                  record_name,
                  record_value,
                  ttl
                  ):
    """
    Create a DNS entry using the VULTR API
    """

    endpoints = ["domains",
                 domain_name,
                 "records"]

    kind = "post"
    json_blob = {
        "name": record_name,
        "type": record_kind,
        "data": record_value,
        "ttl": ttl,
        "priority": 0
    }

def get_instances():
    return make_request("instances", blob = dict())

def get_os_ids(selector: str = None):
    blob = make_request("os", blob = dict())

    kinds = {}
    for os in blob['os']:
        if not os['family'] in kinds.keys():
            kinds[os['family']] = {}
        kinds[os['family']][os['name']] = os['id']

    if selector:
        return kinds.get(selector)
    else:
        return kinds

def get_ssh_keys():
    return make_request("ssh-keys", blob = dict())

def get_ssh_key_id(name):
    blob = make_request("ssh-keys", blob = dict())
    for key in blob['ssh_keys']:
        if key['name'] == name:
            return key['id']



def create_instance(
        hostname,
        label,
        os_id,
        enable_ipv6: bool = False,

        region: str = "lax"
):
    ...


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--domain", action = "store", default = "slovendor.com"
)
parser.add_argument(
    "-n", "--name", action = "store", required = True
)
parser.add_argument(
    "-k", "--key", action = "store"
)
parser.add_argument(
    "--no-dns", action = "store_true", default = False
)
parser.add_argument(
    "--no-provision", action = "store_true", default = False
)

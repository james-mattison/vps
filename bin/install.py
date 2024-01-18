#!/usr/bin/env python3

import subprocess
import mysql.connector as mysql
import argparse
import getpass
import os
import sys
import yaml

ONE_DOWN=os.path.dirname(os.path.dirname(sys.argv[0]))
CONFIG_FILE=os.path.join(ONE_DOWN, "config.yaml")
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE="/vps/config.yaml"

class Config:

    def __init__(self):
        with open(CONFIG_FILE, "r") as _o:
            self.config = yaml.load(_o, Loader = yaml.Loader)
        for k, v in self.config['install'].items():
            setattr(self, k, v)

    def __getitem__(self, item):
        if item in self.config['install'].keys():
            return self.config['install'].get(item)
        else:
            raise KeyError(f"Not found in {self.__dict__.keys()} - '{item}'")



config = Config()

class BootstrappingException(BaseException):

    def __init__(self, m: str):
        self.m = m

    def __str__(self):
        return f"BootstrappingException: {self.m}"


parser = argparse.ArgumentParser()
parser.add_argument("target_fqdn", action = "store", help = "The FQDN of the target node.")
parser.add_argument("--no-build", action = "store_true", default = False)


def push(target: str, local_path: str, remote_path: str):
    cmd = f"scp -r {local_path} root@{target}:{remote_path}"
    ret = subprocess.run(cmd, shell = True)
    if ret.returncode != 0:
        raise BootstrappingException(f"Bad return from {cmd}!")


class Runner:

    def __init__(self, target: str):
        self.target = target

    def open_tunnel(self):
        cmd = f"ssh -fN 4222:localhost:22 -L root@{self.target}"
        return self.run(cmd, die_on_fail = True)

    def _run(self, cmd: str, get_code: bool = False, die_on_fail = False, silent = False):
        s = ""
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while proc.poll() is None:
            ln = proc.stdout.readline().decode(errors = 'ignore')
            if ln:
                if not silent: print(ln.strip("\n"))
                s += ln
        ln = ""
        while ln:
            s += ln
            if not silent: print(ln)
            ln = proc.stdout.readline().decode(errors = 'ignore')

        if get_code:
            if die_on_fail and proc.returncode != 0:
                raise BootstrappingException(f"Failed: {cmd} execution returned {proc.returncode}!")
            else:
                return proc.returncode
        else:
            return s

    def push(self, local_path: str, remote_path: str, die_on_fail = True):
        cmd = f"scp -o 'StrictHostKeyChecking=no' -r {local_path} root@{self.target}:{remote_path}"
        return self._run(cmd, die_on_fail = die_on_fail)

    def run(self, cmd: str, die_on_fail = True):
        cmd = f"ssh -o 'StrictHostKeyChecking=no' root@{self.target} '{cmd}'"
        return self._run(cmd, die_on_fail = die_on_fail)

    def run_cmds(self, *cmds, die_on_fail = True):
        for cmd in cmds:
            self._run(cmd, die_on_fail = die_on_fail)

class Bootstrap:

    def create_vps_dir(self):
        ...

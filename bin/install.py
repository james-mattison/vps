#!/usr/bin/env python3

import subprocess
import mysql.connector as mysql
import argparse
import getpass
import os
import sys
import yaml
import time


BASE_PACKAGES = [
    "python3-pip",
    "python3-dev",
    "python3-venv",
    "build-essential",
    "libssl-dev",
    "libffi-dev",
    "python3-setuptools",
    "iptables",
    "iptables-persistent",
    "mysql-client"
]

PIP_PACKAGES = [
    "flask",
    "flask-bootstrap",
    "mysql-connector-python",
    "pyyaml"
]


HERE=os.path.dirname(__file__)
CONFIG_FILE=os.path.join(HERE, "config.yaml")
ONE_DOWN=os.path.dirname(os.path.dirname(__file__))

boldunderline = lambda text: u'\u001b[1m\u001b[4m' + str(text) + u'\u001b[0m'

def progress(text, step, end):
    try:
        x, y = os.get_terminal_size()
    except OSError as e:
        x, y = 80, 24
    where = int(step / end * x) - 20
    sys.stdout.write(f"{text:20s}" + (where * ">") + "\r")
    sys.stdout.flush()

class Config:

    def __init__(self):
        with open(CONFIG_FILE, "r") as _o:
            self.config = yaml.load(_o, Loader = yaml.Loader)
        for k, v in self.config['install'].items():
            setattr(self, k, v)

    def __getitem__(self, item):
        if item in self.config.keys():
            return self.config[item]
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
parser.add_argument("-p", "--push-only", action = "store_true", default = False)


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

    def _run(self, cmd: str, get_code: bool = False, die_on_fail = False, silent = False, stop_if: str = None):
        s = ""
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while proc.poll() is None:
            ln = proc.stdout.readline().decode(errors = 'ignore')
            if ln:
                if not silent:
                    print("\t", ln.strip("\n"))
                s += ln

                if stop_if is not None and stop_if in s:
                    print(f"Got stop-if match. Stopping execution!")
                    proc.kill()
        ln = ""
        while ln:
            ln = proc.stdout.readline().decode(errors = 'ignore')
            if not silent: print("\t", ln)
            s += ln

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

    def run(self, cmd: str, **kwargs):
        cmd = f"ssh -o 'StrictHostKeyChecking=no' root@{self.target} '{cmd}'"
        return self._run(cmd, **kwargs)

    def run_cmds(self, *cmds, die_on_fail = True):
        for cmd in cmds:
            self._run(cmd, die_on_fail = die_on_fail)

runner = Runner(config['install']['target_fqdn'])
class Bootstrap:

    def __init__(self):
        print("{:^20}".format("VPS System Bootstrapper"))

    def create_vps_dir(self):
        runner.run("mkdir -p /vps")

    def push_files(self):
        print(boldunderline("1. PUSHING FILES TO DEPLOYMENT"))
        ignore = [".git", "venv", ".idea"]
        obs = [f for f in os.listdir(ONE_DOWN) if not f in ignore]
        for i, ob in enumerate(obs):
            if not ob in ignore:
                progress(ob, i , len(obs))
                runner.push(os.path.join(ONE_DOWN, ob), f"/vps/")
        print("[OK]")

    def install_base_packages(self):
        print(boldunderline("2. INSTALLING BASE PACKAGES"))
        for i, package in enumerate(BASE_PACKAGES):
            runner.run(f"apt-get -y install {package}", silent = True)
            if package == BASE_PACKAGES[-1]:
                print("OK")
            else:
                progress(package, i, len(BASE_PACKAGES))
    def create_venv(self):
        print(boldunderline("3. CREATING VPS VENV"))
        runner.run("python3 -m venv /vps/venv")

    def install_pip_packages(self):
        print(boldunderline("4. INSTALLING PIP PACKAGES"))
        runner.run(f"/vps/venv/bin/pip3 install -r /vps/requirements.txt --upgrade", silent = True)
        # for package in PIP_PACKAGES:
        #     runner.run(f"/vps/venv/bin/pip3 install flask docker wheel setuptools flask-bootstrap ")

    def disable_ufw(self):
        print(boldunderline("5. INSTALLING IPTABLES, REMOVING UFW"))
        runner.run("ufw disable ; systemctl stop ufw ; systemctl disable ufw")

    def enable_iptables(self):
        runner.run("systemctl enable iptables ; systemctl start iptables")

    def install_docker(self):
        print(boldunderline("6. INSTALLING DOCKER"))
        runner.run("wget -O - http://get.docker.com | bash", stop_if = "abort this script")
        runner.run("systemctl enable docker", die_on_fail =  True)

        print(boldunderline("7. INSTALLING DOCKER-COMPOSE"))
        runner.run("curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose")
        runner.run("chmod +x /usr/local/bin/docker-compose", die_on_fail =  True)

    def login_registry(self):
        print(boldunderline("8. LOGGING INTO THE VPS DOCKER REGISTRY"))
        runner.run(f"docker login -u {config['registry']['username']} -p {config['registry']['password']} {config['registry']['registry_fqdn']}")

    def pull_images(self):
        print(boldunderline("9. PULLING DOCKER IMAGES"))
        runner.run("cd /vps && HERE=/vps docker-compose -f docker-compose.yml pull")

    def create_db_volume(self):
        print(boldunderline("10. CREATE DB VOLUME"))
        runner.run("docker volume create db")

    def configure_dev_credentials(self):
        cmd = "docker run -d -e MYSQL_ROOT_PASSWORD=123456 -v /var/lib/mysql:/var/lib/mysql --net=host --name=db registry.slovendor.com/db"

        cmd2 = """
        docker exec db mysql -uroot -p123456 -h127.0.0.1 -e "CREATE USER 'root'@'10.0.0.1'"
        """
        cmd3 = """
        docker exec db mysql -uroot -p123456 -h127.0.0.1 -e "SET PASSWORD FOR 'root'@'10.0.0.1' = PASSWORD('123456')" 
        """

        cmd4 = """
        docker exec db mysql -uroot -p123456 -h127.0.0.1 -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.0.0.1' WITH GRANT OPTION"
        """

        cmd5 = "docker exec db mysql -uroot -p123456 -h127.0.0.1 -e 'FLUSH PRIVILEGES'"
        runner.run("docker container prune -f")
        runner.run(cmd)
        for i in range(10):
            progress("Waiting for DB to start", i, 10)
            time.sleep(1)
        runner.run(cmd2)
        runner.run(cmd3)
        runner.run(cmd4)
        runner.run(cmd5)

    def inject_data_into_db(self):
        cmds = [
            "cd /vps/db && ./load-schema && mysql < test.sql",
            "cd /vps/db && python3 generate_data.py -t all -X",
            "cd /vps/db mysql < test.sql"
        ]

        for cmd in cmds:
            runner.run(cmd)
    def start_vps(self):
        print(boldunderline("11. START VPS SYSTEM"))
        runner.run("cd /vps && docker-compose up -d --remove-orphans")

def install(push_only: bool = False):
    bootstrapper = Bootstrap()
    bootstrapper.create_vps_dir()
    bootstrapper.push_files()
    if push_only:
        print(f"--push-only specified. Exiting")
        quit(0)
    bootstrapper.install_base_packages()
    bootstrapper.create_venv()
    bootstrapper.install_pip_packages()
    bootstrapper.disable_ufw()
    bootstrapper.enable_iptables()
    bootstrapper.install_docker()
    bootstrapper.login_registry()
    bootstrapper.create_db_volume()
    bootstrapper.pull_images()
    bootstrapper.configure_dev_credentials()
    bootstrapper.start_vps()

if __name__ == "__main__":
    args = parser.parse_args()
    install(args.push_only)

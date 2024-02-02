from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import json

import argparse
import time


class Driver:

    def __init__(self,
                 host,
                 port,
                 user,
                 password
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.driver = Chrome()
        self.get_endpoint("login")

    @classmethod
    def from_json(cls):
        with open("config.json", "r") as _o:
            ob = json.load(_o)
        return cls(**ob)

    def get(self, endpoint):
        print(f"GET -> {endpoint}")
        self.driver.get(endpoint)

    def get_endpoint(self, endpoint):
        endpoint = f"http://{self.host}:{self.port}/{endpoint}"
        self.get(endpoint)


    def login(self):
        # self.driver.get("http://{self.host}:{self.port}/login")
        time.sleep(1)
        username = self.driver.find_element(By.ID, "username")
        print("Found username field")
        password = self.driver.find_element(By.ID, "password")
        print("Found password field")
        submit = self.driver.find_element(By.ID, "submit")
        print("Found submit button")
        username.send_keys(self.user)
        print(f"INSERT {self.user} -> `username`")
        password.send_keys(self.password)
        print(f"INSERT {self.password} -> `password`")
        submit.click()
        time.sleep(2)

    def go_to_each_page(self):
        pages = [
            "customers",
            "orders",
            "products",
            "modules",
            "about"
        ]

        for page in pages:
            self.get_endpoint(page)
            time.sleep(3)

    def test_search_bar(self, endpoint):
        endpoint = self.get_endpoint(endpoint)

        if endpoint == "customers":
            search_bar = self.driver.find_element(By.ID, "search_bar")
            text = "oatse"
            for i in text:
                time.sleep(0.25)
                search_bar.send_key(i)

if __name__ == "__main__":
    d = Driver.from_json()
    d.login()
    d.go_to_each_page()
    d.test_search_bar("customers")
    time.sleep(10)
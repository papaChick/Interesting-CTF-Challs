import requests
import urllib.parse
import string
from flask import Flask, request
from threading import Thread

WEBHOOK_TOKEN = ""
BASE_URL = "http://localhost:1392"
CHARSET = string.printable
MAX_LENGTH = "4096" # Max Length Cookie: https://datatracker.ietf.org/doc/html/rfc6265#section-6.1

def solve():
    pass

def visit(target):
    encoded_target = urllib.parse.quote(target)
    resp = requests.get(f"{BASE_URL}/visit?target={encoded_target}")
    print(resp.text)
    
if __name__ == "__main__":
    session = requests.Session()
    
    
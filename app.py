#!/usr/bin/python3
# app to test the spotify api

from dotenv import load_dotenv
import os
import requests
import base64
import json

load_dotenv()
id = os.getenv("CLIENT_ID")
secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth = base64.b64encode(bytes(id + ":" + secret, "utf-8")).decode("ascii")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    token = json.loads(response.content)["access_token"]

    print(token) # for testing

get_token()
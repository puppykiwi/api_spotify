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

    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_artist_id(artist, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {"q": artist, "type": "artist"}
    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)["artists"]["items"][0]["id"]
    return result

if __name__ == "__main__":
    token = get_token()
    print(get_artist_id("The Beatles", token))
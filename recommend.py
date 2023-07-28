#!/usr/bin/python3

# A better recommendation engine 

from dotenv import load_dotenv
import os
import requests
import base64
import json
import random
from playlist import Playlist

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

def get_playlist_id(playlist, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {"q": playlist, "type": "playlist"}
    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)
    return result

def get_playlist_id(playlist_name, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {"q": playlist_name, "type": "playlist"}
    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)
    playlists = result.get("playlists", {}).get("items", [])
    if playlists:
        return playlists[0]["id"]  # Return the first playlist ID found (assumes unique names)
    return None


if __name__ == "__main__":
    print("Running recommend.py")
    token = get_token()
    print("token: ",token)
    id = get_playlist_id("S+Puppy", token)
    print("id: ",id)
    pl = Playlist(id, token)
    if pl:
        print("Playlist object created")
    else:
        print("Error creating Playlist object")
    
    result = pl.get_playlist_info()
    print(result["id"])
    print(result["name"])
    print(result["description"])
    pl.get_playlist_tracks()
#!/usr/bin/python3

# A better recommendation engine 
# This is a work in progress

from dotenv import load_dotenv
import os
import requests
import base64
import json
import random

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


class Playlist:
    params = {"country": "KE"}
    
    
    def __init__(self, playlist_id, token):
        self.playlist_id = playlist_id
        self.token = token
        self.base_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
    
    def get_playlist_tracks(self):
        url = self.base_url + "/tracks"
        headers = get_auth_header(self.token)
        result = self.get_request(url)
        for idx in result["items"]:
            print(idx["track"]["name"])

    def get_request(self, custom_url=None):
        headers = get_auth_header(self.token)

        try:
            url = custom_url if custom_url else self.base_url
            response = requests.get(url, headers=headers, params=self.params)
            response.raise_for_status()  # Raise an exception for any HTTP error status
            return json.loads(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    token = get_token()
    pl = Playlist("7eG04lBozqMlzgmpM1omp3", token)
    tracks = pl.get_playlist_tracks()

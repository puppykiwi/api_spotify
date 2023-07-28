#!/usr/bin/python3

import os
import requests
import base64
import json
import random

###
from dotenv import load_dotenv
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


###


"""  Playlist class  """

class Playlist:
    params = {"country": "KE"}
    
    def __init__(self, playlist_id,token):
        self.playlist_id = playlist_id
        self.token = token
        self.base_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
    
    def get_playlist_info(self):
        url = self.base_url
        headers = get_auth_header(self.token)
        result = self.get_request(url)
        return result
    
    def print_playlist_info(self):
        result = self.get_playlist_info()
        print(result["id"])
        print(result["name"])
        print(result["description"])
        print(result["owner"]["display_name"])
        print(result["tracks"]["total"])

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
            return json.loads(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    @classmethod
    def get_playlist_id(cls, token, playlist_name):
        url = "https://api.spotify.com/v1/me/playlists"
        headers = get_auth_header(get_token())
        params = cls.params

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            playlists_data = response.json()["items"]
            for playlist in playlists_data:
                if playlist["name"] == playlist_name:
                    return playlist["id"]
            return None
        else:
            # Handle API error
            return None

    @classmethod
    def create_playlist_by_name(cls, token, playlist_name):
        playlist_id = cls.get_playlist_id(token, playlist_name)
        if playlist_id:
            return cls(token, playlist_id)
        else:
            # Playlist with the given name not found, create a new one
            url = "https://api.spotify.com/v1/me/playlists"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            data = {
                "name": playlist_name,
                "public": False, 
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 201:
                playlist_data = response.json()
                return cls(token, playlist_data["id"])
            else:
                return None

if __name__ == "__main__":
    print("Running playlist.py")
    token = get_token()
    print (token)
    pl = Playlist("7eG04lBozqMlzgmpM1omp3", token)
    if pl:
        print("Playlist object created")
    else:
        print("Error creating Playlist object")
    id = pl.get_playlist_id(token, "sultry")
    print(id)
#!/usr/bin/python3

# A better recommendation engine 

from dotenv import load_dotenv
import os
import requests
import base64
import json
import random
from playlist import Playlist
from init import get_token, get_auth_header

def get_playlist_id(playlist_name, username, token):
    print("Getting playlist ID") # debug
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #print("Headers: ", headers) # debug
    params = {"q": f"{playlist_name} owner:{username}", "type": "playlist"}
    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)
    #print("Result: ", result) # debug
    playlists = result.get("playlists", {}).get("items", [])
    if playlists:
        id = playlists[0]["id"]
        print("Playlist ID: ", id) # debug
        return id 
    return None


    
if __name__ == "__main__":
    print("Running recommend.py")
    token = get_token()
    indie_id = "7eG04lBozqMlzgmpM1omp3"
    #print("Token: ", token) # debug
    #print("indie_id: ", indie_id) # debug
    
    get_playlist_id(input("Enter playlist name: "), "test", token)

    #pl = Playlist(indie_id, token)
    #result = pl.print_playlist_info()
    #pl.print_playlist_tracks()
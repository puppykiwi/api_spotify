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
    
    if len(result) == 0:
        print("No artist found")
        return None
    else:
        return result

def get_artist_tracks(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    params = {"country": "KE"}
    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)["tracks"]
    
    for idx, track in enumerate(result):
        print(f"{idx+1}. {track['name']}")

    if len(result) == 0:
        print("No tracks found")
        return None
    else:
        return result



if __name__ == "__main__":
    token = get_token()
    artist_id = get_artist_id("Still Woozy", token)
    tracks = get_artist_tracks(artist_id, token)
    #print(tracks)
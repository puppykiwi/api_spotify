#!/usr/bin/python3

import os
import requests
import base64
import json
import random
from init import get_token, get_auth_header

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
        print("\nPlaylist info:")
        print("id: ",result["id"])
        print("name: ",result["name"])
        print("descr: ",result["description"])
        print("owner: ",result["owner"]["display_name"])
        print("No. ",result["tracks"]["total"])

    def get_playlist_tracks(self):
        url = self.base_url + "/tracks"
        headers = get_auth_header(self.token)
        result = self.get_request(url)

        tracks_list = []
        if "items" in result:
            # print("items found") #debug
            for track in result["items"]:
                #print(track_data) #debug
                track_name = track["track"]["name"]
                artists = track["track"]["artists"]
                artist_name = ", ".join([artist["name"] for artist in artists])

                if track_name and artist_name:
                    track_info = {
                        "track": track_name,
                        "artist": artist_name,
                    }
                    #print("track_info",track_info) #debug
                    tracks_list.append(track_info)
        return tracks_list

    def print_playlist_tracks(self):
        result = self.get_playlist_tracks()
        print("\nPlaylist tracks:")
        for index, value in enumerate(result):
            print(f"{index+1}. {value['track']} by {value['artist']}")

    def get_request(self, custom_url=None):
        headers = get_auth_header(self.token)
        try:
            url = custom_url if custom_url else self.base_url
            response = requests.get(url, headers=headers, params=self.params)
            return json.loads(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
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
    id = pl.get_playlist_id(token, "indie infusion")
    print(id)
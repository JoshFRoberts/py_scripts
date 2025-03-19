import argparse

import requests
import json

class SpotifyAPIException(Exception):
    pass

def get_client_credentials() -> dict[str, str]:
    client_id:str
    client_secret:str

    with open('/home/joshuafroberts/.spt_client_id', 'r', encoding='utf-8') as client_id_file:
        client_id = client_id_file.read().splitlines()[0]

    with open('/home/joshuafroberts/.spt_client_secret', 'r', encoding='utf-8') as client_secret_file:
        client_secret = client_secret_file.read().splitlines()[0]

    return {
        'client_id': client_id,
        'client_secret': client_secret
    }

class SpotifyConnection:
    def __init__(self, credentials: dict[str, str]):
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']
        self.access_token = self._get_auth_key()

    def _get_auth_key(self):
        response = requests.post('https://accounts.spotify.com/api/token',
                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                     params={
                         'grant_type': 'client_credentials',
                         'client_id': self.client_id,
                         'client_secret': self.client_secret
                     })
        if response.status_code != 200:
            print(response.status_code)
            print(response.reason)
        else:
            return response.json().get('access_token')

    def get_artist(self, artist_id:str) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/artists' + f'/{artist_id}',
                 headers={
                     'Authorization': f'Bearer {self.client_id}',
                 })
        response.raise_for_status()

        return dict(response.json())

    def get_album(self, album_id) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/albums' + f'/{album_id}',
                 headers={
                     'Authorization': f'Bearer {self.client_id}',
                 })
        response.raise_for_status()

        return dict(response.json())

    def get_song(self):
        ...

    def get_playlist(self, playlist_id:str) -> list:
        response = requests.get(
            f'https://api.spotify.com/v1/playlists/{playlist_id}',
                headers={'Authorization': f'Bearer {self.access_token}'},
                params={
                    'market': 'DE',
                    'fields': 'tracks.items(track(name, artists(name))'
                }
            )
        response.raise_for_status()

        tracks = response.json().get('tracks').get('items')
        returned_list: list[dict[str, str]] = []

        for track in tracks:
            song = track['track']['name']
            artists = track['track']['artists']
            artist_names: list[str] = []
            for artist in artists:
                artist_name = artist['name']
                artist_names.append(artist_name)

            returned_list.append({
                'name': song,
                'all_artists': artist_names,
            })

            print(f'{song['name']}: ', end='')
            for index, artist in enumerate(song['all_artists']):
                print(f'{artist}', end='')
                if not index == len(song['all_artists']) - 1:
                    print(', ', end='')
                print()

        return returned_list

    def search(self, key:str, value:str) -> dict:
        response = requests.get(
            'https://api.spotify.com/v1/search',
                headers={ 'Authorization': f'Bearer {self.client_id}'},
                params={
                    'q': f'{value}',
                    'type': f'{key}',
                    'market': 'DE',
                    'limit': '10',
                    'offset': '0'
                })
        response.raise_for_status()

        return dict(response.json())


if __name__ == '__main__':

    from genius_scraper.web_crawler import GeniusConnection
    con = SpotifyConnection(get_client_credentials())

    default_value = '0xfprdFzAdLVlSRvbskpd5'
    # replace default value with playlist id found in spotify link to playlist
    # maybe later on replace with full link and parse id to improve usability

    print(con.search(key='artists', value='Fatoni'))


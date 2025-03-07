import requests
import json

from numpy.f2py.auxfuncs import throw_error
class SpotifyAPIException(Exception):
    pass

def get_client_credentials() -> dict[str, str]:
    client_id:str
    client_secret:str

    with open('/home/joshuafroberts/.spt_client_id', 'r', encoding='utf-8') as client_id_file:
        client_id = client_id_file.read().splitlines()[0]
        print(f"client_id: '{client_id}'")

    with open('/home/joshuafroberts/.spt_client_secret', 'r', encoding='utf-8') as client_secret_file:
        client_secret = client_secret_file.read().splitlines()[0]
        print(f"client_secret: '{client_secret}'")

    return {
        'client_id': client_id,
        'client_secret': client_secret
    }

class SpotifyConnection:
    def __init__(self, client_id:str , client_secret:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self._get_auth_key()

    def _get_auth_key(self):
        response = requests.post('https://accounts.spotify.com/api/token',
                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                     params={
                         'grant_type': 'client_credentials',
                         'client_id': self.client_id,
                         'client_secret': self.client_secret
                     })
        #breakpoint()
        if response.status_code != 200:
            print(response.status_code)
            print(response.reason)
        else:
            return response.json().get('access_token')

    def get_artist(self, artist_id:str) -> dict:
        response = requests.get(
            'https://accounts.spotify.com/api/artists' + f'/{artist_id}',
                 headers={
                     'Authorization': 'Bearer ' + self.client_id,
                 })
        if response.status_code != 200:
            print(response.status_code)
            print(response.reason)
            raise SpotifyAPIException('reason: ' + response.reason)
        else:
            return dict(response.json())

    def get_album(self, album_id) -> dict:
        response = requests.get(
            'https://accounts.spotify.com/api/albums' + f'/{album_id}',
                 headers={
                     'Authorization': 'Bearer ' + self.client_id,
                 })
        if response.status_code != 200:
            print(response.status_code)
            print(response.reason)
            raise SpotifyAPIException('reason: ' + response.reason)
        else:
            return dict(response.json())

    def get_song(self):
        ...

    def get_playlist(self):
        ...


if __name__ == '__main__':

    cred = get_client_credentials()
    SpotifyConnection(cred['client_id'], cred['client_secret']).get_auth_key()
import requests
from bs4 import BeautifulSoup

class GeniusConnection:
    def __init__(self):
        self.domain = 'https://www.genius.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.songtext: str

    def get_songtext(self, artist: str, song: str) -> str:

        artist = artist.replace(' ', '-')
        song = song.replace(' ', '-')
        url = f'{self.domain}{artist}-{song}-Lyrics'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_container = soup.find('div', attrs={'data-lyrics-container': 'true'})
        if not lyrics_container:
            raise Exception('No lyrics found')

        _lyrics = ""
        for element in lyrics_container:
            if element.name == 'br':
                _lyrics += '\n'
            elif element.string:
                _lyrics += element.string
            elif hasattr(element, 'get_text'):
                _lyrics += element.get_text()

        return _lyrics.strip()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Scrape Songtexte von Genius.com')
    parser.add_argument('artist', help='Name des Künstlers')
    parser.add_argument('song', help='Name des Songs')

    args = parser.parse_args()
    con = GeniusConnection()

    try:
        lyrics = con.get_songtext(args.artist,args.song)
        print(lyrics)
    except Exception as e:
        print(f"Fehler beim Scrapern: {e}")
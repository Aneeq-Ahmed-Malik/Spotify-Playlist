import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "playlist-modify-private"

CLIENT_ID = os.environ.get("CLIENT-ID")
CLIENT_SECRET = os.environ.get("CLIENT-SECRET")


spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_secret=CLIENT_SECRET,
    client_id=CLIENT_ID,
    redirect_uri="http://example.com"
    )
)

id = spotify.current_user()["id"]

URL = "https://www.billboard.com/charts/hot-100"
date = input("Which year do you want to travel yyyy-mm-dd : ")
year = date.split("-")[0]

response = requests.get(f"{URL}/{date}")
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

song_list = [song.text.strip() for song in soup.select(selector="div ul li ul li h3")]
song_uri = []

playlist_id = spotify.user_playlist_create(user=id, name=f"{date} Billboard 100", public=False)['id']

for song in song_list:
    try:
        uri = spotify.search(q=f"track: {song} year: {year}", type="track", limit=1)["tracks"]['items'][0]['uri']
    except IndexError:
        continue
    else:
        song_uri.append(uri)

spotify.playlist_add_items(playlist_id=playlist_id, items=song_uri)

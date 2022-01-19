#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json


def authKey(auth_filename):
	with open(auth_filename, 'r') as auth:
		try:
			token = auth.read().strip()
		except FileNotFoundError:
			print('auth_token file not found')
			raise
	return token

def json_to_temp(myJSON):
	with open('temp.json', 'w') as jFile:
		try:
			jFile.write(json.dumps(myJSON))
		except Exception:
			pass


AUTH_URL = 'https://accounts.spotify.com/api/token'
SP_BASE_URL = 'https://api.spotify.com/v1/'
# Spotify Share link: https://open.spotify.com/track/18dkRsYxeVNO6c3FlvSUTi?si=a6badc2d17cf4355
# Apple Music Share Link: https://music.apple.com/us/album/moving-blind/1520275309?i=1520275310
SPOTIFY_URL = input("Please paste your Spotify song here:")
#SPOTIFY_URL = "https://open.spotify.com/track/0WrX6QI8a84YIQeJLSb3uD"


search_limit = "5"
bad_words = ["by", "&"]

###################################################################
##Turn all this spotify API request nonsense into a function please
CLIENT_ID = '848979a1e610451b87746a1a05a37edc'
CLIENT_SECRET = authKey('spotifyAuth.tmp')

#Set up an API authorization token
auth_response = requests.post(AUTH_URL, {
	'grant_type': 'client_credentials',
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
	'Authorization': f'Bearer {access_token}'
}
####################################################################

trackID = SPOTIFY_URL.split("/")[-1]
# trackID = '1jRgrTBpB8GIB99bYjnDL3'

spoofy = requests.get(f"{SP_BASE_URL}tracks/{trackID}", headers=headers)
spoofy = spoofy.json()


#Collect the names of each artist on the song and prepend the title of the track
myQuery = [i['name'] for i in spoofy['artists']]
myQuery.insert(0, spoofy['name'])
myQuery = " ".join(myQuery)
myQuery.replace(" ", "+")

itunes = requests.get(f"https://itunes.apple.com/search?term={myQuery}")
itunes = itunes.json()

jFile = open("tmp.json", 'w')
jFile.write(json.dumps(itunes))
jFile.close()

AMLink = itunes["results"][0]['trackViewUrl']
print(f"The Apple Music link to this track is {AMLink}")

# f = open('temp.html','w')
# f.write(r.prettify())
# f.close()

#AMlink = r.find_all('a', attrs={"class": "line lockup__name has-adjacent-link"})[0]['href']
#print(f"{AMlink=}")
#SpotifyLink = spoofy['tracks']['items'][0]['external_urls']['spotify']


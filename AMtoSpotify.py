#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json

def percentEncode(mystr):
	return

def authKey(auth_filename):
	with open(auth_filename, 'r') as auth:
		try:
			token = auth.read().strip()
		except FileNotFoundError:
			print('auth_token file not found')
			raise
	return token

AUTH_URL = 'https://accounts.spotify.com/api/token'
SP_BASE_URL = 'https://api.spotify.com/v1/'
# Spotify Share link: https://open.spotify.com/track/18dkRsYxeVNO6c3FlvSUTi?si=a6badc2d17cf4355
# Apple Music Share Link: https://music.apple.com/us/album/moving-blind/1520275309?i=1520275310
# AM_URL = 'https://music.apple.com/us/album/right-spot/1515634025?i=1515634149'
AM_URL = input("Please paste your Apple Music song here:")

search_limit = "5"
bad_words = ["by", "&"]

##Copied from the spotify handshake 
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

AMPage = requests.get(AM_URL).text
r = BeautifulSoup(AMPage, 'html.parser')

#<title> element on Apple Music page is "{Song Name} by {Artist (& others)} on Apple Music
#this block of text parses the 
title = r.find_all('title')[0].text.encode("ascii","ignore")
title = title.decode().split()
for i in bad_words:
	try:
		title.remove(i)
	except:
		pass

#The last two elements of title at this point will always be "on", "AppleMusic" so we drop them
myQuery = "%20".join(title[:-2])

spoofy = requests.get(SP_BASE_URL + 'search?q=' + myQuery + '&type=track&limit=' + search_limit, headers=headers)
spoofy = spoofy.json()

jFile = open("tmp.json", 'w')
jFile.write(json.dumps(spoofy))

SpotifyLink = spoofy['tracks']['items'][0]['external_urls']['spotify']
print(f"The Spotify link to this Apple Music song is {SpotifyLink}")

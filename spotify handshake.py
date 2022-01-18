#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json

AUTH_URL = 'https://accounts.spotify.com/api/token'
SP_BASE_URL = 'https://api.spotify.com/v1/'
AM_BASE_URL = 'https://music.apple.com/us/album/moving-blind/1520275309?i=1520275310'

track_id = '18dkRsYxeVNO6c3FlvSUTi'
myQuery = 'moving blind dom dolla'
#myQuery = input("Enter Spotify search query:")
search_limit = "5"

auth_response = requests.post(AUTH_URL, {
	'grant_type': 'client_credentials',
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET,
})



def percentEncode(mystr):
	return mystr

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {
	'Authorization': f'Bearer {access_token}'
}

#r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
r = requests.get(SP_BASE_URL + 'search?q=' + myQuery + '&type=track&limit=' + search_limit, headers=headers)
r = r.json()
jFile = open("myJSON.json", 'w')
jFile.write(json.dumps(r))

for i in range(len(r['tracks']['items'])):
	print(r['tracks']['items'][i]['external_urls'])
#print(r)
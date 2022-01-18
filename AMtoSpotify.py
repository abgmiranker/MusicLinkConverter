#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

AUTH_URL = 'https://accounts.spotify.com/api/token'
SP_BASE_URL = 'https://api.spotify.com/v1/'
#Spotify Share link: https://open.spotify.com/track/18dkRsYxeVNO6c3FlvSUTi?si=a6badc2d17cf4355
#Apple Music Share Link: https://music.apple.com/us/album/moving-blind/1520275309?i=1520275310
AM_URL = 'https://music.apple.com/us/album/moving-blind/1520275309?i=1520275310'

track_id = '18dkRsYxeVNO6c3FlvSUTi'
myQuery = 'isrc:USZ4V2100038'
#myQuery = input("Enter Spotify search query:")
search_limit = "5"
bad_words = ["by", "&"]




def percentEncode(mystr):
	return mystr
AMPage = requests.get(AM_URL).text
AMPage.raise_for_status()
r = BeautifulSoup(AMPage, 'html.parser')

metatags = r.find_all('meta')
song_title = r.find_all('meta', attrs={"name": "apple:title"})[0]['content']
print(f"{song_title=}")

#<title> element on Apple Music page is "{Song Name} by {Artist (& others)} on Apple Music
#this block of text parses the 
title = r.find_all('title')[0].text.encode("ascii","ignore")
title = title.decode().split()
print(f"{title=}")
for i in bad_words:
	title.remove(i)

#The last two elements of title at this point will always be "on", "AppleMusic" so we drop them
keywords = " ".join(title[:-2])
print(f"{keywords=}")

# auth_response_data = auth_response.json()

# access_token = auth_response_data['access_token']

# headers = {
# 	'Authorization': f'Bearer {access_token}'
# }

#r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
# r = requests.get(BASE_URL + 'search?q=' + myQuery + '&type=track&limit=' + search_limit, headers=headers)
# r = r.json()
# for i in range(len(r['tracks']['items'])):
# 	print(r['tracks']['items'][i]['external_urls'])
#print(r)
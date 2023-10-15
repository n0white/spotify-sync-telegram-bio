import asyncio, time
from telethon import TelegramClient, errors
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
import requests
from bs4 import BeautifulSoup


#get these api values from telegram website

api_id = 16403576 #don't use quote
api_hash = "1ea4a07bb76422ac783defd8477adddc"

#Spotify api uid
uid="31dldizp7kobgvdfb4or4brza5ca"



client=TelegramClient('tguser',api_id, api_hash)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

def spotifynow():
	r = requests.get('https://spotify-github-profile.vercel.app/api/view?uid='+uid+'&cover_image=true&theme=novatorem&show_offline=true&background_color=121212&bar_color=53b14f&bar_color_cover=false', headers=headers)
	soup = BeautifulSoup(r.content, 'html.parser')
	artist = soup.find('div', class_="artist")
	song=soup.find('div', class_="song scrolling")
	prebio="t.me/thewickedkarma"
	try:
		artist= artist.get_text(strip=True, separator=' ')
	except AttributeError:
		artist="Advertisements"

	try:
		song=song.get_text(strip=True, separator=' ')
	except AttributeError:
		song=" "
	now = "▷ " + artist + " - " + song + " ılılllılı"
	if len(now) >70:
		now=now[0:69]

	try:
		async def main():
			user= await client(GetFullUserRequest('me'))
			bio = user.full_user.about
			
			if artist=="Offline" and bio==prebio:
				return
			elif artist=="Offline" and bio!=prebio:
				await client(UpdateProfileRequest(about=prebio))
				print("Updated prebio")
			elif artist=="Offline" and bio==now:
				await client(UpdateProfileRequest(about=prebio))
				print("Not updated, offline")
			elif artist!="Offline" and bio==now:
				print("Song still playing, skip update")
			else:	
				await client(UpdateProfileRequest(about=now))
				print("updated successfully")
		
	except errors.FloodWaitError as e:
		print('Have to sleep', e.seconds, 'seconds')
		time.sleep(e.seconds)
		
	with client:
		client.loop.run_until_complete(main())


while 1>0:
	time.sleep(15)
	spotifynow()






import csv 
import requests

token ="BQBG2l8LzaeYo_LVDNtyuVwxEG4ECp80Jgr-909Ve1J7qYjYIjqCaJV-RIC2x0PkCGtr93r0SFYo4gJ6mymKJ8JgNU4_XNU9borq39_e-pvwwDM5Lzw"

headers={"Authorization": f"Bearer {token}"}

test = requests.get("https://api.spotify.com/v1/playlists/0Hm1tCeFv45CJkNeIAtrfF/tracks",headers=headers)

track_list = test.json()['items']
print("-------------------------------------------------")
artists = {}

for item in track_list:
    artist_info = item['track']['artists']
    for artist in artist_info:
        id = artist['id']
        name = artist['name']
        api_link = artist['href']
        print(name)

        artists.append(name)

print(len(artists))
import csv 
import requests
import classes as cs

token ="BQDcRH6qD4QW6HX2pRy3Wv3wxqePrnCxy-gdlLnJCKfg0CtPpi9ukEj38VUSkjQZVoBDpkYvv4V6nMbeJA-Fu29XPwC0qmyGGYNc6ErlcdpOqwVYVgA"

headers={"Authorization": f"Bearer {token}"}

test = requests.get("https://api.spotify.com/v1/playlists/0Hm1tCeFv45CJkNeIAtrfF/tracks",headers=headers)

def parse_playlist(api_output):
    track_list = api_output.json()['items']
    artists = {}

    for item in track_list:
        artist_info = item['track']['artists']
        for artist in artist_info:
            id = artist['id']
            name = artist['name']
            api_link = artist['href']
            print(name)

            artists[name]={'id':id,
                        'api_link':api_link}
    return artists

print(parse_playlist(test)['Gunna'])
import csv 
import requests
import wikipediaapi
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
            #print(name)

            artists[name]={'id':id,
                        'api_link':api_link}
    return artists

#print(parse_playlist(test)['Gunna'])

#############Now I'm looking at wikipedia###################
#https://enterprise.wikimedia.com/docs/on-demand/#article-lookup

wikimedia_token ="eyJraWQiOiJzeVNnS1JaZWdwcDFlSGZEYnlsR2YrTnBjVmVXUDZJNGJlSFpOWjBDZVdrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxNGQ2MGMxOC04MGQ2LTQ5NzAtYTA4Mi0yYTY4MTRkMzFjZDkiLCJjb2duaXRvOmdyb3VwcyI6WyJncm91cF8xIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0tiNW5ZZDN6dSIsImNsaWVudF9pZCI6IjY0MXU0aTdncHR1ZmZzc2w0bTlvYXR2NHU5Iiwib3JpZ2luX2p0aSI6Ijc2MDk2MDI2LWM0NzgtNDljNy1iNDdmLTA5ZGVmOWViZjAzZCIsImV2ZW50X2lkIjoiNWQyOTdlYTMtZWNmOC00YWY0LTg5ZTUtMTAwNjQyOGQ3NmVjIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcwMTI4NDIzNywiZXhwIjoxNzAxMzcwNjM3LCJpYXQiOjE3MDEyODQyMzcsImp0aSI6ImMzYjUzOTg0LWY2OGMtNDI4Ny04ZThjLTZkYzgzODhiOTg2ZiIsInVzZXJuYW1lIjoic2t5ZWxlcmJlYXIifQ.Gr5qgDJK0RKQHQuJXfyZG0GJUz69UDAw_d0Yk1M_LbW5OFvwgUW-brsngF_QL8-clzW_hjwweGRueN5rQyL2yEEXWDKfnZfRA9NjRn3xqOSLgd2cKrYO-Ta6oP1bLZJ8sW3jJ6HNxhz9EKkVDG813n2T63PBN712144FYUFJHNTL_hhqU77Azltr5dmF-QtU-1VqrKCw7FMhpR9Y7l5vaooRafyrlonVhXloBr7BwZZcQdTxTQ7FjgZuQutWSh6FZFWlYQLOljEAwB_S0iS2eE2Hmd2mzvSDHQV2AdPLtbns-4e5mBY4OjyRa0vF2fUTe26E3-ktTRhvPTyNweapEg"

wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}


wiki_test=requests.get('https://api.enterprise.wikimedia.com/v2/structured-contents/Ella_Fitzgerald?fields=in_language&fields=infobox',headers=wiki_headers)


wiki_two=requests.get('https://api.enterprise.wikimedia.com/v2/structured-contents/Selena_Gomez?fields=in_language&fields=infobox',headers=wiki_headers)

# print(wiki_test.json())



def parse_wikimedia_request(wiki_result):

    temp_json = wiki_result.json()
    english_info=None

    for num in range(len(temp_json)):
        if 'in_language' in temp_json[num].keys():
            if temp_json[num]['in_language']['identifier']=='en':
                english_info = temp_json[num]['infobox']

    #print(len(english_info[0]['has_parts'][0]['has_parts']))
    #print(english_info[0]['has_parts'][0]['has_parts'][9]) #Birth place
    #print(english_info[0]['has_parts'][0]['has_parts'][2]['value'].lower().split(" ")) #occupations 
    #print(english_info[0]['has_parts'][0]['has_parts'][9]['value'].lower().split(" ")) #instruments

    birth = None
    died = None
    occupation = []
    instruments = []

    for item in english_info[0]['has_parts'][0]['has_parts']:
        try:
            if item['name']=='Born':
                birth = item['value']
        except:
            print("--")
        try:
            if item['name']=='Died':
                died = item['value']
        except:
            pass
        try:
            if 'occupation' in item['name'].lower():
                occupation = item['value'].lower().split(" ")
        except:
            pass
        try:
            if 'instrument' in item['name'].lower():
                instruments = item['value'].lower().split(" ")
        except:
            pass
    print(birth,died,occupation,instruments)
# info_box_info = wiki_test.json()[0]['infobox'][0]
parse_wikimedia_request(wiki_test)
parse_wikimedia_request(wiki_two)

#born = info_box_info['Born']
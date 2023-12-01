import csv 
import requests
import wikipediaapi
import classes as cs


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
print("---------------------------------------------------------------------------------")


def get_artist_genres(link,headers):
   info = requests.get(link,headers=headers).json()
   print(info)
   genres = info['genres']
   img_info = info['images']
   popularity = info['popularity']




#############Now I'm looking at wikipedia###################
#https://enterprise.wikimedia.com/docs/on-demand/#article-lookup


def wikimedia_request(wikimedia_token,artist):
        wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}
        artist_new = artist.replace(' ',"_")
        return requests.get(f'https://api.enterprise.wikimedia.com/v2/structured-contents/{artist_new}?fields=in_language&fields=infobox',headers=wiki_headers)

#wiki_test=requests.get('https://api.enterprise.wikimedia.com/v2/structured-contents/Ella_Fitzgerald?fields=in_language&fields=infobox',headers=wiki_headers)

#wiki_two=requests.get('https://api.enterprise.wikimedia.com/v2/structured-contents/Selena_Gomez?fields=in_language&fields=infobox',headers=wiki_headers)

# print(wiki_test.json())

artists_full_info = {}

def parse_wikimedia_request(name, wiki_result, artists_full_info):
    '''

    PARAMETERS
    ----------
    name: str
      The name of the artist that was searched
    wiki_result: request
      This is
    artists_full_info: dict
      The dictionary of artists where the key is their name (string) and the value
      is a dictionary with information about them. 

    RETURNS
    ----------
    None
      The function adds a new element to the input artists_full_info
    '''

    temp_json = wiki_result.json()
    english_info=None

    for num in range(len(temp_json)):
        if 'in_language' in temp_json[num].keys():
            if temp_json[num]['in_language']['identifier']=='en':
                english_info = temp_json[num]['infobox']
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
    artists_full_info[name]={'birth':birth,
                             'died': died,
                             'instruments': instruments,
                             'occupations': occupation}
# parse_wikimedia_request('Ella Fitzgerald', wiki_test, artists_full_info)
# parse_wikimedia_request('Selena Gomez', wiki_two,artists_full_info)


#born = info_box_info['Born']

def main():
    token ="BQCGMGhKtzRJc8kRxPDhx7S1NLJtraGqbMYvsEQGea0qpRLt-g8JcFm1CKGpketn6NOZMwzCcvSDmOoQHFr3SFSKccIOgU2iSYY6GqGy9wjPe8DzVg0"

    headers={"Authorization": f"Bearer {token}"}

    top100 = requests.get("https://api.spotify.com/v1/playlists/0Hm1tCeFv45CJkNeIAtrfF/tracks",headers=headers)

    parsed_100 = parse_playlist(top100)

    test_link = "https://api.spotify.com/v1/artists/07YZf4WDAMNwqr4jfgOZ8y"
    get_artist_genres(test_link,headers)

    wikimedia_token ="eyJraWQiOiJzeVNnS1JaZWdwcDFlSGZEYnlsR2YrTnBjVmVXUDZJNGJlSFpOWjBDZVdrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxNGQ2MGMxOC04MGQ2LTQ5NzAtYTA4Mi0yYTY4MTRkMzFjZDkiLCJjb2duaXRvOmdyb3VwcyI6WyJncm91cF8xIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0tiNW5ZZDN6dSIsImNsaWVudF9pZCI6IjY0MXU0aTdncHR1ZmZzc2w0bTlvYXR2NHU5Iiwib3JpZ2luX2p0aSI6ImQyOTI2MDU3LWI3MjYtNGZkMC05MWMwLTk1NjgyN2U4YzEyYSIsImV2ZW50X2lkIjoiMDMyM2JjMzAtZDg1YS00NjE3LThhMTktMTdhZjRmZDhmYTAxIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcwMTQ2NDcyNiwiZXhwIjoxNzAxNTUxMTI2LCJpYXQiOjE3MDE0NjQ3MjYsImp0aSI6ImM5OThkZWI3LTdmZTMtNGY1OC1hMjg1LWMyZWVmMDMzNDUyNCIsInVzZXJuYW1lIjoic2t5ZWxlcmJlYXIifQ.dStqBiuARmLYz_k6tEpbOnjenjQevBsZXo_EcQdgubDLTSkmHIzVZNP_EzHGT4uj6AkkVYiXFdZjTt5fHWiZTVB0ufGR3JndBwb3D5n62j8blwZoE5FNI8gFz9Aio0c4TUqwoEoDXjPRiXIVeGH0LimNkH3nrS_qQsLya_zJ3e8E2A6-3VVoSummjVZhDw99a5swqzQR-SIGig3e1RU4sKB8v7ThUMDAiT5wlXUgia5LI-Cx6HWaQ5zxZI0VF0kiIY_iNwK9QGeqybKcPkez0e7qvsDMkh4SDsEb_ZkoO1kRKbhAjGoWwodfix45hi-GYnBSr0lfEesvz5wKx-X6EA"
    wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}

    

    pass

if __name__ == '__main__':
    main()
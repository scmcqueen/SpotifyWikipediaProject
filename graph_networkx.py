import csv 
import requests
import wikipediaapi
import classes as cs
import json
import networkx as nx

############# Cache info ############# 

def open_cache(CACHE_FILENAME):
    ''' This function opens the cache json if it exists and loads
    it into a dictionary. If it doesn't exist, then this function
    creates a new cache dictionary.
    Parameters
    ----------
    CACHE_FILENAME: str
        The name of the cache file 
    Returns
    ----------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict,CACHE_FILENAME):
    ''' saves the current state of the cache
    Parameters
    ----------
    CACHE_FILENAME: str
        The name of the cache file 
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def parse_playlist(api_output):
    print(api_output.json())
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



def get_artist_genres(link,headers):
   info = requests.get(link,headers=headers).json()
   #print(info)
   genres = info['genres']
   img_info = info['images']
   popularity = info['popularity']
   return {'genres':genres,
           'img_info':img_info,
           'popularity':popularity}




############# Now I'm looking at wikipedia ###################
#https://enterprise.wikimedia.com/docs/on-demand/#article-lookup


def wikimedia_request(wikimedia_token,artist):
        wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}
        artist_new = artist.replace(' ',"_")
        return requests.get(f'https://api.enterprise.wikimedia.com/v2/structured-contents/{artist_new}?fields=in_language&fields=infobox',headers=wiki_headers)


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
    birth = None
    died = None
    occupation = []
    instruments = []
    print(name)
    try:
        for num in range(len(temp_json)):
            if 'in_language' in temp_json[num].keys():
                if temp_json[num]['in_language']['identifier']=='en':
                    english_info = temp_json[num]['infobox']

        for item in english_info[0]['has_parts'][0]['has_parts']:
            try:
                if item['name']=='Born':
                    birth = item['value']
            except:
                continue
            try:
                if item['name']=='Died':
                    died = item['value']
            except:
                continue
            try:
                if 'occupation' in item['name'].lower():
                    occupation = item['value'].lower().split(" ")
            except:
                continue
            try:
                if 'instrument' in item['name'].lower():
                    instruments = item['value'].lower().split(" ")
            except:
                continue
            if died ==None:
                died = 'alive'
    except:
        print('----------Nah')
    artists_full_info['birth']=birth
    artists_full_info['died']=died
    artists_full_info['instruments']=instruments
    artists_full_info['occupations']=occupation
    #artists_full_info[name]={'birth':birth,
                                # 'died': died,
                                # 'instruments': instruments,
                                # 'occupations': occupation}

def createMyGraph():
    token ="BQCqN1f9J0sTBh-OFxuNFWc584q0uQNtc1rPJPUyX2XnVA2_v-nyDpvvHsX97AogACuUjfeaxHS65oF5kLGvYszPdZz6Uz3hTsKZqjkGgknhHJiO99E"

    headers={"Authorization": f"Bearer {token}"}

    CACHE_FILENAME = "spotify_wikipedia.json" #step 7

    spotify_cache = open_cache(CACHE_FILENAME)

    #top100 = requests.get("https://api.spotify.com/v1/playlists/0Hm1tCeFv45CJkNeIAtrfF/tracks",headers=headers) #ACTUAL TOP 100 PLAYLIST
    #3elUaCbtaDQytMZrHbItmy
    #https://open.spotify.com/playlist/1epzzJHOES6doiLf16R6Jw?si=WBINOs5vQ0yvBwLniKMV1w
    top100 = requests.get("https://api.spotify.com/v1/playlists/1epzzJHOES6doiLf16R6Jw/tracks",headers=headers) #current playlist

    parsed_100 = parse_playlist(top100)

    test_link = "https://api.spotify.com/v1/artists/07YZf4WDAMNwqr4jfgOZ8y"
    get_artist_genres(test_link,headers)

    wikimedia_token ="eyJraWQiOiJzeVNnS1JaZWdwcDFlSGZEYnlsR2YrTnBjVmVXUDZJNGJlSFpOWjBDZVdrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxNGQ2MGMxOC04MGQ2LTQ5NzAtYTA4Mi0yYTY4MTRkMzFjZDkiLCJjb2duaXRvOmdyb3VwcyI6WyJncm91cF8xIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0tiNW5ZZDN6dSIsImNsaWVudF9pZCI6IjY0MXU0aTdncHR1ZmZzc2w0bTlvYXR2NHU5Iiwib3JpZ2luX2p0aSI6ImEzMGRmMmZmLWNlNDAtNDBkMS04YjdkLWUzNWEyZmFiMDA3ZSIsImV2ZW50X2lkIjoiOWE3MjViMjYtNDMwNy00YjM5LThiMzktZTE0MDllMTYxMmY4IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcwMTk3MDgwMCwiZXhwIjoxNzAyMDU3MjAwLCJpYXQiOjE3MDE5NzA4MDAsImp0aSI6ImVlNjE3NjBlLTI3MzMtNDQwMC1iNDg2LTIwNjIwMDlhYzMxOSIsInVzZXJuYW1lIjoic2t5ZWxlcmJlYXIifQ.nI2jNZWALbgFRfLybK405Fjjp28uBBVrD5yEW2sFOJ6UPg4PrnNqkwjJ9Ch8lzCtq45MOl9AwrEf7hzFMWnJ5-_pSX6pCi1X8YZ0VA-kXGhjUhfOmtKUbCcl6T62xAuyN9GCQ2168BAv-GFR2vzz3YYrFzknEXn_-6d0u3nELmI2I_0NMxvCrfp6nfhV7SpSAwc0Uo3KsE2zjRjbruWHSM5pVokHwYuMRiVez2bdH_FIQTE76XNOVDEW4aI9sywm6Ig1f4R2lRn8xWacZcyd9CmzC9ROClgDw-GWMRmURRsoonVoKFO04n2lG9NXrk_1XVQWjU-EXoVykHWp-kqfnw"
    wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}

    for celeb in parsed_100.keys():
        if celeb not in spotify_cache.keys():
            more_deets = get_artist_genres(parsed_100[celeb]['api_link'],headers)

            wiki_deets = wikimedia_request(wikimedia_token,celeb)
            parse_wikimedia_request(celeb,wiki_deets,more_deets)
            print(more_deets)
            
            for item in more_deets.keys():
                parsed_100[celeb][item]=more_deets[item]
            
            spotify_cache[celeb]=parsed_100[celeb]
        else: #already cached
            parsed_100[celeb] = spotify_cache[celeb]
    save_cache(spotify_cache,CACHE_FILENAME)
    
    mygraph = nx.Graph()

    for artist in parsed_100:
        parsed_100[artist]['type']='artist'

        mygraph.add_nodes_from([(artist,{'type':'artist'})])


        for gen in parsed_100[artist]['genres']:
            mygraph.add_nodes_from([(gen,{'type':'genre'})])
            mygraph.nodes[gen]['type']='genre'
            mygraph.add_edge(artist,gen)
    # print(mygraph)
    # print("---------------")
    print(f'Nodes: {str(len(list(mygraph.nodes)))}')
    # print(list(mygraph.nodes))
    # print("---------------")
    print(f'Edges: {str(len(list(mygraph.edges)))}')
    # #print(f"The number of vertices is: {len(mygraph.vertList)}!")
    # print("---------------")
    # print(mygraph.nodes['Katy Perry'])
    return([mygraph,parsed_100,"placeholder playlist name"])

if __name__ == '__main__':
    createMyGraph()


    
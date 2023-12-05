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
# parse_wikimedia_request('Ella Fitzgerald', wiki_test, artists_full_info)
# parse_wikimedia_request('Selena Gomez', wiki_two,artists_full_info)


#born = info_box_info['Born']

def createMyGraph():
    token ="BQBDhUnf-pBCr5Qiuhij08_X4HTZnKCx2bwyMaZIBGUNqH0F4VkBe-_u_NZD3n9m9HhzQhza4Es46jMa5LaggY-mltfXhuNQekwCpVroHwsiMyqsMVw"

    headers={"Authorization": f"Bearer {token}"}

    CACHE_FILENAME = "spotify_wikipedia.json" #step 7

    spotify_cache = open_cache(CACHE_FILENAME)

    top100 = requests.get("https://api.spotify.com/v1/playlists/0Hm1tCeFv45CJkNeIAtrfF/tracks",headers=headers)

    parsed_100 = parse_playlist(top100)

    test_link = "https://api.spotify.com/v1/artists/07YZf4WDAMNwqr4jfgOZ8y"
    get_artist_genres(test_link,headers)

    wikimedia_token ="eyJraWQiOiJzeVNnS1JaZWdwcDFlSGZEYnlsR2YrTnBjVmVXUDZJNGJlSFpOWjBDZVdrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxNGQ2MGMxOC04MGQ2LTQ5NzAtYTA4Mi0yYTY4MTRkMzFjZDkiLCJjb2duaXRvOmdyb3VwcyI6WyJncm91cF8xIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0tiNW5ZZDN6dSIsImNsaWVudF9pZCI6IjY0MXU0aTdncHR1ZmZzc2w0bTlvYXR2NHU5Iiwib3JpZ2luX2p0aSI6ImFlM2RlZTU5LWRlZjEtNGViOS05Njk0LWJjZWU1YTQ2YWIwZiIsImV2ZW50X2lkIjoiZTJmMjdmYWUtNWVmZi00NWM0LTlmNDQtOTRhNjA1NjEyN2E1IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcwMTc4ODQ0MSwiZXhwIjoxNzAxODc0ODQxLCJpYXQiOjE3MDE3ODg0NDEsImp0aSI6ImU1ZTRiMTk1LTVkYjEtNDZmMy04OWFkLTdiMzA5YjEyOTgwMyIsInVzZXJuYW1lIjoic2t5ZWxlcmJlYXIifQ.SOwOkuenPGk6o8bCQHDbWBPdvfnSNC-MBzwGFdpsiWFaxSqJQifQuosDkRy5JcCOEW2hpeTESOIlVQKFvALEdVb1dm5hiCXZfA1as2C6pKNeadHn_5QkaoyjZ7Y3BiC444dnlLWg9eE6b_daK-P6pMg8_EVltd2L4up8kQK1Ag3wS00SJkwfyiuEr6-_5RGu6P4z5UsRo0Fq_c09MF8bC5Mac1HYufjoo0wQPXJZRyASCrzY3qPq6Zg-GFgKHSOe79QqR9uOSK_JIMugAlJNY7g62lIbidy-3mMkxqKTX2c2oYTgoxuFovkdMlyhIyhf4um-9wagrNNzBkuJW2zd_w"
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
    
    mygraph = cs.Graph()

    for artist in parsed_100:
        mygraph.addVertex(artist)

        mygraph.vertList[artist].deathDate = parsed_100[artist]['died']
        mygraph.vertList[artist].birthDate = parsed_100[artist]['birth']
        mygraph.vertList[artist].occupations = parsed_100[artist]['occupations']
        mygraph.vertList[artist].instruments = parsed_100[artist]['instruments']
        mygraph.vertList[artist].popularity= parsed_100[artist]['popularity']
        mygraph.vertList[artist].image_info = parsed_100[artist]['img_info']

        for gen in parsed_100[artist]['genres']:
            mygraph.addEdge(gen,'genre',artist,'artist')
    print(mygraph)
    print("---------------")
    print(f"The number of vertices is: {len(mygraph.vertList)}!")
    return(mygraph)

#if __name__ == '__main__':
    #main()
    # test = {'Skyeler': {'id':'teehee','api_link':'boring,','genres':['pov indie','video game music'],'img_info':'too pretty','popularity':0,'birth':'Royal Oak Michigan June 30,1999','died':'alive','instruments':['vocalish'],'occupations':['depressed','student','crafty girl']},
    #         'Samuel': {'id':'toho','api_link':'boring,','genres':['pov indie','musical theater'],'img_info':'too handsome','popularity':100,'birth':'Baltimore Maryland June 30,1999','died':'alive','instruments':['vocals','piano','guitar'],'occupations':['depressed','software engineer','adult lego masters fan']}}

    # for artist in test:
    #     print(artist)
    #     graphy.addVertex(artist)

    #     graphy.vertList[artist].deathDate = test[artist]['died']
    #     graphy.vertList[artist].birthDate = test[artist]['birth']
    #     graphy.vertList[artist].occupations = test[artist]['occupations']
    #     graphy.vertList[artist].instruments = test[artist]['instruments']
    #     graphy.vertList[artist].popularity= test[artist]['popularity']
    #     graphy.vertList[artist].image_info = test[artist]['img_info']
    

    #     for gen in test[artist]['genres']:
    #         graphy.addEdge(gen,'genre',artist,'artist')
    

    
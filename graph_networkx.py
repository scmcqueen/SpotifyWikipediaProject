import requests
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

############# Spotify API Parsing  ############# 
def parse_playlist(api_output):
    '''
    Parses the api output of a spotify api playlist tracks call. 
    Finds each artist per each song on the playlist and adds the artist to a dictionary, 
    with their spotify id and their api_link. 

    PARAMETERS
    ----------
    api_output: requests response type
        the output of an api get request

    RETURNS
    -------
    dict
        dictionary where the key is the name of an artist (str) and the value is a dictionary with info
    '''
    track_list = api_output.json()['items']
    output = {}

    for item in track_list:
        artist_info = item['track']['artists']
        for artist in artist_info:
            id = artist['id']
            name = artist['name']
            api_link = artist['href']
            output[name]={'id':id,
                        'api_link':api_link}
    return output

def get_artist_genres(link,headers):
   '''
   Makes a request based on an artist's link and returns a dictionary with additional 
   info about that artist. 

   PARAMETERS
   ----------
   link: str
        spotify api link to get information about an artist
    headers: dict
        api headers to use in the request, should be a dict with a bearer token.

   RETURNS
   -------
   dict
        a dictionary with the artist's genres, image information, and popularity
   '''
   info = requests.get(link,headers=headers).json()
   genres = info['genres']
   img_info = info['images']
   popularity = info['popularity']
   return {'genres':genres,
           'img_info':img_info,
           'popularity':popularity}

def get_title_info(headers,playlist_id):
    '''
    Makes a spotify api request to get the title and author of a playlist in a pretty string format.

    PARAMETERS
    ----------
    headers: dict
        api headers to use in the request, should be a dict with a bearer token.
    playlist_id: str
        the spotify unique id for a playlist

    RETURNS
    -------
    str
        the playlist name and ownner in the format "<playlist name> by <playlist author>"
    '''
    info = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}",headers=headers).json()
    return(f"{info['name']} by {info['owner']['display_name']}")

############# Wikimedia API Parsing  ############# 

def wikimedia_request(wikimedia_token,artist):
    '''
    create a wikimedia request of a specific artist's infobox and return the request result object. 

    PARAMETERS
    ----------
    wikimedia_token: str
        access token to make wikimedia request
    artist: str
        name of the artist you're looking up 

    RETURNS
    -------
    request result object
        The result of the api request to get the artist's infobox
    '''
    wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'}
    artist_new = artist.replace(' ',"_")
    return requests.get(f'https://api.enterprise.wikimedia.com/v2/structured-contents/{artist_new}?fields=in_language&fields=infobox',headers=wiki_headers)

def parse_wikimedia_request(name, wiki_result, artists_full_info): ###SKYELER DOUBLE CHECK HOW THIS FUNCTION WORKS
    '''
    Parses wikimedia infobox request api output and adds the new information to 
    the artists_full_info dictionary.

    PARAMETERS
    ----------
    name: str
      The name of the artist that was searched
    wiki_result: request
      This is the output of the wikimedia_request function, a request result object
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
        print(f'----------No Wikipedia Page available for {name}')
    artists_full_info['birth']=birth
    artists_full_info['died']=died
    artists_full_info['instruments']=instruments
    artists_full_info['occupations']=occupation

############# Put it all together to create a graph  ############# 

def createMyGraph(wikimedia_token,spotify_token,playlist_id="0Hm1tCeFv45CJkNeIAtrfF"):
    '''
    Run all of the api calls necessary to create a networkx graph of a given spotify playlist, 
    a lookup dictionary with information about the artists, and a string in the format of 
    "<Playlist name> by <playlist owner>".

    PARAMETERS
    ----------
    wikimedia_token: str
        The token to login to the wikimedia API
    spotify_token: str
        The token to login to the spotify API
    playlist_id: str
        The spotify playlist unique id

    RETURNS
    -------
    list: [networkx graph, dict, str]
        The list is described in more detail above
    '''

    headers={"Authorization": f"Bearer {spotify_token}"} #set the spotify headers

    CACHE_FILENAME = "spotify_wikipedia.json" #name of the cache

    spotify_cache = open_cache(CACHE_FILENAME) #open the cache

    title_info = get_title_info(headers,playlist_id)

    top100 = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",headers=headers) #get the tracks
   
    parsed_100 = parse_playlist(top100) #parse the tracs

    wiki_headers = {"Authorization": f'Bearer {wikimedia_token}'} #set the wikimedia headers

    for celeb in parsed_100.keys(): # parse each artist in the list if it isn't in the cache
        if celeb not in spotify_cache.keys():
            more_deets = get_artist_genres(parsed_100[celeb]['api_link'],headers)
            wiki_deets = wikimedia_request(wikimedia_token,celeb)
            parse_wikimedia_request(celeb,wiki_deets,more_deets)
            for item in more_deets.keys():
                parsed_100[celeb][item]=more_deets[item]
            spotify_cache[celeb]=parsed_100[celeb]
        else: 
            parsed_100[celeb] = spotify_cache[celeb]

    save_cache(spotify_cache,CACHE_FILENAME) #save the cache
    
    mygraph = nx.Graph() #initialize the graph object

    for artist in parsed_100: #add each artist to graph
        parsed_100[artist]['type']='artist'
        mygraph.add_nodes_from([(artist,{'type':'artist'})])
        for gen in parsed_100[artist]['genres']: #add each genre to the graph
            mygraph.add_nodes_from([(gen,{'type':'genre'})])
            mygraph.nodes[gen]['type']='genre'
            mygraph.add_edge(artist,gen)

    print(f'Nodes: {str(len(list(mygraph.nodes)))}')
    print(f'Edges: {str(len(list(mygraph.edges)))}')
    return([mygraph,parsed_100,title_info]) #return statment


if __name__ == '__main__':
    #used this to test specific functions
    pass

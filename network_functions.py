import csv 
import requests
import wikipediaapi
import classes as cs
import json
import networkx as nx
import graph_networkx as gnx
import nx_altair as nxa
import pandas as pd
import altair as alt
from networkx.readwrite import json_graph
import re

def draw_network(graph,labels=True,size_v=300):        #labels is true or false
    '''
    Draws the given networkx graph in altair, with nodes colored by type

    Ex implementation: draw_network(graph,False,100).properties(width=500,height=500)

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    labels: bool
        whether each node should have labels or not 
    size_v: int
        the size of the circles representing the nodes
    
    RETURNS
    -------
    altair chart
        chart showing the nodes and edges
    '''

    for n in graph.nodes():
        graph.nodes[n]['id']=str(n)

    position = nx.spring_layout(graph)

    nodelayer = nxa.draw_networkx_nodes(graph,pos=position)
    edgeslayer = nxa.draw_networkx_edges(graph,pos=position,width=5,edge_color="#2CDA9D")
    n1=nodelayer.mark_circle(size=size_v,opacity=1).encode(color=alt.Color('type:N',scale=alt.Scale(range=["#CE1483",'#3772FF'])),tooltip=['id:N'])
    text = nodelayer.mark_text(color='black',dx=25,fontSize=13,fontWeight="bold",align="left",).encode(
        text='id:N'
        )
    if len(graph.nodes)<21:
        return(edgeslayer+n1+text)
    return((edgeslayer+n1).interactive())

def get_genre_artists(graph):
    '''
    Gets easy to parse lists of all the artists in a graph and all the genres.

    Returns the lists in a dict with keys 'artists' and 'genres'

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    
    RETURNS
    -------
    dict: key string, value list
        dict with keys 'artists' & 'genres' with lists of all artists & genres respectively
    
    '''
    artist_list = []
    genre_list = []

    for n in graph.nodes():
        if graph.nodes[n]['type']=='artist':
            artist_list.append(n)
        elif graph.nodes[n]['type']=='genre':
            genre_list.append(n)
        else:
            print(n)
    return({'artists':artist_list,'genres':genre_list})

def get_focus_graph(graph,name):
        '''
        returns a subgraph showing one node and its neighbors or none if the name
        does not correspond to a node id.

        can be used to filter by an artist or a genre.

        PARAMETERS
        ----------
        graph: networkx graph
            graph with nodes and edges, where every node has attributes id and type
        name: str
            id of a node that the user wants to investigate

        RETURNS
        -------
        networkx graph
            a filtered networkx subgraph focusing on the input node and its neighbors
        '''
        try:
            neighbors = [n for n in graph.neighbors(name)]

            def filter_node(n1):
                if n1 ==name: 
                    return True
                return (n1 in neighbors)
        
            sub_graph = nx.subgraph_view(graph,filter_node)
            return sub_graph
        except:
            return None

def get_shortest_graph(graph,name,end):
        '''
        Get a graph with the shortest path from node name to node end.

        Returns a graph with the genres and artists or None if no path exists or if the nodes don't exist.

        PARAMETERS
        ----------
        name: str
            id of the node starting the shortest path
        end: str
            id of the node ending the shortest path
        graph: networkx graph
            graph with nodes and edges, where every node has attributes id and type

        RETURNS
        -------
        networkx graph
            a filtered networkx subgraph with the path from name to end
        '''
        try: #the next line is where most errors would occur
            neighbors = nx.shortest_path(graph,source=name,target=end) 

            def filter_node(n1):
                if n1 ==name: 
                    return True
                return (n1 in neighbors)
            
            sub_graph = nx.subgraph_view(graph,filter_node)
            return(sub_graph)
        except:
            return None

def search_dead(graph, lookup): 
    '''
    Returns a graph object where all of the artists are known to be dead, by referencing the lookup dict.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node_dead(n1):
        #helper function, takes a node and then returns True or False if it should be included in the sub graph
        #basically a filtering function
        if graph.nodes[n1]['type']=='genre': #if its a genre its not dead
            return False
        elif lookup[n1]['died']== None: #if there's no data, we won't count it as dead
                return False
        elif lookup[n1]['died']=='alive': #if its alive, then it is not dead
                return False
        return True
    sub_graph = nx.subgraph_view(graph,filter_node_dead)

    nbrs = []

    for node in sub_graph:
        neighbors = [n for n in graph.neighbors(node)]
        nbrs += neighbors 

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_alive(graph,lookup): 
    '''
    Returns a graph object where all of the artists are known to be alive!

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node(n1):
    #Helper function, returns true if the 'died' attribute of a node has a value of 'alive'
    #if returns true, will be included in subgraph
        if graph.nodes[n1]['type']=='genre': #if its a genre its not alive
            return False
        if lookup[n1]['died'] is None:
             return False
        elif lookup[n1]['died']=='alive':
                return True
        return False
    sub_graph= nx.subgraph_view(graph,filter_node)
    nbrs = []

    for node in sub_graph:
        neighbors = [n for n in graph.neighbors(node)]
        nbrs += neighbors #could clean this up

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_from(graph,place,lookup): 
    '''
    Returns a graph object where all of the artists were born in a specific place or year.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    from: str
        the place of birth or year of birth, e.g. 'New York', 'England', '1997', 'June'
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node(n1):
    #Helper function, returns true if the 'birth' attribute contains the place variable
    #if returns true, will be included in subgraph
        if graph.nodes[n1]['type']=='genre': #discount all genres
            return False
        if lookup[n1]['birth']==None: #don't include things without data
            return False
        elif place.lower() in lookup[n1]['birth'].lower(): 
            return True
        return False
    
    sub_graph = nx.subgraph_view(graph,filter_node)

    nbrs = []

    for node in sub_graph:
        nbrs += [n for n in graph.neighbors(node)]

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_occupations(graph,job,lookup): 
    '''
    Returns a graph object where all of the artists have a specific occupation.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    job: str
        the occupation being searched for, e.g. 'poet', 'television', 'author', 'entrepreneur'
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node(n1):
    #Helper function, returns true if the 'occupation' attribute contains the job variable
    #if returns true, will be included in subgraph
        if graph.nodes[n1]['type']=='genre': #genres don't have jobs
            return False
        if lookup[n1]['occupations']==None:
            return False
        elif job.lower().strip() in lookup[n1]['occupations']: 
            return True
        return False
    
    sub_graph = nx.subgraph_view(graph,filter_node)

    nbrs = []

    for node in sub_graph:
        neighbors = [n for n in graph.neighbors(node)]
        nbrs += neighbors #could clean this up

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_instruments(graph,instru,lookup): 
    '''
    Returns a graph object where all of the artists play a specific instrument.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    instru: str
        the instrument being searched for, e.g. 'vocals', 'guitar', 'piano'
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node(n1):
    #Helper function, returns true if the 'instrument' attribute list contains the instru variable
    #if returns true, will be included in subgraph
        if graph.nodes[n1]['type']=='genre':
            return False
        if lookup[n1]['instruments']==None:
            return False
        elif instru.lower().strip() in lookup[n1]['instruments']: 
            return True
        return False
    
    sub_graph = nx.subgraph_view(graph,filter_node)

    nbrs = []

    for node in sub_graph:
        neighbors = [n for n in graph.neighbors(node)]
        nbrs += neighbors #could clean this up

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)
    
    return nx.subgraph_view(graph,filter_genres)

def calculate_avg_popularity(lookup):
    '''
    Return the average popularity of all artists in the lookup dictionary. 

    Uses Spotify's popularity score, which ranges from 0-100. 

    PARAMETERS
    ----------
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    ------
    float
        The average popularity of all artists in the graph
    '''
    count = 0
    sum=0
    for n in lookup.keys():
        sum +=lookup[n]['popularity']
        count+=1
    return (sum/count)

def filter_popularity(graph,pop,lookup): 
    '''
    Returns a graph object where all of the artists are above popularity score of pop. 

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    pop: int
        the lower bound of popularity, e.g. '70'
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    networkx graph
        a filtered networkx subgraph focusing on the input node and its neighbors
    '''
    def filter_node(n1):
    #Helper function, returns true if the 'popularity' attribute is greater or equal to pop
    #if returns true, will be included in subgraph
        if graph.nodes[n1]['type']=='genre':
            return False
        if lookup[n1]['popularity']==None:
            return False
        elif int(lookup[n1]['popularity'])>=int(pop): #type enforcement
            return True
        return False
    
    sub_graph = nx.subgraph_view(graph,filter_node)

    nbrs = []

    for node in sub_graph:
        neighbors = [n for n in graph.neighbors(node)]
        nbrs += neighbors 

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in (sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)
    

    return nx.subgraph_view(graph,filter_genres)

def load_example_graph(graph_name='test_graph_data',dict_name='test_lookup_data',name="Currently by skyelermcquill"):
    '''
    Loads a networkx graph from a json file with a node-link graph data. 

    Returns a networkx graph! This function was made to save a step from loading API data. 

    PARAMETERS
    ----------
    graph_name: str
        the name of the json file you want to load with graph data
    dict_name: str
        the name of the json file you want to load with lookup dict data
    name: str
        name of the playlist you're loading

    RETURNS
    -------
    list: [networkx graph, dict]
        a node link graph objects
    '''
    ex_file = open(graph_name,"r")
    graph_contents = ex_file.read()
    graph_dict = json.loads(graph_contents)
    ex_file.close()

    dict_file = open(dict_name,"r")
    lookup_cont = dict_file.read()
    lookup = json.loads(lookup_cont)
    dict_file.close()
    return [nx.node_link_graph(graph_dict),lookup,name]

def parse_playlist(link='skyeler'):
    '''
    Get the spotify playlist id from a playlist link 

    PARAMETERS
    ----------
    link: str
        the link to a playlist on spotify
    
    RETURNS
    -------
    str
        the spotify playlist id
    '''
    regex_pattern = r'/playlist/([a-zA-Z0-9]+)'

    regex_match = re.search(regex_pattern,link)

    if regex_match:
        id = regex_match.group(1)
        return id
    return None

def get_most_popular_artist(lookup):
    '''
    Return the most popular artists' names, based on spotify's popularity score. 

    PARAMETERS
    ----------
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.

    RETURNS
    -------
    list
        names of the most popular artist.
    '''

    pop = 0
    persons = []
    for artist in lookup.keys():
        if lookup[artist]['popularity']==pop:
            persons.append(artist)
        elif lookup[artist]['popularity']>pop:
            pop = lookup[artist]['popularity']
            persons = [artist]
    return persons

def get_all_occupations(lookup):
    '''
    return a list of all of the possible occupations that artists have listed on their wikipedia pages. 

    list is unique and lower case.

    PARAMETERS
    ----------
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.
    
    RETURNS
    -------
    list of str
        returns a list of occupations
    '''
    jobs = []
    for item in lookup.keys():
        for occ in lookup[item]['occupations']:
            occ = occ.replace(',','').lower()
            if occ not in jobs:
                jobs.append(occ)
    return jobs

def get_all_instruments(lookup):
    '''
    return a list of all of the possible instruments that artists play based on their wikipedia pages. 

    list is unique and lower case.

    PARAMETERS
    ----------
    lookup: dict
        dict with keys string and value dictionary, contains extra info about the artist.
    
    RETURNS
    -------
    list of str
        returns a list of instruments
    '''
    inst = []
    for item in lookup.keys():
        for occ in lookup[item]['instruments']:
            occ = occ.replace(',','').lower()
            if occ not in inst:
                inst.append(occ)
    return inst

def top_genres_bar(graph):
    '''
    Return a bar chart of the top 10 genres in a graph. 

    Bar chart is an altair object. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type

    RETURNS
    -------
    altair chart
        bar chart with genres on the y axis and count of artists on the x axis
    '''
    genres = []

    for gnode in graph.nodes:
        if graph.nodes[gnode]['type']=='genre':
            genres.append([gnode,len([n for n in graph.neighbors(gnode)])])

    genre_popularity = pd.DataFrame(genres,columns = ['Genres',"Count of Artists"])
    #genre_popularity

    return alt.Chart(genre_popularity).mark_bar(color="#065143").encode(
        x=alt.X('Count of Artists:Q'),
        y=alt.Y('Genres:N',
                sort='-x')).transform_window(
        rank='rank(Neighbors)',
        #sort=[alt.SortField('Neighbors', order='descending')]
    ).transform_filter(
        (alt.datum.rank < 10)
    )

def get_wikimedia_access_token(username,password):
    '''
    Get the access token for the wikimedia api using username and password
    from post request. 

    Will be used to get information from the wikimedia api.

    PARAMETERS
    ----------
    username: str
        the username of your wikimedia account
    password: str
        the password of your wikimedia account

    RETURNS
    -------
    str
        The access token for the wikimedia api
    '''

    info = requests.post(url="https://auth.enterprise.wikimedia.com/v1/login",
                        headers={"Content-Type":"application/json"},
                        data=f'{{"username":"{username}", "password":"{password}"}}')
    return(info.json()['access_token'])

def get_spotify_token(client_id,client_secret):
        '''
        Get the spotify api access token using client id and secret from post request. 

        PARAMETERS
        ----------
        client_id: str
            client id for spotify developer account
        client_secret: str
            client secret for spotify developer account
        RETURNS
        -------
        str
            bearer access token for spotify api
        '''
        info = requests.post(url="https://accounts.spotify.com/api/token",
                        headers={"Content-Type":"application/x-www-form-urlencoded"},
                        data=f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}")
        return(info.json()['access_token'])








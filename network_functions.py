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
    position = nx.spring_layout(graph)

    nodelayer = nxa.draw_networkx_nodes(graph,pos=position)
    edgeslayer = nxa.draw_networkx_edges(graph,pos=position)
    n1=nodelayer.mark_circle(size=size_v,opacity=1).encode(color='type:N',tooltip=['id:N'])
    text = nodelayer.mark_text(color='black').encode(
        text='id:N'
        )
    if labels:
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

def search_from(graph,place): 
    '''
    Returns a graph object where all of the artists were born in a specific place or year.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    from: str
        the place of birth or year of birth, e.g. 'New York', 'England', '1997', 'June'

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
        if graph.nodes[n1]['birth']==None: #don't include things without data
            return False
        elif place.lower() in graph.nodes[n1]['birth'].lower(): 
            return True
        return False
    
    sub_graph = nx.subgraph_view(graph,filter_node)

    nbrs = []

    for node in sub_graph:
        nbrs += [n for n in graph.neighbors(node)]

    def filter_genres(n1):
        #similar helper function to one above, returns true or false if the node should be included
        #filters to include the nodes from sub_graph and their neighbors
        if n1 in list(sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_occupations(graph,job): 
    '''
    Returns a graph object where all of the artists have a specific occupation.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    job: str
        the occupation being searched for, e.g. 'poet', 'television', 'author', 'entrepreneur'

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
        if graph.nodes[n1]['occupations']==None:
            return False
        elif job.lower() in graph.nodes[n1]['occupations']: 
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
        if n1 in list(sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)

    return nx.subgraph_view(graph,filter_genres)

def search_instruments(graph,instru): 
    '''
    Returns a graph object where all of the artists play a specific instrument.

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    instru: str
        the instrument being searched for, e.g. 'vocals', 'guitar', 'piano'

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
        if graph.nodes[n1]['instruments']==None:
            return False
        elif instru.lower() in graph.nodes[n1]['instruments']: 
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
        if n1 in list(sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)
    
    return nx.subgraph_view(graph,filter_genres)

def calculate_avg_popularity(graph):
    '''
    Return the average popularity of all artists in the graph. 

    Uses Spotify's popularity score, which ranges from 0-100. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type

    RETURNS
    ------
    float
        The average popularity of all artists in the graph
    '''
    count = 0
    sum = 0

    for n in graph.nodes:
        if graph.nodes[n]['type']!='genre':
            sum +=graph.nodes[n]['popularity']
            count+=1
    return (sum/count)

def filter_popularity(graph,pop): 
    '''
    Returns a graph object where all of the artists are above popularity score of pop. 

    Contains the artists and their genres. 

    PARAMETERS
    ----------
    graph: networkx graph
        graph with nodes and edges, where every node has attributes id and type
    pop: int
        the lower bound of popularity, e.g. '70'

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
        if graph.nodes[n1]['popularity']==None:
            return False
        elif int(graph.nodes[n1]['popularity'])>=int(pop): #type enforcement
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
        if n1 in list(sub_graph.nodes): 
            return True
        elif graph.nodes[n1]['type']!='genre':
            return False
        return (n1 in nbrs)
    

    return nx.subgraph_view(graph,filter_genres)

def load_example_graph(filename='test_graph_data'):
    '''
    Loads a networkx graph from a json file with a node-link graph data. 

    Returns a networkx graph! This function was made to save a step from loading API data. 

    PARAMETERS
    ----------
    filename: str
        the name of the json file you want to load

    RETURNS
    -------
    networkx graph
        a node link graph objects
    '''
    ex_file = open(filename,"r")
    graph_contents = ex_file.read()
    graph_dict = json.loads(graph_contents)
    ex_file.close()
    return nx.node_link_graph(graph_dict)

def parse_playlist(link='skyeler'):
    if link.lower() == 'skyeler':
        return load_example_graph()
    return None
    #SKYELER TO DO!!! ADD PARSING OF API LINK
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



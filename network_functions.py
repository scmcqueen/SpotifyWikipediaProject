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
        return(edgeslayer+n1)
    return((edgeslayer+n1).interactive())

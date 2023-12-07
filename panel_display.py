# load up the libraries
import panel as pn
import pandas as pd
import altair as alt
from altair_transform import extract_data
import time,json
import networkx as nx
import nx_altair as nxa
import traceback
import pygraphviz
import graph_networkx as gnx
import network_functions as ntf
import json
import requests
import csv 
import requests
import wikipediaapi
import classes as cs
import json
import networkx as nx
from networkx.readwrite import json_graph

pn.extension('vega')
alt.renderers.enable('default')

# we want to use bootstrap/template, tell Panel to load up what we need
pn.extension(design='bootstrap')

#initialize global variables
graph = None
blank_chart = alt.Chart(pd.DataFrame([], columns=['Waiting for good tunes...'])).mark_point().encode(
            x='Waiting for good tunes..:Q',
        )

#Here I will define my left sidecol
sidecol = pn.Column()
welcome_text = pn.pane.Markdown(
    '''
    ## Input a link to a public playlist on Spotify

    #### or type "Skyeler" to see what Skyeler is listening to now...
    ''')


#left hand widgets
start_button = pn.widgets.Button(name='Start',button_type='primary')
playlist_input= pn.widgets.TextInput(name='Playlist link:', placeholder='Skyeler')
#append widgets to side col
sidecol.append(welcome_text)
sidecol.append(playlist_input)
sidecol.append(start_button)
#define function to bind
def click_start(event):
    global graph
    #graph = ntf.parse_playlist(playlist_input.value)

# playlist_graph = pn.panel(alt.Chart(pd.DataFrame([], columns=['data'])).mark_bar().encode(
#             x='data:Q',
#         ).properties(title="Waiting for data..."))

data =  {'directed': False, 'graph': {}, 'links': [{'source': 'Lia Pappas-Kemps', 'target': 'pov: indie'},{'source': 'Lia Pappas-Kemps', 'target': 'toronto indie'}], 'multigraph': False, 'nodes': [{'id':'Lia Pappas-Kemps','type':'artist'},{'id':'toronto indie','type':'genre'},{'id':'pov: indie','type':'genre'},{'id':'bussy','type':'genre'},{'id':'baddy','type':'genre'},{'id':'Lia 11Pappas-Kemps','type':'artist'},{'id':'toronto in111111die','type':'genre'},{'id':'pov: 11111indie','type':'genre'},{'id':'bus111111sy','type':'genre'},{'id':'bad1111dy','type':'genre'}]}

print("ABOUT TO LOAD")
#graph= ntf.load_example_graph()

# ex_file = open('test_graph_data',"r")
# graph_contents = ex_file.read()
# graph_dict = json.loads(graph_contents)
# ex_file.close()
graph = nx.node_link_graph(data)

#poppy = ntf.filter_popularity(graph,'50')
test2 ={'directed': False, 'multigraph': False, 'graph': {}, 'nodes': [{'birth': 'Maisie Hannah Peters 28 May 2000 Steyning, England', 'died': 'alive', 'type': 'artist', 'id': 'Maisie Peters'}, {'type': 'genre', 'id': 'alt z'}, {'type': 'genre', 'id': 'uk pop'},  {'birth': None, 'died': None,  'type': 'artist', 'id': 'Chappell Roan'}, {'type': 'genre', 'id': 'indie pop'}, {'type': 'genre', 'id': 'springfield mo indie'}], 'links': [{'source': 'Maisie Peters', 'target': 'alt z'}, {'source': 'Maisie Peters', 'target': 'uk pop'}, {'source': 'Chappell Roan', 'target': 'indie pop'}, {'source': 'Chappell Roan', 'target': 'springfield mo indie'}]}
poppy=nx.node_link_graph(test2)
pop=ntf.draw_network(poppy,labels=True,size_v=400).interactive()

graph = nx.node_link_graph(data)
playlist_graph = pn.panel(ntf.draw_network(poppy,labels=True,size_v=400).interactive())
print("OBJECT UPDATED")
##GODDAMN GET RID OF THOSE MFIN LISTS

row1=pn.Row()
title_panel = pn.pane.Markdown('''# Playlist
                               ''')

row1.append(playlist_graph)
print("ADDED MY GRAPH TO ROW 1")
template = pn.template.BootstrapTemplate(
    title='507 Dashboard',
    sidebar=sidecol
)

print("can we get here or no")

template.main.append(title_panel)
print("hmm")
template.main.append(row1)
print("just added row 1")
template.servable()
print("ITS NOT ")

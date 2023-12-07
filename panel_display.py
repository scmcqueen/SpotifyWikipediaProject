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
test2 ={'directed': False, 'multigraph': False, 'graph': {}, 'nodes': [{'type': 'genre', 'id': 'Lia Pappas-Kemps'}, {'type': 'genre', 'id': 'Jensen McRae'}, {'type': 'genre', 'id': 'gen z singer-songwriter'}, {'type': 'genre', 'id': 'Maisie Peters'}, {'type': 'genre', 'id': 'alt z'}, {'type': 'genre', 'id': 'uk pop'}, {'type': 'genre', 'id': 'WATERBEAR'}, {'type': 'genre', 'id': 'Celia'}, {'type': 'genre', 'id': 'Juliana Madrid'}, {'type': 'genre', 'id': 'Chloe Dadd'}, {'type': 'genre', 'id': 'Lauren Juzang'}, {'type': 'genre', 'id': 'ok.danke.tschüss'}, {'type': 'genre', 'id': 'Leanna Firestone'}, {'type': 'genre', 'id': 'Kayla Grace'}, {'type': 'genre', 'id': 'MELE'}, {'type': 'genre', 'id': 'The Beaches'}, {'type': 'genre', 'id': 'toronto indie'}, {'type': 'genre', 'id': 'Blond'}, {'type': 'genre', 'id': 'german indie'}, {'type': 'genre', 'id': 'Power Plush'}, {'type': 'genre', 'id': 'Dilla'}, {'type': 'genre', 'id': 'neue neue deutsche welle'}, {'type': 'genre', 'id': 'NoSo'}, {'type': 'genre', 'id': 'Chappell Roan'}, {'type': 'genre', 'id': 'indie pop'}, {'type': 'genre', 'id': 'springfield mo indie'}, {'type': 'genre', 'id': 'Emei'}, {'type': 'genre', 'id': 'singer-songwriter pop'}, {'type': 'genre', 'id': 'Moira & Claire'}, {'type': 'genre', 'id': 'SOMOH'}, {'type': 'genre', 'id': 'Casey Bishop'}, {'type': 'genre', 'id': 'Straats'}, {'type': 'genre', 'id': 'Ethan Hibbs'}, {'type': 'genre', 'id': 'Boyish'}, {'type': 'genre', 'id': 'Sydney Rose'}, {'type': 'genre', 'id': 'chloe moriondo'}, {'type': 'genre', 'id': 'bedroom pop'}, {'type': 'genre', 'id': 'pov: indie'}, {'type': 'genre', 'id': 'Sophie Truax'}, {'type': 'genre', 'id': 'frown line'}, {'type': 'genre', 'id': 'Vines'}, {'type': 'genre', 'id': 'Ahli'}, {'type': 'genre', 'id': 'Caity Krone'}, {'type': 'genre', 'id': 'Amy Lawton'}, {'type': 'genre', 'id': 'Stevie Bill'}, {'type': 'genre', 'id': 'SKYLAR'}, {'type': 'genre', 'id': 'Eliza Harrison Smith'}, {'type': 'genre', 'id': 'Chase Petra'}, {'type': 'genre', 'id': 'socal indie'}, {'type': 'genre', 'id': 'EASHA'}, {'type': 'genre', 'id': 'Mel Bryant & the Mercy Makers'}, {'type': 'genre', 'id': 'Them Fantasies'}, {'type': 'genre', 'id': 'boston indie'}, {'type': 'genre', 'id': 'Babygirl'}, {'type': 'genre', 'id': 'milk.'}, {'type': 'genre', 'id': 'Annika Kilkenny'}, {'type': 'genre', 'id': 'Good Boy Daisy'}, {'type': 'genre', 'id': 'phoenix indie'}, {'type': 'genre', 'id': 'Haley Blais'}, {'type': 'genre', 'id': 'vancouver indie'}, {'type': 'genre', 'id': 'Willow Avalon'}, {'type': 'genre', 'id': 'Field Medic'}, {'type': 'genre', 'id': 'small room'}, {'type': 'genre', 'id': 'flor'}, {'type': 'genre', 'id': 'hopebeat'}, {'type': 'genre', 'id': 'indie poptimism'}, {'type': 'genre', 'id': 'metropopolis'}, {'type': 'genre', 'id': 'Alt Fiction'}, {'type': 'genre', 'id': 'Jesse Detor'}, {'type': 'genre', 'id': 'Blusher'}, {'type': 'genre', 'id': 'Evan Honer'}, {'type': 'genre', 'id': 'Blondshell'}, {'type': 'genre', 'id': 'bubblegrunge'}, {'type': 'genre', 'id': 'Imani Graham'}, {'type': 'genre', 'id': 'chlothegod'}], 'links': [{'source': 'Jensen McRae', 'target': 'gen z singer-songwriter'}, {'source': 'gen z singer-songwriter', 'target': 'Sydney Rose'}, {'source': 'Maisie Peters', 'target': 'alt z'}, {'source': 'Maisie Peters', 'target': 'uk pop'}, {'source': 'alt z', 'target': 'Leanna Firestone'}, {'source': 'alt z', 'target': 'Emei'}, {'source': 'alt z', 'target': 'chloe moriondo'}, {'source': 'alt z', 'target': 'Imani Graham'}, {'source': 'The Beaches', 'target': 'toronto indie'}, {'source': 'Blond', 'target': 'german indie'}, {'source': 'Dilla', 'target': 'neue neue deutsche welle'}, {'source': 'Chappell Roan', 'target': 'indie pop'}, {'source': 'Chappell Roan', 'target': 'springfield mo indie'}, {'source': 'indie pop', 'target': 'Boyish'}, {'source': 'indie pop', 'target': 'chloe moriondo'}, {'source': 'indie pop', 'target': 'Babygirl'}, {'source': 'indie pop', 'target': 'Haley Blais'}, {'source': 'Emei', 'target': 'singer-songwriter pop'}, {'source': 'chloe moriondo', 'target': 'bedroom pop'}, {'source': 'chloe moriondo', 'target': 'pov: indie'}, {'source': 'Chase Petra', 'target': 'socal indie'}, {'source': 'Them Fantasies', 'target': 'boston indie'}, {'source': 'Good Boy Daisy', 'target': 'phoenix indie'}, {'source': 'Haley Blais', 'target': 'vancouver indie'}, {'source': 'Field Medic', 'target': 'small room'}, {'source': 'flor', 'target': 'hopebeat'}, {'source': 'flor', 'target': 'indie poptimism'}, {'source': 'flor', 'target': 'metropopolis'}, {'source': 'Blondshell', 'target': 'bubblegrunge'}]}
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

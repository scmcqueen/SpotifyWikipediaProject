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
    pass

#load in example data, use these local variables
example_info = ntf.load_example_graph()
graph = example_info[0]
lookup_dict = example_info[1]
title = example_info[2]

#playlist main widget
playlist_graph = pn.panel(ntf.draw_network(graph,labels=False,size_v=400).interactive().properties(height=550,width=550))


#row 1 right col
row1rightcol = pn.Column()

average_pop = ntf.calculate_avg_popularity(lookup_dict)
funny_pop_comment = "Looks like you have good taste."
if average_pop < 40:
    funny_pop_comment = "So clearly you're an ~indie icon~"
if average_pop > 65:
    funny_pop_comment = "Hey no one said being mainstream is a bad thing!"
average_pop_pane = pn.pane.Markdown(f'''### The artists on your playlist have an average popularity of {str(round(average_pop,2))}.
###### {funny_pop_comment}
                                    ''',width=300)

row1rightcol.append(average_pop_pane)


row1=pn.Row()
title_panel = pn.pane.Markdown(f'''# {title}
                               ''')

row1.append(playlist_graph)
row1.append(row1rightcol)


template = pn.template.BootstrapTemplate(
    title='507 Dashboard',
    sidebar=sidecol
)



template.main.append(title_panel)

template.main.append(row1)

template.servable()


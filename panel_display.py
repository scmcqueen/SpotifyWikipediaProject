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
from panel.theme import Material #might mess with this...
import network_functions as ntf

pn.extension('vega')
alt.renderers.enable('default')

# we want to use bootstrap/template, tell Panel to load up what we need
pn.extension(design='bootstrap')

#initialize global variables
graph = None

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
    graph = ntf.parse_playlist(playlist_input.value)
    return None
#bind them!
start_button.on_click(click_start)

template = pn.template.BootstrapTemplate(
    title='Analyze your playlist',
    sidebar=sidecol
)

#set up title 
title_panel = pn.pane.Markdown(f''' # Let's analyze your playlist [PLACEHOLDER]
                               ''')



template.main.append(title_panel)
template.servable()
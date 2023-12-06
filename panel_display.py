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

pn.extension('vega')
alt.renderers.enable('default')

# we want to use bootstrap/template, tell Panel to load up what we need
pn.extension(design='bootstrap')

#Here I will define my left sidecol

sidecol = pn.Column()

welcome_text = pn.pane.Markdown(
    '''
    ## Input a link to a public playlist on Spotify
    ''')

playlist_link_input = pn.widgets.TextInput(name='',placeholder='')
start_button = pn.widgets.Button(name='Start',button_type='primary')

sidecol.append(welcome_text)
sidecol.append(start_button)

template = pn.template.BootstrapTemplate(
    title='Analyze your playlist',
    sidebar=sidecol
)


#template.main.append(sidecol)



template.servable()
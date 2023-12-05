# load up the libraries
import panel as pn
import pandas as pd
import altair as alt
from altair_transform import extract_data
import time,json
import networkx as nx
import traceback
import pygraphviz

pn.extension('vega')
alt.renderers.enable('default')

# we want to use bootstrap/template, tell Panel to load up what we need
pn.extension(design='bootstrap')

template = pn.template.BootstrapTemplate(
    title='Spotify & Wikipedia',
    #sidebar=sidecol
)


template.main.append()



template.servable()
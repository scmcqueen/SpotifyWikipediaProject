
# Spotify & Wikipedia Project

Let's query the artists from a Spotify playlist and filter them based on Wikipedia demographic information.


## Required Packages

import panel as pn
import pandas as pd
import altair as alt
import graph_networkx as gnx
import network_functions as ntf
import json
import requests
import json
import networkx as nx
import urllib.request 
import nx_altair as nxa
import re

## Data Structures

We use a networkx node link graph and a lookup dictionary to filter the artists & genres per playlist. 

- Networkx Node Link Graph
    - Id = Name ('Orla Gartland', 'bubblegrunge', 'LMFAO', 'pop', etc.)
    - Type = 'Artist' or 'Genre'
- Lookup Dictionary
    - Key = Name ('Orla Gartland', 'bubblegrunge', 'LMFAO', 'pop', etc.)
    - Value = Dictionary
        - Birth = full name, date of birth, and birth location ('James Tiberius Kirk, March 22 2223, Riverside Iowa')
        - Death = date of death and location ('San Mateo California, June 17th 2055')
        - Occupation = list of jobs (['captain','entrepreneur','songwriter'])
        - Instruments = list of instruments an artist can play (['piano','saxophone','vocals'])



## Running this Code 
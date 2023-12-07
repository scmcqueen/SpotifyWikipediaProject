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
import urllib.request 
from PIL import Image 


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
artist_genres = ntf.get_genre_artists(graph)
artists_list = artist_genres['artists']
genres_list = artist_genres['genres']

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

popular_artists = ntf.get_most_popular_artist(lookup_dict)
popular_artists_string = ", ".join(popular_artists)
popular_artists_pane = pn.pane.Markdown(f''' ###### The most popular artist on this playlist is {popular_artists_string}.
                                        ''',width=300)
row1rightcol.append(popular_artists_pane)
for item in popular_artists:
    urllib.request.urlretrieve( 
    lookup_dict[item]['img_info'][1]['url'], 
   "cute.png") 
    row1rightcol.append(pn.pane.Image("cute.png",width=lookup_dict[item]['img_info'][1]['width'],height=lookup_dict[item]['img_info'][1]['height']))

#lookup artists
lookup_artist_col = pn.Column()

autocomplete_lookup = pn.widgets.AutocompleteInput(
    name='Look up an artist or genre:', options=(artists_list+genres_list),
    case_sensitive=False, search_strategy='includes',
    placeholder=popular_artists[0])
search_button = pn.widgets.Button(name='Search',button_type='primary')

lookup_artist_col.append(autocomplete_lookup)
lookup_artist_col.append(search_button)

focused_chart_pane = pn.panel(ntf.draw_network(ntf.get_focus_graph(graph,popular_artists[0]),size_v=400).interactive())
lookup_artist_col.append(focused_chart_pane)
searched_image_pane = pn.pane.Image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Black.png",width=250)
lookup_artist_col.append(searched_image_pane)

def update_search(event):
    global searched_image_pane
    new_term = autocomplete_lookup.value
    if new_term not in artists_list and new_term not in genres_list:
        focused_chart_pane.object = ntf.draw_network(ntf.get_focus_graph(graph,popular_artists[0]),size_v=400).interactive().properties(title=f'{new_term} not in your playlist, try again!')
        searched_image_pane = pn.pane.Image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Black.png",width=250)
        return
    focused_chart_pane.object = ntf.draw_network(ntf.get_focus_graph(graph,new_term),size_v=400).interactive()
    if new_term in artists_list:
        urllib.request.urlretrieve(lookup_dict[new_term]['img_info'][1]['url'], "search.png") 
        lookup_artist_col.remove(searched_image_pane)
        searched_image_pane = pn.pane.Image("search.png",width=lookup_dict[new_term]['img_info'][1]['width'],height=lookup_dict[new_term]['img_info'][1]['height'])
        lookup_artist_col.append(searched_image_pane)
    return


search_button.on_click(update_search)


#dead of alive column

dead_or_alive = pn.Column()


#Rows etc
row1=pn.Row()
title_panel = pn.pane.Markdown(f'''# {title}
                               ''')

row1.append(playlist_graph)
row1.append(row1rightcol)
row1.append(lookup_artist_col)

template = pn.template.BootstrapTemplate(
    title='507 Dashboard',
    sidebar=sidecol
)



template.main.append(title_panel)

template.main.append(row1)

template.servable()


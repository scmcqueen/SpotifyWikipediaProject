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
import re


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
    ''',styles={'color': "#CE1483"})


#left hand widgets
start_button = pn.widgets.Button(name='Start',button_type='success',button_style='outline')
playlist_input= pn.widgets.TextInput(name='Playlist link:', placeholder='Skyeler')
wikimedia_username_password_input = pn.widgets.TextInput(name='Wikimedia username & password:', placeholder='username,password')
spotify_username_password_input = pn.widgets.TextInput(name='Spotify id & secret:', placeholder='id,secret')

sidecol.append(welcome_text)
sidecol.append(playlist_input)
sidecol.append(wikimedia_username_password_input)
sidecol.append(spotify_username_password_input)
sidecol.append(start_button)

sidecol.append(pn.pane.Markdown('''#### Or try one of our recommended playlists!
**Top 100 Artists Playlist**
https://open.spotify.com/playlist/0Hm1tCeFv45CJkNeIAtrfF?si=Tg1QrqCwTcqWyIVcIAPjsA&pi=u-2p99hT2OTseU
**Dana's Emo Music**
https://open.spotify.com/playlist/1wzmHWDXTgPQjSzaAMYSr8?si=nAfKLU8XQqyul7GhLw69fw&pt=53a8902253dfa4d789c3d87d6173779c
**The Barbie Soundtrack**
https://open.spotify.com/playlist/4SS7ARjCKiJmtqthv54dAG?si=agryaLlaRMWVSaO0EBCLWg&pi=u-UAcbEZPCQ_S0
**Veganism by Olivia**
https://open.spotify.com/playlist/5kyhuJwtqAlkWCdPiQ1Ltn?si=qn_uKfklQu-qidJX5oZpEA&pi=u-CCYhGueuQQSG      
**Skyeler's Top Songs of 2023**
https://open.spotify.com/playlist/37i9dQZF1Fa3HdyrNWa6vZ?si=oCJikSSSSkuLqPnNWt1A-g&pi=u-1y-ex8nkT9il  
**Samuel's Top Songs of 2023**
https://open.spotify.com/playlist/37i9dQZF1FacGl8FhVmMo5?si=r7i5rTpgQB606g2T4TXuaQ&pi=u-Vl-ofu93TXmp                
                                
                                ''',width=300,styles={'color': "#160F29"}))


template = pn.template.BootstrapTemplate(
    title='Spotify + Wikipedia Playlist Exploration',
    sidebar=sidecol,
    header_background =  "#3772FF"
)

#define function to bind
#example_info = is a preloaded playlist by skyeler!
example_info = ntf.load_example_graph()

graph = example_info[0]
lookup_dict = example_info[1]
title = example_info[2]
artist_genres = ntf.get_genre_artists(graph)
artists_list = artist_genres['artists']
genres_list = artist_genres['genres']

#playlist main widget
playlist_graph = pn.panel(ntf.draw_network(graph,labels=False,size_v=400).interactive().properties(height=700,width=700))


#row 1 right col
row1rightcol = pn.Column(width=500)

average_pop = ntf.calculate_avg_popularity(lookup_dict)
funny_pop_comment = "Looks like you have good taste."
if average_pop < 40:
    funny_pop_comment = "So clearly you're an ~indie icon~"
if average_pop > 65:
    funny_pop_comment = "You only like the *really* good ones!"
average_pop_pane = pn.pane.Markdown(f'''### The artists on your playlist have an average popularity of {str(round(average_pop,2))}.
###### {funny_pop_comment}
                                    ''',width=400,styles={'color': "#CE1483"})

row1rightcol.append(average_pop_pane)

popular_artists = ntf.get_most_popular_artist(lookup_dict)
popular_artists_string = ", ".join(popular_artists)
if len(popular_artists)>1:
    popular_artists_pane = pn.pane.Markdown(f''' ###### The most popular artists on this playlist are {popular_artists_string}.
                                        ''',width=400)
else:
    popular_artists_pane = pn.pane.Markdown(f''' ###### The most popular artist on this playlist is {popular_artists_string}.
                                        ''',width=400)
row1rightcol.append(popular_artists_pane)


urllib.request.urlretrieve( 
lookup_dict[popular_artists[0]]['img_info'][1]['url'], "cute.png") 
photo_col = (pn.pane.Image("cute.png",width=lookup_dict[popular_artists[0]]['img_info'][1]['width'],height=lookup_dict[popular_artists[0]]['img_info'][1]['height']))
row1rightcol.append(photo_col)

#lookup artists
lookup_artist_col = pn.Column(pn.pane.Markdown(''' ### Focus on one artist or genre '''))

autocomplete_lookup = pn.widgets.AutocompleteInput(
    name='Look up an artist or genre:', options=(artists_list+genres_list),
    case_sensitive=False, search_strategy='includes',
    placeholder=popular_artists[0])
search_button = pn.widgets.Button(name='Search',button_type='success',button_style='outline')


lookup_artist_col.append(autocomplete_lookup)
lookup_artist_col.append(search_button)

focused_chart_pane = pn.panel(ntf.draw_network(ntf.get_focus_graph(graph,popular_artists[0]),size_v=400).interactive().properties(width=350,height=300))
lookup_artist_col.append(focused_chart_pane)
searched_image_pane = pn.pane.Image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Black.png",width=250)
lookup_artist_col.append(searched_image_pane)

def update_search(event):
    global searched_image_pane
    new_term = autocomplete_lookup.value
    if new_term not in artists_list and new_term not in genres_list:
        focused_chart_pane.object = ntf.draw_network(ntf.get_focus_graph(graph,popular_artists[0]),size_v=400).interactive().properties(title=f'{new_term} not in your playlist, try again!',width=250,height=250)
        searched_image_pane = pn.pane.Image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Black.png",width=350)
        return
    focused_chart_pane.object = ntf.draw_network(ntf.get_focus_graph(graph,new_term),size_v=400).interactive().properties(width=350,height=300)
    if new_term in artists_list:
        urllib.request.urlretrieve(lookup_dict[new_term]['img_info'][1]['url'], "search.png") 
        lookup_artist_col.remove(searched_image_pane)
        searched_image_pane = pn.pane.Image("search.png",width=lookup_dict[new_term]['img_info'][1]['width'],height=lookup_dict[new_term]['img_info'][1]['height'])
        lookup_artist_col.append(searched_image_pane)
    return


search_button.on_click(update_search)


#dead of alive column
dead_or_alive = pn.Column(pn.pane.Markdown(
    ''' ### Dead artists on your playlist

    based on available wikipedia data
'''
))
dead_pane = pn.panel(ntf.draw_network(ntf.search_dead(graph,lookup_dict)).interactive())

dead_or_alive.append(dead_pane)
dead_or_alive.append(pn.pane.Markdown(
    ''' ### Alive artists on your playlist

    based on available wikipedia data
'''
))

alive_pane = pn.panel(ntf.draw_network(ntf.search_alive(graph,lookup_dict)).interactive())

dead_or_alive.append(alive_pane)

#the second row -- search for path
lookup_path_column = pn.Column(pn.pane.Markdown(''' ### Get from A to Z on your playlist
                                                '''),width=600)

start_lookup = pn.widgets.AutocompleteInput(
    name='Starting point:', options=(artists_list+genres_list),
    case_sensitive=False, search_strategy='includes',
    placeholder='A')
end_lookup = pn.widgets.AutocompleteInput(
    name='Ending point:', options=(artists_list+genres_list),
    case_sensitive=False, search_strategy='includes',
    placeholder='Z')
path_button = pn.widgets.Button(name='Find path',button_type='success',button_style='outline')

path_graph = pn.panel(alt.Chart(pd.DataFrame([''],columns=['Waiting for data...'])).encode(x='Waiting for data...:Q').mark_circle().properties(width=400)) #blank chart

def run_path_lookup(event):
    start = start_lookup.value
    end= end_lookup.value

    new_graph = ntf.get_shortest_graph(graph,start,end)

    if new_graph is None:
        path_graph.object = alt.Chart(pd.DataFrame([''],columns=['No Path Available'])).encode(x='No Path Available:Q').mark_circle().properties(width=400)
        return
    path_graph.object = ntf.draw_network(new_graph,size_v=400).interactive().properties(title=f"Path from {start} to {end}",width=400,height=400)
    return

path_button.on_click(run_path_lookup)

lookup_path_column.append(start_lookup)
lookup_path_column.append(end_lookup)
lookup_path_column.append(path_button)
lookup_path_column.append(path_graph)

##filter popularity 
popularity_filter_col = pn.Column(pn.pane.Markdown(''' ### Filter artists by popularity 
based on Spotify's built-in popularity metric
                                                '''),width=600)
enter_popularity = pn.widgets.EditableIntSlider(name='Popularity',start=0,end=100)
pop_button = pn.widgets.Button(name='Filter!',button_type='success',button_style='outline')
temp = ntf.filter_popularity(graph,65,lookup_dict) # -- keeps throiwng error?
popularity_graph = pn.panel(ntf.draw_network(ntf.filter_popularity(graph,50,lookup_dict),size_v=400).interactive().properties(title=f"Artists with a popularity of 50 or higher",width=400,height=400))

def pop_filter(event):
    popularity_graph.object = ntf.draw_network(ntf.filter_popularity(graph,int(enter_popularity.value),lookup_dict),size_v=400).interactive().properties(title=f"Artists with a popularity of {str(enter_popularity.value)} or higher",width=400,height=400)
    return
pop_button.on_click(pop_filter)

popularity_filter_col.append(enter_popularity)
popularity_filter_col.append(pop_button)
popularity_filter_col.append(popularity_graph)

### search from

where_ya_from = pn.Column(pn.pane.Markdown(''' ### Where did you come from? 
Or when did you come from? Try inputting a place, year, or month to see where and when your artists were born.
''',width=600))
year_or_place_input = pn.widgets.TextInput(name='Enter a place or year:',placeholder='California')
year_or_place_button = pn.widgets.Button(name='Search',button_type='success',button_style='outline')
year_or_place_graph = pn.panel(ntf.draw_network(ntf.search_from(graph,'california',lookup_dict)).interactive().properties(title='Artists who are California girls at heart <3',width=400,height=400))
def search_year_or_place(event):
    term = year_or_place_input.value
    year_or_place_graph.object = ntf.draw_network(ntf.search_from(graph,term,lookup_dict)).interactive().properties(title=f'{term} artists',width=400,height=400)
    return
year_or_place_button.on_click(search_year_or_place)

where_ya_from.append(year_or_place_input)
where_ya_from.append(year_or_place_button)
where_ya_from.append(year_or_place_graph)


## search occupation & instruments
job_and_music_col = pn.Column(pn.pane.Markdown(''' ### Filter by occupations and instrument '''))

occ_and_inst = pn.Row()

instrument_list = ntf.get_all_instruments(lookup_dict)
job_list = ntf.get_all_occupations(lookup_dict)

checkbutton_inst = pn.widgets.RadioButtonGroup(name='Check Button Group', value='all', options=(instrument_list+['all']),orientation='vertical')
checkbutton_occ = pn.widgets.RadioButtonGroup(name='Check Button Group', options=(job_list+['all']), value='a;;', orientation='vertical')
multi_go =pn.widgets.Button(name="Let's go!",button_type='success',button_style='outline')

selection_col1 = pn.Column(multi_go)
selection_col1.append(pn.pane.Markdown('''###### Instruments '''))
selection_col1.append(checkbutton_inst)
selection_col2 = pn.Column(pn.pane.Markdown('''###### Occupations '''))
selection_col2.append(checkbutton_occ)


multiselect_graph_pane = pn.panel(ntf.draw_network(graph).properties(title=f'Click the buttons to filter this graph!',width=400,height=400).interactive())

def multiselect_selection(event):
    newinst = checkbutton_inst.value
    newjob = checkbutton_occ.value

    if newinst=="all":
        innergraph = graph
    else:
        innergraph = ntf.search_instruments(graph,newinst,lookup_dict)
    if newjob=='all':
        multiselect_graph_pane.object=ntf.draw_network(innergraph).interactive().properties(title=f"{newinst}",width=400,height=400)
    else:
        multiselect_graph_pane.object=ntf.draw_network(ntf.search_occupations(innergraph,newjob,lookup_dict)).properties(title=f'{newjob} + {newinst}').interactive().properties(width=400,height=400)
    return

multi_go.on_click(multiselect_selection)
#checkbutton_occ.on_click(multiselect_selection)


occ_and_inst.append(selection_col1)
occ_and_inst.append(selection_col2)
occ_and_inst.append(multiselect_graph_pane)

job_and_music_col.append(occ_and_inst)

##Top genres
genre_col = pn.Column()
genre_chart = pn.panel(ntf.top_genres_bar(graph).properties(title=f"Top Genres in {title}",height=450,width=400).configure_title(fontSize=24))
genre_col.append(genre_chart)

#Rows etc
row1=pn.Row(height=850)
title_panel = pn.pane.Markdown(f'''# **{title}**
                            ''',styles={'color': "#065143"})

row1.append(playlist_graph)
row1.append(row1rightcol)
row1.append(lookup_artist_col)
#row1.append(dead_or_alive)

row2 = pn.Row(height=700)

row2.append(lookup_path_column)
row2.append(popularity_filter_col)
row2.append(where_ya_from)


row3=pn.Row(dead_or_alive)
row3.append(job_and_music_col)
row3.append(genre_col)

template.main.append(title_panel)

template.main.append(row1)
template.main.append(row2)
template.main.append(row3)

wikitoken = None
spotifytoken = None


###################### Define the function to update everything ################
rerun_count =0
def update_everything(event):
    global graph, lookup_dict, title,artist_genres,artists_list,genres_list,  rerun_count, wikitoken, spotifytoken

    wiki_cred = wikimedia_username_password_input.value.split(',')
    spot_cred = spotify_username_password_input.value.split(',')

    rerun_count+=1
    
    link = ntf.parse_playlist(playlist_input.value) 

    try:
        new_info = gnx.createMyGraph(playlist_id=link,wikimedia_token=wikitoken,spotify_token=spotifytoken) 
    except:
        print("generating new token")
        wikitoken = ntf.get_wikimedia_access_token(wiki_cred[0],wiki_cred[1])
        spotifytoken = ntf.get_spotify_token(spot_cred[0],spot_cred[1])
        new_info = gnx.createMyGraph(playlist_id=link,wikimedia_token=wikitoken,spotify_token=spotifytoken) 
    graph = new_info[0]
    lookup_dict = new_info[1]
    title = new_info[2]
    artist_genres = ntf.get_genre_artists(graph)
    artists_list = artist_genres['artists']
    genres_list = artist_genres['genres']   

    #update the title
    title_panel.object = f''' # {title} '''

    #update the big graph
    playlist_graph.object = ntf.draw_network(graph,labels=False,size_v=400).interactive().properties(height=700,width=700)

    #updat popularity pics
    average_pop = ntf.calculate_avg_popularity(lookup_dict)
    funny_pop_comment = "Looks like you have good taste."
    if average_pop < 40:
        funny_pop_comment = "So clearly you're an ~indie icon~"
    if average_pop > 65:
        funny_pop_comment = "You only like the *really* good ones!"
    average_pop_pane.object =f'''### The artists on your playlist have an average popularity of {str(round(average_pop,2))}.
###### {funny_pop_comment}'''

    popular_artists = ntf.get_most_popular_artist(lookup_dict)
    popular_artists_string = ", ".join(popular_artists)
    if len(popular_artists)>1:
        popular_artists_pane.object =f''' ###### The most popular artists on this playlist are {popular_artists_string}.'''
    else:
        popular_artists_pane.object =f''' ###### The most popular artist on this playlist is {popular_artists_string}.'''
    
    

    urllib.request.urlretrieve(lookup_dict[popular_artists[0]]['img_info'][1]['url'], f"new{str(rerun_count)}.png") 
    photo_col.object = f"new{str(rerun_count)}.png"
    photo_col.width = lookup_dict[popular_artists[0]]['img_info'][1]['width']
    photo_col.height = lookup_dict[popular_artists[0]]['img_info'][1]['height']

    #update focus

    autocomplete_lookup.options=(artists_list+genres_list)
    autocomplete_lookup.placeholder=popular_artists[0]

    focused_chart_pane.object = ntf.draw_network(ntf.get_focus_graph(graph,popular_artists[0]),size_v=400).interactive().properties(width=350,height=300)

    searched_image_pane.object = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Black.png"
    searched_image_pane.width = 250

    #update path

    start_lookup.options = (artists_list+genres_list)
    end_lookup.options = (artists_list+genres_list)

    path_graph.object = alt.Chart(pd.DataFrame([''],columns=['Waiting for data...'])).encode(x='Waiting for data...:Q').mark_circle().properties(width=400)

    #update pop filter
    popularity_graph.object = ntf.draw_network(ntf.filter_popularity(graph,50,lookup_dict),size_v=400).interactive().properties(title=f"Artists with a popularity of 50 or higher",width=400,height=400)

    #update where you come from
    year_or_place_graph.object = ntf.draw_network(ntf.search_from(graph,'california',lookup_dict)).interactive().properties(title='Artists who are California girls at heart <3',width=400,height=400)

    #update dead or alive
    dead_pane.object = ntf.draw_network(ntf.search_dead(graph,lookup_dict)).interactive()
    alive_pane.object = ntf.draw_network(ntf.search_alive(graph,lookup_dict)).interactive()

    #update instrument
    instrument_list = ntf.get_all_instruments(lookup_dict)
    job_list = ntf.get_all_occupations(lookup_dict)

    checkbutton_inst.options = (instrument_list+['all'])
    checkbutton_inst.value = 'all'
    
    checkbutton_occ.options = (job_list+['all'])
    checkbutton_occ.value='all'
    

    multiselect_graph_pane.object = ntf.draw_network(graph).properties(title=f'Click the buttons to filter this graph!',width=400,height=400).interactive()
    #update top genre
    genre_chart.object= ntf.top_genres_bar(graph).properties(title=f"Top Genres in {title}",height=450,width=400).configure_title(fontSize=24)
    print(graph)
    return


start_button.on_click(update_everything)


template.servable()


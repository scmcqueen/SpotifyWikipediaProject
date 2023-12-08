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
#example_info = ntf.load_example_graph()

#example_info = gnx.createMyGraph("5kyhuJwtqAlkWCdPiQ1Ltn")
#37i9dQZF1Fa3HdyrNWa6vZ
#37i9dQZF1FacGl8FhVmMo5
example_info = gnx.createMyGraph("37i9dQZF1FacGl8FhVmMo5")

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
                                    ''',width=400)

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
for item in popular_artists:
    urllib.request.urlretrieve( 
    lookup_dict[item]['img_info'][1]['url'], 
   "cute.png") 
    row1rightcol.append(pn.pane.Image("cute.png",width=lookup_dict[item]['img_info'][1]['width'],height=lookup_dict[item]['img_info'][1]['height']))

#lookup artists
lookup_artist_col = pn.Column(pn.pane.Markdown(''' #### Focus on one artist or genre '''))

autocomplete_lookup = pn.widgets.AutocompleteInput(
    name='Look up an artist or genre:', options=(artists_list+genres_list),
    case_sensitive=False, search_strategy='includes',
    placeholder=popular_artists[0])
search_button = pn.widgets.Button(name='Search',button_type='primary')

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
dead_or_alive.append(pn.panel(ntf.draw_network(ntf.search_dead(graph,lookup_dict)).interactive()))
dead_or_alive.append(pn.pane.Markdown(
    ''' ### Alive artists on your playlist

    based on available wikipedia data
'''
))
dead_or_alive.append(pn.panel(ntf.draw_network(ntf.search_alive(graph,lookup_dict)).interactive()))

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
path_button = pn.widgets.Button(name='Find path',button_type='primary')

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
path_button = pn.widgets.Button(name='Filter!',button_type='primary')
temp = ntf.filter_popularity(graph,65,lookup_dict) # -- keeps throiwng error?
popularity_graph = pn.panel(ntf.draw_network(ntf.filter_popularity(graph,50,lookup_dict),size_v=400).interactive().properties(title=f"Artists with a popularity of 50 or higher",width=400,height=400))

def pop_filter(event):
    popularity_graph.object = ntf.draw_network(ntf.filter_popularity(graph,int(enter_popularity.value),lookup_dict),size_v=400).interactive().properties(title=f"Artists with a popularity of {str(enter_popularity.value)} or higher",width=400,height=400)
    return
path_button.on_click(pop_filter)

popularity_filter_col.append(enter_popularity)
popularity_filter_col.append(path_button)
popularity_filter_col.append(popularity_graph)

### search from

where_ya_from = pn.Column(pn.pane.Markdown(''' ### Where did you come from? 
Or when did you come from? Try inputting a place, year, or month to see where and when your artists were born.
''',width=600))
year_or_place_input = pn.widgets.TextInput(name='Enter a place or year:',placeholder='California')
year_or_place_button = pn.widgets.Button(name='Search',button_type='primary')
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

checkbutton_inst = pn.widgets.RadioButtonGroup(name='Check Button Group', value=instrument_list[0], options=(instrument_list+['all']),orientation='vertical')
checkbutton_occ = pn.widgets.RadioButtonGroup(name='Check Button Group', options=(job_list+['all']), value=job_list[0], orientation='vertical')
multi_go =pn.widgets.Button(name="Let's go!",button_type='primary')

selection_col1 = pn.Column(multi_go)
selection_col1.append(pn.pane.Markdown('''###### Instruments '''))
selection_col1.append(checkbutton_inst)
selection_col2 = pn.Column(pn.pane.Markdown('''###### Occupations '''))
selection_col2.append(checkbutton_occ)


multiselect_graph_pane = pn.panel(ntf.draw_network(ntf.search_instruments(ntf.search_occupations(graph,job_list[0],lookup_dict),instrument_list[0],lookup_dict)).properties(title=f'Artists who also {job_list[0]} and play {instrument_list[0]}',width=400,height=400).interactive())

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
genre_col = pn.Column(pn.panel(ntf.top_genres_bar(graph).properties(title=f"Top Genres in {title}",height=450,width=400).configure_title(fontSize=24)))



#Rows etc
row1=pn.Row(height=850)
title_panel = pn.pane.Markdown(f'''# {title}
                               ''')

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

template = pn.template.BootstrapTemplate(
    title='507 Dashboard',
    sidebar=sidecol
)


######## NOTE: could add more -- graph of genres maybe switch with dead and alive? or add all three to botom (dead alive, multisearhc, etc.)


template.main.append(title_panel)

template.main.append(row1)
template.main.append(row2)
template.main.append(row3)

template.servable()


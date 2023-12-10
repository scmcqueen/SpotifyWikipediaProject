
# Spotify & Wikipedia Project

Let's query the artists from a Spotify playlist and filter them based on Wikipedia demographic information.


## Required Python Packages

- panel

- pandas

- altair 

- graph_networkx 

- network_functions 

- json

- requests

- json

- networkx 

- urllib.request 

- nx_altair

- re

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

1. Please download or clone this repo. The png files are non essential.
2. Ensure you have all the necessary packages.
3. Open a terminal window and cd to the where this code is saved.
4. Run this command "panel serve panel_display.py --autoreload --show" and click allow if a pop-up appears. This should open a window in your web browser (chrome works best).
5. Explore the preloaded data! 
    1. **Note for 507 grading team:** If you want to load new data input your Wikipedia API username and password in the format 'username,password' and your Spotify id & secret in the format 'id,secret' along with a Spotify playlist link. **My username,password and id,secret are in my Final Project Report.**
    2. Click Start to load your data! It may take a minute to load the information (my cache mostly has indie music).
6. If you have any questions, please refer to the videos. 

## Next steps 
#### Ideas for me to improve this project after the semester
- Write a git.ignore file so that png files are not synced.
- Find a better way to search for wikipedia pages - for example "https://en.wikipedia.org/wiki/Gunna" does not take you to the artist Gunna's page, even though he has one.
- Make the recommended playlists section more aesthetically pleasing.
- Host this on my website!
- Fix image on top row - sometimes cuts into second row if image size is too large
#Final Project 507
#using Nickmachak's top 100 artists 
#https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks

import wikipediaapi

class Node: 
    '''
    
    '''

    def __init__(self,name):
        self.id = name
        self.neighbors = {} #key is the name of the genre/artist, value is the object
        self.degree =0
        self.type = 'genre'
    
    def calcDegree(self):
        self.degree = len(self.neighbors.keys())
        return(self.degree)

    def addNeighbor(self,nbr):
        if nbr.id not in self.neighbors.keys():
            self.neighbors[nbr.id] = nbr
            self.degree+=1
        if self.id not in nbr.neighbors.keys():
            nbr.neighbors[self.id] = self
            nbr.degree+=1
    def __str__(self):
        return(f"This is {self.id} with {str(self.degree)} neighbors.")

class Artist(Node):
    def __init__(self,name):
        Node.__init__(self,name)
        self.birthCountry = None
        self.birthState = None
        self.deathDate = None
        self.birthDate = None
        self.origin = None
        self.type = "Artist"

        self.occupations = []
        self.instruments = []
    
    def __str__(self):
        return(f"This is the artist {self.id} who makes music in {str(self.degree)} genres.")

class Graph():
    '''
    '''
    def __init__(self) -> None:
        self.vertList = {} #key is id and value is object
        self.numVertices = 0
        self.genres = {} #key is id and value is object
    
    def __str__(self):
        return(f"This graph has {str(len(self.vertList.keys()))} composed of {str(len(self.genres.keys()))} genres and {str(len(self.vertList.keys())-len(self.genres.keys()))} artists.")
    
    def addVertex

##########  testing my Nodes ##########
rock = Node("Rock and Roll")
# print(rock)
# print(rock.type)
country = Node('Country')
# rock.addNeighbor(country)
# print(rock.neighbors)
# print(rock.degree)
# print(country.neighbors)
# print(rock)
# print(country)

####### testing Artist Nodes #####
lilnas = Artist("Lis Nas X")
# lilnas.addNeighbor(country)
# lilnas.addNeighbor(rock)
# print(lilnas)
# print(lilnas.degree)
# print(country.degree)
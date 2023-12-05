#Final Project 507
#using Nickmachak's top 100 artists 
#https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks

import wikipediaapi

class Node: 
    '''
    
    '''

    def __init__(self,name,type='genre'):
        self.id = name
        self.neighbors = {} #key is the name of the genre/artist, value is the object
        self.degree =0
        self.type = type #can be either genre or artists

        #All these will always be null for genres
        self.deathDate = None
        self.birthDate = None
        self.occupations = []
        self.instruments = []
        self.popularity= None
        self.image_info = None
    
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
        self.calcDegree()
        return(f"This is {self.id} with {str(self.degree)} neighbors.")


class Graph():
    '''
    '''
    def __init__(self) -> None:
        self.vertList = {} #key is name and value is object
        self.numVertices = 0
        self.genres = {} #key is name and value is object
    
    def __str__(self):
        return(f"This graph has {str(len(self.vertList.keys()))} composed of {str(len(self.genres.keys()))} genres and {str(len(self.vertList.keys())-len(self.genres.keys()))} artists.")
    
    def addVertex(self,id,type="artist"):
        if "artist" in type.lower():
            if id not in self.vertList.keys():
                self.vertList[id]=Node(id,type)
        else: #genre
            if id not in self.genres.keys():
                new = Node(id,type)
                self.vertList[id]=new
                self.genres[id]=new
    def addEdge(self,id1,type1,id2,type2):
        #check if id1 in
        if id1 not in self.vertList.keys():
            self.vertList[id1]=Node(id1,type1)
            if "genre" in type1.lower():
                self.genres[id1]=self.vertList[id1]
        #check if id2 in 
        if id2 not in self.vertList.keys():
            self.vertList[id2]=Node(id2,type2)
            if "genre" in type2.lower():
                self.genres[id2]=self.vertList[id2]
        #check is id2 is a neighbor of id1 
        if id2 not in self.vertList[id1].neighbors.keys():
            self.vertList[id1].neighbors[id2]=self.vertList[id2]
        #check if id1 is a neighbor of id2
        if id1 not in self.vertList[id2].neighbors.keys():
            self.vertList[id2].neighbors[id1]=self.vertList[id1]


##########  testing my Nodes ##########
rock = Node("Rock and Roll","genre")

country = Node('Country','genre')
Nas = Node('Nas',"artist")

Nas.addNeighbor(rock)
Nas.addNeighbor(country)

#print(Nas.degree)

graph = Graph()
graph.addEdge('Taylor Swift','artist','Country','genre')
graph.addEdge('Taylor Swift','artist','Pop','genre')

# rock.addNeighbor(country)
# print(rock.neighbors)
# print(rock.degree)
# print(country.neighbors)
# print(rock)
# print(country)

import network_functions as ntf
import networkx as nx 
import json 

example = ntf.load_example_graph()
print(f'Here is the example graph: {example[0]}')
print(f'Here are the example nodes: {example[0].nodes}')
print(f'Here is an example node: {example[0].nodes["Maisie Peters"]}')
print(f'Here are the example edges: {example[0].edges}')
print('----------------------------------')
print(f'Here is the example lookupdict: {example[1]}')
print('----------------------------------')
print(f'Here is the example playlist title: {example[2]}')
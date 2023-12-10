import network_functions as ntf
import networkx as nx 
import json 

def load_example_graph(graph_name='test_graph_data',dict_name='test_lookup_data',name="Currently by skyelermcquill"):
    '''
    Loads a networkx graph from a json file with a node-link graph data. 

    Returns a networkx graph! This function was made to save a step from loading API data. 

    PARAMETERS
    ----------
    graph_name: str
        the name of the json file you want to load with graph data
    dict_name: str
        the name of the json file you want to load with lookup dict data
    name: str
        name of the playlist you're loading

    RETURNS
    -------
    list: [networkx graph, dict]
        a node link graph objects
    '''
    ex_file = open(graph_name,"r")
    graph_contents = ex_file.read()
    graph_dict = json.loads(graph_contents)
    ex_file.close()

    dict_file = open(dict_name,"r")
    lookup_cont = dict_file.read()
    lookup = json.loads(lookup_cont)
    dict_file.close()
    return [nx.node_link_graph(graph_dict),lookup,name]

example = ntf.load_example_graph()
print(f'Here is the example graph: {example[0]}')
print(f'Here are the example nodes: {example[0].nodes}')
print(f'Here is an example node: {example[0].nodes["Maisie Peters"]}')
print(f'Here are the example edges: {example[0].edges}')
print('----------------------------------')
print(f'Here is the example lookupdict: {example[1]}')
print('----------------------------------')
print(f'Here is the example playlist title: {example[2]}')
from src.algorithms.intent_network import *
import re
import networkx as nx

def parser(text):

    intent_g = nx.Graph()

    subnets = re.findall(re.compile(r'[[](.*?)[]]', re.S),text)
    subnet_names = subnets[0].split(", ")


    for subnet_name in subnet_names:
        intent_g.add_node(subnet_name)



    reaches = re.findall(re.compile(r'[(](.*?)[)]', re.S),text)
    for item in reaches:
        reachability = item.split(", ")
        intent_g.add_edge(reachability[0],reachability[1])

    pos = nx.spring_layout(intent_g)
    #print(pos)

    return pos

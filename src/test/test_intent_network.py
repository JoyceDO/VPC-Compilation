from src.defs.intents import *
from src.algorithms.intent_network import *
import networkx as nx
import matplotlib.pyplot as plt
import csv

def generate_intent_network_test1(intent_Graph,intsubnetid_to_subnet):
    '''
    int_nw = IntentNetwork()

    G = nx.random_geometric_graph(100, 0.325)

    #G = nx.erdos_renyi_graph(50, 0.075)
    print(len(G.edges()))


    ernode_to_subnet={}
    for node in G.nodes():
        obj = int_nw.add_subnet(host_number=5)
        ernode_to_subnet[node] = obj
        intsubnetid_to_subnet[obj.id] = node
        intent_Graph.add_node(node)

    for edge in G.edges():
        int_nw.add_intent_reachability(ernode_to_subnet[edge[0]],ernode_to_subnet[edge[1]])
        intent_Graph.add_edge(edge[0], edge[1])



    return int_nw
    '''
    int_nw = IntentNetwork()

    subnet_to_intsubnet = {}

    subnets = []
    connect = []
    columnb = []
    columnc = []
    with open('../subnet2subnetIntent.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0] == "PolicyType.Reachability":
                connect.append([row[1], row[2]])
            if row[0] != "type" and row[3] == "0":
                columnb.append(row[1])
                columnc.append(row[2])

    for i in range(0, len(columnb)):
        if columnb[i] not in subnets:
            subnets.append(columnb[i])

    for i in range(0, len(columnc)):
        if columnc[i] not in subnets:
            subnets.append(columnc[i])

    for subnet in subnets:
        obj = int_nw.add_subnet(host_number=5)
        subnet_to_intsubnet[subnet] = obj
        intsubnetid_to_subnet[obj.id] = subnet

    for con in connect:
        int_nw.add_intent_reachability(subnet_to_intsubnet[con[0]], subnet_to_intsubnet[con[1]])

    return int_nw

def generate_intent_network_test2(intent_Graph,intsubnetid_to_subnet):

    int_nw = IntentNetwork()

    G = nx.random_geometric_graph(50,0.2)

    #G = nx.erdos_renyi_graph(50, 0.075)
    #print(len(G.edges()))


    ernode_to_subnet={}
    for node in G.nodes():
        obj = int_nw.add_subnet(host_number=5)
        ernode_to_subnet[node] = obj
        intsubnetid_to_subnet[obj.id] = node
        intent_Graph.add_node(node)

    for edge in G.edges():
        int_nw.add_intent_reachability(ernode_to_subnet[edge[0]],ernode_to_subnet[edge[1]])
        int_nw.add_intent_reachability(ernode_to_subnet[edge[1]], ernode_to_subnet[edge[0]])
        intent_Graph.add_edge(edge[0], edge[1])



    return int_nw
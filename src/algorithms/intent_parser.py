from src.algorithms.intent_network import *
import csv
import re


def from_dataset():
    int_nw = IntentNetwork()
    subnet_to_intsubnet = {}

    csvFile = open("dataset/subnet.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        #print(item)
        obj = int_nw.add_subnet(host_number=5,name = item[0])
        subnet_to_intsubnet[item[0]] = obj

    csvFile = open("dataset/reachability.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        #print(item)
        int_nw.add_intent_reachability(subnet_to_intsubnet[item[0]], subnet_to_intsubnet[item[1]])

    return int_nw


def from_text_to_intnw(text,intent_Graph,intsubnetid_to_subnet):

    int_nw = IntentNetwork()
    subnet_to_intsubnet = {}

    subnets = re.findall(re.compile(r'[[](.*?)[]]', re.S),text)
    subnet_names = subnets[0].split(", ")
    #print(subnet_names)
    for subnet_name in subnet_names:
        obj = int_nw.add_subnet(host_number=5, name=subnet_name)
        subnet_to_intsubnet[subnet_name] = obj
        intsubnetid_to_subnet[obj.id] = subnet_name
        intent_Graph.add_node(subnet_name)
    #print(subnet_to_intsubnet)

    reaches = re.findall(re.compile(r'[(](.*?)[)]', re.S),text)

    for item in reaches:
        reachability = item.split(", ")
        int_nw.add_intent_reachability(subnet_to_intsubnet[reachability[0]], subnet_to_intsubnet[reachability[1]])
        intent_Graph.add_edge(reachability[0], reachability[1])

    return int_nw

from src.algorithms.intent_network import *
import re
import csv

def parser_to_csv(text):

    subnets = re.findall(re.compile(r'[[](.*?)[]]', re.S),text)
    subnet_names = subnets[0].split(", ")

    with open("dataset/subnet.csv", "w",newline="") as csvfile:
        writer = csv.writer(csvfile)
        for subnet_name in subnet_names:
            writer.writerow([subnet_name])


    reaches = re.findall(re.compile(r'[(](.*?)[)]', re.S),text)
    with open("dataset/reachability.csv", "w",newline="") as csvfile:
        writer = csv.writer(csvfile)
        for item in reaches:
            reachability = item.split(", ")
            writer.writerow([reachability[0],reachability[1]])

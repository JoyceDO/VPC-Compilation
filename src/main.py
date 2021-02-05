from algorithms.intent_network import *
from algorithms.vpc_network import *
from utils.cidr import *
from src.test.test_intent_network import *
from algorithms.converter import *
from algorithms.converter1 import *
from algorithms.intent_parser import *
from interface.parser import *
from interface.parser_to_csv import *
from algorithms.converter2 import *
from algorithms.converter3 import *
from algorithms.converter4 import *
from algorithms.converter5 import *
from algorithms.converter6 import *
from algorithms.converter7 import *
from algorithms.converter8 import *
import time
import networkx as nx
import matplotlib.pyplot as plt


def main():
     #int_nw = generate_intent_network_test1()
     #start = time.perf_counter()
     #converter1 = Converter1()
     #converter1.convert_intent_network(int_nw)
     #end = time.perf_counter()
     #print('Running time: %s Seconds' % (end - start))
     '''
     with open("G:/华为项目/演示.txt", "r") as subnet_file:
         text = subnet_file.read()
     #print(text)


     intent_Graph = nx.Graph()
     intsubnetid_to_subnet = {}

     int_nw = from_text_to_intnw(text, intent_Graph,intsubnetid_to_subnet)

     pos = nx.spring_layout(intent_Graph)
     nx.draw_networkx_nodes(intent_Graph, pos, node_color='w')
     nx.draw_networkx_edges(intent_Graph, pos, alpha=0.4, edge_color='g')
     nx.draw_networkx_labels(intent_Graph, pos, font_size=10, font_family="sans-serif")
     plt.show()

     converter1 = Converter1()
     converter1.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     pass
     '''
    # vpc_nw = VPCNetwork()
    # vpc_nw.trans_intent_network(int_nw)
    #parser_to_csv("# subnet count [p1, p2, p3]  reachablitity(p1, p2)reachablitity(p3, p1)")
    # int_nw = from_dataset()
    # converter = Converter()
    # converter.convert_intent_network(int_nw)



    # print(converter1.distribution)
    # print(converter1.subnets)
    # print(converter1.data)

    # print(converter)
    # print(converter1)
    # print(vpc_nw)

     intent_Graph = nx.Graph()
     intsubnetid_to_subnet = {}

     int_nw = generate_intent_network_test1(intent_Graph, intsubnetid_to_subnet)

     pos = nx.spring_layout(intent_Graph)

     converter6 = Converter6()
     time_start6 = time.time()
     converter6.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end6 = time.time()
     print('totally cost', time_end6 - time_start6)

     converter7 = Converter7()
     time_start7 = time.time()
     converter7.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end7 = time.time()
     print('totally cost', time_end7 - time_start7)
     
     
     converter8 = Converter8()
     time_start8 = time.time()
     converter8.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end8 = time.time()
     print('totally cost', time_end8 - time_start8)


     '''
     intent_Graph = nx.Graph()
     intsubnetid_to_subnet = {}

     int_nw = generate_intent_network_test2(intent_Graph, intsubnetid_to_subnet)

     pos = nx.spring_layout(intent_Graph)

     converter5 = Converter5()
     time_start5 = time.time()
     converter5.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end5 = time.time()
     print('totally cost', time_end5 - time_start5)
     '''


     '''
     nx.draw_networkx_nodes(intent_Graph, pos, node_color='w',node_size= 20)
     nx.draw_networkx_edges(intent_Graph, pos, alpha=0.4, edge_color='g')
     #nx.draw_networkx_labels(intent_Graph, pos, font_size=10, font_family="sans-serif")
     plt.show()
     '''

     '''
     converter = Converter()
     time_start = time.time()
     converter.convert_intent_network(int_nw, intent_Graph, intsubnetid_to_subnet, pos)
     time_end = time.time()
     print('totally cost', time_end - time_start)


     converter1 = Converter1()
     time_start1 = time.time()
     converter1.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end1 = time.time()
     print('totally cost', time_end1 - time_start1)
     '''
     '''
     converter3 = Converter3()
     time_start = time.time()
     converter3.convert_intent_network(int_nw, intent_Graph, intsubnetid_to_subnet, pos)
     time_end = time.time()
     print('totally cost', time_end - time_start)

     converter5 = Converter5()
     time_start5 = time.time()
     converter5.convert_intent_network(int_nw, intent_Graph, intsubnetid_to_subnet, pos)
     time_end5 = time.time()
     print('totally cost', time_end5 - time_start5)

     converter1 = Converter1()
     time_start1 = time.time()
     converter1.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end1 = time.time()
     print('totally cost', time_end1 - time_start1)
     '''

     '''
     converter2 = Converter2()
     time_start2 = time.time()
     converter2.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end2 = time.time()
     print('totally cost', time_end2 - time_start2)
     '''

     '''
     converter2 = Converter2()
     time_start2 = time.time()
     converter2.convert_intent_network(int_nw, intent_Graph,intsubnetid_to_subnet,pos)
     time_end2 = time.time()
     print('totally cost', time_end2 - time_start2)
     '''
     
     '''
     converter4 = Converter4()
     time_start4 = time.time()
     converter4.convert_intent_network(int_nw, intent_Graph, intsubnetid_to_subnet, pos)
     time_end4 = time.time()
     print('totally cost', time_end4 - time_start4)
     '''
     pass



if __name__ == "__main__":
    main()
    pass

from algorithms.intent_network import *
from algorithms.vpc_network import *
from utils.cidr import *
from src.test.test_intent_network import *
from algorithms.converter import *
from algorithms.converter1 import *
from algorithms.intent_parser import *
from interface.parser_to_csv import *


def distributor(text):
    #parser_to_csv(text)

    #int_nw = from_dataset()
    #converter = Converter()
    #converter.convert_intent_network(int_nw)
    int_nw = from_text_to_intnw(text)
    converter1 = Converter1()
    converter1.convert_intent_network(int_nw)

    return converter1
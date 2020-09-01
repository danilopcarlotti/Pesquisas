from collections import Counter
from math import log2

def entropy_calculator(list_items):
    counter_l = Counter(list_items)
    result = 0
    for _,v in counter_l.items():
        result += (v/len(list_items))*log2(v/len(list_items))
    return -1*result
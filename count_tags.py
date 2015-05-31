#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This program is used to find the different kind of tags present in 'new_delhi.osm'
Since the file is large, it is processed in an iterative manner
"""
import xml.etree.ElementTree as ET
import pprint

# function count_tags counts the number of times each tag is present in the input file
def count_tags(filename):
    
    tags = {} # tags will hold the final output
    
    # Since the input file may be very large, an iterative parser is used to parse the file
    for event,element in ET.iterparse(filename):
        
        if element.tag in tags: # if tag is already present increment its counter by 1
            tags[element.tag] = tags[element.tag] + 1
        else:                   # else create a new key in the 'tags' dictionary and initialize its counter to 1
            tags[element.tag] = 1
    return tags


def test():

    tags = count_tags('new_delhi.osm')
    pprint.pprint(tags)    

if __name__ == "__main__":
    test()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
In this program we wrangle the data and change the shape of each element as in last 
exercise of chapter 6. The reshping is done in shape_element() function

Also all the abbreviations found have been removed using the update_name() function

The abbreviations that have been removed are listed in the 'mapping' dictionary
"""

# Regular expression to check for existence of problematic charcaters
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# The keys in following dictionary represents some of the abbreviations present
# in the 'new_delhi.osm' dataset. The value corresponding to the keys is the correction
# applied so that such abbreviation are removed
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Sec": "Sector",
            "cantt":"cantonment",
            "h/no": "House Number",
            "opp":  "Opposite",
            "Poket":"Pocket"
            }


 # function update_name() removes the over abbreviation present in addresses        
def update_name(name):
    
    # name is the input string value
    updated_name = name
    
    # name will be compared against all possible abbreviations (defined in mapping)
    # If any abbreviation is found then it will be replaced by the non abbreviated value
    for keys in mapping:
        pos =  updated_name.find(keys)
        if pos>=0:
            updated_name = updated_name[:pos]+mapping[keys]+updated_name[pos+len(keys):]
    return updated_name
    

# function shape_element() reshapes 'element' into an intuitve data model chosen in an earlier exercise
def shape_element(element):
    # node will hold the reshaped data_element
    node = {}
    #global count
    
    # We need to process only 'node' and 'way' tags, Following check ensures that
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        
        #count = count +1
        
        # 'id', 'type', 'visible' attributes do not require any reshaping. So they are updated normally
        node["id"] = element.attrib["id"]
        node["type"] = element.tag
        if "visible" in element.attrib:
            node["visible"] = element.attrib["visible"]
            
        # not all tags will have the "addr:street" value
        # So we create an empty address dictionary and initialize its count to 0
        # If any address entry is found later it will be reshaped appropriately and the count will be updated
        # Finally if the address_count is non zero, address will be added to 'node'
        address = {}
        address_count = 0
        
        # not all tags will have the "nd" value
        # So we create an empty nd_refs list and initialize its count to 0
        # If any nd entry is found later it will be reshaped appropriately and the count will be updated
        # Finally if the nd_refs_count is non zero, nd_refs will be added to 'node'
        nd_refs = []
        nd_refs_count = 0;
        
        # following loop will ensure that all sub-tags are processed 
        for tag in element.iter():
            
            # if the tag value is 'node' or 'way', then reshaping happens as per the guidelines given above
            # information related to the user are captured and added to node under "created" key
            if element.tag == "node" or element.tag == "way" :
                create_dict = {}
                create_dict["uid"] = element.attrib["uid"]
                create_dict["user"] = element.attrib["user"]
                create_dict["timestamp"] = element.attrib["timestamp"]
                create_dict["changeset"] = element.attrib["changeset"]
                create_dict["version"] = element.attrib["version"]
                node["created"] = create_dict
            
            # The tag value is node
            # information related to the psoition are captured and added to node under "pos" key
            if element.tag == "node":
                pos_value = []
                pos_value.append(float(element.attrib["lat"]))
                pos_value.append(float(element.attrib["lon"]))
                node["pos"] = pos_value
            
            # The tag value is nd
            # the value under 'nd' is captured and appended to nd_refs list
            # nd_refs_count is also updated
            if tag.tag == "nd":
                nd_refs.append(tag.attrib["ref"])
                nd_refs_count += 1
            
            # The tag value is 'tag'
            # the value under 'tag' is captured and processed according to guidelines above
            if tag.tag == "tag":
                value = tag.attrib["k"]              
               
                # the tag value is not added if it contains problematic characters
                if problemchars.search(value):
                    continue
                # if the number of ':' is more than 1, then this tag is ignored
                elif value.count(':') > 1:
                    continue
                elif tag.attrib["k"] == "type":
                    node["special_type"] = tag.attrib["v"]                    
                # if tag value begins with "addr", then the address dictionary is updated
                # address_count is also increased by 1
                elif value.find("addr:") == 0:
                    pos_adress = value.find(":")
                    value_address = value[pos_adress+1:len(value)]
                    updated_name = update_name(tag.attrib["v"])
                    address[value_address] = updated_name
                    address_count += 1
                # in all the other cases the values are updated by using the 'k' value as key and 'v' value as attribute
                elif value.count(':') == 1:
                    node[tag.attrib["k"]] = tag.attrib["v"]
                else:
                    node[tag.attrib["k"]] = tag.attrib["v"]
                    
        # if address_count is greater than 0, node is updated with the "address" entry        
        if address_count > 0:
            node["address"] = address
        
        # if nd_refs_count is greater than 0, node is updated with the "nd_refs" entry 
        if nd_refs_count > 0:
            node["node_refs"] = nd_refs
        
        if not(node["type"]=="way" or node["type"]=="node"):
            print node["type"]
        return node
    # if element.tag is neither 'node' nor 'way', 'None' is returned
    else:
        return None

# function process_map() processes 'new_delhi.osm' in an iterative manner
# Inside it shape_element() is called that creates the data model to be stored 
# in 'new_delhi.osm.json' 
def process_map(file_in, pretty = False):    
    file_out = "{0}.json".format(file_in)
    data = []     
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)               
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__": 
    data = process_map('new_delhi.osm', False)
  
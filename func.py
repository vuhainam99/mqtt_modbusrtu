import json
# from rio4220 import *

def Get_device(point):
    name = point['name']
    add = point['add']
    funcode = point['funcode']
    size = point['size']
    return 1


def Set_device(point,value):
    name = point['name']
    add = point['add']
    funcode = point['funcode']
    size = point['size']
    return 2 


def Get_map():
    data_map = open("/Users/vuhainam/Desktop/map.json", "r").read()
    json_map = json.loads(data_map)
    data_att = open("/Users/vuhainam/Desktop/attributes.txt", "r").read()
    json_att = json.loads(data_att)
    ls_json = []
    for attri in json_att['attributes']:
        for dic in json_map:
            if dic['name'] == attri['name']:
                ls_json.append(dic)
    
    return ls_json


import bpy
import os
import csv


def get_file_path(file_name):
    '''Get filepath'''
    file_path = os.path.join(os.path.dirname(__file__), "..", file_name)
    return file_path


def read_csv(file_path):
    '''Read CSV data'''
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def csv_column(data, col):
    '''Parse CSV data by index as array'''
    array = []
    for y, row in enumerate(data):
        if y == 0:
            continue
        array.append(row[col])
    return array


def trigger_update():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    

def add_attribute(obj, attr_name, type="FLOAT", domain="POINT"):
    attr = obj.data.attributes.new(attr_name, type, domain)
    return attr



#=====================================================================#
#=====================================================================#
#=====================================================================#
#=====================================================================#



#read the csv
#file_name = "UK_september_sales.csv" #555 entries
file_name = "price_pc_lat_lon.csv" #19,824 entries
#file_name = "full_price_list.csv" #131,070 entries

data = read_csv(get_file_path(file_name))

price = csv_column(data, 0)
latitude = csv_column(data, 2)
longitude = csv_column(data, 3)



#we have an object
obj = bpy.context.active_object

geo_nodes = obj.modifiers.new("make_vertices", "NODES")
geo_nodes.node_group = bpy.data.node_groups['make_vertices']

#set the number of vertices
geo_nodes["Input_2"] = len(price)

trigger_update()

#apply modifier
bpy.ops.object.modifier_apply(modifier=geo_nodes.name)


price_seq = []
for i in range(len(price)):
    price_seq.append(int(price[i]))

#store the prices onto the points (integer)
#create a new attribute
attr = add_attribute(obj, "Price", "INT")

#write the csv data into that attribute
attr.data.foreach_set('value', price_seq)


#storing the coordinates (lat and long) onto the points
coordinates = []
for i in range(len(price)):
    coordinates.append(float(latitude[i]))
    coordinates.append(float(longitude[i]))
    coordinates.append(0)

#create a new attribute
attr = add_attribute(obj, "Coordinates", "FLOAT_VECTOR")

#write the csv data into that attribute
attr.data.foreach_set('vector', coordinates)


geo_nodes = obj.modifiers.new("map", "NODES")
geo_nodes.node_group = bpy.data.node_groups['map']
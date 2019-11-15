# 
# This program read gps points (UTM coordinates) from file
# put all the points from the same trip id in a tuple
# and then create a Polyline of the sequence of the points 
# which is then added in a Folium map object
# That map is saved in a html file that user can open 
# from a Browser
#
# created on 14.11.2019

import folium
import os
import webbrowser
from pyproj import Proj, transform
from random import randrange
# here you can put the labels
#labels=[]

filepath = 'file:///home/stgr/eclipse-workspace/Folium_Examples/'
map_filename = 'map.html'
traj_file = 'tracks_test.csv'
#traj_file = '/home/stgr/Desktop/tracks.csv'
clr_options = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

# The default tiles are set to OpenStreetMap,
# but Stamen Terrain, Stamen Toner, Mapbox Bright, and Mapbox Control Room, and many others tiles are built in.
m = folium.Map(
   
    location=[52.399784, 9.73569699999], # you can give the junction center
    tiles='OpenstreetMap',
    zoom_start= 16
)

inProj = Proj(init='epsg:32632')
outProj = Proj(init='epsg:4326')
num_traj = 0
trip_file = open(traj_file, 'r')
lines = trip_file.readlines()
prev_trip = "null"
points = ()
#read the trajectory points
for line_index in lines[1 :]:
    cur_line = line_index.split(',')
    trip_id = int(cur_line[2])
    #print trip_id
    if trip_id == prev_trip:
        northUTM  = float(cur_line[7]) 
        eastUTM  = float(cur_line[8]) 
        #print "read", northUTM, eastUTM
        lon,lat = transform(inProj,outProj, eastUTM, northUTM)
        #print lon, lat
        prev_trip = trip_id
        points = points + ((lat, lon),)
    else: # new trajectory/trip
        if prev_trip != "null": 
            #print points
            # I colored randomly the trajectories. If you put the labels in the label[] list then 
            # modify the randrange() with the next commented line
            folium.PolyLine(points, color=clr_options[randrange(11)], weight=2.5, opacity=1).add_to(m)
            #folium.PolyLine(points, color=clr_options[label[traj_num]], weight=2.5, opacity=1).add_to(m)
            m.save(map_filename)
            num_traj = num_traj + 1


        points =()
        prev_trip = trip_id
        northUTM  = float(cur_line[7]) 
        eastUTM  = float(cur_line[8]) 
        #print "read", northUTM, eastUTM
        lon,lat = transform(inProj,outProj, eastUTM, northUTM)
        points = points + ((lat, lon),)
        #print lon, lat
print "Program Ended"


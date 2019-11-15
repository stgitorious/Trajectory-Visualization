# 
# This program read gps points (UTM coordinates) from a file
# and then create Polylines (trajectory geometries) that then are exported as
# shapefile, to be viewed afterawards from QGIS.
#
# created on 15.11.2019
 
import shapefile
from pyproj import Proj, transform
inProj = Proj(init='epsg:32632')
outProj = Proj(init='epsg:4326')


# Suppose this is the list of your labels [trip_id, class]
# Make the output of the classification to have the form of a list
# just like the example here
label_list = [[818, 0], [831, 1], [819,5], [822, 6], [832,4], [859,10], [865,11]]
traj_ids = []
# Create a list with the trip_ids
for i in range (0, len(label_list)):
    traj_ids = traj_ids + [label_list[i][0]]
print traj_ids    

traj_file = 'tracks_test.csv'
#traj_file = '/home/stgr/Desktop/tracks.csv'

# create a POLYLINE shapefile object
Traj_shp = shapefile.Writer(shapefile.POLYLINE)
# for every record there must be a corresponding geometry.
Traj_shp.autoBalance = 1

# Create featured for the shapefile shapefile
Traj_shp.field("trip_id", "N") # N: integer field
Traj_shp.field("pred_class", "N") # for the predicted class of the classifier
Traj_shp.field("field", "C") # character type field

num_traj = 0
trip_file = open(traj_file, 'r')
lines = trip_file.readlines()
prev_trip = "null"
points = []
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
        prev_trip = trip_id
        points = points + [[lon, lat],]
    else: # new trajectory/trip
        if prev_trip != "null": 
            #print points
            num_traj = num_traj + 1
            #Traj_shp.poly(parts=[[[1,3],[5,3]]], shapeType=shapefile.POLYLINE)
            print "Create Polyline for trip_id: ", trip_id
            a = traj_ids.index(trip_id)
            if a != None : # you pass the class value to shapefile too!
               pred_class = label_list[a][1]
            else :
                print "Error"   
            Traj_shp.line(parts=[points]) # Create the geometery of the trajectory
            Traj_shp.record(trip_id, pred_class, "") # Write the reatures to the shapefile object

        points =[]
        prev_trip = trip_id
        northUTM  = float(cur_line[7]) 
        eastUTM  = float(cur_line[8]) 
        lon,lat = transform(inProj,outProj, eastUTM, northUTM)
        points = points + [[lon, lat],]

trip_file.close()
Traj_shp.save("./output/line"+".shp") # Save all the trajectories in the shapefile object
print "Shapefile exported!"




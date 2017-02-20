#worksites.py

#purpose extracts worksite json into gis format

#import modukes
import json, urllib.request
##import arcpy

#make the pointArray
def makePolygon(pointArray):
    n = 0
    pts = []
    while n < len(pointArray):
        longitude = pointArray[n]
        latitude = pointArray[n + 1]
##        pt = arcpy.Point(X = longitude, Y = latitude)
##        pts.append(pt)
        n += 2
##    return polygon = arcpy.Polygon(inputs = pts)
    polygon = pts #arcpy.Polygon(pts)
    return polygon
        

#parameters
worksiteUrl = r'c:/apps/leaflet/data/worksite.json'
fs = open("c:/temp/worksite.txt","w")

#banner
print('***\nExport worksites.json\n')

with open(worksiteUrl) as jsonData:
    responses = json.load(jsonData)

#process Responses
rows = []
n = 1
for response in responses["data"]:
    f = fs.write(str(n)  + "\n")
    row = []
    row.append(response["attributes"]["name"]) #0
    row.append(response["attributes"]["address"]) #1
    row.append(response["attributes"]["company"]["name"]) #2
    row.append(response["attributes"]["startDate"]) #3
    row.append(response["attributes"]["endDate"]) #4
    row.append(response["attributes"]["worksiteType"]) #5
    row.append(response["attributes"]["worksiteCode"]) #6
    row.append(response["attributes"]["location"]["coordinates"]) #7
    rows.append(tuple(row))
    f = fs.write("Name\t" + str(response["attributes"]["name"]) + "\n")
    f = fs.write("Company Addres\t" + str(response["attributes"]["address"]) + "\n")
    f = fs.write("Company Name\t" + str(response["attributes"]["company"]["name"]) + "\n")
    f = fs.write("Start date\t" + str(response["attributes"]["startDate"]) + "\n")
    f = fs.write("End date\t" + str(response["attributes"]["endDate"]) + "\n")
    f = fs.write("Worksite Type\t" + str(response["attributes"]["worksiteType"]) + "\n")
    f = fs.write("Worksite Code\t" + str(response["attributes"]["worksiteCode"]) + "\n")
    f = fs.write("")
##    polygon = makePolygon(str(response["attributes"]["location"]["coordinates"]).replace("[","").replace("]","").replace(" ","").split(","))
    n += 1


#cleanUp
fs.close()
del responses

#completes
print('\ncompleted')

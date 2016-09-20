#disconnectArcSDEProcesses.py

#Purpose:
#This script gets rid of schema locking. It is designed to run each night to clear out
#orphaned connections.

#Author: Susan Jones
#Created: 29 March 2016
#Modified: 30 March 2016

#Dependency modules;
#   arcpy

#Dependency files and folders:
#   \\atalgisau01\ADMIN\Maintenance\connections

#import Modules
import arcpy, string, datetime

#start Time
start = datetime.datetime.now()

#banner
print "*******************************\nDisconnect All AreSDE Processes\n\nSusan Jones\n30 March 2016\n*******************************\n"

#todo: build up connection list
connList = []
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@AC@atalgissdbp01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@AC@atalgissdbu01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@AT@atalgissdbp01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@AT@atalgissdbu01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@EXT@atalgissdbp01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@EXT@atalgissdbu01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@AT_EXT@atalgissdbu01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@GIS@atalgissdbp01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@GIS@atalgissdbu01.sde")
connList.append(r"\\atalgisau01\ADMIN\Maintenance\connections\sde@POC@atalgissdbu01.sde")

#todo: set the users to Exclude
print "\nUsers to Exclude:"
usernames = ['SDE','"TRANSPORT\\SVC_ARCGIS"']
for user in usernames:
    print user

#todo: Cycle through each ArcSDE Database and remove the connections
for conn in connList:

    #set the sde workspace
    print "\nCycle " + conn
    gdb = conn

    #todo: Cycle through the users hitting the ArcSDE Databases
    users = arcpy.ListUsers(sde_workspace = gdb)
    for user in users:

        #todo: disconnect the user if not in the exclusion list
        if user.Name not in usernames:
            
            arcpy.DisconnectUser(sde_workspace = gdb, users = user.ID)
            print user
            status = user
            

#end Time
end = datetime.datetime.now()

#todo: process completed successfully
print "\nElapsed Time:\t" + str((end - start).seconds) + " seconds"
print "\nProcess completed successfully"


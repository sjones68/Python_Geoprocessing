#loadCRMRapidResponse.py

#Purpose:
#Loading Enterprise Data Warehouse Rapid Response CRM into ArcSDE Featureclasses

#Tasks
#1 - Create The EDW Query
#2 - Open up the ArcSDE Workspace for Editing
#3 - Establish the connection to the Data Warehouse
#4 -Execute the Query and Load the Rapid Response Featureclass
#5 - Cleanup

#Dependency modules;
#1 - arcpy
#2 - pyodbc

#Susan Jones
#2 September 2016


#todo: import Modules
import arcpy, string, os, pyodbc, datetime


#purpose: convert between WGS84 and NZTM
def projectCoordinates(longitude, latitude):

    #projectAs
    wgs84Sr = arcpy.SpatialReference(4326)
    NZTMSr = arcpy.SpatialReference(2193)
    gcs = "NZGD_2000_To_WGS_1984_1"
    pt = arcpy.Point(float(longitude), float(latitude))
    ptGeom = arcpy.PointGeometry(pt, wgs84Sr)
    nztmGeom = ptGeom.projectAs(NZTMSr, gcs)
    
    #return
    return [nztmGeom.firstPoint.X, nztmGeom.firstPoint.Y]


#banner
print "***\nRefresh CRM Rapid Response Layer\n\nSusan Jones\n4 September 2016\n***"

start = datetime.datetime.now()

#todo: variables
arcpy.env.overwriteOutput = 1
SERVER = "ATALSDBP01"
DB = "ARTA_DW"

#todo: create The Query
#0 - TicketNumber
#1 - Received
#2 - CRM_Month
#3 - CRM_OwningTeamName
#4 - StateName
#5 - CallType
#6 - Description
#7 - Topic
#8 - SubTopic 
#9 - Longitude
#10 - Latitude
#11 - Owner_Name
#12 - Shape
print "\ntodo: Create The EDW Query"
sql = ""
sql = sql + "--Gather all Rapid Response Incidents after 31 December 2013\n"
sql = sql + "SELECT dbo.fact_CRM_Incident.TicketNumber, CONVERT(nvarchar(50), CONVERT(datetime, dbo.dim_CRM_Incident_CreatedOn_Date.CRM_Incident_CreatedOn_date, 112)) "
sql = sql + "AS Received, REPLACE(dbo.dim_CRM_Incident_CreatedOn_Date.cal_month_yr_name, \'-\', \' \') AS CRM_Month, dbo.dim_CRM_QueueTeam.TeamName as CRM_OwningTeamName, "
sql = sql + "dbo.fact_CRM_Incident.StateName, dbo.fact_CRM_Incident.ata_CallTypeIdName AS CallType, dbo.fact_CRM_Incident.Description, "
sql = sql + "dbo.dim_CRM_ata_Topic.ata_name AS Topic, dbo.dim_CRM_ata_SubTopic.ata_name AS SubTopic, CONVERT(numeric(12, 8), dbo.fact_CRM_Incident.ata_LongitudeS) "
sql = sql + "AS Longitude, CONVERT(numeric(12, 8), dbo.fact_CRM_Incident.ata_LatitudeS) AS Latitude, dbo.dim_CRM_Owner.Owner_Name, "
sql = sql + "dbo.dim_CRM_OwningTeam.CRM_OwningTeamBusinessUnitIdName "
sql = sql + "--join Tables\n"
sql = sql + "FROM  dbo.dim_CRM_Incident_CreatedOn_Date INNER JOIN "
sql = sql + "dbo.fact_CRM_Incident ON dbo.dim_CRM_Incident_CreatedOn_Date.dim_CRM_Incident_CreatedOnDate_key = dbo.fact_CRM_Incident.dim_CRM_Incident_CreatedOnDate_key INNER JOIN "
sql = sql + "--add the dim_CRM_Queue\n"
sql = sql + "dim_CRM_QueueTeam  on (dim_CRM_QueueTeam.dim_CRM_QueueTeam_key = fact_CRM_Incident.dim_CRM_QueueTeam_key ) INNER JOIN "
sql = sql + "dbo.dim_CRM_OwningTeam ON dbo.dim_CRM_OwningTeam.dim_CRM_OwningTeam_key = dbo.fact_CRM_Incident.dim_CRM_OwningTeam_key INNER JOIN "
sql = sql + "dbo.dim_CRM_ata_SubTopic ON dbo.fact_CRM_Incident.dim_CRM_ata_SubTopic_key = dbo.dim_CRM_ata_SubTopic.dim_CRM_ata_SubTopic_key INNER JOIN "
sql = sql + "dbo.dim_CRM_ata_Topic ON dbo.dim_CRM_ata_Topic.dim_CRM_ata_Topic_key = dbo.fact_CRM_Incident.dim_CRM_ata_Topic_key INNER JOIN "
sql = sql + "dbo.dim_CRM_ata_LocalBoard ON dbo.fact_CRM_Incident.dim_CRM_ata_LocalBoard_key = dbo.dim_CRM_ata_LocalBoard.dim_CRM_ata_LocalBoard_key INNER JOIN "
sql = sql + "dbo.dim_CRM_Owner ON dbo.fact_CRM_Incident.dim_CRM_Owner_key = dbo.dim_CRM_Owner.dim_CRM_Owner_key "
sql = sql + "-- where clause\n"
sql = sql + "WHERE        (dbo.dim_CRM_Incident_CreatedOn_Date.dim_CRM_Incident_CreatedOnDate_key  >= 20131231) "
sql = sql + "and dbo.dim_CRM_QueueTeam.TeamName in (\'Rapid Response\', \'Walking & Cycling\', \'Walking, Cycling & Safety\', \'Network Operations & Safety\') "
sql = sql + "and (convert(numeric(18, 8), dbo.fact_CRM_Incident.ata_LongitudeS) > 0 or convert(numeric(18, 8), dbo.fact_CRM_Incident.ata_LatitudeS) > 0) "
sql = sql + "order by CRM_Month desc "


#todo: print the CRM Statement
#ArcSDE Feature class
print "\ntodo: Truncate CR_CRMRapidResponseComplaint_DV"
fc = "GISADMIN.CR_CRMRapidResponseComplaint_DV"
sdeWsp = r"\\atalgisau01\admin\Maintenance\connections\dba@GIS@atalgissdbu01.sde"
arcpy.env.workspace = sdeWsp

crmLink = "http://atalcrmp02.aucklandtransport.govt.nz:5555/AucklandTransport/main.aspx"
sstart = datetime.datetime.now()
arcpy.DeleteFeatures_management(fc)
send = datetime.datetime.now()
print str(send - sstart) + " seconds"

#todo: open an Edit Workspace
print "\ntodo: Open up the ArcSDE Workspace for Editing"
edit = arcpy.da.Editor(sdeWsp)
edit.startEditing(with_undo = False, multiuser_mode = True)
edit.startOperation()

fields = ["TicketNumber", "Received", "Month", "OwningTeam", "State", "CallType", "Description", "Topic", "SubTopic" , "Latitude", "Longitude", "SHAPE", "CRMLINK"]
crmrows = arcpy.da.InsertCursor(in_table = fc, field_names = fields)


#Create to the edw
print "\ntodo: Establish the connection to the Data Warehouse"
connString = r'DRIVER={SQL Server};SERVER='+SERVER+';DATABASE='+DB+';Trusted_Connection=True;'
conn = pyodbc.connect(connString)


#todo Cycle Throug the cursor
sstart = datetime.datetime.now()
print "\ntodo: Execute the Query and Load the Rapid Response Featureclass"
cnt = 0
cursor = conn.execute(sql)
for row in cursor:
    coords = projectCoordinates(row[9],row[10])
    nztmPt = arcpy.Point(coords[0], coords[1])
    crmrow = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], nztmPt, crmLink]
    crmrows.insertRow(crmrow)
    cnt += 1
    send = datetime.datetime.now()
print str(send - sstart) + " seconds"
print "\ntodo: Number of rows " + str(cnt)


#todo: Cleanup
del conn
del crmrow
del crmrows


#todo: open an Edit Workspace
edit.stopOperation()
edit.stopEditing(save_changes = True)


#completed
print "\ncompleted"

end = datetime.datetime.now()


#todo: duration
print "\n" + str(end - start) + " seconds\n"

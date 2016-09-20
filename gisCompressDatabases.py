#gisCompressDatabases.py

#purpose:
#compress GIS database servers and daily maintenance

#import modules
import arcpy, datetime, os
print 'COMPRESS THE ARCSDE DATABASES'
print 'Author: Susan Jones'
print 'Script date: 1/8/2014'
print 'Modified date: 8/5/2015'
print 'Auckland Transport'

#fetch Datasets
def fetchDatasets(gdbConn):
    allGDBData=[]
    arcpy.env.workspace = gdbConn
    allGDBData = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()
    arcpy.env.workspace = gdbConn
    datasets = arcpy.ListDatasets('*', 'ALL')
    for data in datasets:
        arcpy.env.workspace = os.path.join(gdbConn, data)
        allGDBData += arcpy.ListFeatureClasses() + arcpy.ListDatasets()
    return allGDBData

#list Versions to Reconcile
def versionsToReconcile(connection, versionsToExclude): #expect a connection string
    arcpy.env.workspace = connection
    verList = []
    vers = arcpy.da.ListVersions()
    for ver in vers:
        if not ver.name.lower() in versionsToExclude:
            print ver.name.lower()
            verList.append(ver.name)
    return verList    

print '\nRUN:'+str(datetime.datetime.now())

#variables
lfPProd=r'\\atalgisau01\ADMIN\Maintenance\etl\log\reconcile_ATALGISSDBU01.log' ##logfile PProd
lfProd=r'\\atalgisau01\ADMIN\Maintenance\etl\log\reconcile_ATALGISSDBP01.log' ##logfile Prod

#connection String
#gisadmin
connGISProd=r'D:\ADMIN\Maintenance\connections\gisadmin@GIS@atalgissdbp01.sde'
connGISPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@GIS@atalgissdbu01.sde'
connACProd=r'D:\ADMIN\Maintenance\connections\gisadmin@AC@atalgissdbp01.sde'
connATProd=r'D:\ADMIN\Maintenance\connections\gisadmin@AT@atalgissdbp01.sde'
connEXTProd=r'D:\ADMIN\Maintenance\connections\gisadmin@EXT@atalgissdbp01.sde'
connACPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@AC@atalgissdbu01.sde'
connATPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@AT@atalgissdbu01.sde'
connATEXTPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@AT_EXT@atalgissdbu01.sde'
connEXTPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@EXT@atalgissdbu01.sde'
connPOCPProd=r'D:\ADMIN\Maintenance\connections\gisadmin@POC@atalgissdbu01.sde'
#sde
connSDE_GISProd=r'D:\ADMIN\Maintenance\connections\sde@GIS@atalgissdbp01.sde'
connSDE_ACProd=r'D:\ADMIN\Maintenance\connections\sde@AC@atalgissdbp01.sde'
connSDE_ATProd=r'D:\ADMIN\Maintenance\connections\sde@AT@atalgissdbp01.sde'
connSDE_EXTProd=r'D:\ADMIN\Maintenance\connections\sde@EXT@atalgissdbp01.sde'
connSDE_GISPProd=r'D:\ADMIN\Maintenance\connections\sde@GIS@atalgissdbu01.sde'
connSDE_ACPProd=r'D:\ADMIN\Maintenance\connections\sde@AC@atalgissdbu01.sde'
connSDE_ATPProd=r'D:\ADMIN\Maintenance\connections\sde@AT@atalgissdbu01.sde'
connSDE_ATEXTPProd=r'D:\ADMIN\Maintenance\connections\sde@AT_EXT@atalgissdbu01.sde'
connSDE_EXTPProd=r'D:\ADMIN\Maintenance\connections\sde@EXT@atalgissdbu01.sde'
connSDE_POCPProd=r'D:\ADMIN\Maintenance\connections\sde@POC@atalgissdbu01.sde'
#dba
connDBA_GISProd=r'D:\ADMIN\Maintenance\connections\dba@GIS@atalgissdbp01.sde'
connDBA_ACProd=r'D:\ADMIN\Maintenance\connections\dba@AC@atalgissdbp01.sde'
connDBA_ATProd=r'D:\ADMIN\Maintenance\connections\dba@AT@atalgissdbp01.sde'
connDBA_EXTProd=r'D:\ADMIN\Maintenance\connections\dba@EXT@atalgissdbp01.sde'
connDBA_GISPProd=r'D:\ADMIN\Maintenance\connections\dba@GIS@atalgissdbu01.sde'
connDBA_ACPProd=r'D:\ADMIN\Maintenance\connections\dba@AC@atalgissdbu01.sde'
connDBA_ATPProd=r'D:\ADMIN\Maintenance\connections\dba@AT@atalgissdbu01.sde'
connDBA_ATEXTPProd=r'D:\ADMIN\Maintenance\connections\dba@AT_EXT@atalgissdbu01.sde'
connDBA_EXTPProd=r'D:\ADMIN\Maintenance\connections\dba@EXT@atalgissdbu01.sde'
connDBA_POCPProd=r'D:\ADMIN\Maintenance\connections\dba@POC@atalgissdbu01.sde'


#sets
reconcileDB = [connGISProd, connACProd, connATProd, connEXTProd, connGISPProd, connACPProd, connATPProd, connATEXTPProd, connEXTPProd, connPOCPProd]
compressDB = [connSDE_GISProd, connSDE_ACProd, connSDE_ATProd, connSDE_EXTProd, connSDE_GISPProd, connSDE_ACPProd, connSDE_ATPProd, connSDE_ATEXTPProd,connSDE_EXTPProd, connSDE_POCPProd] 
analyzeDB = [connDBA_GISProd, connDBA_ACProd, connDBA_ATProd, connDBA_EXTProd, connDBA_GISPProd, connDBA_ACPProd, connDBA_ATPProd, connDBA_ATEXTPProd, connDBA_EXTPProd, connDBA_POCPProd]


#start ATALGISSDBU01
start=datetime.datetime.now()

print '\n***\nReconcile and compress\n***'

#todo: reconcile
print "\nreconcile"
for conn in reconcileDB:
    print 'reconcile ' + conn
    arcpy.env.workspace = conn
    if os.path.exists(lfPProd): #logfile
        os.remove(lfPProd)
    versionsToExclude = ['sde.default', 'gisadmin.validate', 'gisadmin.edit']
    ##versionsToExclude = []
    versions = versionsToReconcile(conn, versionsToExclude)
    arcpy.ReconcileVersions_management(input_database = conn, reconcile_mode = 'ALL_VERSIONS', target_version = 'sde.DEFAULT', edit_versions = versions, acquire_locks = 'LOCK_ACQUIRED', abort_if_conflicts = 'NO_ABORT', conflict_definition = 'BY_OBJECT', conflict_resolution = 'FAVOR_EDIT_VERSION', with_post = 'POST', with_delete = 'KEEP_VERSION', out_log = lfPProd)

#todo: compress
print "\ncompress"
for conn in compressDB:
    print 'compressing ' + conn
    arcpy.Compress_management(conn)

#todo: analyze
print "\nanalyze"
for conn in analyzeDB:
    print 'analyzing ' + conn
    pyData = fetchDatasets(conn)
    try:
        arcpy.AnalyzeDatasets_management(input_database=conn, in_datasets=pyData, include_system='SYSTEM', analyze_base='ANALYZE_BASE', analyze_delta='ANALYZE_DELTA')
    except:
        status = "continue"


#get The Time
print '\nTIME ELAPSED:'+str(datetime.datetime.now()-start)

#completed
print '\ncompleted'

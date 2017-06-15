#sjSendMyWorksitesEmail.py

#Purpose: send myworksties email with summary details

#Process
#1. Extract data from Media Suite into ArcSDE (atalgissdbp01)  ext.gisadmin.MediaSuite_MyWorksite_XR
#2. Filter to current records
#3. Upload to AGOL
#4. send Email

#import The Python Modules
import smtplib, arcpy, datetime


#banner
print("Sending myWorksites notification email")

#set Todays Date
today = datetime.date.today()

#get The Feature Count
conn = r'\\atalgisap01\Projects\PJ\MyWorksite\Scripts\gisadmin@EXT@atalgissdbp01.sde'

#get The number of myworksites from Media suite
arcpy.env.workspace = conn
myWorksites = arcpy.GetCount_management(in_rows = "MediaSuite_MyWorksite_XR")

#Prepare the Email
sender = 'Susan.Jones@at.govt.nz'
receivers = ['Susan.Jones@at.govt.nz', 'Amit.Kokje@at.govt.nz', 'Chris.Pedrezuela@at.govt.nz']
receivers = ['Susan.Jones@at.govt.nz']

#Email body and content
message = """From: Susan Jones <Susan.Jones@at.govt.nz>
To: GRP AT IT GIS Team <Susan.Jones@at.govt.nz>
Subject: myWorksites updated to """ + str(myWorksites) + """ Features on """ + str(today) + """
myWorksites has been updated in https://www.arcgis.com/apps/View/index.html?appid=864f8ae5a605415b976fffab69ffbc61. 
"""

try:
   smtpObj = smtplib.SMTP('smtp.at.govt.nz')
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except SMTPException:
   print("Error: unable to send email")

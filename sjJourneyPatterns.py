#sjJourneyPatterns.py

#purpose;
#process the journey patterns Rapid Extract file and write the contents as a csv file

#input - user specified XML file
#input file eg d:\tmp\JourneyPatterns.xml

#output - csv file
#JourneyPatterns.csv
#JourneyPatternSections.csv
#JourneyPatternTimingLink.csv


#import modules
import datetime, string
from xml.dom import minidom

#measure Start Time
start = datetime.datetime.now()

#banner
print "***\nProcess Journey Patterns XML FIle\n\nSusan Jones\n19 September 2016\n***\n"

#sources and destinations
sourceFile = raw_input("Input JourneyPatterns XML file: ")
print "\nPrepare Input XML File"
doc = minidom.parse(sourceFile)
print "\nPrepare Output Files"
outFile = sourceFile.replace(".xml",".csv")
jpsFile = sourceFile.replace("JourneyPatterns.xml","JourneyPatternSections.csv")
jptlFile = sourceFile.replace("JourneyPatterns.xml","JourneyPatternTimingLink.csv")



#todo: process Each JourneyPattern
sstart = datetime.datetime.now()
print "\nProcess Journey Patterns " + sourceFile + " into " + outFile
#JourneyPattern
#RouteRef
#ModalType
#JourneyPatternSectionRef
fs = open(outFile, 'w') #open the File for writing
fs.write("JourneyPattern,RouteRef,ModalType,JourneyPatternSectionRef\n") #write the header
jps = doc.getElementsByTagName("JourneyPattern") 
for jp in jps:
    sid = jp.getAttribute("Id")
    rr = jp.getElementsByTagName("RouteRef")[0].childNodes[0].data
    md = jp.getElementsByTagName("ModalType")[0].childNodes[0].data
    #process Each JourneyPatternSections
    for section in jp.getElementsByTagName("JourneyPatternSections"):
        jpsr = section.getElementsByTagName("JourneyPatternSectionRef")[0].childNodes[0].data
        fs.write(sid + "," + rr + "," + md + "," + jpsr + "\n") #write the xml elements 
fs.close() #close the file
eend = datetime.datetime.now()
print "elapsed: " + str(eend - sstart)



#process JourneyPatternSections
sstart = datetime.datetime.now()
print "\nProcess Journey PatternSections " + sourceFile + " into " + jpsFile
#JourneyPatternSections
#JourneyPatternTimingLinkRef
fs = open(jpsFile, 'w') #open the File for writing
fs.write("JourneyPatternSection,JourneyPatternTimingLinkRef\n") #write the header
jps = doc.getElementsByTagName("JourneyPatternSections")
for sect in jps:
    #process Each JourneyPatternSection
    for jp in sect.getElementsByTagName("JourneyPatternSection"):
        #get Id
        Id = jp.getAttribute("Id")
        #JourneyPatternTimingLinks
        for jptl in jp.getElementsByTagName("JourneyPatternTimingLinks"):
            #JourneyPatternTimingLinkRef
            for jptlr in jptl.getElementsByTagName("JourneyPatternTimingLinkRef"):
                linkRef = jptlr.childNodes[0].data
                fs.write(Id + "," + linkRef + "\n")
fs.close()
eend = datetime.datetime.now()
print "elapsed: " + str(eend - sstart)



#process JourneyPatternTimingLink
sstart = datetime.datetime.now()
cnt = 0
print "\nProcess Journey Pattern Timing Link " + sourceFile + " into " + jptlFile
#JourneyPatternTimingLink
#RouteLinkRef
#From TimingStatus, From Activity
#To TimingStatus, To Activity
#JourneyPatternTimingLinkRef
fs = open(jptlFile, 'w') #open the File for writing
fs.write("JourneyPatternTimingLink,RouteLinkRef,FromTimingStatus,FromActivity,ToTimingStatus,ToActivity\n") #write the header
jps = doc.getElementsByTagName("JourneyPatternTimingLinks")
for sect in jps:
    #process Each JourneyPatternSection
    for jp in sect.getElementsByTagName("JourneyPatternTimingLink"):
        #get Id
        Id = jp.getAttribute("Id")
        #RouteLinkRef
        for rlr in jp.getElementsByTagName("RouteLinkRef"):
            routeLinkRef = rlr.childNodes[0].data
        #From
        for fromAtt in jp.getElementsByTagName("From"):
            fromStatus = fromAtt.getElementsByTagName("TimingStatus")[0].childNodes[0].data
            fromActivity = fromAtt.getElementsByTagName("Activity")[0].childNodes[0].data
        #To
        for toAtt in jp.getElementsByTagName("To"):
            toStatus = toAtt.getElementsByTagName("TimingStatus")[0].childNodes[0].data
            toActivity = toAtt.getElementsByTagName("Activity")[0].childNodes[0].data
        fs.write(Id + "," + routeLinkRef + "," + fromStatus + "," + fromActivity + "," + toStatus + "," + toActivity + "\n")
fs.close()
eend = datetime.datetime.now()
print "elapsed: " + str(eend - sstart)


#measure Finish Time
end = datetime.datetime.now()

#completion
print "\nElapsed: " + str(end - start)
print '\ncompleted'

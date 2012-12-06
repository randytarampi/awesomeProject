#This is just a python file with some useful functions that allow us to convert and parse strings 
# that we get from the datebase into useful information

from datetime import datetime

def convertStringToDate(inputString):
    outputdate = datetime.strptime(inputString, '%Y-%m-%d')
    #print outputdate
    return outputdate

def convertStringToTime(inputString):
    outputdate = datetime.strptime(inputString, '%H:%M:%S')
    #print outputdate
    return outputdate

#Tests two sets of start and end dates to see if they overlap and conflict
# This can work for time and for dates
def datetimeconflict(startdate1, enddate1, startdate2, enddate2):
    if startdate1 <= enddate1 and startdate2 <= enddate2:
        if startdate1 < startdate2:
            if enddate1 < startdate2:
		#print 'No Conflict first dates happen before second dates'
		return False
            else :
		#print 'There is a conflict'
		return True
        else:
            if enddate2 < startdate1:
                #print 'No Conflict dates 2 happen first'
		return False
            else:
                #print 'There is a conflict'
		return True
    else:
         print 'Improper inputs'


def timeConflict(starttime1, endtime1, starttime2, endtime2):
    if starttime1 <= endtime1 and starttime2 <= endtime2:
        if starttime1 < starttime2:
            if endtime1 < starttime2:
		return False
            else :
		return True
        else:
            if endtime2 < starttime1:
                #print 'No Conflict time 2 happens before time 1'
		return False
            else:
		return True
    else:
         print 'Improper inputs'

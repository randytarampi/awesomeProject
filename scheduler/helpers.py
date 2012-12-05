from datetime import time
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from scheduler.models import *
from scheduler.algorithm import *

# A file that holds helper functions

def hourIsAMorPM(h):
	if h >= 12:
		out = "p.m."
	else:
		out = "a.m."
	return out

def changeFrom24To12(h):
	out = h % 12
	if out == 0:
		out = 12
	return out

def weeklyScheduleRows(meetingTimes, time, proposedCourse=None):
	tableRow = []

	for day in range(6):
		for meeting in meetingTimes:
			rowCount = 0
			if meeting.weekday == day:
				if meeting.start_time == time:
					testTime = time
					while meeting.end_time > testTime:
						try: 
							testTime = testTime.replace(minute=testTime.minute+30)
						except ValueError: 
							testTime = testTime.replace(hour=testTime.hour+1, minute=0)
						rowCount += 1
					scheduledOrProposed = "scheduleTableClass" if (meeting.course != proposedCourse) else "scheduleTableProposedClass"
					tableRow.append('\n\t<td rowspan="%i" class="scheduleTableCell %s" id={{ meeting%s.id }}>\n\t\t<span class="classDescription" id={{ meeting%s.id }}>{{ meeting%s.course }}<br />{{ meeting%s.typeChoice }}<br />{{ meeting%s.start_time }} to {{ meeting%s.end_time }}<br />{{ meeting%s.room }}</span></td>' % (rowCount, scheduledOrProposed, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id))
					break
				elif meeting.start_time < time and time <= meeting.end_time:
					break
		else:
			tableRow.append('\n\t<td class="scheduleTableCell">&nbsp;</td>')
	
	return ''.join(tableRow)

def weeklySchedule(scheduledTimes, proposedTimes=[]):
	meetingTimes = scheduledTimes
	meetingTimes.extend(proposedTimes)
	meetingTimes = sorted(meetingTimes, key=lambda meeting: meeting.start_time)
	proposedCourse = proposedTimes[0].course if proposedTimes else None
	meetingTable = []
	meetingContext = {}
	earlyBound = meetingTimes[0].start_time
	lateBound = meetingTimes[len(meetingTimes)-1].end_time
	tableBounds = []
	
	for meeting in meetingTimes:
		meetingContext[('meeting%s' % meeting.id)] = meeting
		earlyBound = meeting.start_time if (meeting.start_time < earlyBound) else earlyBound
		lateBound = meeting.end_time if (meeting.end_time > lateBound) else lateBound
	
	for hour in range(earlyBound.hour, lateBound.hour+1):
		tableBounds.append(time(hour))
	
	for slot in tableBounds:
		meetingContext[('time%s' % slot.hour)] = slot
	
		# First Row (Top of the Hour)
		meetingTable.append('\n<tr class="scheduleTableRow topHour"><th class="scheduleTableTime" rowspan="2">{{ time%s }}</th>' % slot.hour)
		meetingTable.append(weeklyScheduleRows(meetingTimes, slot, proposedCourse))
		meetingTable.append('\n</tr>')
		
		# Second Row (Bottom of the Hour)
		slot = slot.replace(minute=slot.minute+30)
		meetingTable.append('\n<tr class="scheduleTableRow bottomHour">')
		meetingTable.append(weeklyScheduleRows(meetingTimes, slot, proposedCourse))
		meetingTable.append('\n</tr>')
	
	return Template(''.join(meetingTable)).render(Context(meetingContext))

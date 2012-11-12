#!/usr/bin/python

# SFU courses JSON import
# See https://courses.cs.sfu.ca/data/courses/1131 for example input

import sys
import json

assert len(sys.argv) == 3

# Initialize
inputJSON = json.load(open(sys.argv[1]))
#INSERT INTO `scheduler_course` (`title`, `section`, `component`, `number`, `semester`, `campus`, `subject`) VALUES ('TESTING 102', 'D100', 'LEC', '102', '1131', 'VANCR', 'TEST')
coursesSQL = "INSERT INTO `scheduler_course` (`title`, `section`, `component`, `number`, `semester`, `campus`, `subject`) "
#INSERT INTO `scheduler_instructor` (`userid`, `name`, `course_id`) VALUES ('tstInstr', 'Test Instructor', 2)
meetingtimeSQL = "INSERT INTO `scheduler_meetingtime` (`start_day`, `room`, `start_time`, `end_day`, `weekday`, `type`, `end_time`, `course_id`) "
#INSERT INTO `scheduler_meetingtime` (`start_day`, `room`, `start_time`, `end_day`, `weekday`, `type`, `end_time`, `course_id`) VALUES ('2012-11-01', 'School', '10:30:00', '2012-11-30', 3, 'LEC', '13:30:00', 2)
instructorSQL = "INSERT INTO `scheduler_instructor` (`userid`, `name`, `course_id`) "
courseSQL = ""
outputSQL = ""

# Parse the JSON, Build the SQL
for course in inputJSON['courses']:
	courseSQL += coursesSQL + "VALUES ("
	courseSQL += "'" + course['title'].replace("'", "''") + "', "
	courseSQL += "'" + course['section'] + "', "
	courseSQL += "'" + course['component'] + "', "
	courseSQL += "'" + course['number'] + "', "
	courseSQL += "'" + course['semester'] + "', "
	courseSQL += "'" + course['campus'] + "', "
	courseSQL += "'" + course['subject'] + "');\n"
	
	# Get the course_id for the last two queries
	courseSQL += "SET @course_id = LAST_INSERT_ID();\n"
	
	# Add the instructor(s)
	for instructor in course['instructors']:
		courseSQL += instructorSQL + "VALUES ("
		courseSQL += "'" + instructor['userid'].replace("'", "''") + "', " if instructor['userid'] else "NULL, "
		courseSQL += "'" + instructor['name'].replace("'", "''") + "', "
		courseSQL += " @course_id);\n"
	
	# Add the meeting time(s)
	for meetingtime in course['meetingtimes']:
		courseSQL += meetingtimeSQL + "VALUES ("
		courseSQL += "'" + meetingtime['start_day'] + "', "
		courseSQL += "'" + meetingtime['room'].replace("'", "''") + "', "
		courseSQL += "'" + meetingtime['start_time'] + "', "
		courseSQL += "'" + meetingtime['end_day'] + "', "
		courseSQL += str(meetingtime['weekday']) + ", "
		courseSQL += "'" + meetingtime['type'] + "', "
		courseSQL += "'" + meetingtime['end_time'] + "', "
		courseSQL += " @course_id);\n"
	
	# Concatenate to outputSQL
	outputSQL += courseSQL
	courseSQL = ""

# Write to file
outputFile = open(sys.argv[2], "wb")
outputFile.write(outputSQL)
outputFile.close

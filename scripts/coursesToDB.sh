#!/bin/bash

projDir=~/awesomeProject
semesterNum=1131

rm $projDir/static/courses.json
wget -O $projDir/static/courses.json https://courses.cs.sfu.ca/data/courses/$semesterNum
$projDir/scripts/coursesToSQL.py $projDir/static/courses.json $projDir/scheduler/sql/course.sql
python $projDir/manage.py syncdb
rm $projDir/scheduler/sql/course.sql

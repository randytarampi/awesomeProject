#!/bin/bash

projDir=~/awesomeProject

sudo apache2ctl stop
python $projDir/manage.py collectstatic --noinput
sudo chmod +r -R $projDir/static/
sudo chown awesomeadmin:www-data -R $projDir
sudo apache2ctl start

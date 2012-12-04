#!/bin/bash

projDir=~/awesomeProject

python $projDir/manage.py collectstatic --noinput
sudo chmod +r -R $projDir/static/
sudo chown awesomeadmin:www-data -R $projDir
sudo apache2ctl restart

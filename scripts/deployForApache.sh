#!/bin/bash

projDir=~/awesomeProject

python $projDir/manage.py collectstatic --noinput
chmod +r -R $projDir/static/
sudo apache2ctl restart

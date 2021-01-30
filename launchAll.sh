#!/bin/bash

cd $home
source /GIT/lightAlarmClock/env/bin/activate
python --version

cd $home
cd /GIT/lightAlarmClock/
python backend/src/restAPI.py&

sleep 5

python frontend/main.py

exit 0

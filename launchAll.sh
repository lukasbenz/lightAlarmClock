#!/bin/bash
source env/bin/activate
cd ~/GIT/lightAlarmClock/
python backend/src/restAPI.py&
sleep 5
python frontend/main.py&

#!/bin/bash
source ~/GIT/lightAlarmClock/env/bin/activate
cd ~/GIT/lightAlarmClock/
python backend/src/restAPI.py&
sleep 5
python frontend/main.py&

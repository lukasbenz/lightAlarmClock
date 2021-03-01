#!/bin/bash
cd ~/GIT/lightAlarmClock/
/home/pi/GIT/lightAlarmClock/env/bin/python backend/src/restAPI.py&

sleep 5

#cd ~/GIT/lightAlarmClock/frontend
#/home/pi/GIT/lightAlarmClock/env/bin/python visuKivy.py

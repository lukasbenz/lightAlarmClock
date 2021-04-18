#!/bin/bash
cd ~/GIT/lightAlarmClock/backend/src
/home/pi/GIT/lightAlarmClock/env/bin/python restAPI.py&

sleep 5

cd ~/GIT/lightAlarmClock/frontend
/home/pi/GIT/lightAlarmClock/env/bin/python visuKivy.py

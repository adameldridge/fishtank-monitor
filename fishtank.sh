#!/bin/bash
nohup node ~/Documents/FishTank/app.js &
nohup python ~/Documents/FishTank/io/powerSchedule.py &
nohup python ~/Documents/FishTank/io/waterTempLog.py &

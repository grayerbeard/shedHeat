#!/bin/bash
cd /home/pi/shedHeat
echo looking to kill any old tmux tank session
tmux kill-session -t shedHeat
echo now new tmux shedHeat session 
tmux new-session -d -s shedHeat 'python3 shedHeat.py'
echo tmux session has been started    Press Enter 
exit 0

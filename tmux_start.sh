#!/bin/bash
cd /home/pi/powerMonitor
echo looking to kill any old tmux power session
tmux kill-session -t power
echo now new tmux power session 
tmux new-session -d -s power 'python3 powerMonitor.py'
echo tmux session has been started    Press Enter 
exit 0

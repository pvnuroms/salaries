#!/bin/bash
if pgrep -f "run.py" >&/dev/null
 then {

    echo "Exit! Python bot is already running!" >> /home/pupkin/projects/salaries/logs/log_launch.txt
    exit 1
  }
else
  {
    sleep 1  #delay
    /home/pupkin/projects/salaries/run.py.py
    exit 0
  }
fi;
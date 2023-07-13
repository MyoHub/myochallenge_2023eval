#!/bin/bash
# This script test the communication of the agent with the environment
GreenBK='\033[1;42m'
RedBK='\033[1;41m'
RC='\033[0m'

python environment/test_loco_environment.py &

# TO BE REPLACED WITH A DOCKER --> docker run myochallengeeval_loco_agent &

python agent/agent_loco_random.py
if [ $? -eq 0 ]; then
    printf "${GreenBK}Chase Tag Agent script correctly connecting with the environment!${RC} \n"
else
    printf "${RedBK}Something is wrong! Check agent script!${RC} \n"
    echo FAIL
fi

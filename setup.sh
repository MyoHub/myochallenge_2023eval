#!/bin/bash
GreenBK='\033[1;42m'
RedBK='\033[1;41m'
RC='\033[0m'
PassEvalAI=false
PassDocker=false

#check if docker is installed
docker info
if [ $? -eq 0 ]; then
    PassDocker=true
    printf "${GreenBK}Docker: Passed!${RC} \n"
else
    printf "${RedBK}Docker doesn't seem to be installed!${RC} \n"
    echo FAIL
fi


evalai challenges --participant
if [ $? -eq 0 ]; then
    PassEvalAI=true
    printf "${GreenBK}EvalAI: Passed!${RC} \n"
else
    printf "${RedBK}The team doesn't seem to have a valid EvalAI account!${RC} \n"
    echo FAIL
fi

if [ "$PassEvalAI" = "true" ] && [ "$PassDocker" = "true" ]; then
    # Install required dependences
    pip install --upgrade pip
    pip install torch
    pip install -r requirements/agent.txt  -f https://download.pytorch.org/whl/torch_stable.html
    pip install grpcio grpcio-tools myosuite

    export PYTHONPATH="./utils/:$PYTHONPATH"
    export PYTHONPATH="./agent/:$PYTHONPATH"
    export PYTHONPATH="./environment/:$PYTHONPATH"


    chmod u+r+x ./test/test_mani_agent.sh
    chmod u+r+x ./test/test_loco_agent.sh

    ./test/test_mani_agent.sh
    ./test/test_loco_agent.sh
fi

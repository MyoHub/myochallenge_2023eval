import os
import pickle
import time
from utils import RemoteConnection
import numpy as np

time.sleep(30)

LOCAL_EVALUATION = os.environ.get("LOCAL_EVALUATION")

if LOCAL_EVALUATION:
    rc = RemoteConnection("environment:8086")
else:
    rc = RemoteConnection("localhost:8086")


################################################
## A -replace with your trained policy.
## HERE it is shown an example from a previously trained policy with MJRL (see https://github.com/facebookresearch/myosuite/blob/main/docs/source/tutorials/4_Train_policy.ipynb)
## additional dependences such as gym and mujoco_py might be needed
path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
print(path)
pi = pickle.load(open(path+'/policies/loco_test_policy.pickle', 'rb'))
print('CHASE-TAG agent: policy loaded')
################################################

flag_completed = None # this flag will detect then the whole eval is finished
repetition = 0
while not flag_completed:
    flag_trial = None # this flag will detect the end of an episode/trial
    counter = 0
    repetition +=1
    while not flag_trial :

        if counter == 0:
            print('CHASE-TAG: Trial #'+str(repetition)+'Start Resetting the environment and get 1st obs')
            obs = rc.reset()

        ################################################
        ### B - HERE it is obtained the action from the model and passed to the remove environment
        action = pi.get_action(obs)[0]
        ################################################

        ## gets info from the environment
        base = rc.act_on_environment(action)
        obs =  base["feedback"][0]

        flag_trial = base["feedback"][2]
        flag_completed = base["eval_completed"]

        print(f"CHASE-TAG ): Agent Feedback iter {counter} -- trial solved: {flag_trial} -- task solved: {flag_completed}")
        print("*" * 100)
        counter +=1

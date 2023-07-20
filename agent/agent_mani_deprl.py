import os
import pickle
import time
from utils import RemoteConnection, DummyEnv
import numpy as np


def get_custom_observation(rc):
    """
    Use this function to create an observation vector from the
    environment provided observation dict for your own policy.
    By using the same keys as in your local training, you can ensure that
    your observation still works.
    """
    # example of obs_keys for deprl baseline
    obs_keys = [
            'hand_qpos',
            'hand_qvel',
            'obj_pos',
            'goal_pos',
            'pos_err',
            'obj_rot',
            'goal_rot',
            'rot_err'
    ]
    obs_keys.append('act')

    obs_dict = rc.get_obsdict()
    # add new features here that can be computed from obs_dict
    # obs_dict['qpos_without_xy'] = np.array(obs_dict['internal_qpos'][2:35].copy())

    return rc.obsdict2obsvec(obs_dict, obs_keys)


time.sleep(60)

LOCAL_EVALUATION = os.environ.get("LOCAL_EVALUATION")

if LOCAL_EVALUATION:
    rc = RemoteConnection("environment:8085")
else:
    rc = RemoteConnection("localhost:8085")



# compute correct observation space
shape = get_custom_observation(rc).shape
rc.set_observation_space(shape)


################################################
## A -replace with your trained policy.
## HERE an example from a previously trained policy with deprl is shown (see https://github.com/facebookresearch/myosuite/blob/main/docs/source/tutorials/4a_deprl.ipynb)
## additional dependencies such as gym and deprl might be needed
import deprl
policy = deprl.load_baseline(DummyEnv(env_name='myoChallengeRelocateP1-v0', stub=rc))
print('Relocate agent: policy loaded')
################################################



flag_completed = None # this flag will detect then the whole eval is finished
repetition = 0
while not flag_completed:
    flag_trial = None # this flag will detect the end of an episode/trial
    counter = 0
    repetition +=1
    while not flag_trial :

        if counter == 0:
            print('Relocate: Trial #'+str(repetition)+'Start Resetting the environment and get 1st obs')
            obs = rc.reset()

        ################################################
        ### B - HERE the action is obtained from the policy and passed to the remote environment
        obs = get_custom_observation(rc)
        action = policy(obs)
        ################################################

        ## gets info from the environment
        base = rc.act_on_environment(action)
        obs =  base["feedback"][0]

        flag_trial = base["feedback"][2]
        flag_completed = base["eval_completed"]

        print(f"Relocate: Agent Feedback iter {counter} -- trial solved: {flag_trial} -- task solved: {flag_completed}")
        print("*" * 100)
        counter +=1

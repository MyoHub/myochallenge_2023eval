import evaluation_pb2
import evaluation_pb2_grpc
import grpc
import os
import pickle
import time

import numpy as np

time.sleep(60)

LOCAL_EVALUATION = os.environ.get("LOCAL_EVALUATION")

if LOCAL_EVALUATION:
    channel = grpc.insecure_channel("environment:8086")
else:
    channel = grpc.insecure_channel("localhost:8086")



def pack_for_grpc(entity):
    return pickle.dumps(entity)


def unpack_for_grpc(entity):
    return pickle.loads(entity)


stub = evaluation_pb2_grpc.EnvironmentStub(channel)


print( unpack_for_grpc(
        stub.get_output_keys(
            evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))
        ).SerializedEntity
        ))
print(f'Len OBS: {len(unpack_for_grpc( stub.reset(evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))).SerializedEntity))}')

print("Original Ouput Obs keys:"+str(unpack_for_grpc(
        stub.get_output_keys(
            evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))
        ).SerializedEntity
        )))

keys = ['hand_pos']

unpack_for_grpc(
        stub.set_output_keys(
            evaluation_pb2.Package(SerializedEntity=pack_for_grpc(keys))
        ).SerializedEntity
        )
print("Reduced Set of Ouput Obs keys: "+str(unpack_for_grpc(
        stub.get_output_keys(
            evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))
        ).SerializedEntity
        ))+"  Len:"+str(len(unpack_for_grpc( stub.reset(evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))).SerializedEntity))))



flag_completed = None # this flag will detect then the whole eval is finished
repetition = 0

while not flag_completed:
    flag_trial = None # this flag will detect the end of an episode/trial
    counter = 0
    repetition +=1
    while not flag_trial :

        if counter == 0:
            print('BB : Start Resetting the environment and get 1st obs')
            obs = unpack_for_grpc(
            stub.reset(
                evaluation_pb2.Package(SerializedEntity=pack_for_grpc(None))
            ).SerializedEntity
            )

        action = np.random.rand(39)

        ## stub gets info from the environment
        p = evaluation_pb2.Package(SerializedEntity=pack_for_grpc(action))
        s = stub.act_on_environment(p)
        ss = s.SerializedEntity
        base = unpack_for_grpc(ss)


        obs =  base["feedback"][0]

        flag_trial = base["feedback"][2]
        flag_completed = base["eval_completed"]

        print(f"BAODING : Random Agent Feedback iter {counter} -- solved: {flag_trial}")
        print("*" * 100)
        counter +=1
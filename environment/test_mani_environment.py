import grpc
import gym
import pickle
import sys
import os
import requests
import json


from concurrent import futures
import time

import evaluation_pb2
import evaluation_pb2_grpc

LOCAL_EVALUATION = os.environ.get("LOCAL_EVALUATION")
EVALUATION_COMPLETED = False

import myosuite

class evaluator_environment:
    def __init__(self, environment="myoChallengeDieReorient-v0"):
        self.score = 0
        self.feedback = None
        self.env = gym.make(environment)

    def reset(self):
        return self.env.reset()

    def get_action_space(self):
        return len(self.env.action_space.sample())

    def get_observation_space(self):
        return len(self.env.observation_space.sample())

    def get_obsdict(self):
        return self.env.get_obs_dict(self.env.sim)

    def next_score(self):
        self.score += 1


class Environment(evaluation_pb2_grpc.EnvironmentServicer):
    def __init__(self, challenge_pk, phase_pk, submission_pk, server):
        self.challenge_pk = challenge_pk
        self.phase_pk = phase_pk
        self.submission_pk = submission_pk
        self.server = server
        self.iter = 0
        self.repetition = 0

    def reset(self, request, context):
        self.score = 0
        self.iter = 0
        self.repetition += 1
        message = pack_for_grpc(env.reset())
        env.feedback = []
        return evaluation_pb2.Package(SerializedEntity=message)

    def get_action_space(self, request, context):
        message = pack_for_grpc(env.get_action_space())
        return evaluation_pb2.Package(SerializedEntity=message)

    def get_observation_space(self, request, context):
        message = pack_for_grpc(env.get_observation_space())
        return evaluation_pb2.Package(SerializedEntity=message)

    def get_obsdict(self, request, context):
        message = pack_for_grpc(env.get_obsdict())
        return evaluation_pb2.Package(SerializedEntity=message)


    def act_on_environment(self, request, context):
        global EVALUATION_COMPLETED

        if not env.feedback or not env.feedback[2]:
            action = unpack_for_grpc(request.SerializedEntity)
            env.next_score()
            env.feedback = env.env.step(action)

        feedback = [env.feedback[0],env.feedback[1],False]
        if self.iter == 10:
            feedback = [env.feedback[0],env.feedback[1],True]
            if self.repetition == 5:
                EVALUATION_COMPLETED = True
        self.iter += 1
        return evaluation_pb2.Package(
            SerializedEntity=pack_for_grpc(
                {"feedback": feedback, "current_score": env.score, "eval_completed": EVALUATION_COMPLETED,}
            )
        )


env = evaluator_environment()


def pack_for_grpc(entity):
    return pickle.dumps(entity)


def unpack_for_grpc(entity):
    return pickle.loads(entity)


def reset(self):
    return env.reset()



def main():

    challenge_pk = "1"
    phase_pk = "1"
    submission_pk = "1"

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    evaluation_pb2_grpc.add_EnvironmentServicer_to_server(
        Environment(challenge_pk, phase_pk, submission_pk, server), server
    )
    print("Starting server. Listening on port 8085.")
    server.add_insecure_port("[::]:8085")
    server.start()
    try:
        while not EVALUATION_COMPLETED:
            time.sleep(4)
        server.stop(0)
    except KeyboardInterrupt:
        server.stop(0)
    exit(0)

if __name__ == "__main__":
    main()

import pickle
import evaluation_pb2
import evaluation_pb2_grpc
import grpc
import gym
import numpy as np


class RemoteConnection():
    def __init__(self, str_connection):
        self.channel = grpc.insecure_channel(str_connection)
        self.stub = evaluation_pb2_grpc.EnvironmentStub(self.channel)
        self._construct_action_and_observation_space()

    def pack_for_grpc(self, entity):
        return pickle.dumps(entity)

    def unpack_for_grpc(self, entity):
        return pickle.loads(entity)

    def get_action_space(self):
        act_space = self.unpack_for_grpc(
            self.stub.get_action_space(
                evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(None))
            ).SerializedEntity
            )
        return act_space

    def get_observation_space(self):
        observation_space = self.unpack_for_grpc(
            self.stub.get_observation_space(
                evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(None))
            ).SerializedEntity
            )
        return observation_space 

    def get_obsdict(self):
        obs_dict = self.unpack_for_grpc(
            self.stub.get_obsdict(
                evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(None))
            ).SerializedEntity
            )
        return obs_dict

    def reset(self):
        obs = self.unpack_for_grpc(
            self.stub.reset(
                evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(None))
            ).SerializedEntity
            )
        return obs

    def act_on_environment(self,action):
        p = evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(action))
        s = self.stub.act_on_environment(p)
        ss = s.SerializedEntity
        base = self.unpack_for_grpc(ss)
        return base

    def set_observation_space(self, shape):
        self.observation_space = gym.spaces.Box(shape=shape, high=1e6, low=-1e6)

    def _construct_action_and_observation_space(self):
        """
        Construct observation and action space to make the usage of popular RL frameworks easier.
        """
        action_len = self.get_action_space()
        obs_len = self.get_observation_space()
        self.observation_space = gym.spaces.Box(shape=(obs_len,), high=1e6, low=-1e6)
        self.action_space = gym.spaces.Box(shape=(action_len,), high=1.0, low=-1.0)
        # TODO case for remapping of [-1 1] -> [0 1]

    def obsdict2obsvec(self, obs_dict, ordered_obs_keys):
        """
        Create observation vector from obs_dict
        """
        obsvec = np.zeros(0)
        for key in ordered_obs_keys:
            obsvec = np.concatenate([obsvec, obs_dict[key].ravel()]) # ravel helps with images
        return obsvec


class DummyEnv:
    def __init__(self, env_name, stub):
        self.env_name = env_name
        self.observation_space = gym.spaces.Box(-np.inf, +np.inf, (stub.get_observation_space(),))
        self.action_space = gym.spaces.Box(-1, 1, (stub.get_action_space(),))

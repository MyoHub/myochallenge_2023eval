import pickle
import evaluation_pb2
import evaluation_pb2_grpc
import grpc

class RemoteConnection():
    def __init__(self, str_connection):
        self.channel = grpc.insecure_channel(str_connection)
        self.stub = evaluation_pb2_grpc.EnvironmentStub(self.channel)

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

    def get_output_keys(self):
        out_keys = self.unpack_for_grpc(
            self.stub.get_output_keys(
                evaluation_pb2.Package(SerializedEntity=self.pack_for_grpc(None))
            ).SerializedEntity
            )
        return out_keys

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

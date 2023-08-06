import json
import grpc
from .channel import CHANNEL
from .gRPC_proto.user import user_pb2, user_pb2_grpc, auth_pb2_grpc, auth_pb2


class User:
    def __init__(self, username=None, password=None, metadata=None):
        self.stub = user_pb2_grpc.UserControllerStub(CHANNEL)
        self.auth_stub = auth_pb2_grpc.AuthenticationStub(CHANNEL)
        self.username = username
        self.password = password
        self.metadata = metadata

    def change_password(self, new_password):
        try:
            response = self.stub.ChangePassword(
                user_pb2.PasswordRequest(username=self.username, password=self.password,
                                         new_password=new_password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def change_key(self):
        try:
            response = self.stub.ChangeKey(
                user_pb2.KeyRequest(username=self.username, password=self.password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def get_key(self):
        try:
            response = self.stub.GetKey(
                user_pb2.KeyRequest(username=self.username, password=self.password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def login(self):
        try:
            response = self.auth_stub.Login(auth_pb2.LoginRequest(username=self.username, password=self.password))
            response = json.loads(response.token)
            meta = [('jwt-access-token', response['token']),
                    ('user-role', response['role']),
                    ('user-status', str(response['status'])),
                    ('username', response['username'])]
            return meta
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def dropdown(self):
        try:
            if self.metadata is None:
                self.metadata = self.login()
            response = self.stub.DropDown(user_pb2.UserListRequest(), metadata=self.metadata)
            return response.option
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def check_token(self):
        try:
            response = self.stub.CheckJWT(user_pb2.TokenRequest(), metadata=self.metadata)
            return {"valid": response.valid, "remark": response.remark}
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
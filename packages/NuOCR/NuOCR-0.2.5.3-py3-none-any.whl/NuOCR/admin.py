from .gRPC_proto.user import user_pb2, user_pb2_grpc
from .channel import CHANNEL
import grpc


class Admin:
    def __init__(self, metadata):
        self.stub = user_pb2_grpc.UserControllerStub(CHANNEL)
        self.metadata = metadata

    def create_user(self, username, password, email, first_name, last_name):
        try:
            request = user_pb2.User(username=username, password=password, email=email, first_name=first_name,
                                    last_name=last_name)
            response = self.stub.Create(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def list_user(self):
        request = user_pb2.UserListRequest()
        response = self.stub.List(request, metadata=self.metadata)
        for post in response:
            print(post, end='')

    def retrieve_user(self, id):
        try:
            request = user_pb2.UserRetrieveRequest(id=id)
            response = self.stub.Retrieve(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def update_user(self, username, password, email, first_name, last_name):
        try:
            request = user_pb2.User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            response = self.stub.Update(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def delete_user(self, username, password, email, first_name, last_name):
        try:
            request = user_pb2.User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            response = self.stub.Destroy(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def add_access(self, username, access):
        try:
            request = user_pb2.UserRequest(username=username, access=access)
            response = self.stub.AddAccess(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove_access(self, username, access):
        try:
            request = user_pb2.UserRequest(username=username, access=access)
            response = self.stub.RemoveAccess(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def add_dropdown(self, username, option):
        try:
            request = user_pb2.DropRequest(username=username, option=option)
            self.stub.AddDropDown(request, metadata=self.metadata)
            return "Request completed successfully!"
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove_dropdown(self, username, option):
        try:
            request = user_pb2.DropRequest(username=username, option=option)
            self.stub.RemoveDropDown(request, metadata=self.metadata)
            return "Request completed successfully!"
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

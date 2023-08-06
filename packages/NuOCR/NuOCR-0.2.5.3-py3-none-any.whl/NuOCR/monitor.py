import json
from .gRPC_proto.monitor import monitor_pb2, monitor_pb2_grpc
from .channel import CHANNEL
import grpc


class Analysis:
    def __init__(self, metadata):
        self.stub = monitor_pb2_grpc.AnalysisControllerStub(CHANNEL)
        self.metadata = metadata

    def usage(self, filter=None):

        if filter is None:
            filter = {}
        try:
            filter_str = json.dumps(filter, indent=4, sort_keys=True)
            request = monitor_pb2.Request(body=filter_str)
            response = self.stub.usageAnalyse(request, metadata=self.metadata)
            return [json.loads(post.body) for post in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def extractor(self, filter=None):

        if filter is None:
            filter = {}
        try:
            filter_str = json.dumps(filter, indent=4, sort_keys=True)
            request = monitor_pb2.Request(body=filter_str)
            response = self.stub.extractorAnalyse(request, metadata=self.metadata)
            return [json.loads(post.body) for post in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def adaptor(self, filter=None):

        if filter is None:
            filter = {}
        try:
            filter_str = json.dumps(filter, indent=4, sort_keys=True)
            request = monitor_pb2.Request(body=filter_str)
            response = self.stub.adaptorAnalyse(request, metadata=self.metadata)
            return [json.loads(post.body) for post in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def templated_flow(self, filter=None):

        if filter is None:
            filter = {}
        try:
            filter_str = json.dumps(filter, indent=4, sort_keys=True)
            request = monitor_pb2.Request(body=filter_str)
            response = self.stub.templatedFlowAnalyse(request, metadata=self.metadata)
            return [json.loads(post.body) for post in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def text_processor(self, filter=None):

        if filter is None:
            filter = {}
        try:
            filter_str = json.dumps(filter, indent=4, sort_keys=True)
            request = monitor_pb2.Request(body=filter_str)
            response = self.stub.textProcessorAnalyse(request, metadata=self.metadata)
            return [json.loads(post.body) for post in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

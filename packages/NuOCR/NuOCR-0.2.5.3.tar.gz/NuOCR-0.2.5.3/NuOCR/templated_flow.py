import json
from .gRPC_proto.templated_flow import templated_flow_pb2, templated_flow_pb2_grpc
from .channel import CHANNEL
import grpc


class TemplatedFlow:
    def __init__(self, metadata):
        self.stub = templated_flow_pb2_grpc.TemplatedFlowControllerStub(CHANNEL)
        self.metadata = metadata

    def createTemplate(self, documentName, base64, description, boundingBox):
        try:
            request = templated_flow_pb2.TemplateRequest(
                documentName=documentName,
                base64=base64,
                description=description,
                box=[templated_flow_pb2.BoundingBox(
                    label=i['label'],
                    x=i['x'],
                    y=i['y'],
                    h=i['h'],
                    w=i['w'],
                ) for i in boundingBox]
            )
            response = self.stub.CreateTemplate(request, metadata=self.metadata)
            return json.loads(response.status)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def fetchTemplate(self):
        try:
            request = templated_flow_pb2.FetchRequest()
            response = self.stub.FetchTemplate(request, metadata=self.metadata)
            list_data = [{'id': i.documentId,
                          'name': i.documentName,
                          'base64': i.base64,
                          'mimeType': i.mimeType} for i in response]
            return list_data
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def extractTemplate(self, documentName, documentId, base64, fileName, readStatus=True, rawJson=True):
        try:
            request = templated_flow_pb2.ExtractRequest(
                documentId=documentId,
                documentName=documentName,
                base64=base64,
                fileName=fileName,
                readStatus=readStatus,
                rawJson=rawJson
            )
            response = self.stub.Extract(request, metadata=self.metadata)
            return json.loads(response.response)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def deleteTemplate(self, documentName, documentId):
        try:
            request = templated_flow_pb2.DeleteRequest(
                documentId=documentId,
                documentName=documentName,
            )
            self.stub.Delete(request, metadata=self.metadata)
            return "Template deleted Successfully"
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

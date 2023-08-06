from .gRPC_proto.multiformats import multiformats_pb2_grpc, multiformats_pb2
import grpc


class Multiformats:
    def __init__(self, metadata, jsonfile):
        self.stub = multiformats_pb2_grpc.MultiFormatsControllerStub(CHANNEL)
        self.metadata = metadata
        self.Jsonfile = jsonfile

    def Jsontocsv(self):
        try:
            request = multiformats_pb2.Request(jsonfile=self.Jsonfile)
            response = self.stub.JsonToCsv(request, metadata=self.metadata)
            return [{"filename": rec.filename, "bytes": rec.fileBytes} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
        
    def Jsontoxml(self):
        try:
            request = multiformats_pb2.Request(jsonfile=self.Jsonfile)
            response = self.stub.JsonToXml(request, metadata=self.metadata)
            return [{"filename": rec.filename, "bytes": rec.fileBytes} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
        
    def Jsontobson(self):
        try:
            request = multiformats_pb2.Request(jsonfile=self.Jsonfile)
            response = self.stub.JsonToBson(request, metadata=self.metadata)
            return [{"filename": rec.filename, "bytes": rec.fileBytes} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
        
    def Jsontotext(self):
        try:
            request = multiformats_pb2.Request(jsonfile=self.Jsonfile)
            response = self.stub.JsonToText(request, metadata=self.metadata)
            return [{"filename": rec.filename, "bytes": rec.fileBytes} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
        
    def Jsontomsgpack(self):
        try:
            request = multiformats_pb2.Request(jsonfile=self.Jsonfile)
            response = self.stub.JsonToMesgpack(request, metadata=self.metadata)
            return [{"filename": rec.filename, "bytes": rec.fileBytes} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
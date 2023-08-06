import grpc
import json
from .channel import CHANNEL
from .gRPC_proto.extractor import extractor_pb2, extractor_pb2_grpc


class Extractor:
    def __init__(self, metadata):
        self.stub = extractor_pb2_grpc.ExtractorControllerStub(CHANNEL)
        self.metadata = metadata

    def extract(
            self,
            fileName,
            language='',
            inputType='base64',
            url='',
            base64='',
            pages=0,
            mimeType='application/pdf',
            extractionType='',
            rawJson=False,
            preProcessors=None,
            extractionHints=None,
    ):

        if extractionHints is None:
            extractionHints = []
        if preProcessors is None:
            preProcessors = []
        try:
            request = extractor_pb2.Request(language=language,
                                            inputType=inputType,
                                            fileName=fileName,
                                            url=url,
                                            base64=base64,
                                            pages=pages,
                                            mimeType=mimeType,
                                            extractionType=extractionType,
                                            rawJson=rawJson,
                                            preProcessors=preProcessors,
                                            extractionHints=extractionHints,
                                            )
            response = self.stub.Extractor(request, metadata=self.metadata)
            return json.loads(response.body)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

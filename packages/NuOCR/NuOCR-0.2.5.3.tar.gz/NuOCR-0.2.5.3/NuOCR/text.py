import grpc

from .gRPC_proto.text_processors import text_processor_pb2_grpc, text_processor_pb2
from .channel import CHANNEL


class TextProcessors:
    def __init__(self, metadata, text=''):
        self.stub = text_processor_pb2_grpc.TextProcessorControllerStub(CHANNEL)
        self.metadata = metadata
        self.text = text

    def summarizer(self):
        try:
            request = text_processor_pb2.Request(
                text=self.text,
            )
            response = self.stub.Summarize(request, metadata=self.metadata)
            return response.summary
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def sentiment_analysis(self):
        try:
            request = text_processor_pb2.Request(
                text=self.text,
            )
            response = self.stub.SentimentAnalysis(request, metadata=self.metadata)
            return response.summary
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def cognitive_upload(self, filename, base64):
        try:
            request = text_processor_pb2.Upload(filename=filename, base64=base64)
            self.stub.CognitiveUpload(request, metadata=self.metadata)
            return "File uploaded Successfully!"
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def cognitive_search(self, question, top_k=10):
        try:
            request = text_processor_pb2.SearchRequest(question=question, top_k=top_k)
            response = self.stub.CognitiveSearch(request, metadata=self.metadata)
            return [
                {"index": index+1, "confidence": rec.confidence, "page_number": rec.page_number, "filename": rec.filename}
                for index, rec in enumerate(response)]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

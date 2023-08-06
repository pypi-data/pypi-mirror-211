import json
from .gRPC_proto.preprocessor import preprocessor_pb2, preprocessor_pb2_grpc
from .channel import CHANNEL
import grpc


class Preprocessor:
    def __init__(self, metadata):
        self.stub = preprocessor_pb2_grpc.PreProcessorControllerStub(CHANNEL)
        self.metadata = metadata

    def Image2PDF(self, file_details=None):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.ImagetoPdfRequest(file_details=files)
            response = self.stub.ImagetoPdf(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def PDF2Image(self, file_details=None):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.PdftoImageRequest(file_details=files)
            response = self.stub.PdftoImage(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def image_compress(self, file_details=None, quality=10):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.CompressImageRequest(file_details=files, quality=quality)
            response = self.stub.CompressImage(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def image_crop(self, file_details=None, left=0, top=0, right=10, bottom=10):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.CropImageRequest(file_details=files, left=left, top=top, right=right,
                                                        bottom=bottom)
            response = self.stub.CropImage(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def image_rotate(self, file_details=None, degrees=0):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.RotateImageRequest(file_details=files, rotatedegree=degrees)
            response = self.stub.RotateImage(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def PDF_compress(self, file_details=None):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.CompressPdfRequest(file_details=files)
            response = self.stub.CompressPdf(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def rgb2grey(self, file_details=None):
        if file_details is None:
            file_details = []
        try:
            files = [preprocessor_pb2.file_info(fileName=file['filename'], fileBytes=file['fileBytes'],
                                                mimeType=file["mimeType"]) for file in file_details]
            request = preprocessor_pb2.RGBToGreyRequest(file_details=files)
            response = self.stub.ConvertRGBToGrey(request, metadata=self.metadata)
            return [{"filename": rec.fileName, "bytes": rec.fileBytes, "details": rec.details, "status": rec.status} for
                    rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

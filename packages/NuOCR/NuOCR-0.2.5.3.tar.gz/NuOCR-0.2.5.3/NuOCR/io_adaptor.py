from .channel import CHANNEL
from .gRPC_proto.io_adaptors import io_adaptors_pb2, io_adaptors_pb2_grpc
import grpc


class FTP:
    def __init__(self, metadata, host, port, username, password, isSecure=False):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.isSecure = isSecure

    def inbound(self, remoteFolder, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # FTP Inbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username,
                                                 password=self.password, isSecure=self.isSecure,
                                                 remoteFolder=remoteFolder, file_details=files)
            response = self.stub.FTPInBound(request, metadata=self.metadata)
            return [{"filename": rec.filename, "base64": rec.base64} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def outbound(self, remoteFolder, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # FTP Outbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username,
                                                 password=self.password, isSecure=self.isSecure,
                                                 remoteFolder=remoteFolder, file_details=files)
            response = self.stub.FTPOutBound(request, metadata=self.metadata)
            return [{"filename": rec.filename, "status": rec.status} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove(self, remoteFolder, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # FTP Remove File
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username,
                                                 password=self.password, isSecure=self.isSecure,
                                                 remoteFolder=remoteFolder, file_details=files)
            response = self.stub.FTPRemoveFile(request, metadata=self.metadata)
            return [{"filename": rec.filename, "status": rec.status} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def list_directory(self, remoteFolder, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # FTP List Directories
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username,
                                                 password=self.password, isSecure=self.isSecure,
                                                 remoteFolder=remoteFolder, file_details=files)
            response = self.stub.FTPDirectoryStructure(request, metadata=self.metadata)
            return [rec.directory_path for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))


class S3:
    def __init__(self, metadata, regionName, accessKey, secretKey, bucketName):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.regionName = regionName
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.bucketName = bucketName

    def inbound(self, folderName, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # S3 Inbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey,
                                                secretKey=self.secretKey, bucketName=self.bucketName,
                                                folderName=folderName, file_details=files)
            response = self.stub.S3InBound(request, metadata=self.metadata)
            return [{"filename": rec.filename, "base64": rec.base64} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def outbound(self, folderName, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # S3 Outbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey,
                                                secretKey=self.secretKey, bucketName=self.bucketName,
                                                folderName=folderName, file_details=files)
            response = self.stub.S3OutBound(request, metadata=self.metadata)
            return [{"filename": rec.filename, "status": rec.status} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove(self, folderName, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # S3 Remove File
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey,
                                                secretKey=self.secretKey, bucketName=self.bucketName,
                                                folderName=folderName, file_details=files)
            response = self.stub.S3RemoveFile(request, metadata=self.metadata)
            return [{"filename": rec.filename, "status": rec.status} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def list_directory(self, folderName, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # S3 List Directories
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey,
                                                secretKey=self.secretKey, bucketName=self.bucketName,
                                                folderName=folderName, file_details=files)
            response = self.stub.S3DirectoryStructure(request, metadata=self.metadata)
            return [rec.directory_path for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))


class Blob:
    def __init__(self, metadata, accountName, accountKey, containerName):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.accountName = accountName
        self.accountKey = accountKey
        self.containerName = containerName

    def inbound(self, filepath, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # Blob Inbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.BlobRequest(storageAccountName=self.accountName,
                                                  storageAccountKey=self.accountKey,
                                                  blobContainerName=self.containerName, blobFilepath=filepath,
                                                  file_details=files)
            response = self.stub.BlobInBound(request, metadata=self.metadata)
            return [{"filename": rec.filename, "base64": rec.base64} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def outbound(self, filepath, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # Blob Outbound
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.BlobRequest(storageAccountName=self.accountName,
                                                  storageAccountKey=self.accountKey,
                                                  blobContainerName=self.containerName, blobFilepath=filepath,
                                                  file_details=files)
            response = self.stub.BlobOutBound(request, metadata=self.metadata)
            return [{"filename": rec.blobName, "blobUrl": rec.blobUrl} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove(self, filepath, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # Blob Remove File
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.BlobRequest(storageAccountName=self.accountName,
                                                  storageAccountKey=self.accountKey,
                                                  blobContainerName=self.containerName, blobFilepath=filepath,
                                                  file_details=files)
            response = self.stub.BlobRemoveFiles(request, metadata=self.metadata)
            return [{"filename": rec.filename, "status": rec.status} for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def list_directory(self, filepath, file_details=None):
        if file_details is None:
            file_details = []
        try:
            # Blob List Directories
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.BlobRequest(storageAccountName=self.accountName,
                                                  storageAccountKey=self.accountKey,
                                                  blobContainerName=self.containerName, blobFilepath=filepath,
                                                  file_details=files)
            response = self.stub.BlobDirectoryStructure(request, metadata=self.metadata)
            return [rec.directory_path for rec in response]
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))


class Email:
    def __init__(self, metadata, email_username, email_password, email_server):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.email_username = email_username
        self.email_password = email_password
        self.email_server = email_server

    def inbound(self, email_folder="INBOX", email_filter="UNSEEN"):
        try:
            request = io_adaptors_pb2.EmailOutBoundRequest(email_username=self.email_username,
                                                           email_password=self.email_password,
                                                           email_server=self.email_server, email_folder=email_folder,
                                                           email_filter=email_filter)
            response = self.stub.EmailInBound(request, metadata=self.metadata)
            lst_response = []
            for rec in response:
                res = {"subject": rec.email_subject, "sender": rec.email_sender, "received": rec.email_received,
                       "body": rec.email_body,
                       "attachments": [{"filename": file.filename, "base64": file.base64, "mimeType": file.mimeType} for
                                       file in rec.attachments]}
                lst_response.append(res)
            return lst_response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def outbound(self, email_subject, email_receiver, email_body, file_details=None):
        if file_details is None:
            file_details = []
        try:
            files = [io_adaptors_pb2.file_info(filename=file['filename'], base64=file['base64'],
                                               mimeType=file["mimeType"]) for file in file_details]
            request = io_adaptors_pb2.EmailOutBoundRequest(email_username=self.email_username,
                                                           email_password=self.email_password,
                                                           email_server=self.email_server, email_subject=email_subject,
                                                           email_receiver=email_receiver, email_body=email_body,
                                                           attachments=files)
            response = self.stub.EmailOutBound(request, metadata=self.metadata)
            return response.status
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

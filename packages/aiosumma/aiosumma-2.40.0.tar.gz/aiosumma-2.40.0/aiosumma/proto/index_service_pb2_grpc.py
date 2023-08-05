# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import index_service_pb2 as index__service__pb2


class IndexApiStub(object):
    """Manages indices
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.attach_index = channel.unary_unary(
                '/summa.proto.IndexApi/attach_index',
                request_serializer=index__service__pb2.AttachIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.AttachIndexResponse.FromString,
                )
        self.commit_index = channel.unary_unary(
                '/summa.proto.IndexApi/commit_index',
                request_serializer=index__service__pb2.CommitIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.CommitIndexResponse.FromString,
                )
        self.copy_documents = channel.unary_unary(
                '/summa.proto.IndexApi/copy_documents',
                request_serializer=index__service__pb2.CopyDocumentsRequest.SerializeToString,
                response_deserializer=index__service__pb2.CopyDocumentsResponse.FromString,
                )
        self.create_index = channel.unary_unary(
                '/summa.proto.IndexApi/create_index',
                request_serializer=index__service__pb2.CreateIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.CreateIndexResponse.FromString,
                )
        self.copy_index = channel.unary_unary(
                '/summa.proto.IndexApi/copy_index',
                request_serializer=index__service__pb2.CopyIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.CopyIndexResponse.FromString,
                )
        self.delete_documents = channel.unary_unary(
                '/summa.proto.IndexApi/delete_documents',
                request_serializer=index__service__pb2.DeleteDocumentsRequest.SerializeToString,
                response_deserializer=index__service__pb2.DeleteDocumentsResponse.FromString,
                )
        self.delete_index = channel.unary_unary(
                '/summa.proto.IndexApi/delete_index',
                request_serializer=index__service__pb2.DeleteIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.DeleteIndexResponse.FromString,
                )
        self.documents = channel.unary_stream(
                '/summa.proto.IndexApi/documents',
                request_serializer=index__service__pb2.DocumentsRequest.SerializeToString,
                response_deserializer=index__service__pb2.DocumentsResponse.FromString,
                )
        self.get_indices_aliases = channel.unary_unary(
                '/summa.proto.IndexApi/get_indices_aliases',
                request_serializer=index__service__pb2.GetIndicesAliasesRequest.SerializeToString,
                response_deserializer=index__service__pb2.GetIndicesAliasesResponse.FromString,
                )
        self.get_index = channel.unary_unary(
                '/summa.proto.IndexApi/get_index',
                request_serializer=index__service__pb2.GetIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.GetIndexResponse.FromString,
                )
        self.get_indices = channel.unary_unary(
                '/summa.proto.IndexApi/get_indices',
                request_serializer=index__service__pb2.GetIndicesRequest.SerializeToString,
                response_deserializer=index__service__pb2.GetIndicesResponse.FromString,
                )
        self.index_document_stream = channel.stream_unary(
                '/summa.proto.IndexApi/index_document_stream',
                request_serializer=index__service__pb2.IndexDocumentStreamRequest.SerializeToString,
                response_deserializer=index__service__pb2.IndexDocumentStreamResponse.FromString,
                )
        self.index_document = channel.unary_unary(
                '/summa.proto.IndexApi/index_document',
                request_serializer=index__service__pb2.IndexDocumentRequest.SerializeToString,
                response_deserializer=index__service__pb2.IndexDocumentResponse.FromString,
                )
        self.merge_segments = channel.unary_unary(
                '/summa.proto.IndexApi/merge_segments',
                request_serializer=index__service__pb2.MergeSegmentsRequest.SerializeToString,
                response_deserializer=index__service__pb2.MergeSegmentsResponse.FromString,
                )
        self.set_index_alias = channel.unary_unary(
                '/summa.proto.IndexApi/set_index_alias',
                request_serializer=index__service__pb2.SetIndexAliasRequest.SerializeToString,
                response_deserializer=index__service__pb2.SetIndexAliasResponse.FromString,
                )
        self.vacuum_index = channel.unary_unary(
                '/summa.proto.IndexApi/vacuum_index',
                request_serializer=index__service__pb2.VacuumIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.VacuumIndexResponse.FromString,
                )
        self.warmup_index = channel.unary_unary(
                '/summa.proto.IndexApi/warmup_index',
                request_serializer=index__service__pb2.WarmupIndexRequest.SerializeToString,
                response_deserializer=index__service__pb2.WarmupIndexResponse.FromString,
                )


class IndexApiServicer(object):
    """Manages indices
    """

    def attach_index(self, request, context):
        """Attaches index to Summa server. Attaching allows to incorporate and start using of downloaded or network indices
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def commit_index(self, request, context):
        """Committing all collected writes to the index
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def copy_documents(self, request, context):
        """Copy documents from one index to another
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_index(self, request, context):
        """Creates new index from scratch
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def copy_index(self, request, context):
        """Creates new index from scratch
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_documents(self, request, context):
        """Deletes single document from the index by its primary key (therefore, index must have primary key)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_index(self, request, context):
        """Deletes index and physically removes file in the case of `FileEngine`
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def documents(self, request, context):
        """Stream of all documents from the index
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_indices_aliases(self, request, context):
        """Gets all existing index aliases
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_index(self, request, context):
        """Gets index description
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_indices(self, request, context):
        """Gets all existing index descriptions
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def index_document_stream(self, request_iterator, context):
        """Adds document to the index in a streaming way
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def index_document(self, request, context):
        """Adds document to the index
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def merge_segments(self, request, context):
        """Merges multiple segments into a single one. Used for service purposes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_index_alias(self, request, context):
        """Sets or replaces existing index alias
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def vacuum_index(self, request, context):
        """Removes deletions from all segments
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def warmup_index(self, request, context):
        """Loads all hot parts of the index into the memory
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IndexApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'attach_index': grpc.unary_unary_rpc_method_handler(
                    servicer.attach_index,
                    request_deserializer=index__service__pb2.AttachIndexRequest.FromString,
                    response_serializer=index__service__pb2.AttachIndexResponse.SerializeToString,
            ),
            'commit_index': grpc.unary_unary_rpc_method_handler(
                    servicer.commit_index,
                    request_deserializer=index__service__pb2.CommitIndexRequest.FromString,
                    response_serializer=index__service__pb2.CommitIndexResponse.SerializeToString,
            ),
            'copy_documents': grpc.unary_unary_rpc_method_handler(
                    servicer.copy_documents,
                    request_deserializer=index__service__pb2.CopyDocumentsRequest.FromString,
                    response_serializer=index__service__pb2.CopyDocumentsResponse.SerializeToString,
            ),
            'create_index': grpc.unary_unary_rpc_method_handler(
                    servicer.create_index,
                    request_deserializer=index__service__pb2.CreateIndexRequest.FromString,
                    response_serializer=index__service__pb2.CreateIndexResponse.SerializeToString,
            ),
            'copy_index': grpc.unary_unary_rpc_method_handler(
                    servicer.copy_index,
                    request_deserializer=index__service__pb2.CopyIndexRequest.FromString,
                    response_serializer=index__service__pb2.CopyIndexResponse.SerializeToString,
            ),
            'delete_documents': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_documents,
                    request_deserializer=index__service__pb2.DeleteDocumentsRequest.FromString,
                    response_serializer=index__service__pb2.DeleteDocumentsResponse.SerializeToString,
            ),
            'delete_index': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_index,
                    request_deserializer=index__service__pb2.DeleteIndexRequest.FromString,
                    response_serializer=index__service__pb2.DeleteIndexResponse.SerializeToString,
            ),
            'documents': grpc.unary_stream_rpc_method_handler(
                    servicer.documents,
                    request_deserializer=index__service__pb2.DocumentsRequest.FromString,
                    response_serializer=index__service__pb2.DocumentsResponse.SerializeToString,
            ),
            'get_indices_aliases': grpc.unary_unary_rpc_method_handler(
                    servicer.get_indices_aliases,
                    request_deserializer=index__service__pb2.GetIndicesAliasesRequest.FromString,
                    response_serializer=index__service__pb2.GetIndicesAliasesResponse.SerializeToString,
            ),
            'get_index': grpc.unary_unary_rpc_method_handler(
                    servicer.get_index,
                    request_deserializer=index__service__pb2.GetIndexRequest.FromString,
                    response_serializer=index__service__pb2.GetIndexResponse.SerializeToString,
            ),
            'get_indices': grpc.unary_unary_rpc_method_handler(
                    servicer.get_indices,
                    request_deserializer=index__service__pb2.GetIndicesRequest.FromString,
                    response_serializer=index__service__pb2.GetIndicesResponse.SerializeToString,
            ),
            'index_document_stream': grpc.stream_unary_rpc_method_handler(
                    servicer.index_document_stream,
                    request_deserializer=index__service__pb2.IndexDocumentStreamRequest.FromString,
                    response_serializer=index__service__pb2.IndexDocumentStreamResponse.SerializeToString,
            ),
            'index_document': grpc.unary_unary_rpc_method_handler(
                    servicer.index_document,
                    request_deserializer=index__service__pb2.IndexDocumentRequest.FromString,
                    response_serializer=index__service__pb2.IndexDocumentResponse.SerializeToString,
            ),
            'merge_segments': grpc.unary_unary_rpc_method_handler(
                    servicer.merge_segments,
                    request_deserializer=index__service__pb2.MergeSegmentsRequest.FromString,
                    response_serializer=index__service__pb2.MergeSegmentsResponse.SerializeToString,
            ),
            'set_index_alias': grpc.unary_unary_rpc_method_handler(
                    servicer.set_index_alias,
                    request_deserializer=index__service__pb2.SetIndexAliasRequest.FromString,
                    response_serializer=index__service__pb2.SetIndexAliasResponse.SerializeToString,
            ),
            'vacuum_index': grpc.unary_unary_rpc_method_handler(
                    servicer.vacuum_index,
                    request_deserializer=index__service__pb2.VacuumIndexRequest.FromString,
                    response_serializer=index__service__pb2.VacuumIndexResponse.SerializeToString,
            ),
            'warmup_index': grpc.unary_unary_rpc_method_handler(
                    servicer.warmup_index,
                    request_deserializer=index__service__pb2.WarmupIndexRequest.FromString,
                    response_serializer=index__service__pb2.WarmupIndexResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'summa.proto.IndexApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IndexApi(object):
    """Manages indices
    """

    @staticmethod
    def attach_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/attach_index',
            index__service__pb2.AttachIndexRequest.SerializeToString,
            index__service__pb2.AttachIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def commit_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/commit_index',
            index__service__pb2.CommitIndexRequest.SerializeToString,
            index__service__pb2.CommitIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def copy_documents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/copy_documents',
            index__service__pb2.CopyDocumentsRequest.SerializeToString,
            index__service__pb2.CopyDocumentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/create_index',
            index__service__pb2.CreateIndexRequest.SerializeToString,
            index__service__pb2.CreateIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def copy_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/copy_index',
            index__service__pb2.CopyIndexRequest.SerializeToString,
            index__service__pb2.CopyIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_documents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/delete_documents',
            index__service__pb2.DeleteDocumentsRequest.SerializeToString,
            index__service__pb2.DeleteDocumentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/delete_index',
            index__service__pb2.DeleteIndexRequest.SerializeToString,
            index__service__pb2.DeleteIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def documents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/summa.proto.IndexApi/documents',
            index__service__pb2.DocumentsRequest.SerializeToString,
            index__service__pb2.DocumentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_indices_aliases(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/get_indices_aliases',
            index__service__pb2.GetIndicesAliasesRequest.SerializeToString,
            index__service__pb2.GetIndicesAliasesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/get_index',
            index__service__pb2.GetIndexRequest.SerializeToString,
            index__service__pb2.GetIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_indices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/get_indices',
            index__service__pb2.GetIndicesRequest.SerializeToString,
            index__service__pb2.GetIndicesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def index_document_stream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/summa.proto.IndexApi/index_document_stream',
            index__service__pb2.IndexDocumentStreamRequest.SerializeToString,
            index__service__pb2.IndexDocumentStreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def index_document(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/index_document',
            index__service__pb2.IndexDocumentRequest.SerializeToString,
            index__service__pb2.IndexDocumentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def merge_segments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/merge_segments',
            index__service__pb2.MergeSegmentsRequest.SerializeToString,
            index__service__pb2.MergeSegmentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_index_alias(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/set_index_alias',
            index__service__pb2.SetIndexAliasRequest.SerializeToString,
            index__service__pb2.SetIndexAliasResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def vacuum_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/vacuum_index',
            index__service__pb2.VacuumIndexRequest.SerializeToString,
            index__service__pb2.VacuumIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def warmup_index(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/summa.proto.IndexApi/warmup_index',
            index__service__pb2.WarmupIndexRequest.SerializeToString,
            index__service__pb2.WarmupIndexResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

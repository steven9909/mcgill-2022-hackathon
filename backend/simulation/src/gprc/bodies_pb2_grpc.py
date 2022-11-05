# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import bodies_pb2 as bodies__pb2


class UnaryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Start = channel.unary_unary(
                '/unary.Unary/Start',
                request_serializer=bodies__pb2.EmptyParam.SerializeToString,
                response_deserializer=bodies__pb2.Response.FromString,
                )
        self.Stop = channel.unary_unary(
                '/unary.Unary/Stop',
                request_serializer=bodies__pb2.EmptyParam.SerializeToString,
                response_deserializer=bodies__pb2.Response.FromString,
                )
        self.Pause = channel.unary_unary(
                '/unary.Unary/Pause',
                request_serializer=bodies__pb2.EmptyParam.SerializeToString,
                response_deserializer=bodies__pb2.Response.FromString,
                )
        self.CreatePlanet = channel.unary_unary(
                '/unary.Unary/CreatePlanet',
                request_serializer=bodies__pb2.CreateBodyParam.SerializeToString,
                response_deserializer=bodies__pb2.Response.FromString,
                )
        self.UpdatePlanet = channel.unary_unary(
                '/unary.Unary/UpdatePlanet',
                request_serializer=bodies__pb2.UpdateBodyParam.SerializeToString,
                response_deserializer=bodies__pb2.Response.FromString,
                )


class UnaryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Start(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pause(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreatePlanet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePlanet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UnaryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Start': grpc.unary_unary_rpc_method_handler(
                    servicer.Start,
                    request_deserializer=bodies__pb2.EmptyParam.FromString,
                    response_serializer=bodies__pb2.Response.SerializeToString,
            ),
            'Stop': grpc.unary_unary_rpc_method_handler(
                    servicer.Stop,
                    request_deserializer=bodies__pb2.EmptyParam.FromString,
                    response_serializer=bodies__pb2.Response.SerializeToString,
            ),
            'Pause': grpc.unary_unary_rpc_method_handler(
                    servicer.Pause,
                    request_deserializer=bodies__pb2.EmptyParam.FromString,
                    response_serializer=bodies__pb2.Response.SerializeToString,
            ),
            'CreatePlanet': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePlanet,
                    request_deserializer=bodies__pb2.CreateBodyParam.FromString,
                    response_serializer=bodies__pb2.Response.SerializeToString,
            ),
            'UpdatePlanet': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePlanet,
                    request_deserializer=bodies__pb2.UpdateBodyParam.FromString,
                    response_serializer=bodies__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'unary.Unary', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Unary(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Start(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unary.Unary/Start',
            bodies__pb2.EmptyParam.SerializeToString,
            bodies__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unary.Unary/Stop',
            bodies__pb2.EmptyParam.SerializeToString,
            bodies__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Pause(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unary.Unary/Pause',
            bodies__pb2.EmptyParam.SerializeToString,
            bodies__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreatePlanet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unary.Unary/CreatePlanet',
            bodies__pb2.CreateBodyParam.SerializeToString,
            bodies__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdatePlanet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unary.Unary/UpdatePlanet',
            bodies__pb2.UpdateBodyParam.SerializeToString,
            bodies__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
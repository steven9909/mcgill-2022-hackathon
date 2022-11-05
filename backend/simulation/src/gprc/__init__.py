import grpc

import grpc
from concurrent import futures
import simulation.src.gprc.bodies_pb2_grpc as pb2_grpc
import simulation.src.gprc.bodies_pb2 as pb2


class BodiesService(pb2_grpc.UnaryServicer):
    def __init__(self, *args, **kwargs):
        pass

    def Start(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)

    def Stop(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)

    def Pause(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)

    def Start(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)
    
    def CreateBody(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)

    def UpdateBody(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)

    def DeleteBody(self, request, context):
        result = {'received': True}
        return pb2.Response(**result)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    pb2_grpc.add_UnaryServicer_to_server(BodiesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
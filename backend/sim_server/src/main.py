import grpc
from concurrent import futures
import simulation_pb2_grpc as pb2_grpc
import simulation_pb2 as pb2
from simulation.simulation import Simulator
from simulation.body import Body


class SimulationService(pb2_grpc.SimulationServicer):
    def __init__(self, simulator):
        self.simulator = simulator

    def Start(self, request, context):
        self.simulator.start([])
        result = {"received": True}
        return pb2.Response(**result)

    def Stop(self, request, context):
        self.simulator.stop()
        result = {"received": True}
        return pb2.Response(**result)

    def Pause(self, request, context):
        self.simulator.pause()
        result = {"received": True}
        return pb2.Response(**result)

    def CreateBody(self, request, context):
        self.simulator.add_body(
            Body(
                request.id,
                request.mass,
                request.p_x,
                request.p_y,
                request.v_x,
                request.v_y,
            )
        )
        result = {"received": True}
        return pb2.Response(**result)

    def UpdateBody(self, request, context):
        self.simulator.update_body(
            request.id, request.p_x, request.p_y, request.v_x, request.v_y
        )
        result = {"received": True}
        return pb2.Response(**result)

    def DeleteBody(self, request, context):
        self.simulator.remove_body(request.id)
        result = {"received": True}
        return pb2.Response(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_SimulationServicer_to_server(SimulationService(Simulator()), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

import logging
from concurrent import futures

import grpc
import numpy as np
import simulation_pb2
import simulation_pb2_grpc
from models.body import Body
from simulation.simulation import Simulator


class SimulationService(simulation_pb2_grpc.SimulationServicer):
    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def Start(self, request, context):

        return simulation_pb2.Empty()

    def Pause(self, request, context):

        return simulation_pb2.Empty()

    def Stop(self, request, context):

        return simulation_pb2.Empty()

    def Reset(self, request, context):

        return simulation_pb2.Empty()

    def CreateBody(self, request, context):
        body = Body(
            request.id,
            request.mass,
            np.array([request.position.x, request.position.y]),
            np.array([request.velocity.x, request.velocity.y]),
        )

        return simulation_pb2.Empty()

    def UpdateBody(self, request, context):
        body = Body(
            request.id,
            request.mass,
            np.array([request.position.x, request.position.y]),
            np.array([request.velocity.x, request.velocity.y]),
        )

        return simulation_pb2.Empty()

    def DeleteBody(self, request, context):

        return simulation_pb2.Empty()


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simulation_pb2_grpc.add_SimulationServicer_to_server(
        SimulationService(Simulator()), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

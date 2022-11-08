import logging
from concurrent import futures

import grpc
import numpy as np
import simulation_pb2
import simulation_pb2_grpc
from models.body import Body
from simulation import Simulator


class SimulationService(simulation_pb2_grpc.SimulationServicer):
    def __init__(self, simulator: Simulator):
        self.simulator = simulator

    def Start(self, request, context):
        self.simulator.start()
        return simulation_pb2.Empty()

    def Pause(self, request, context):
        self.simulator.start()
        return simulation_pb2.Empty()

    def Stop(self, request, context):
        self.simulator.stop()
        return simulation_pb2.Empty()

    def CreateBody(self, request, context):
        body = Body(
            request.id,
            request.mass,
            np.array([request.position.x, request.position.y]),
            np.array([request.velocity.x, request.velocity.y]),
        )
        self.simulator.create_body(body)
        return simulation_pb2.Empty()

    def UpdateBody(self, request, context):
        body = Body(
            request.id,
            request.mass,
            np.array([request.position.x, request.position.y])
            if request.position is not None
            else None,
            np.array([request.velocity.x, request.velocity.y])
            if request.velocity is not None
            else None,
        )
        self.simulator.create_body(body)
        return simulation_pb2.Empty()

    def DeleteBody(self, request, context):
        self.simulator.delete_body(request.id)
        return simulation_pb2.Empty()


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simulation_pb2_grpc.add_SimulationServicer_to_server(
        SimulationService(Simulator()), server
    )
    server.add_insecure_port(f"localhost:{port}")
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

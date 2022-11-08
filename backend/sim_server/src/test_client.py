import grpc
import simulation_pb2
import simulation_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        # stub = simulation_pb2_grpc.SimulationStub(channel)
        # response = stub.Start(simulation_pb2.Empty())
        # print(response)

        stub = simulation_pb2_grpc.SimulationStub(channel)
        response = stub.CreateBody(
            simulation_pb2.CreateBodyRequest(
                id=1, mass=100, position={"x": 0, "y": 0}, velocity={"x": 0, "y": 0}
            )
        )
        print(response)


run()

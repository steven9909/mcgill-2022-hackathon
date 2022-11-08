SIM_SERVER_DIR=./sim_server/src/
python3 -m grpc_tools.protoc -I./protos --python_out=$SIM_SERVER_DIR --pyi_out=$SIM_SERVER_DIR --grpc_python_out=$SIM_SERVER_DIR ./protos/simulation.proto
cd $SIM_SERVER_DIR && python3 main.py 
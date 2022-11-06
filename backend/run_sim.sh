SIM_SERVER=./sim_server/src/
python -m grpc_tools.protoc -I./protos --python_out=$SIM_SERVER --pyi_out=$SIM_SERVER --grpc_python_out=$SIM_SERVER ./protos/simulation.proto
cd $SIM_SERVER && python main.py 
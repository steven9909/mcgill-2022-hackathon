API_SERVER_DIR=./api_server/src/
python3 -m grpc_tools.protoc -I./protos --python_out=$API_SERVER_DIR --pyi_out=$API_SERVER_DIR --grpc_python_out=$API_SERVER_DIR ./protos/simulation.proto
cd $API_SERVER_DIR && python3 main.py
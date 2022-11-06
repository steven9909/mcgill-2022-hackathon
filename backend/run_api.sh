API_SERVER=./api_server/src/
python3 -m grpc_tools.protoc -I./protos --python_out=$API_SERVER --pyi_out=$API_SERVER --grpc_python_out=$API_SERVER ./protos/simulation.proto
uvicorn main:app --app-dir api_server/src --host 0.0.0.0 --reload


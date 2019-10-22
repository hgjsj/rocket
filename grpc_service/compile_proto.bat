cd C:\my_project\rocket\grpc_service
c:\python36\python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ services.proto
pause
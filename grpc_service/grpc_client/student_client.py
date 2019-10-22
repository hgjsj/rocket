import grpc
import time
#import services_pb2_grpc
#import services_pb2

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    services_pb2_grpc = __import__('services_pb2_grpc')
    services_pb2 = __import__('services_pb2')
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = getattr(services_pb2_grpc, 'StutdentsServiceStub')(channel)
        students = getattr(stub, 'GetStudentsByArray')(getattr(services_pb2,'EmptyRequest')())
        #stub = services_pb2_grpc.StutdentsServiceStub(channel)
        #student = stub.GetStudentInfo(services_pb2.StudentRequest(name="sutton"))
        #print ('%s %d %s' % (student.name, student.age, student.phone))
        #students = stub.GetStudentsByArray(getattr(services_pb2,'EmptyRequest')())
        print (students.count)
        for item in students.members:
            print('%s %d %s' % (item.name, item.age, item.phone))
        
        filters = [ {'key': 'phone','value': '12345678'}]
        request_itereator = (services_pb2.StudentFilter(key=filter['key'],value=filter['value']) for filter in filters)

        for ret in stub.GetSpecifyStudents(request_itereator):
            print('%s %d %s' % (ret.name, ret.age, ret.phone))
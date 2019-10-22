from concurrent import futures
import grpc
import time
import json
import services_pb2_grpc
import services_pb2


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
class Student(services_pb2_grpc.StutdentsServiceServicer):
    def __init__(self):
        with open('data.pb', 'rb') as f:
            unmarshal = services_pb2.Studentlist()
            unmarshal.ParseFromString(f.read())
            self.student_list = [{'name': st.name, 'age': st.age, 'phone': st.phone} for st in unmarshal.members]

    def GetStudentInfo(self, request, context):
        st = [item for item in self.student_list if request.name == item['name']]
        if len(st) > 0:
            return services_pb2.StudentInfo(name=st[0]['name'], age=st[0]['age'], phone=st[0]['phone'])
        else:
            return {}

    def GetStudentList(self, request, context):
        for st in self.student_list:
            yield services_pb2.StudentInfo(name=st['name'], age=st['age'], phone=st['phone'])
    
    def GetStudentsByArray(self, request, context):
        members = []
        for st in self.student_list:
            members.append(services_pb2.StudentInfo(name=st['name'], age=st['age'], phone=st['phone']))
        return services_pb2.Studentlist(count=len(members), members=members)

    def GetSpecifyStudents(self, request_iterator, context):
        ret_student = self.student_list
        for filter in request_iterator:
            ret_student = [item for item in ret_student if item[filter.key] == filter.value]
        
        for st in ret_student:
            print (st['name'])
            yield services_pb2.StudentInfo(name=st['name'], age=st['age'], phone=st['phone'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_StutdentsServiceServicer_to_server(Student(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
import services_pb2

if __name__ == '__main__':
    student_list = services_pb2.Studentlist()
    
    data_depot =[
                    {
                        "name": "sutton",
                        "age": 38,
                        "phone": "12345678"
                    },
                    {
                        "name": "vanessa",
                        "age": 36,
                        "phone": "12345678"
                    },
                    {
                        "name": "steven",
                        "age": 8,
                        "phone": "12345678"
                    }
                ]
    for item in data_depot:
        each_student = student_list.members.add()
        each_student.name = item['name']
        each_student.age = item['age']
        each_student.phone = item['phone']
    student_list.count = len(student_list.members)
    with open('data.pb','wb') as f:
        f.write(student_list.SerializeToString())
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import services_pb2 as services__pb2


class StutdentsServiceStub(object):
  """The greeting service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetStudentInfo = channel.unary_unary(
        '/student.StutdentsService/GetStudentInfo',
        request_serializer=services__pb2.StudentRequest.SerializeToString,
        response_deserializer=services__pb2.StudentInfo.FromString,
        )
    self.GetStudentList = channel.unary_stream(
        '/student.StutdentsService/GetStudentList',
        request_serializer=services__pb2.EmptyRequest.SerializeToString,
        response_deserializer=services__pb2.StudentInfo.FromString,
        )
    self.GetStudentsByArray = channel.unary_unary(
        '/student.StutdentsService/GetStudentsByArray',
        request_serializer=services__pb2.EmptyRequest.SerializeToString,
        response_deserializer=services__pb2.Studentlist.FromString,
        )
    self.GetSpecifyStudents = channel.stream_stream(
        '/student.StutdentsService/GetSpecifyStudents',
        request_serializer=services__pb2.StudentFilter.SerializeToString,
        response_deserializer=services__pb2.StudentInfo.FromString,
        )


class StutdentsServiceServicer(object):
  """The greeting service definition.
  """

  def GetStudentInfo(self, request, context):
    """Sends a greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetStudentList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetStudentsByArray(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSpecifyStudents(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_StutdentsServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetStudentInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetStudentInfo,
          request_deserializer=services__pb2.StudentRequest.FromString,
          response_serializer=services__pb2.StudentInfo.SerializeToString,
      ),
      'GetStudentList': grpc.unary_stream_rpc_method_handler(
          servicer.GetStudentList,
          request_deserializer=services__pb2.EmptyRequest.FromString,
          response_serializer=services__pb2.StudentInfo.SerializeToString,
      ),
      'GetStudentsByArray': grpc.unary_unary_rpc_method_handler(
          servicer.GetStudentsByArray,
          request_deserializer=services__pb2.EmptyRequest.FromString,
          response_serializer=services__pb2.Studentlist.SerializeToString,
      ),
      'GetSpecifyStudents': grpc.stream_stream_rpc_method_handler(
          servicer.GetSpecifyStudents,
          request_deserializer=services__pb2.StudentFilter.FromString,
          response_serializer=services__pb2.StudentInfo.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'student.StutdentsService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

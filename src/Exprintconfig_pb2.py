#!/usr/bin/python2.4
# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2



_EXPRINTCONFIG_EXPRINT = descriptor.Descriptor(
  name='Exprint',
  full_name='exprint.Exprintconfig.Exprint',
  filename='Exprintconfig.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='subjectcode', full_name='exprint.Exprintconfig.Exprint.subjectcode', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='paralell', full_name='exprint.Exprintconfig.Exprint.paralell', index=1,
      number=5, type=9, cpp_type=9, label=1,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='solutions', full_name='exprint.Exprintconfig.Exprint.solutions', index=2,
      number=3, type=8, cpp_type=7, label=1,
      default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)

_EXPRINTCONFIG = descriptor.Descriptor(
  name='Exprintconfig',
  full_name='exprint.Exprintconfig',
  filename='Exprintconfig.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='exprints', full_name='exprint.Exprintconfig.exprints', index=0,
      number=1, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='printer', full_name='exprint.Exprintconfig.printer', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EXPRINTSERVERSETCONFIGRESPONSE = descriptor.Descriptor(
  name='ExprintserverSetConfigResponse',
  full_name='exprint.ExprintserverSetConfigResponse',
  filename='Exprintconfig.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='responsecode', full_name='exprint.ExprintserverSetConfigResponse.responsecode', index=0,
      number=1, type=9, cpp_type=9, label=1,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_VOID = descriptor.Descriptor(
  name='Void',
  full_name='exprint.Void',
  filename='Exprintconfig.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EXPRINTCONFIG.fields_by_name['exprints'].message_type = _EXPRINTCONFIG_EXPRINT

class Exprintconfig(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Exprint(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _EXPRINTCONFIG_EXPRINT
  DESCRIPTOR = _EXPRINTCONFIG

class ExprintserverSetConfigResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EXPRINTSERVERSETCONFIGRESPONSE

class Void(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VOID


_EXPRINTSERVER = descriptor.ServiceDescriptor(
  name='Exprintserver',
  full_name='exprint.Exprintserver',
  index=0,
  options=None,
  methods=[
  descriptor.MethodDescriptor(
    name='get_config',
    full_name='exprint.Exprintserver.get_config',
    index=0,
    containing_service=None,
    input_type=_VOID,
    output_type=_EXPRINTCONFIG,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='reset_config',
    full_name='exprint.Exprintserver.reset_config',
    index=1,
    containing_service=None,
    input_type=_VOID,
    output_type=_VOID,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='set_config',
    full_name='exprint.Exprintserver.set_config',
    index=2,
    containing_service=None,
    input_type=_EXPRINTCONFIG,
    output_type=_EXPRINTSERVERSETCONFIGRESPONSE,
    options=None,
  ),
])

class Exprintserver(service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _EXPRINTSERVER
class Exprintserver_Stub(Exprintserver):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _EXPRINTSERVER

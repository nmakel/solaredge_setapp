# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device_manager.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='device_manager.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x14\x64\x65vice_manager.proto\"\x0f\n\rDeviceManagerb\x06proto3')
)




_DEVICEMANAGER = _descriptor.Descriptor(
  name='DeviceManager',
  full_name='DeviceManager',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=39,
)

DESCRIPTOR.message_types_by_name['DeviceManager'] = _DEVICEMANAGER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeviceManager = _reflection.GeneratedProtocolMessageType('DeviceManager', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEMANAGER,
  __module__ = 'device_manager_pb2'
  # @@protoc_insertion_point(class_scope:DeviceManager)
  ))
_sym_db.RegisterMessage(DeviceManager)


# @@protoc_insertion_point(module_scope)

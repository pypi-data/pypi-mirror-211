# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dag_pb.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x64\x61g_pb.proto\x12\x06\x64\x61g_pb\"`\n\x06PBLink\x12\x11\n\x04hash\x18\x01 \x01(\x0cH\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x13\n\x06t_size\x18\x03 \x01(\x04H\x02\x88\x01\x01\x42\x07\n\x05_hashB\x07\n\x05_nameB\t\n\x07_t_size\"C\n\x06PBNode\x12\x1d\n\x05links\x18\x02 \x03(\x0b\x32\x0e.dag_pb.PBLink\x12\x11\n\x04\x64\x61ta\x18\x01 \x01(\x0cH\x00\x88\x01\x01\x42\x07\n\x05_datab\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dag_pb_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PBLINK._serialized_start=24
  _PBLINK._serialized_end=120
  _PBNODE._serialized_start=122
  _PBNODE._serialized_end=189
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: network_policy.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14network_policy.proto\x12\x08\x63z.proto\"=\n\rNetworkPolicy\x12,\n\x07\x63ontent\x18\x01 \x01(\x0b\x32\x1b.cz.proto.NetworkPolicyData\"j\n\x11NetworkPolicyData\x12\x15\n\rworkspaceList\x18\x01 \x03(\t\x12\x14\n\x0cusernameList\x18\x02 \x03(\t\x12\x13\n\x0b\x62lockedList\x18\x03 \x03(\t\x12\x13\n\x0b\x61llowedList\x18\x04 \x03(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'network_policy_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NETWORKPOLICY._serialized_start=34
  _NETWORKPOLICY._serialized_end=95
  _NETWORKPOLICYDATA._serialized_start=97
  _NETWORKPOLICYDATA._serialized_end=203
# @@protoc_insertion_point(module_scope)

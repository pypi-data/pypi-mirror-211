# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rm_app_meta.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11rm_app_meta.proto\x12\x11\x63om.clickzetta.rm\"\xaa\x02\n\tRMAppMeta\x12\x13\n\x06\x61pp_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x15\n\x08\x61pp_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x15\n\x08priority\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x12\n\x05vc_id\x18\x04 \x01(\x03H\x03\x88\x01\x01\x12\x35\n\tapp_state\x18\x05 \x01(\x0e\x32\x1d.com.clickzetta.rm.RMAppStateH\x04\x88\x01\x01\x12\x18\n\x0bsubmit_time\x18\x06 \x01(\x03H\x05\x88\x01\x01\x12\x18\n\x0b\x66inish_time\x18\x07 \x01(\x03H\x06\x88\x01\x01\x42\t\n\x07_app_idB\x0b\n\t_app_nameB\x0b\n\t_priorityB\x08\n\x06_vc_idB\x0c\n\n_app_stateB\x0e\n\x0c_submit_timeB\x0e\n\x0c_finish_time*G\n\nRMAppState\x12\x12\n\x0eRM_APP_RUNNING\x10\x00\x12\x12\n\x0eRM_APP_SUCCESS\x10\x01\x12\x11\n\rRM_APP_FAILED\x10\x02\x42(\n\x17\x63om.clickzetta.rm.protoB\x0bRMAppProtosP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rm_app_meta_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027com.clickzetta.rm.protoB\013RMAppProtosP\001'
  _RMAPPSTATE._serialized_start=341
  _RMAPPSTATE._serialized_end=412
  _RMAPPMETA._serialized_start=41
  _RMAPPMETA._serialized_end=339
# @@protoc_insertion_point(module_scope)

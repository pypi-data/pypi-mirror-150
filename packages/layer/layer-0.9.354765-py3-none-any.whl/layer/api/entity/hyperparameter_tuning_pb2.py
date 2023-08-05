# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/entity/hyperparameter_tuning.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layer.api import ids_pb2 as api_dot_ids__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&api/entity/hyperparameter_tuning.proto\x12\x03\x61pi\x1a\rapi/ids.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb2\x05\n\x14HyperparameterTuning\x12\'\n\x02id\x18\x01 \x01(\x0b\x32\x1b.api.HyperparameterTuningId\x12\x1e\n\x08model_id\x18\x02 \x01(\x0b\x32\x0c.api.ModelId\x12-\n\x10model_version_id\x18\x03 \x01(\x0b\x32\x13.api.ModelVersionId\x12\x1c\n\x07user_id\x18\x04 \x01(\x0b\x32\x0b.api.UserId\x12,\n\x0forganization_id\x18\x05 \x01(\x0b\x32\x13.api.OrganizationId\x12\x0c\n\x04\x64\x61ta\x18\x06 \x01(\t\x12\x30\n\x15output_model_train_id\x18\x07 \x01(\x0b\x32\x11.api.ModelTrainId\x12\x30\n\x06status\x18\x08 \x01(\x0e\x32 .api.HyperparameterTuning.Status\x12\x30\n\x0c\x63reated_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0cstarted_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rfinished_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bstatus_info\x18\x0c \x01(\t\"\xb7\x01\n\x06Status\x12\x12\n\x0eSTATUS_INVALID\x10\x00\x12\x12\n\x0eSTATUS_PENDING\x10\x01\x12\x12\n\x0eSTATUS_RUNNING\x10\x02\x12\x13\n\x0fSTATUS_FINISHED\x10\x03\x12\x11\n\rSTATUS_FAILED\x10\x04\x12\x17\n\x13STATUS_INITIALIZING\x10\x05\x12\x1b\n\x17STATUS_CANCEL_REQUESTED\x10\x06\x12\x13\n\x0fSTATUS_CANCELED\x10\x07\x42\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_HYPERPARAMETERTUNING = DESCRIPTOR.message_types_by_name['HyperparameterTuning']
_HYPERPARAMETERTUNING_STATUS = _HYPERPARAMETERTUNING.enum_types_by_name['Status']
HyperparameterTuning = _reflection.GeneratedProtocolMessageType('HyperparameterTuning', (_message.Message,), {
  'DESCRIPTOR' : _HYPERPARAMETERTUNING,
  '__module__' : 'api.entity.hyperparameter_tuning_pb2'
  # @@protoc_insertion_point(class_scope:api.HyperparameterTuning)
  })
_sym_db.RegisterMessage(HyperparameterTuning)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _HYPERPARAMETERTUNING._serialized_start=96
  _HYPERPARAMETERTUNING._serialized_end=786
  _HYPERPARAMETERTUNING_STATUS._serialized_start=603
  _HYPERPARAMETERTUNING_STATUS._serialized_end=786
# @@protoc_insertion_point(module_scope)

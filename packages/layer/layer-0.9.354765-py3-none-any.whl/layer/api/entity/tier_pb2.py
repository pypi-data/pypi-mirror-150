# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/entity/tier.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layer.api import ids_pb2 as api_dot_ids__pb2
from layer.api.value import tier_type_pb2 as api_dot_value_dot_tier__type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61pi/entity/tier.proto\x12\x03\x61pi\x1a\rapi/ids.proto\x1a\x19\x61pi/value/tier_type.proto\"c\n\x04Tier\x12\x17\n\x02id\x18\x01 \x01(\x0b\x32\x0b.api.TierId\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1b\n\x04type\x18\x03 \x01(\x0e\x32\r.api.TierType\x12\x17\n\x0fmax_active_runs\x18\x04 \x01(\x05\x42\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_TIER = DESCRIPTOR.message_types_by_name['Tier']
Tier = _reflection.GeneratedProtocolMessageType('Tier', (_message.Message,), {
  'DESCRIPTOR' : _TIER,
  '__module__' : 'api.entity.tier_pb2'
  # @@protoc_insertion_point(class_scope:api.Tier)
  })
_sym_db.RegisterMessage(Tier)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _TIER._serialized_start=72
  _TIER._serialized_end=171
# @@protoc_insertion_point(module_scope)

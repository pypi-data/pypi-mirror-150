# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/value/big_decimal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x61pi/value/big_decimal.proto\x12\x03\x61pi\"*\n\nBigDecimal\x12\r\n\x05scale\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x0c\x42\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_BIGDECIMAL = DESCRIPTOR.message_types_by_name['BigDecimal']
BigDecimal = _reflection.GeneratedProtocolMessageType('BigDecimal', (_message.Message,), {
  'DESCRIPTOR' : _BIGDECIMAL,
  '__module__' : 'api.value.big_decimal_pb2'
  # @@protoc_insertion_point(class_scope:api.BigDecimal)
  })
_sym_db.RegisterMessage(BigDecimal)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _BIGDECIMAL._serialized_start=36
  _BIGDECIMAL._serialized_end=78
# @@protoc_insertion_point(module_scope)

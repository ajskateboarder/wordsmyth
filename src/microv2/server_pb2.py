# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\x12\nmodelsuite\"\x16\n\x05texts\x12\r\n\x05texts\x18\x01 \x03(\t\"\x18\n\x06\x65mojis\x12\x0e\n\x06\x65mojis\x18\x01 \x03(\t\" \n\nsentiments\x12\x12\n\nsentiments\x18\x01 \x03(\t2u\n\x05Model\x12\x34\n\ttorchmoji\x12\x11.modelsuite.texts\x1a\x12.modelsuite.emojis\"\x00\x12\x36\n\x07roberta\x12\x11.modelsuite.texts\x1a\x16.modelsuite.sentiments\"\x00\x62\x06proto3')



_TEXTS = DESCRIPTOR.message_types_by_name['texts']
_EMOJIS = DESCRIPTOR.message_types_by_name['emojis']
_SENTIMENTS = DESCRIPTOR.message_types_by_name['sentiments']
texts = _reflection.GeneratedProtocolMessageType('texts', (_message.Message,), {
  'DESCRIPTOR' : _TEXTS,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:modelsuite.texts)
  })
_sym_db.RegisterMessage(texts)

emojis = _reflection.GeneratedProtocolMessageType('emojis', (_message.Message,), {
  'DESCRIPTOR' : _EMOJIS,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:modelsuite.emojis)
  })
_sym_db.RegisterMessage(emojis)

sentiments = _reflection.GeneratedProtocolMessageType('sentiments', (_message.Message,), {
  'DESCRIPTOR' : _SENTIMENTS,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:modelsuite.sentiments)
  })
_sym_db.RegisterMessage(sentiments)

_MODEL = DESCRIPTOR.services_by_name['Model']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TEXTS._serialized_start=28
  _TEXTS._serialized_end=50
  _EMOJIS._serialized_start=52
  _EMOJIS._serialized_end=76
  _SENTIMENTS._serialized_start=78
  _SENTIMENTS._serialized_end=110
  _MODEL._serialized_start=112
  _MODEL._serialized_end=229
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/administration/v0/users/user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'qwak/administration/v0/users/user.proto\x12\x18qwak.administration.user\x1a\x1fgoogle/protobuf/timestamp.proto\"\x8f\x03\n\x0cQwakUserSpec\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x39\n\tuser_kind\x18\x03 \x01(\x0e\x32&.qwak.administration.user.QwakUserKind\x12\x38\n\x06status\x18\x04 \x01(\x0e\x32(.qwak.administration.user.QwakUserStatus\x12\x43\n\x0cjob_function\x18\x05 \x01(\x0e\x32-.qwak.administration.user.QwakUserJobFunction\x12=\n\tjob_level\x18\x06 \x01(\x0e\x32*.qwak.administration.user.QwakUserJobLevel\x12.\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10last_modified_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"Y\n\x08QwakUser\x12\x34\n\x04spec\x18\x01 \x01(\x0b\x32&.qwak.administration.user.QwakUserSpec\x12\x17\n\x0f\x65nvironment_ids\x18\x02 \x03(\t*[\n\x0eQwakUserStatus\x12\x17\n\x13USER_STATUS_INVALID\x10\x00\x12\x16\n\x12USER_STATUS_ACTIVE\x10\x01\x12\x18\n\x14USER_STATUS_DISABLED\x10\x02*\xcb\x01\n\x13QwakUserJobFunction\x12\x18\n\x14JOB_FUNCTION_INVALID\x10\x00\x12\x1e\n\x1aJOB_FUNCTION_DATA_ENGINEER\x10\x01\x12\x1f\n\x1bJOB_FUNCTION_DATA_SCIENTIST\x10\x02\x12\x1c\n\x18JOB_FUNCTION_ML_ENGINEER\x10\x03\x12\x17\n\x13JOB_FUNCTION_DEVOPS\x10\x04\x12\"\n\x1eJOB_FUNCTION_SOFTWARE_ENGINEER\x10\x05*\xc5\x01\n\x10QwakUserJobLevel\x12\x15\n\x11JOB_LEVEL_INVALID\x10\x00\x12$\n JOB_LEVEL_INDIVIDUAL_CONTRIBUTOR\x10\x01\x12\x17\n\x13JOB_LEVEL_ARCHITECT\x10\x02\x12\x15\n\x11JOB_LEVEL_MANAGER\x10\x03\x12\x16\n\x12JOB_LEVEL_DIRECTOR\x10\x04\x12\x15\n\x11JOB_LEVEL_P_OR_VP\x10\x05\x12\x15\n\x11JOB_LEVEL_C_LEVEL\x10\x06*\xd5\x01\n\x0cQwakUserKind\x12\x15\n\x11USER_KIND_INVALID\x10\x00\x12\x1e\n\x1aUSER_KIND_QWAK_SIMPLE_USER\x10\x01\x12\x18\n\x14USER_KIND_QWAK_ADMIN\x10\x02\x12+\n#USER_KIND_QWAK_SERVICE_ACCOUNT_CORE\x10\x03\x1a\x02\x08\x01\x12+\n#USER_KIND_QWAK_SERVICE_ACCOUNT_EDGE\x10\x04\x1a\x02\x08\x01\x12\x1a\n\x16USER_KIND_QWAK_SUPPORT\x10\x05*\\\n\x0fQwakAccountRole\x12\x18\n\x14\x41\x43\x43OUNT_ROLE_INVALID\x10\x00\x12\x16\n\x12\x41\x43\x43OUNT_ROLE_ADMIN\x10\x01\x12\x17\n\x13\x41\x43\x43OUNT_ROLE_MEMBER\x10\x02\x42\xa5\x01\n\x1e\x63om.qwak.ai.administration.apiP\x01Z\x80\x01github.com/qwak-ai/qwak-platform/services/core/java/user-management/user-management-api/pb/qwak/administration/v0/users;users_v0b\x06proto3')

_QWAKUSERSTATUS = DESCRIPTOR.enum_types_by_name['QwakUserStatus']
QwakUserStatus = enum_type_wrapper.EnumTypeWrapper(_QWAKUSERSTATUS)
_QWAKUSERJOBFUNCTION = DESCRIPTOR.enum_types_by_name['QwakUserJobFunction']
QwakUserJobFunction = enum_type_wrapper.EnumTypeWrapper(_QWAKUSERJOBFUNCTION)
_QWAKUSERJOBLEVEL = DESCRIPTOR.enum_types_by_name['QwakUserJobLevel']
QwakUserJobLevel = enum_type_wrapper.EnumTypeWrapper(_QWAKUSERJOBLEVEL)
_QWAKUSERKIND = DESCRIPTOR.enum_types_by_name['QwakUserKind']
QwakUserKind = enum_type_wrapper.EnumTypeWrapper(_QWAKUSERKIND)
_QWAKACCOUNTROLE = DESCRIPTOR.enum_types_by_name['QwakAccountRole']
QwakAccountRole = enum_type_wrapper.EnumTypeWrapper(_QWAKACCOUNTROLE)
USER_STATUS_INVALID = 0
USER_STATUS_ACTIVE = 1
USER_STATUS_DISABLED = 2
JOB_FUNCTION_INVALID = 0
JOB_FUNCTION_DATA_ENGINEER = 1
JOB_FUNCTION_DATA_SCIENTIST = 2
JOB_FUNCTION_ML_ENGINEER = 3
JOB_FUNCTION_DEVOPS = 4
JOB_FUNCTION_SOFTWARE_ENGINEER = 5
JOB_LEVEL_INVALID = 0
JOB_LEVEL_INDIVIDUAL_CONTRIBUTOR = 1
JOB_LEVEL_ARCHITECT = 2
JOB_LEVEL_MANAGER = 3
JOB_LEVEL_DIRECTOR = 4
JOB_LEVEL_P_OR_VP = 5
JOB_LEVEL_C_LEVEL = 6
USER_KIND_INVALID = 0
USER_KIND_QWAK_SIMPLE_USER = 1
USER_KIND_QWAK_ADMIN = 2
USER_KIND_QWAK_SERVICE_ACCOUNT_CORE = 3
USER_KIND_QWAK_SERVICE_ACCOUNT_EDGE = 4
USER_KIND_QWAK_SUPPORT = 5
ACCOUNT_ROLE_INVALID = 0
ACCOUNT_ROLE_ADMIN = 1
ACCOUNT_ROLE_MEMBER = 2


_QWAKUSERSPEC = DESCRIPTOR.message_types_by_name['QwakUserSpec']
_QWAKUSER = DESCRIPTOR.message_types_by_name['QwakUser']
QwakUserSpec = _reflection.GeneratedProtocolMessageType('QwakUserSpec', (_message.Message,), {
  'DESCRIPTOR' : _QWAKUSERSPEC,
  '__module__' : 'qwak.administration.v0.users.user_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.user.QwakUserSpec)
  })
_sym_db.RegisterMessage(QwakUserSpec)

QwakUser = _reflection.GeneratedProtocolMessageType('QwakUser', (_message.Message,), {
  'DESCRIPTOR' : _QWAKUSER,
  '__module__' : 'qwak.administration.v0.users.user_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.user.QwakUser)
  })
_sym_db.RegisterMessage(QwakUser)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.qwak.ai.administration.apiP\001Z\200\001github.com/qwak-ai/qwak-platform/services/core/java/user-management/user-management-api/pb/qwak/administration/v0/users;users_v0'
  _QWAKUSERKIND.values_by_name["USER_KIND_QWAK_SERVICE_ACCOUNT_CORE"]._options = None
  _QWAKUSERKIND.values_by_name["USER_KIND_QWAK_SERVICE_ACCOUNT_CORE"]._serialized_options = b'\010\001'
  _QWAKUSERKIND.values_by_name["USER_KIND_QWAK_SERVICE_ACCOUNT_EDGE"]._options = None
  _QWAKUSERKIND.values_by_name["USER_KIND_QWAK_SERVICE_ACCOUNT_EDGE"]._serialized_options = b'\010\001'
  _QWAKUSERSTATUS._serialized_start=595
  _QWAKUSERSTATUS._serialized_end=686
  _QWAKUSERJOBFUNCTION._serialized_start=689
  _QWAKUSERJOBFUNCTION._serialized_end=892
  _QWAKUSERJOBLEVEL._serialized_start=895
  _QWAKUSERJOBLEVEL._serialized_end=1092
  _QWAKUSERKIND._serialized_start=1095
  _QWAKUSERKIND._serialized_end=1308
  _QWAKACCOUNTROLE._serialized_start=1310
  _QWAKACCOUNTROLE._serialized_end=1402
  _QWAKUSERSPEC._serialized_start=103
  _QWAKUSERSPEC._serialized_end=502
  _QWAKUSER._serialized_start=504
  _QWAKUSER._serialized_end=593
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/ecosystem/v0/ecosystem.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from _qwak_proto.qwak.administration.account.v1 import preferences_pb2 as qwak_dot_administration_dot_account_dot_v1_dot_preferences__pb2
from _qwak_proto.qwak.administration.account.v1 import account_pb2 as qwak_dot_administration_dot_account_dot_v1_dot_account__pb2
from _qwak_proto.qwak.administration.v0.environments import configuration_pb2 as qwak_dot_administration_dot_v0_dot_environments_dot_configuration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!qwak/ecosystem/v0/ecosystem.proto\x12\x11qwak.ecosystem.v0\x1a\x30qwak/administration/account/v1/preferences.proto\x1a,qwak/administration/account/v1/account.proto\x1a\x37qwak/administration/v0/environments/configuration.proto\"<\n\x16UsernamePasswordMethod\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"(\n\x10QwakApiKeyMethod\x12\x14\n\x0cqwak_api_key\x18\x01 \x01(\t\"\\\n\x18\x41uthenticatedUserContext\x12@\n\x04user\x18\x01 \x01(\x0b\x32\x32.qwak.ecosystem.v0.AuthenticatedUnifiedUserContext\"y\n\x1f\x41uthenticatedUnifiedUserContext\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x45\n\x0f\x61\x63\x63ount_details\x18\x05 \x01(\x0b\x32,.qwak.ecosystem.v0.UserContextAccountDetails\"\xfe\x04\n\x19UserContextAccountDetails\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1e\n\x16\x64\x65\x66\x61ult_environment_id\x18\x03 \x01(\t\x12\x44\n\x0bpreferences\x18\x05 \x01(\x0b\x32/.qwak.administration.account.AccountPreferences\x12\\\n\x11\x65nvironment_by_id\x18\x04 \x03(\x0b\x32\x41.qwak.ecosystem.v0.UserContextAccountDetails.EnvironmentByIdEntry\x12t\n\x1euser_context_environment_by_id\x18\x06 \x03(\x0b\x32L.qwak.ecosystem.v0.UserContextAccountDetails.UserContextEnvironmentByIdEntry\x12\x39\n\x04type\x18\x07 \x01(\x0e\x32+.qwak.administration.account.v1.AccountType\x1a]\n\x14\x45nvironmentByIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.qwak.ecosystem.v0.EnvironmentDetails:\x02\x38\x01\x1as\n\x1fUserContextEnvironmentByIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12?\n\x05value\x18\x02 \x01(\x0b\x32\x30.qwak.ecosystem.v0.UserContextEnvironmentDetails:\x02\x38\x01\"\x1f\n\x1dUserContextEnvironmentDetails\"\x80\x03\n\x0e\x41\x63\x63ountDetails\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x44\n\x0bpreferences\x18\x03 \x01(\x0b\x32/.qwak.administration.account.AccountPreferences\x12\x1e\n\x16\x64\x65\x66\x61ult_environment_id\x18\x05 \x01(\t\x12S\n\x12\x65nvironments_by_id\x18\x04 \x03(\x0b\x32\x37.qwak.ecosystem.v0.AccountDetails.EnvironmentsByIdEntry\x12\x39\n\x04type\x18\x06 \x01(\x0e\x32+.qwak.administration.account.v1.AccountType\x1a^\n\x15\x45nvironmentsByIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.qwak.ecosystem.v0.EnvironmentDetails:\x02\x38\x01\"\x84\x01\n\x12\x45nvironmentDetails\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12T\n\rconfiguration\x18\x03 \x01(\x0b\x32=.qwak.administration.environment.QwakEnvironmentConfiguration\"\xde\x01\n\x0fUserAccountList\x12\x1a\n\x12\x64\x65\x66\x61ult_account_id\x18\x01 \x01(\t\x12L\n\x0e\x61\x63\x63ounts_by_id\x18\x02 \x03(\x0b\x32\x34.qwak.ecosystem.v0.UserAccountList.AccountsByIdEntry\x1a\x61\n\x11\x41\x63\x63ountsByIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12;\n\x05value\x18\x02 \x01(\x0b\x32,.qwak.ecosystem.v0.UserContextAccountDetails:\x02\x38\x01\x42\x30\n\x1c\x63om.qwak.ai.common.ecosystemP\x01Z\x0e.;ecosystem_v0b\x06proto3')



_USERNAMEPASSWORDMETHOD = DESCRIPTOR.message_types_by_name['UsernamePasswordMethod']
_QWAKAPIKEYMETHOD = DESCRIPTOR.message_types_by_name['QwakApiKeyMethod']
_AUTHENTICATEDUSERCONTEXT = DESCRIPTOR.message_types_by_name['AuthenticatedUserContext']
_AUTHENTICATEDUNIFIEDUSERCONTEXT = DESCRIPTOR.message_types_by_name['AuthenticatedUnifiedUserContext']
_USERCONTEXTACCOUNTDETAILS = DESCRIPTOR.message_types_by_name['UserContextAccountDetails']
_USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY = _USERCONTEXTACCOUNTDETAILS.nested_types_by_name['EnvironmentByIdEntry']
_USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY = _USERCONTEXTACCOUNTDETAILS.nested_types_by_name['UserContextEnvironmentByIdEntry']
_USERCONTEXTENVIRONMENTDETAILS = DESCRIPTOR.message_types_by_name['UserContextEnvironmentDetails']
_ACCOUNTDETAILS = DESCRIPTOR.message_types_by_name['AccountDetails']
_ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY = _ACCOUNTDETAILS.nested_types_by_name['EnvironmentsByIdEntry']
_ENVIRONMENTDETAILS = DESCRIPTOR.message_types_by_name['EnvironmentDetails']
_USERACCOUNTLIST = DESCRIPTOR.message_types_by_name['UserAccountList']
_USERACCOUNTLIST_ACCOUNTSBYIDENTRY = _USERACCOUNTLIST.nested_types_by_name['AccountsByIdEntry']
UsernamePasswordMethod = _reflection.GeneratedProtocolMessageType('UsernamePasswordMethod', (_message.Message,), {
  'DESCRIPTOR' : _USERNAMEPASSWORDMETHOD,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UsernamePasswordMethod)
  })
_sym_db.RegisterMessage(UsernamePasswordMethod)

QwakApiKeyMethod = _reflection.GeneratedProtocolMessageType('QwakApiKeyMethod', (_message.Message,), {
  'DESCRIPTOR' : _QWAKAPIKEYMETHOD,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.QwakApiKeyMethod)
  })
_sym_db.RegisterMessage(QwakApiKeyMethod)

AuthenticatedUserContext = _reflection.GeneratedProtocolMessageType('AuthenticatedUserContext', (_message.Message,), {
  'DESCRIPTOR' : _AUTHENTICATEDUSERCONTEXT,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.AuthenticatedUserContext)
  })
_sym_db.RegisterMessage(AuthenticatedUserContext)

AuthenticatedUnifiedUserContext = _reflection.GeneratedProtocolMessageType('AuthenticatedUnifiedUserContext', (_message.Message,), {
  'DESCRIPTOR' : _AUTHENTICATEDUNIFIEDUSERCONTEXT,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.AuthenticatedUnifiedUserContext)
  })
_sym_db.RegisterMessage(AuthenticatedUnifiedUserContext)

UserContextAccountDetails = _reflection.GeneratedProtocolMessageType('UserContextAccountDetails', (_message.Message,), {

  'EnvironmentByIdEntry' : _reflection.GeneratedProtocolMessageType('EnvironmentByIdEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY,
    '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
    # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserContextAccountDetails.EnvironmentByIdEntry)
    })
  ,

  'UserContextEnvironmentByIdEntry' : _reflection.GeneratedProtocolMessageType('UserContextEnvironmentByIdEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY,
    '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
    # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserContextAccountDetails.UserContextEnvironmentByIdEntry)
    })
  ,
  'DESCRIPTOR' : _USERCONTEXTACCOUNTDETAILS,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserContextAccountDetails)
  })
_sym_db.RegisterMessage(UserContextAccountDetails)
_sym_db.RegisterMessage(UserContextAccountDetails.EnvironmentByIdEntry)
_sym_db.RegisterMessage(UserContextAccountDetails.UserContextEnvironmentByIdEntry)

UserContextEnvironmentDetails = _reflection.GeneratedProtocolMessageType('UserContextEnvironmentDetails', (_message.Message,), {
  'DESCRIPTOR' : _USERCONTEXTENVIRONMENTDETAILS,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserContextEnvironmentDetails)
  })
_sym_db.RegisterMessage(UserContextEnvironmentDetails)

AccountDetails = _reflection.GeneratedProtocolMessageType('AccountDetails', (_message.Message,), {

  'EnvironmentsByIdEntry' : _reflection.GeneratedProtocolMessageType('EnvironmentsByIdEntry', (_message.Message,), {
    'DESCRIPTOR' : _ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY,
    '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
    # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.AccountDetails.EnvironmentsByIdEntry)
    })
  ,
  'DESCRIPTOR' : _ACCOUNTDETAILS,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.AccountDetails)
  })
_sym_db.RegisterMessage(AccountDetails)
_sym_db.RegisterMessage(AccountDetails.EnvironmentsByIdEntry)

EnvironmentDetails = _reflection.GeneratedProtocolMessageType('EnvironmentDetails', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTDETAILS,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.EnvironmentDetails)
  })
_sym_db.RegisterMessage(EnvironmentDetails)

UserAccountList = _reflection.GeneratedProtocolMessageType('UserAccountList', (_message.Message,), {

  'AccountsByIdEntry' : _reflection.GeneratedProtocolMessageType('AccountsByIdEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERACCOUNTLIST_ACCOUNTSBYIDENTRY,
    '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
    # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserAccountList.AccountsByIdEntry)
    })
  ,
  'DESCRIPTOR' : _USERACCOUNTLIST,
  '__module__' : 'qwak.ecosystem.v0.ecosystem_pb2'
  # @@protoc_insertion_point(class_scope:qwak.ecosystem.v0.UserAccountList)
  })
_sym_db.RegisterMessage(UserAccountList)
_sym_db.RegisterMessage(UserAccountList.AccountsByIdEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034com.qwak.ai.common.ecosystemP\001Z\016.;ecosystem_v0'
  _USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY._options = None
  _USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY._serialized_options = b'8\001'
  _USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY._options = None
  _USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY._serialized_options = b'8\001'
  _ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY._options = None
  _ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY._serialized_options = b'8\001'
  _USERACCOUNTLIST_ACCOUNTSBYIDENTRY._options = None
  _USERACCOUNTLIST_ACCOUNTSBYIDENTRY._serialized_options = b'8\001'
  _USERNAMEPASSWORDMETHOD._serialized_start=209
  _USERNAMEPASSWORDMETHOD._serialized_end=269
  _QWAKAPIKEYMETHOD._serialized_start=271
  _QWAKAPIKEYMETHOD._serialized_end=311
  _AUTHENTICATEDUSERCONTEXT._serialized_start=313
  _AUTHENTICATEDUSERCONTEXT._serialized_end=405
  _AUTHENTICATEDUNIFIEDUSERCONTEXT._serialized_start=407
  _AUTHENTICATEDUNIFIEDUSERCONTEXT._serialized_end=528
  _USERCONTEXTACCOUNTDETAILS._serialized_start=531
  _USERCONTEXTACCOUNTDETAILS._serialized_end=1169
  _USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY._serialized_start=959
  _USERCONTEXTACCOUNTDETAILS_ENVIRONMENTBYIDENTRY._serialized_end=1052
  _USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY._serialized_start=1054
  _USERCONTEXTACCOUNTDETAILS_USERCONTEXTENVIRONMENTBYIDENTRY._serialized_end=1169
  _USERCONTEXTENVIRONMENTDETAILS._serialized_start=1171
  _USERCONTEXTENVIRONMENTDETAILS._serialized_end=1202
  _ACCOUNTDETAILS._serialized_start=1205
  _ACCOUNTDETAILS._serialized_end=1589
  _ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY._serialized_start=1495
  _ACCOUNTDETAILS_ENVIRONMENTSBYIDENTRY._serialized_end=1589
  _ENVIRONMENTDETAILS._serialized_start=1592
  _ENVIRONMENTDETAILS._serialized_end=1724
  _USERACCOUNTLIST._serialized_start=1727
  _USERACCOUNTLIST._serialized_end=1949
  _USERACCOUNTLIST_ACCOUNTSBYIDENTRY._serialized_start=1852
  _USERACCOUNTLIST_ACCOUNTSBYIDENTRY._serialized_end=1949
# @@protoc_insertion_point(module_scope)

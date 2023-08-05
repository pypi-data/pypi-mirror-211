# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/automation/v1/automation_management_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from _qwak_proto.qwak.automation.v1 import automation_pb2 as qwak_dot_automation_dot_v1_dot_automation__pb2
from _qwak_proto.qwak.automation.v1 import automation_execution_pb2 as qwak_dot_automation_dot_v1_dot_automation__execution__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6qwak/automation/v1/automation_management_service.proto\x12\x12qwak.automation.v1\x1a#qwak/automation/v1/automation.proto\x1a-qwak/automation/v1/automation_execution.proto\"V\n\x17\x43reateAutomationRequest\x12;\n\x0f\x61utomation_spec\x18\x01 \x01(\x0b\x32\".qwak.automation.v1.AutomationSpec\"1\n\x18\x43reateAutomationResponse\x12\x15\n\rautomation_id\x18\x01 \x01(\t\"m\n\x17UpdateAutomationRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\x12;\n\x0f\x61utomation_spec\x18\x02 \x01(\x0b\x32\".qwak.automation.v1.AutomationSpec\"\x1a\n\x18UpdateAutomationResponse\"0\n\x17\x44\x65leteAutomationRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\"\x1a\n\x18\x44\x65leteAutomationResponse\"*\n\x16ListAutomationsRequest\x12\x10\n\x08model_id\x18\x01 \x01(\t\"N\n\x17ListAutomationsResponse\x12\x33\n\x0b\x61utomations\x18\x01 \x03(\x0b\x32\x1e.qwak.automation.v1.Automation\"-\n\x14GetAutomationRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\"K\n\x15GetAutomationResponse\x12\x32\n\nautomation\x18\x01 \x01(\x0b\x32\x1e.qwak.automation.v1.Automation\"5\n\x1aGetAutomationByNameRequest\x12\x17\n\x0f\x61utomation_name\x18\x01 \x01(\t\"Q\n\x1bGetAutomationByNameResponse\x12\x32\n\nautomation\x18\x01 \x01(\x0b\x32\x1e.qwak.automation.v1.Automation\"8\n\x1fListAutomationExecutionsRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\"q\n ListAutomationExecutionsResponse\x12M\n\x15\x61utomation_executions\x18\x01 \x03(\x0b\x32..qwak.automation.v1.AutomationExecutionMessage\"Q\n\"RegisterAutomationExecutionRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\x12\x14\n\x0c\x65xecution_id\x18\x02 \x01(\t\"%\n#RegisterAutomationExecutionResponse\"}\n UpdateAutomationExecutionRequest\x12\x14\n\x0c\x65xecution_id\x18\x01 \x01(\t\x12\x43\n\x0brun_details\x18\x02 \x01(\x0b\x32..qwak.automation.v1.ExecutionRunDetailsMessage\"#\n!UpdateAutomationExecutionResponse\"L\n\x1fToggleAutomationActivityRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\x12\x12\n\nis_enabled\x18\x02 \x01(\x08\"\"\n ToggleAutomationActivityResponse\"-\n\x14RunAutomationRequest\x12\x15\n\rautomation_id\x18\x01 \x01(\t\"\x17\n\x15RunAutomationResponse2\xc6\n\n\x1b\x41utomationManagementService\x12m\n\x10\x43reateAutomation\x12+.qwak.automation.v1.CreateAutomationRequest\x1a,.qwak.automation.v1.CreateAutomationResponse\x12m\n\x10UpdateAutomation\x12+.qwak.automation.v1.UpdateAutomationRequest\x1a,.qwak.automation.v1.UpdateAutomationResponse\x12m\n\x10\x44\x65leteAutomation\x12+.qwak.automation.v1.DeleteAutomationRequest\x1a,.qwak.automation.v1.DeleteAutomationResponse\x12\x64\n\rGetAutomation\x12(.qwak.automation.v1.GetAutomationRequest\x1a).qwak.automation.v1.GetAutomationResponse\x12v\n\x13GetAutomationByName\x12..qwak.automation.v1.GetAutomationByNameRequest\x1a/.qwak.automation.v1.GetAutomationByNameResponse\x12j\n\x0fListAutomations\x12*.qwak.automation.v1.ListAutomationsRequest\x1a+.qwak.automation.v1.ListAutomationsResponse\x12\x85\x01\n\x18ListAutomationExecutions\x12\x33.qwak.automation.v1.ListAutomationExecutionsRequest\x1a\x34.qwak.automation.v1.ListAutomationExecutionsResponse\x12\x8e\x01\n\x1bRegisterAutomationExecution\x12\x36.qwak.automation.v1.RegisterAutomationExecutionRequest\x1a\x37.qwak.automation.v1.RegisterAutomationExecutionResponse\x12\x88\x01\n\x19UpdateAutomationExecution\x12\x34.qwak.automation.v1.UpdateAutomationExecutionRequest\x1a\x35.qwak.automation.v1.UpdateAutomationExecutionResponse\x12\x85\x01\n\x18ToggleAutomationActivity\x12\x33.qwak.automation.v1.ToggleAutomationActivityRequest\x1a\x34.qwak.automation.v1.ToggleAutomationActivityResponse\x12\x64\n\rRunAutomation\x12(.qwak.automation.v1.RunAutomationRequest\x1a).qwak.automation.v1.RunAutomationResponseB!\n\x1d\x63om.qwak.ai.automation.api.v1P\x01\x62\x06proto3')



_CREATEAUTOMATIONREQUEST = DESCRIPTOR.message_types_by_name['CreateAutomationRequest']
_CREATEAUTOMATIONRESPONSE = DESCRIPTOR.message_types_by_name['CreateAutomationResponse']
_UPDATEAUTOMATIONREQUEST = DESCRIPTOR.message_types_by_name['UpdateAutomationRequest']
_UPDATEAUTOMATIONRESPONSE = DESCRIPTOR.message_types_by_name['UpdateAutomationResponse']
_DELETEAUTOMATIONREQUEST = DESCRIPTOR.message_types_by_name['DeleteAutomationRequest']
_DELETEAUTOMATIONRESPONSE = DESCRIPTOR.message_types_by_name['DeleteAutomationResponse']
_LISTAUTOMATIONSREQUEST = DESCRIPTOR.message_types_by_name['ListAutomationsRequest']
_LISTAUTOMATIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListAutomationsResponse']
_GETAUTOMATIONREQUEST = DESCRIPTOR.message_types_by_name['GetAutomationRequest']
_GETAUTOMATIONRESPONSE = DESCRIPTOR.message_types_by_name['GetAutomationResponse']
_GETAUTOMATIONBYNAMEREQUEST = DESCRIPTOR.message_types_by_name['GetAutomationByNameRequest']
_GETAUTOMATIONBYNAMERESPONSE = DESCRIPTOR.message_types_by_name['GetAutomationByNameResponse']
_LISTAUTOMATIONEXECUTIONSREQUEST = DESCRIPTOR.message_types_by_name['ListAutomationExecutionsRequest']
_LISTAUTOMATIONEXECUTIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListAutomationExecutionsResponse']
_REGISTERAUTOMATIONEXECUTIONREQUEST = DESCRIPTOR.message_types_by_name['RegisterAutomationExecutionRequest']
_REGISTERAUTOMATIONEXECUTIONRESPONSE = DESCRIPTOR.message_types_by_name['RegisterAutomationExecutionResponse']
_UPDATEAUTOMATIONEXECUTIONREQUEST = DESCRIPTOR.message_types_by_name['UpdateAutomationExecutionRequest']
_UPDATEAUTOMATIONEXECUTIONRESPONSE = DESCRIPTOR.message_types_by_name['UpdateAutomationExecutionResponse']
_TOGGLEAUTOMATIONACTIVITYREQUEST = DESCRIPTOR.message_types_by_name['ToggleAutomationActivityRequest']
_TOGGLEAUTOMATIONACTIVITYRESPONSE = DESCRIPTOR.message_types_by_name['ToggleAutomationActivityResponse']
_RUNAUTOMATIONREQUEST = DESCRIPTOR.message_types_by_name['RunAutomationRequest']
_RUNAUTOMATIONRESPONSE = DESCRIPTOR.message_types_by_name['RunAutomationResponse']
CreateAutomationRequest = _reflection.GeneratedProtocolMessageType('CreateAutomationRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEAUTOMATIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.CreateAutomationRequest)
  })
_sym_db.RegisterMessage(CreateAutomationRequest)

CreateAutomationResponse = _reflection.GeneratedProtocolMessageType('CreateAutomationResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEAUTOMATIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.CreateAutomationResponse)
  })
_sym_db.RegisterMessage(CreateAutomationResponse)

UpdateAutomationRequest = _reflection.GeneratedProtocolMessageType('UpdateAutomationRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUTOMATIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.UpdateAutomationRequest)
  })
_sym_db.RegisterMessage(UpdateAutomationRequest)

UpdateAutomationResponse = _reflection.GeneratedProtocolMessageType('UpdateAutomationResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUTOMATIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.UpdateAutomationResponse)
  })
_sym_db.RegisterMessage(UpdateAutomationResponse)

DeleteAutomationRequest = _reflection.GeneratedProtocolMessageType('DeleteAutomationRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEAUTOMATIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.DeleteAutomationRequest)
  })
_sym_db.RegisterMessage(DeleteAutomationRequest)

DeleteAutomationResponse = _reflection.GeneratedProtocolMessageType('DeleteAutomationResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEAUTOMATIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.DeleteAutomationResponse)
  })
_sym_db.RegisterMessage(DeleteAutomationResponse)

ListAutomationsRequest = _reflection.GeneratedProtocolMessageType('ListAutomationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTAUTOMATIONSREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ListAutomationsRequest)
  })
_sym_db.RegisterMessage(ListAutomationsRequest)

ListAutomationsResponse = _reflection.GeneratedProtocolMessageType('ListAutomationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTAUTOMATIONSRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ListAutomationsResponse)
  })
_sym_db.RegisterMessage(ListAutomationsResponse)

GetAutomationRequest = _reflection.GeneratedProtocolMessageType('GetAutomationRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETAUTOMATIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GetAutomationRequest)
  })
_sym_db.RegisterMessage(GetAutomationRequest)

GetAutomationResponse = _reflection.GeneratedProtocolMessageType('GetAutomationResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETAUTOMATIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GetAutomationResponse)
  })
_sym_db.RegisterMessage(GetAutomationResponse)

GetAutomationByNameRequest = _reflection.GeneratedProtocolMessageType('GetAutomationByNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETAUTOMATIONBYNAMEREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GetAutomationByNameRequest)
  })
_sym_db.RegisterMessage(GetAutomationByNameRequest)

GetAutomationByNameResponse = _reflection.GeneratedProtocolMessageType('GetAutomationByNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETAUTOMATIONBYNAMERESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.GetAutomationByNameResponse)
  })
_sym_db.RegisterMessage(GetAutomationByNameResponse)

ListAutomationExecutionsRequest = _reflection.GeneratedProtocolMessageType('ListAutomationExecutionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTAUTOMATIONEXECUTIONSREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ListAutomationExecutionsRequest)
  })
_sym_db.RegisterMessage(ListAutomationExecutionsRequest)

ListAutomationExecutionsResponse = _reflection.GeneratedProtocolMessageType('ListAutomationExecutionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTAUTOMATIONEXECUTIONSRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ListAutomationExecutionsResponse)
  })
_sym_db.RegisterMessage(ListAutomationExecutionsResponse)

RegisterAutomationExecutionRequest = _reflection.GeneratedProtocolMessageType('RegisterAutomationExecutionRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERAUTOMATIONEXECUTIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.RegisterAutomationExecutionRequest)
  })
_sym_db.RegisterMessage(RegisterAutomationExecutionRequest)

RegisterAutomationExecutionResponse = _reflection.GeneratedProtocolMessageType('RegisterAutomationExecutionResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERAUTOMATIONEXECUTIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.RegisterAutomationExecutionResponse)
  })
_sym_db.RegisterMessage(RegisterAutomationExecutionResponse)

UpdateAutomationExecutionRequest = _reflection.GeneratedProtocolMessageType('UpdateAutomationExecutionRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUTOMATIONEXECUTIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.UpdateAutomationExecutionRequest)
  })
_sym_db.RegisterMessage(UpdateAutomationExecutionRequest)

UpdateAutomationExecutionResponse = _reflection.GeneratedProtocolMessageType('UpdateAutomationExecutionResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUTOMATIONEXECUTIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.UpdateAutomationExecutionResponse)
  })
_sym_db.RegisterMessage(UpdateAutomationExecutionResponse)

ToggleAutomationActivityRequest = _reflection.GeneratedProtocolMessageType('ToggleAutomationActivityRequest', (_message.Message,), {
  'DESCRIPTOR' : _TOGGLEAUTOMATIONACTIVITYREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ToggleAutomationActivityRequest)
  })
_sym_db.RegisterMessage(ToggleAutomationActivityRequest)

ToggleAutomationActivityResponse = _reflection.GeneratedProtocolMessageType('ToggleAutomationActivityResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOGGLEAUTOMATIONACTIVITYRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.ToggleAutomationActivityResponse)
  })
_sym_db.RegisterMessage(ToggleAutomationActivityResponse)

RunAutomationRequest = _reflection.GeneratedProtocolMessageType('RunAutomationRequest', (_message.Message,), {
  'DESCRIPTOR' : _RUNAUTOMATIONREQUEST,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.RunAutomationRequest)
  })
_sym_db.RegisterMessage(RunAutomationRequest)

RunAutomationResponse = _reflection.GeneratedProtocolMessageType('RunAutomationResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNAUTOMATIONRESPONSE,
  '__module__' : 'qwak.automation.v1.automation_management_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.automation.v1.RunAutomationResponse)
  })
_sym_db.RegisterMessage(RunAutomationResponse)

_AUTOMATIONMANAGEMENTSERVICE = DESCRIPTOR.services_by_name['AutomationManagementService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.qwak.ai.automation.api.v1P\001'
  _CREATEAUTOMATIONREQUEST._serialized_start=162
  _CREATEAUTOMATIONREQUEST._serialized_end=248
  _CREATEAUTOMATIONRESPONSE._serialized_start=250
  _CREATEAUTOMATIONRESPONSE._serialized_end=299
  _UPDATEAUTOMATIONREQUEST._serialized_start=301
  _UPDATEAUTOMATIONREQUEST._serialized_end=410
  _UPDATEAUTOMATIONRESPONSE._serialized_start=412
  _UPDATEAUTOMATIONRESPONSE._serialized_end=438
  _DELETEAUTOMATIONREQUEST._serialized_start=440
  _DELETEAUTOMATIONREQUEST._serialized_end=488
  _DELETEAUTOMATIONRESPONSE._serialized_start=490
  _DELETEAUTOMATIONRESPONSE._serialized_end=516
  _LISTAUTOMATIONSREQUEST._serialized_start=518
  _LISTAUTOMATIONSREQUEST._serialized_end=560
  _LISTAUTOMATIONSRESPONSE._serialized_start=562
  _LISTAUTOMATIONSRESPONSE._serialized_end=640
  _GETAUTOMATIONREQUEST._serialized_start=642
  _GETAUTOMATIONREQUEST._serialized_end=687
  _GETAUTOMATIONRESPONSE._serialized_start=689
  _GETAUTOMATIONRESPONSE._serialized_end=764
  _GETAUTOMATIONBYNAMEREQUEST._serialized_start=766
  _GETAUTOMATIONBYNAMEREQUEST._serialized_end=819
  _GETAUTOMATIONBYNAMERESPONSE._serialized_start=821
  _GETAUTOMATIONBYNAMERESPONSE._serialized_end=902
  _LISTAUTOMATIONEXECUTIONSREQUEST._serialized_start=904
  _LISTAUTOMATIONEXECUTIONSREQUEST._serialized_end=960
  _LISTAUTOMATIONEXECUTIONSRESPONSE._serialized_start=962
  _LISTAUTOMATIONEXECUTIONSRESPONSE._serialized_end=1075
  _REGISTERAUTOMATIONEXECUTIONREQUEST._serialized_start=1077
  _REGISTERAUTOMATIONEXECUTIONREQUEST._serialized_end=1158
  _REGISTERAUTOMATIONEXECUTIONRESPONSE._serialized_start=1160
  _REGISTERAUTOMATIONEXECUTIONRESPONSE._serialized_end=1197
  _UPDATEAUTOMATIONEXECUTIONREQUEST._serialized_start=1199
  _UPDATEAUTOMATIONEXECUTIONREQUEST._serialized_end=1324
  _UPDATEAUTOMATIONEXECUTIONRESPONSE._serialized_start=1326
  _UPDATEAUTOMATIONEXECUTIONRESPONSE._serialized_end=1361
  _TOGGLEAUTOMATIONACTIVITYREQUEST._serialized_start=1363
  _TOGGLEAUTOMATIONACTIVITYREQUEST._serialized_end=1439
  _TOGGLEAUTOMATIONACTIVITYRESPONSE._serialized_start=1441
  _TOGGLEAUTOMATIONACTIVITYRESPONSE._serialized_end=1475
  _RUNAUTOMATIONREQUEST._serialized_start=1477
  _RUNAUTOMATIONREQUEST._serialized_end=1522
  _RUNAUTOMATIONRESPONSE._serialized_start=1524
  _RUNAUTOMATIONRESPONSE._serialized_end=1547
  _AUTOMATIONMANAGEMENTSERVICE._serialized_start=1550
  _AUTOMATIONMANAGEMENTSERVICE._serialized_end=2900
# @@protoc_insertion_point(module_scope)

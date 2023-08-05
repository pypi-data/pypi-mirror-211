# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/self_service/account/v0/account_membership_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from _qwak_proto.qwak.self_service.account.v0 import account_membership_pb2 as qwak_dot_self__service_dot_account_dot_v0_dot_account__membership__pb2
from _qwak_proto.qwak.self_service.user.v1 import user_pb2 as qwak_dot_self__service_dot_user_dot_v1_dot_user__pb2
from _qwak_proto.qwak.administration.v0.users import user_pb2 as qwak_dot_administration_dot_v0_dot_users_dot_user__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=qwak/self_service/account/v0/account_membership_service.proto\x12\x1cqwak.self_service.account.v0\x1a\x35qwak/self_service/account/v0/account_membership.proto\x1a$qwak/self_service/user/v1/user.proto\x1a\'qwak/administration/v0/users/user.proto\" \n\x1eListAccountUserProfilesRequest\"`\n\x1fListAccountUserProfilesResponse\x12=\n\ruser_profiles\x18\x01 \x03(\x0b\x32&.qwak.self_service.user.v1.UserProfile\"d\n\x15UpdateUserRoleRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12?\n\x0c\x61\x63\x63ount_role\x18\x02 \x01(\x0e\x32).qwak.administration.user.QwakAccountRole\"V\n\x16UpdateUserRoleResponse\x12<\n\x0cuser_profile\x18\x01 \x01(\x0b\x32&.qwak.self_service.user.v1.UserProfile\"*\n\x1cRemoveUserFromAccountRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x1f\n\x1dRemoveUserFromAccountResponse\"Z\n\x1aInviteToJoinAccountRequest\x12<\n\x07options\x18\x01 \x03(\x0b\x32+.qwak.self_service.account.v0.InviteOptions\"n\n\x1bInviteToJoinAccountResponse\x12O\n\x0binvitations\x18\x01 \x03(\x0b\x32:.qwak.self_service.account.v0.JoiningInvitationDescription\"q\n\x17UpdateInvitationRequest\x12\x15\n\rinvitation_id\x18\x01 \x01(\t\x12?\n\x0c\x61\x63\x63ount_role\x18\x02 \x01(\x0e\x32).qwak.administration.user.QwakAccountRole\"j\n\x18UpdateInvitationResponse\x12N\n\ninvitation\x18\x01 \x01(\x0b\x32:.qwak.self_service.account.v0.JoiningInvitationDescription\"0\n\x17\x41\x63\x63\x65ptInvitationRequest\x12\x15\n\rinvitation_id\x18\x01 \x01(\t\"\x1a\n\x18\x41\x63\x63\x65ptInvitationResponse\"7\n\x1e\x43\x61ncelJoiningInvitationRequest\x12\x15\n\rinvitation_id\x18\x01 \x01(\t\"!\n\x1f\x43\x61ncelJoiningInvitationResponse\"\x1f\n\x1dListAccountInvitationsRequest\"q\n\x1eListAccountInvitationsResponse\x12O\n\x0binvitations\x18\x01 \x03(\x0b\x32:.qwak.self_service.account.v0.JoiningInvitationDescription\"\x1c\n\x1aListUserInvitationsRequest\"n\n\x1bListUserInvitationsResponse\x12O\n\x0binvitations\x18\x01 \x03(\x0b\x32:.qwak.self_service.account.v0.JoiningInvitationDescription2\x94\n\n\x18\x41\x63\x63ountMembershipService\x12\x96\x01\n\x17ListAccountUserProfiles\x12<.qwak.self_service.account.v0.ListAccountUserProfilesRequest\x1a=.qwak.self_service.account.v0.ListAccountUserProfilesResponse\x12{\n\x0eUpdateUserRole\x12\x33.qwak.self_service.account.v0.UpdateUserRoleRequest\x1a\x34.qwak.self_service.account.v0.UpdateUserRoleResponse\x12\x90\x01\n\x15RemoveUserFromAccount\x12:.qwak.self_service.account.v0.RemoveUserFromAccountRequest\x1a;.qwak.self_service.account.v0.RemoveUserFromAccountResponse\x12\x8a\x01\n\x13InviteToJoinAccount\x12\x38.qwak.self_service.account.v0.InviteToJoinAccountRequest\x1a\x39.qwak.self_service.account.v0.InviteToJoinAccountResponse\x12\x81\x01\n\x10UpdateInvitation\x12\x35.qwak.self_service.account.v0.UpdateInvitationRequest\x1a\x36.qwak.self_service.account.v0.UpdateInvitationResponse\x12\x81\x01\n\x10\x41\x63\x63\x65ptInvitation\x12\x35.qwak.self_service.account.v0.AcceptInvitationRequest\x1a\x36.qwak.self_service.account.v0.AcceptInvitationResponse\x12\x96\x01\n\x17\x43\x61ncelJoiningInvitation\x12<.qwak.self_service.account.v0.CancelJoiningInvitationRequest\x1a=.qwak.self_service.account.v0.CancelJoiningInvitationResponse\x12\x93\x01\n\x16ListAccountInvitations\x12;.qwak.self_service.account.v0.ListAccountInvitationsRequest\x1a<.qwak.self_service.account.v0.ListAccountInvitationsResponse\x12\x8a\x01\n\x13ListUserInvitations\x12\x38.qwak.self_service.account.v0.ListUserInvitationsRequest\x1a\x39.qwak.self_service.account.v0.ListUserInvitationsResponseB\xb9\x01\n#com.qwak.ai.self_service.account.v0P\x01Z\x8f\x01github.com/qwak-ai/qwak-platform/services/core/java/user-management/user-management-api/pb/qwak/self_service/account/v0;self_service_account_v0b\x06proto3')



_LISTACCOUNTUSERPROFILESREQUEST = DESCRIPTOR.message_types_by_name['ListAccountUserProfilesRequest']
_LISTACCOUNTUSERPROFILESRESPONSE = DESCRIPTOR.message_types_by_name['ListAccountUserProfilesResponse']
_UPDATEUSERROLEREQUEST = DESCRIPTOR.message_types_by_name['UpdateUserRoleRequest']
_UPDATEUSERROLERESPONSE = DESCRIPTOR.message_types_by_name['UpdateUserRoleResponse']
_REMOVEUSERFROMACCOUNTREQUEST = DESCRIPTOR.message_types_by_name['RemoveUserFromAccountRequest']
_REMOVEUSERFROMACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['RemoveUserFromAccountResponse']
_INVITETOJOINACCOUNTREQUEST = DESCRIPTOR.message_types_by_name['InviteToJoinAccountRequest']
_INVITETOJOINACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['InviteToJoinAccountResponse']
_UPDATEINVITATIONREQUEST = DESCRIPTOR.message_types_by_name['UpdateInvitationRequest']
_UPDATEINVITATIONRESPONSE = DESCRIPTOR.message_types_by_name['UpdateInvitationResponse']
_ACCEPTINVITATIONREQUEST = DESCRIPTOR.message_types_by_name['AcceptInvitationRequest']
_ACCEPTINVITATIONRESPONSE = DESCRIPTOR.message_types_by_name['AcceptInvitationResponse']
_CANCELJOININGINVITATIONREQUEST = DESCRIPTOR.message_types_by_name['CancelJoiningInvitationRequest']
_CANCELJOININGINVITATIONRESPONSE = DESCRIPTOR.message_types_by_name['CancelJoiningInvitationResponse']
_LISTACCOUNTINVITATIONSREQUEST = DESCRIPTOR.message_types_by_name['ListAccountInvitationsRequest']
_LISTACCOUNTINVITATIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListAccountInvitationsResponse']
_LISTUSERINVITATIONSREQUEST = DESCRIPTOR.message_types_by_name['ListUserInvitationsRequest']
_LISTUSERINVITATIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListUserInvitationsResponse']
ListAccountUserProfilesRequest = _reflection.GeneratedProtocolMessageType('ListAccountUserProfilesRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTUSERPROFILESREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListAccountUserProfilesRequest)
  })
_sym_db.RegisterMessage(ListAccountUserProfilesRequest)

ListAccountUserProfilesResponse = _reflection.GeneratedProtocolMessageType('ListAccountUserProfilesResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTUSERPROFILESRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListAccountUserProfilesResponse)
  })
_sym_db.RegisterMessage(ListAccountUserProfilesResponse)

UpdateUserRoleRequest = _reflection.GeneratedProtocolMessageType('UpdateUserRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERROLEREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.UpdateUserRoleRequest)
  })
_sym_db.RegisterMessage(UpdateUserRoleRequest)

UpdateUserRoleResponse = _reflection.GeneratedProtocolMessageType('UpdateUserRoleResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERROLERESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.UpdateUserRoleResponse)
  })
_sym_db.RegisterMessage(UpdateUserRoleResponse)

RemoveUserFromAccountRequest = _reflection.GeneratedProtocolMessageType('RemoveUserFromAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEUSERFROMACCOUNTREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.RemoveUserFromAccountRequest)
  })
_sym_db.RegisterMessage(RemoveUserFromAccountRequest)

RemoveUserFromAccountResponse = _reflection.GeneratedProtocolMessageType('RemoveUserFromAccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEUSERFROMACCOUNTRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.RemoveUserFromAccountResponse)
  })
_sym_db.RegisterMessage(RemoveUserFromAccountResponse)

InviteToJoinAccountRequest = _reflection.GeneratedProtocolMessageType('InviteToJoinAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _INVITETOJOINACCOUNTREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.InviteToJoinAccountRequest)
  })
_sym_db.RegisterMessage(InviteToJoinAccountRequest)

InviteToJoinAccountResponse = _reflection.GeneratedProtocolMessageType('InviteToJoinAccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _INVITETOJOINACCOUNTRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.InviteToJoinAccountResponse)
  })
_sym_db.RegisterMessage(InviteToJoinAccountResponse)

UpdateInvitationRequest = _reflection.GeneratedProtocolMessageType('UpdateInvitationRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEINVITATIONREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.UpdateInvitationRequest)
  })
_sym_db.RegisterMessage(UpdateInvitationRequest)

UpdateInvitationResponse = _reflection.GeneratedProtocolMessageType('UpdateInvitationResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEINVITATIONRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.UpdateInvitationResponse)
  })
_sym_db.RegisterMessage(UpdateInvitationResponse)

AcceptInvitationRequest = _reflection.GeneratedProtocolMessageType('AcceptInvitationRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPTINVITATIONREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.AcceptInvitationRequest)
  })
_sym_db.RegisterMessage(AcceptInvitationRequest)

AcceptInvitationResponse = _reflection.GeneratedProtocolMessageType('AcceptInvitationResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPTINVITATIONRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.AcceptInvitationResponse)
  })
_sym_db.RegisterMessage(AcceptInvitationResponse)

CancelJoiningInvitationRequest = _reflection.GeneratedProtocolMessageType('CancelJoiningInvitationRequest', (_message.Message,), {
  'DESCRIPTOR' : _CANCELJOININGINVITATIONREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.CancelJoiningInvitationRequest)
  })
_sym_db.RegisterMessage(CancelJoiningInvitationRequest)

CancelJoiningInvitationResponse = _reflection.GeneratedProtocolMessageType('CancelJoiningInvitationResponse', (_message.Message,), {
  'DESCRIPTOR' : _CANCELJOININGINVITATIONRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.CancelJoiningInvitationResponse)
  })
_sym_db.RegisterMessage(CancelJoiningInvitationResponse)

ListAccountInvitationsRequest = _reflection.GeneratedProtocolMessageType('ListAccountInvitationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTINVITATIONSREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListAccountInvitationsRequest)
  })
_sym_db.RegisterMessage(ListAccountInvitationsRequest)

ListAccountInvitationsResponse = _reflection.GeneratedProtocolMessageType('ListAccountInvitationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTACCOUNTINVITATIONSRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListAccountInvitationsResponse)
  })
_sym_db.RegisterMessage(ListAccountInvitationsResponse)

ListUserInvitationsRequest = _reflection.GeneratedProtocolMessageType('ListUserInvitationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERINVITATIONSREQUEST,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListUserInvitationsRequest)
  })
_sym_db.RegisterMessage(ListUserInvitationsRequest)

ListUserInvitationsResponse = _reflection.GeneratedProtocolMessageType('ListUserInvitationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERINVITATIONSRESPONSE,
  '__module__' : 'qwak.self_service.account.v0.account_membership_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.self_service.account.v0.ListUserInvitationsResponse)
  })
_sym_db.RegisterMessage(ListUserInvitationsResponse)

_ACCOUNTMEMBERSHIPSERVICE = DESCRIPTOR.services_by_name['AccountMembershipService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#com.qwak.ai.self_service.account.v0P\001Z\217\001github.com/qwak-ai/qwak-platform/services/core/java/user-management/user-management-api/pb/qwak/self_service/account/v0;self_service_account_v0'
  _LISTACCOUNTUSERPROFILESREQUEST._serialized_start=229
  _LISTACCOUNTUSERPROFILESREQUEST._serialized_end=261
  _LISTACCOUNTUSERPROFILESRESPONSE._serialized_start=263
  _LISTACCOUNTUSERPROFILESRESPONSE._serialized_end=359
  _UPDATEUSERROLEREQUEST._serialized_start=361
  _UPDATEUSERROLEREQUEST._serialized_end=461
  _UPDATEUSERROLERESPONSE._serialized_start=463
  _UPDATEUSERROLERESPONSE._serialized_end=549
  _REMOVEUSERFROMACCOUNTREQUEST._serialized_start=551
  _REMOVEUSERFROMACCOUNTREQUEST._serialized_end=593
  _REMOVEUSERFROMACCOUNTRESPONSE._serialized_start=595
  _REMOVEUSERFROMACCOUNTRESPONSE._serialized_end=626
  _INVITETOJOINACCOUNTREQUEST._serialized_start=628
  _INVITETOJOINACCOUNTREQUEST._serialized_end=718
  _INVITETOJOINACCOUNTRESPONSE._serialized_start=720
  _INVITETOJOINACCOUNTRESPONSE._serialized_end=830
  _UPDATEINVITATIONREQUEST._serialized_start=832
  _UPDATEINVITATIONREQUEST._serialized_end=945
  _UPDATEINVITATIONRESPONSE._serialized_start=947
  _UPDATEINVITATIONRESPONSE._serialized_end=1053
  _ACCEPTINVITATIONREQUEST._serialized_start=1055
  _ACCEPTINVITATIONREQUEST._serialized_end=1103
  _ACCEPTINVITATIONRESPONSE._serialized_start=1105
  _ACCEPTINVITATIONRESPONSE._serialized_end=1131
  _CANCELJOININGINVITATIONREQUEST._serialized_start=1133
  _CANCELJOININGINVITATIONREQUEST._serialized_end=1188
  _CANCELJOININGINVITATIONRESPONSE._serialized_start=1190
  _CANCELJOININGINVITATIONRESPONSE._serialized_end=1223
  _LISTACCOUNTINVITATIONSREQUEST._serialized_start=1225
  _LISTACCOUNTINVITATIONSREQUEST._serialized_end=1256
  _LISTACCOUNTINVITATIONSRESPONSE._serialized_start=1258
  _LISTACCOUNTINVITATIONSRESPONSE._serialized_end=1371
  _LISTUSERINVITATIONSREQUEST._serialized_start=1373
  _LISTUSERINVITATIONSREQUEST._serialized_end=1401
  _LISTUSERINVITATIONSRESPONSE._serialized_start=1403
  _LISTUSERINVITATIONSRESPONSE._serialized_end=1513
  _ACCOUNTMEMBERSHIPSERVICE._serialized_start=1516
  _ACCOUNTMEMBERSHIPSERVICE._serialized_end=2816
# @@protoc_insertion_point(module_scope)

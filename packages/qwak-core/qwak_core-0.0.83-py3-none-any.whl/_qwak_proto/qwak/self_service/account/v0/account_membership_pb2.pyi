"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import qwak.administration.v0.users.user_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _JoiningInvitationStatusCode:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _JoiningInvitationStatusCodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_JoiningInvitationStatusCode.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    JOINING_INVITATION_STATUS_CODE_INVALID: _JoiningInvitationStatusCode.ValueType  # 0
    PENDING: _JoiningInvitationStatusCode.ValueType  # 1
    """Waiting for response"""
    CANCELLED: _JoiningInvitationStatusCode.ValueType  # 2
    """Canceled by account user"""
    DECLINED: _JoiningInvitationStatusCode.ValueType  # 3
    """Declined by invitee"""
    ACCEPTED: _JoiningInvitationStatusCode.ValueType  # 4
    """Accepted by invitee"""

class JoiningInvitationStatusCode(_JoiningInvitationStatusCode, metaclass=_JoiningInvitationStatusCodeEnumTypeWrapper): ...

JOINING_INVITATION_STATUS_CODE_INVALID: JoiningInvitationStatusCode.ValueType  # 0
PENDING: JoiningInvitationStatusCode.ValueType  # 1
"""Waiting for response"""
CANCELLED: JoiningInvitationStatusCode.ValueType  # 2
"""Canceled by account user"""
DECLINED: JoiningInvitationStatusCode.ValueType  # 3
"""Declined by invitee"""
ACCEPTED: JoiningInvitationStatusCode.ValueType  # 4
"""Accepted by invitee"""
global___JoiningInvitationStatusCode = JoiningInvitationStatusCode

class InviteOptions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INVITATION_SPEC_FIELD_NUMBER: builtins.int
    @property
    def invitation_spec(self) -> global___JoiningInvitationSpec:
        """Spec of the invitation"""
    def __init__(
        self,
        *,
        invitation_spec: global___JoiningInvitationSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["invitation_spec", b"invitation_spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["invitation_spec", b"invitation_spec"]) -> None: ...

global___InviteOptions = InviteOptions

class JoiningInvitationDescription(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    METADATA_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    NUM_OF_ACCOUNT_MEMBERS_FIELD_NUMBER: builtins.int
    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    @property
    def metadata(self) -> global___JoiningInvitationMetadata:
        """The metadata of the invitation"""
    @property
    def spec(self) -> global___JoiningInvitationSpec:
        """The spec of the invitation"""
    @property
    def status(self) -> global___JoiningInvitationStatus:
        """Status information for invitation"""
    num_of_account_members: builtins.int
    """The number of account members"""
    account_name: builtins.str
    """The account name"""
    def __init__(
        self,
        *,
        metadata: global___JoiningInvitationMetadata | None = ...,
        spec: global___JoiningInvitationSpec | None = ...,
        status: global___JoiningInvitationStatus | None = ...,
        num_of_account_members: builtins.int = ...,
        account_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "spec", b"spec", "status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_name", b"account_name", "metadata", b"metadata", "num_of_account_members", b"num_of_account_members", "spec", b"spec", "status", b"status"]) -> None: ...

global___JoiningInvitationDescription = JoiningInvitationDescription

class JoiningInvitationMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INVITATION_ID_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    EXPIRED_AT_FIELD_NUMBER: builtins.int
    INVITED_BY_FIELD_NUMBER: builtins.int
    invitation_id: builtins.str
    """Id of the invitation"""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Created at"""
    @property
    def expired_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Expired at"""
    invited_by: builtins.str
    """The user id of the inviting user"""
    def __init__(
        self,
        *,
        invitation_id: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        expired_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        invited_by: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "expired_at", b"expired_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "expired_at", b"expired_at", "invitation_id", b"invitation_id", "invited_by", b"invited_by"]) -> None: ...

global___JoiningInvitationMetadata = JoiningInvitationMetadata

class JoiningInvitationSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INVITEE_EMAIL_FIELD_NUMBER: builtins.int
    ACCOUNT_ROLE_FIELD_NUMBER: builtins.int
    invitee_email: builtins.str
    """The email of the invitee"""
    account_role: qwak.administration.v0.users.user_pb2.QwakAccountRole.ValueType
    """User account role"""
    def __init__(
        self,
        *,
        invitee_email: builtins.str = ...,
        account_role: qwak.administration.v0.users.user_pb2.QwakAccountRole.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_role", b"account_role", "invitee_email", b"invitee_email"]) -> None: ...

global___JoiningInvitationSpec = JoiningInvitationSpec

class JoiningInvitationStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    LAST_CHANGED_AT_FIELD_NUMBER: builtins.int
    code: global___JoiningInvitationStatusCode.ValueType
    """status code"""
    @property
    def last_changed_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """When the status has been changed"""
    def __init__(
        self,
        *,
        code: global___JoiningInvitationStatusCode.ValueType = ...,
        last_changed_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["last_changed_at", b"last_changed_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "last_changed_at", b"last_changed_at"]) -> None: ...

global___JoiningInvitationStatus = JoiningInvitationStatus

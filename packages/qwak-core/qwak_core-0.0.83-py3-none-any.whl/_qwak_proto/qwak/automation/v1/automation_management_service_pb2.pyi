"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import qwak.automation.v1.automation_execution_pb2
import qwak.automation.v1.automation_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CreateAutomationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_SPEC_FIELD_NUMBER: builtins.int
    @property
    def automation_spec(self) -> qwak.automation.v1.automation_pb2.AutomationSpec: ...
    def __init__(
        self,
        *,
        automation_spec: qwak.automation.v1.automation_pb2.AutomationSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["automation_spec", b"automation_spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_spec", b"automation_spec"]) -> None: ...

global___CreateAutomationRequest = CreateAutomationRequest

class CreateAutomationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id"]) -> None: ...

global___CreateAutomationResponse = CreateAutomationResponse

class UpdateAutomationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    AUTOMATION_SPEC_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    @property
    def automation_spec(self) -> qwak.automation.v1.automation_pb2.AutomationSpec: ...
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
        automation_spec: qwak.automation.v1.automation_pb2.AutomationSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["automation_spec", b"automation_spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id", "automation_spec", b"automation_spec"]) -> None: ...

global___UpdateAutomationRequest = UpdateAutomationRequest

class UpdateAutomationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UpdateAutomationResponse = UpdateAutomationResponse

class DeleteAutomationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to delete."""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id"]) -> None: ...

global___DeleteAutomationRequest = DeleteAutomationRequest

class DeleteAutomationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteAutomationResponse = DeleteAutomationResponse

class ListAutomationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_ID_FIELD_NUMBER: builtins.int
    model_id: builtins.str
    def __init__(
        self,
        *,
        model_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["model_id", b"model_id"]) -> None: ...

global___ListAutomationsRequest = ListAutomationsRequest

class ListAutomationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATIONS_FIELD_NUMBER: builtins.int
    @property
    def automations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[qwak.automation.v1.automation_pb2.Automation]: ...
    def __init__(
        self,
        *,
        automations: collections.abc.Iterable[qwak.automation.v1.automation_pb2.Automation] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automations", b"automations"]) -> None: ...

global___ListAutomationsResponse = ListAutomationsResponse

class GetAutomationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to get."""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id"]) -> None: ...

global___GetAutomationRequest = GetAutomationRequest

class GetAutomationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_FIELD_NUMBER: builtins.int
    @property
    def automation(self) -> qwak.automation.v1.automation_pb2.Automation: ...
    def __init__(
        self,
        *,
        automation: qwak.automation.v1.automation_pb2.Automation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["automation", b"automation"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation", b"automation"]) -> None: ...

global___GetAutomationResponse = GetAutomationResponse

class GetAutomationByNameRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_NAME_FIELD_NUMBER: builtins.int
    automation_name: builtins.str
    """The automation name to get."""
    def __init__(
        self,
        *,
        automation_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_name", b"automation_name"]) -> None: ...

global___GetAutomationByNameRequest = GetAutomationByNameRequest

class GetAutomationByNameResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_FIELD_NUMBER: builtins.int
    @property
    def automation(self) -> qwak.automation.v1.automation_pb2.Automation: ...
    def __init__(
        self,
        *,
        automation: qwak.automation.v1.automation_pb2.Automation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["automation", b"automation"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation", b"automation"]) -> None: ...

global___GetAutomationByNameResponse = GetAutomationByNameResponse

class ListAutomationExecutionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to get executions for."""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id"]) -> None: ...

global___ListAutomationExecutionsRequest = ListAutomationExecutionsRequest

class ListAutomationExecutionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_EXECUTIONS_FIELD_NUMBER: builtins.int
    @property
    def automation_executions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[qwak.automation.v1.automation_execution_pb2.AutomationExecutionMessage]:
        """The automation executions."""
    def __init__(
        self,
        *,
        automation_executions: collections.abc.Iterable[qwak.automation.v1.automation_execution_pb2.AutomationExecutionMessage] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_executions", b"automation_executions"]) -> None: ...

global___ListAutomationExecutionsResponse = ListAutomationExecutionsResponse

class RegisterAutomationExecutionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    EXECUTION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to register."""
    execution_id: builtins.str
    """The execution id."""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
        execution_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id", "execution_id", b"execution_id"]) -> None: ...

global___RegisterAutomationExecutionRequest = RegisterAutomationExecutionRequest

class RegisterAutomationExecutionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___RegisterAutomationExecutionResponse = RegisterAutomationExecutionResponse

class UpdateAutomationExecutionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTION_ID_FIELD_NUMBER: builtins.int
    RUN_DETAILS_FIELD_NUMBER: builtins.int
    execution_id: builtins.str
    """The execution id to update."""
    @property
    def run_details(self) -> qwak.automation.v1.automation_execution_pb2.ExecutionRunDetailsMessage: ...
    def __init__(
        self,
        *,
        execution_id: builtins.str = ...,
        run_details: qwak.automation.v1.automation_execution_pb2.ExecutionRunDetailsMessage | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["run_details", b"run_details"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["execution_id", b"execution_id", "run_details", b"run_details"]) -> None: ...

global___UpdateAutomationExecutionRequest = UpdateAutomationExecutionRequest

class UpdateAutomationExecutionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UpdateAutomationExecutionResponse = UpdateAutomationExecutionResponse

class ToggleAutomationActivityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    IS_ENABLED_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to update"""
    is_enabled: builtins.bool
    """If the automation is enabled."""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
        is_enabled: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id", "is_enabled", b"is_enabled"]) -> None: ...

global___ToggleAutomationActivityRequest = ToggleAutomationActivityRequest

class ToggleAutomationActivityResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ToggleAutomationActivityResponse = ToggleAutomationActivityResponse

class RunAutomationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTOMATION_ID_FIELD_NUMBER: builtins.int
    automation_id: builtins.str
    """The automation id to run now"""
    def __init__(
        self,
        *,
        automation_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["automation_id", b"automation_id"]) -> None: ...

global___RunAutomationRequest = RunAutomationRequest

class RunAutomationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___RunAutomationResponse = RunAutomationResponse

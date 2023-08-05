import re
from abc import ABC
from dataclasses import dataclass, field
from typing import Dict

from _qwak_proto.qwak.automation.v1.action_pb2 import Action as ActionProto
from _qwak_proto.qwak.automation.v1.action_pb2 import BatchExecutionAction
from _qwak_proto.qwak.batch_job.v1.batch_job_service_pb2 import (
    AdvancedDeploymentOptions as BatchAdvancedDeploymentOptions,
)
from _qwak_proto.qwak.batch_job.v1.batch_job_service_pb2 import (
    BatchJobDataDetails,
    BatchJobDeploymentSize,
    BatchJobDestinationPath,
    BatchJobExecutionDetails,
    BatchJobModelDetails,
    BatchJobParameter,
    BatchJobRequest,
    BatchJobSourcePath,
    InputFileType,
    OutputFileType,
)
from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    GpuResources as GpuCommonResourcesProto,
)
from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    GpuType as GpuCommonType,
)
from qwak.automations.common import Action, map_memory_units, map_memory_units_proto

INPUT_FILE_TYPE_STRING_TO_ENUM = {
    "csv": InputFileType.CSV_INPUT_FILE_TYPE,
    "feather": InputFileType.FEATHER_INPUT_FILE_TYPE,
    "parquet": InputFileType.PARQUET_INPUT_FILE_TYPE,
}
INPUT_FILE_TYPE_ENUM_TO_STRING = {
    v: k for k, v in INPUT_FILE_TYPE_STRING_TO_ENUM.items()
}

OUTPUT_FILE_TYPE_STRING_TO_ENUM = {
    "csv": OutputFileType.CSV_OUTPUT_FILE_TYPE,
    "feather": OutputFileType.FEATHER_OUTPUT_FILE_TYPE,
    "parquet": OutputFileType.PARQUET_OUTPUT_FILE_TYPE,
}

OUTPUT_FILE_TYPE_ENUM_TO_STRING = {
    v: k for k, v in OUTPUT_FILE_TYPE_STRING_TO_ENUM.items()
}


def input_file_type_convert_to_enum(input_file_type: str):
    return INPUT_FILE_TYPE_STRING_TO_ENUM.get(
        input_file_type.lower(), InputFileType.UNDEFINED_INPUT_FILE_TYPE
    )


def input_file_type_convert_from_enum(input_file_type: InputFileType):
    return INPUT_FILE_TYPE_ENUM_TO_STRING.get(input_file_type, "")


def output_file_type_convert_to_enum(output_file_type: str):
    return OUTPUT_FILE_TYPE_STRING_TO_ENUM.get(
        output_file_type.lower(), OutputFileType.UNDEFINED_OUTPUT_FILE_TYPE
    )


def output_file_type_convert_from_enum(output_file_type: OutputFileType):
    return OUTPUT_FILE_TYPE_ENUM_TO_STRING.get(output_file_type, "")


@dataclass
class BatchJobDataSpecifications(ABC):
    access_token_secret_name: str = field(default=None)
    access_secret_secret_name: str = field(default=None)
    source_bucket: str = field(default=None)
    source_folder: str = field(default=None)
    input_file_type: str = field(default=None)
    destination_bucket: str = field(default=None)
    destination_folder: str = field(default=None)
    output_file_type: str = field(default=None)

    def to_proto(self):
        return BatchJobDataDetails(
            token_secret=self.access_token_secret_name,
            secret_secret=self.access_secret_secret_name,
            source_path=BatchJobSourcePath(
                source_bucket=self.source_bucket,
                source_folder=self.source_folder,
                input_file_type=input_file_type_convert_to_enum(self.input_file_type),
            ),
            destination_path=BatchJobDestinationPath(
                destination_bucket=self.destination_bucket,
                destination_folder=self.destination_folder,
                output_file_type=output_file_type_convert_to_enum(
                    self.output_file_type
                ),
            ),
        )

    @staticmethod
    def from_proto(message: BatchJobDataDetails):
        return BatchJobDataSpecifications(
            access_token_secret_name=message.token_secret,
            access_secret_secret_name=message.secret_secret,
            source_bucket=message.source_path.source_bucket,
            source_folder=message.source_path.source_folder,
            input_file_type=input_file_type_convert_from_enum(
                message.source_path.input_file_type
            ),
            destination_bucket=message.destination_path.destination_bucket,
            destination_folder=message.destination_path.destination_folder,
            output_file_type=output_file_type_convert_from_enum(
                message.destination_path.output_file_type
            ),
        )

    def __str__(self):
        return (
            f"token secret: {self.access_token_secret_name}\tsecret secret: {self.access_secret_secret_name}\t"
            f"source bucket: {self.source_bucket}\nsource folder: {self.source_folder}\ninput file type: {self.input_file_type}\n"
            f"destination bucket: {self.destination_bucket}\ndestination folder: {self.destination_folder}\noutput file type: {self.output_file_type}\n"
        )


@dataclass
class BatchJobExecutionSpecifications(ABC):
    job_timeout: int = field(default=0)
    task_timeout: int = field(default=0)
    executors: int = field(default=0)
    cpu: float = field(default=0)
    memory: str = field(default="0Mib")
    gpu_type: str = field(default=None)
    gpu_amount: int = field(default="0")
    custom_iam_role_arn: str = field(default="")
    params: Dict[str, str] = field(default_factory=dict)

    def to_proto(self):
        return BatchJobExecutionDetails(
            job_timeout=self.job_timeout,
            task_timeout=self.task_timeout,
            batch_job_deployment_size=BatchJobDeploymentSize(
                number_of_pods=self.executors,
                cpu=self.cpu,
                memory_units=map_memory_units(memory=self.memory),
                memory_amount=int(
                    re.sub(
                        r"\D",
                        "",
                        self.memory,
                    )
                ),
                gpu_resources=GpuCommonResourcesProto(
                    gpu_type=self.gpu_type,
                    gpu_amount=int(self.gpu_amount),
                ),
            ),
            advanced_deployment_options=BatchAdvancedDeploymentOptions(
                custom_iam_role_arn=self.custom_iam_role_arn
            ),
            parameters=parameters_as_list(self.params),
        )

    @staticmethod
    def from_proto(message: BatchJobExecutionDetails):
        return BatchJobExecutionSpecifications(
            job_timeout=message.job_timeout,
            task_timeout=message.task_timeout,
            executors=message.batch_job_deployment_size.number_of_pods,
            cpu=message.batch_job_deployment_size.cpu,
            memory=str(message.batch_job_deployment_size.memory_amount)
            + map_memory_units_proto(message.batch_job_deployment_size.memory_units),
            custom_iam_role_arn=message.advanced_deployment_options.custom_iam_role_arn,
            gpu_type=GpuCommonType.Name(
                message.batch_job_deployment_size.gpu_resources.gpu_type
            ),
            gpu_amount=str(message.batch_job_deployment_size.gpu_resources.gpu_amount),
            params=parmeters_as_dict(message.parameters),
        )

    def __str__(self):
        job_timeout_text = (
            f"job timeout: {self.job_timeout}\t" if self.job_timeout else ""
        )
        task_timeout_text = (
            f"task timeout: {self.task_timeout}\n" if self.task_timeout else ""
        )
        custom_iam_role_arn_text = (
            f"custom_iam_role_arn: {self.custom_iam_role_arn}\n"
            if self.custom_iam_role_arn
            else ""
        )
        gpu_text = (
            f"GPU Type: {self.gpu_type}, GPU Amount: {self.gpu_amount}"
            if int(self.gpu_amount) > 0
            else ""
        )
        resources_text = (
            gpu_text if gpu_text else f"CPU: {self.cpu}, Memory: {self.memory}"
        )
        return (
            f"{job_timeout_text}{task_timeout_text}"
            f"executors:{self.executors}\n"
            f"{custom_iam_role_arn_text}"
            f"{resources_text}"
        )


def parameters_as_list(params: dict):
    return [BatchJobParameter(key=key, value=value) for (key, value) in params.items()]


def parmeters_as_dict(parmas: list):
    return {param.key: param.value for param in parmas}


@dataclass
class BatchExecution(Action):
    build_id: str = field(default="")
    data_specifications: BatchJobDataSpecifications = field(
        default_factory=BatchJobExecutionSpecifications
    )
    execution_specifications: BatchJobExecutionSpecifications = field(
        default_factory=BatchJobExecutionSpecifications
    )

    def to_proto(self):
        return ActionProto(
            batch_execution=BatchExecutionAction(
                execute_batch_job=BatchJobRequest(
                    model_details=BatchJobModelDetails(build_id=self.build_id),
                    data_details=self.data_specifications.to_proto(),
                    execution_details=self.execution_specifications.to_proto(),
                )
            )
        )

    @staticmethod
    def from_proto(message: ActionProto):
        return BatchExecution(
            build_id=message.batch_execution.execute_batch_job.model_details.build_id,
            data_specifications=BatchJobDataSpecifications.from_proto(
                message.batch_execution.execute_batch_job.data_details
            ),
            execution_specifications=BatchJobExecutionSpecifications.from_proto(
                message.batch_execution.execute_batch_job.execution_details
            ),
        )

    def __str__(self):
        build_id_text = f"Running on Build Id{self.build_id}\n" if self.build_id else ""
        return f"Batch Execution:\n{build_id_text}Data Specifications:\n{self.data_specifications}\nExecution Specifications:\n{self.execution_specifications}"

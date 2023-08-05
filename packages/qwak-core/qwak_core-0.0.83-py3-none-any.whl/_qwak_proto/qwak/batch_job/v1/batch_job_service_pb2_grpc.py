# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from _qwak_proto.qwak.batch_job.v1 import batch_job_service_pb2 as qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2


class BatchJobManagementServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartBatchJob = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/StartBatchJob',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobResponse.FromString,
                )
        self.CancelBatchJob = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/CancelBatchJob',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobResponse.FromString,
                )
        self.StartWarmupJob = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/StartWarmupJob',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobResponse.FromString,
                )
        self.CancelWarmupJob = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/CancelWarmupJob',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobResponse.FromString,
                )
        self.GetBatchJobStatus = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobStatus',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusResponse.FromString,
                )
        self.GetBatchJobReport = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobReport',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportResponse.FromString,
                )
        self.UpdateBatchTasksStatus = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/UpdateBatchTasksStatus',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTasksStatusRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTaskStatusResponse.FromString,
                )
        self.ListBatchJobs = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/ListBatchJobs',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsResponse.FromString,
                )
        self.GetBatchJobDetails = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobDetails',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsResponse.FromString,
                )
        self.GetBatchJobPreSignedUploadUrl = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobPreSignedUploadUrl',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlResponse.FromString,
                )
        self.GetBatchJobPreSignedDownloadUrl = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobPreSignedDownloadUrl',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlResponse.FromString,
                )
        self.GetBatchJobUploadDetails = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobUploadDetails',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsResponse.FromString,
                )
        self.GetBatchJobDownloadDetails = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/GetBatchJobDownloadDetails',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsResponse.FromString,
                )
        self.UpdateDefaultParams = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/UpdateDefaultParams',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsResponse.FromString,
                )
        self.DeleteDefaultParams = channel.unary_unary(
                '/qwak.batchjob.BatchJobManagementService/DeleteDefaultParams',
                request_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsRequest.SerializeToString,
                response_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsResponse.FromString,
                )


class BatchJobManagementServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StartBatchJob(self, request, context):
        """Request from client to create a batch job
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelBatchJob(self, request, context):
        """Cancel Job
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartWarmupJob(self, request, context):
        """Request from client to create a warmup job
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelWarmupJob(self, request, context):
        """Cancel warmup
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobStatus(self, request, context):
        """Get the status of a batch job
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobReport(self, request, context):
        """Get the full batch job report
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateBatchTasksStatus(self, request, context):
        """Update batch task status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListBatchJobs(self, request, context):
        """Update batch task status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobDetails(self, request, context):
        """Get Batch Job Details
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobPreSignedUploadUrl(self, request, context):
        """Get Pre-signed URL for files upload
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobPreSignedDownloadUrl(self, request, context):
        """Get Pre-signed URL for files download
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobUploadDetails(self, request, context):
        """Get Paths for upload
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchJobDownloadDetails(self, request, context):
        """Get Object keys for download
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDefaultParams(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDefaultParams(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BatchJobManagementServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartBatchJob': grpc.unary_unary_rpc_method_handler(
                    servicer.StartBatchJob,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobResponse.SerializeToString,
            ),
            'CancelBatchJob': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelBatchJob,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobResponse.SerializeToString,
            ),
            'StartWarmupJob': grpc.unary_unary_rpc_method_handler(
                    servicer.StartWarmupJob,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobResponse.SerializeToString,
            ),
            'CancelWarmupJob': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelWarmupJob,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobResponse.SerializeToString,
            ),
            'GetBatchJobStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobStatus,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusResponse.SerializeToString,
            ),
            'GetBatchJobReport': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobReport,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportResponse.SerializeToString,
            ),
            'UpdateBatchTasksStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateBatchTasksStatus,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTasksStatusRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTaskStatusResponse.SerializeToString,
            ),
            'ListBatchJobs': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBatchJobs,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsResponse.SerializeToString,
            ),
            'GetBatchJobDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobDetails,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsResponse.SerializeToString,
            ),
            'GetBatchJobPreSignedUploadUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobPreSignedUploadUrl,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlResponse.SerializeToString,
            ),
            'GetBatchJobPreSignedDownloadUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobPreSignedDownloadUrl,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlResponse.SerializeToString,
            ),
            'GetBatchJobUploadDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobUploadDetails,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsResponse.SerializeToString,
            ),
            'GetBatchJobDownloadDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchJobDownloadDetails,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsResponse.SerializeToString,
            ),
            'UpdateDefaultParams': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDefaultParams,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsResponse.SerializeToString,
            ),
            'DeleteDefaultParams': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDefaultParams,
                    request_deserializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsRequest.FromString,
                    response_serializer=qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'qwak.batchjob.BatchJobManagementService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BatchJobManagementService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StartBatchJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/StartBatchJob',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartBatchJobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelBatchJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/CancelBatchJob',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelBatchJobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartWarmupJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/StartWarmupJob',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.StartWarmupJobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelWarmupJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/CancelWarmupJob',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.CancelWarmupJobResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobStatus',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobReport(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobReport',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobReportResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateBatchTasksStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/UpdateBatchTasksStatus',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTasksStatusRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateBatchTaskStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListBatchJobs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/ListBatchJobs',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.ListBatchJobsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobDetails',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobPreSignedUploadUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobPreSignedUploadUrl',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedUploadUrlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobPreSignedDownloadUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobPreSignedDownloadUrl',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobPreSignedDownloadUrlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobUploadDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobUploadDetails',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobUploadDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchJobDownloadDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/GetBatchJobDownloadDetails',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.GetBatchJobDownloadDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDefaultParams(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/UpdateDefaultParams',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.UpdateDefaultParamsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDefaultParams(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.batchjob.BatchJobManagementService/DeleteDefaultParams',
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsRequest.SerializeToString,
            qwak_dot_batch__job_dot_v1_dot_batch__job__service__pb2.DeleteDefaultParamsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

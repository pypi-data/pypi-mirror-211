# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/build/v1/build.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19qwak/build/v1/build.proto\x12\x11\x63om.qwak.build.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xda\x01\n\x0bModelSchema\x12+\n\x08\x65ntities\x18\x01 \x03(\x0b\x32\x19.com.qwak.build.v1.Entity\x12,\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x1a.com.qwak.build.v1.Feature\x12\x32\n\x0bpredictions\x18\x03 \x03(\x0b\x32\x1d.com.qwak.build.v1.Prediction\x12<\n\x10inference_output\x18\x04 \x03(\x0b\x32\".com.qwak.build.v1.InferenceOutput\"B\n\x06\x45ntity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\xc9\x02\n\x07\x46\x65\x61ture\x12\x38\n\rbatch_feature\x18\x01 \x01(\x0b\x32\x1f.com.qwak.build.v1.BatchFeatureH\x00\x12>\n\x10\x65xplicit_feature\x18\x02 \x01(\x0b\x32\".com.qwak.build.v1.ExplicitFeatureH\x00\x12@\n\x12on_the_fly_feature\x18\x03 \x01(\x0b\x32\".com.qwak.build.v1.OnTheFlyFeatureH\x00\x12@\n\x11streaming_feature\x18\x04 \x01(\x0b\x32#.com.qwak.build.v1.StreamingFeatureH\x00\x12\x38\n\rrequest_input\x18\x05 \x01(\x0b\x32\x1f.com.qwak.build.v1.RequestInputH\x00\x42\x06\n\x04type\"\x85\x01\n\x0fOnTheFlyFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x39\n\x0fsource_features\x18\x03 \x03(\x0b\x32 .com.qwak.build.v1.SourceFeature\"G\n\x0c\x42\x61tchFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"K\n\x10StreamingFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"K\n\x0f\x45xplicitFeature\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"H\n\x0cRequestInput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\x91\x01\n\rSourceFeature\x12>\n\x10\x65xplicit_feature\x18\x01 \x01(\x0b\x32\".com.qwak.build.v1.ExplicitFeatureH\x00\x12\x38\n\rrequest_input\x18\x02 \x01(\x0b\x32\x1f.com.qwak.build.v1.RequestInputH\x00\x42\x06\n\x04type\"F\n\nPrediction\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"K\n\x0fInferenceOutput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\xa1\x01\n\tValueType\x12\x30\n\x04type\x18\x01 \x01(\x0e\x32\".com.qwak.build.v1.ValueType.Types\"b\n\x05Types\x12\x0b\n\x07INVALID\x10\x00\x12\t\n\x05\x42YTES\x10\x01\x12\n\n\x06STRING\x10\x02\x12\t\n\x05INT32\x10\x03\x12\t\n\x05INT64\x10\x04\x12\n\n\x06\x44OUBLE\x10\x05\x12\t\n\x05\x46LOAT\x10\x06\x12\x08\n\x04\x42OOL\x10\x07\"j\n\x11ParameterCategory\"U\n\x08\x43\x61tegory\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06\x45NTITY\x10\x01\x12\x0b\n\x07\x46\x45\x41TURE\x10\x02\x12\x0e\n\nPREDICTION\x10\x03\x12\x13\n\x0fINFERENCEOUTPUT\x10\x04\"\x91\x04\n\x05\x42uild\x12\x0f\n\x07\x62uildId\x18\x01 \x01(\t\x12\x10\n\x08\x63ommitId\x18\x02 \x01(\t\x12\x10\n\x08\x62ranchId\x18\x03 \x01(\t\x12\x13\n\x0b\x62uildConfig\x18\x04 \x01(\t\x12\x34\n\x0c\x62uild_status\x18\x05 \x01(\x0e\x32\x1e.com.qwak.build.v1.BuildStatus\x12\x0c\n\x04tags\x18\x06 \x03(\t\x12\r\n\x05steps\x18\x07 \x03(\t\x12\x34\n\x06params\x18\x08 \x03(\x0b\x32$.com.qwak.build.v1.Build.ParamsEntry\x12\x36\n\x07metrics\x18\t \x03(\x0b\x32%.com.qwak.build.v1.Build.MetricsEntry\x12\x34\n\x0cmodel_schema\x18\n \x01(\x0b\x32\x1e.com.qwak.build.v1.ModelSchema\x12\'\n\x05\x61udit\x18\x0b \x01(\x0b\x32\x18.com.qwak.build.v1.Audit\x12\x12\n\nmodel_uuid\x18\x0c \x01(\t\x12\x13\n\x0bsdk_version\x18\r \x01(\t\x12\x16\n\x0eimage_name_tag\x18\x0e \x01(\t\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a.\n\x0cMetricsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\x9b\x01\n\x05\x41udit\x12\x12\n\ncreated_by\x18\x01 \x01(\t\x12.\n\ncreated_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x18\n\x10last_modified_by\x18\x03 \x01(\t\x12\x34\n\x10last_modified_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x93\x01\n\x0b\x42uildFilter\x12\x0c\n\x04tags\x18\x01 \x03(\t\x12\x37\n\x0emetric_filters\x18\x02 \x03(\x0b\x32\x1f.com.qwak.build.v1.MetricFilter\x12=\n\x11parameter_filters\x18\x03 \x03(\x0b\x32\".com.qwak.build.v1.ParameterFilter\"r\n\x0cMetricFilter\x12\x13\n\x0bmetric_name\x18\x01 \x01(\t\x12\x14\n\x0cmetric_value\x18\x02 \x01(\x02\x12\x37\n\x08operator\x18\x03 \x01(\x0e\x32%.com.qwak.build.v1.MetricOperatorType\"~\n\x0fParameterFilter\x12\x16\n\x0eparameter_name\x18\x01 \x01(\t\x12\x17\n\x0fparameter_value\x18\x02 \x01(\t\x12:\n\x08operator\x18\x03 \x01(\x0e\x32(.com.qwak.build.v1.ParameterOperatorType*\xe8\x01\n\x0b\x42uildStatus\x12\x0b\n\x07INVALID\x10\x00\x12\x0f\n\x0bIN_PROGRESS\x10\x01\x12\x0e\n\nSUCCESSFUL\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x12\x1d\n\x19REMOTE_BUILD_INITIALIZING\x10\x04\x12\x1a\n\x16REMOTE_BUILD_CANCELLED\x10\x05\x12\x1a\n\x16REMOTE_BUILD_TIMED_OUT\x10\x06\x12\x18\n\x14REMOTE_BUILD_UNKNOWN\x10\x07\x12\x18\n\x14SYNCING_ENVIRONMENTS\x10\x08\x12\x14\n\x10\x46INISHED_SYNCING\x10\t*\xa0\x02\n\x12MetricOperatorType\x12 \n\x1cMETRIC_OPERATOR_TYPE_INVALID\x10\x00\x12\x1f\n\x1bMETRIC_OPERATOR_TYPE_EQUALS\x10\x01\x12#\n\x1fMETRIC_OPERATOR_TYPE_NOT_EQUALS\x10\x02\x12\"\n\x1eMETRIC_OPERATOR_TYPE_LESS_THAN\x10\x03\x12)\n%METRIC_OPERATOR_TYPE_LESS_THAN_EQUALS\x10\x04\x12%\n!METRIC_OPERATOR_TYPE_GREATER_THAN\x10\x05\x12,\n(METRIC_OPERATOR_TYPE_GREATER_THAN_EQUALS\x10\x06*\x88\x01\n\x15ParameterOperatorType\x12#\n\x1fPARAMETER_OPERATOR_TYPE_INVALID\x10\x00\x12\"\n\x1ePARAMETER_OPERATOR_TYPE_EQUALS\x10\x01\x12&\n\"PARAMETER_OPERATOR_TYPE_NOT_EQUALS\x10\x02\x42!\n\x11\x63om.qwak.build.v1B\nBuildProtoP\x01\x62\x06proto3')

_BUILDSTATUS = DESCRIPTOR.enum_types_by_name['BuildStatus']
BuildStatus = enum_type_wrapper.EnumTypeWrapper(_BUILDSTATUS)
_METRICOPERATORTYPE = DESCRIPTOR.enum_types_by_name['MetricOperatorType']
MetricOperatorType = enum_type_wrapper.EnumTypeWrapper(_METRICOPERATORTYPE)
_PARAMETEROPERATORTYPE = DESCRIPTOR.enum_types_by_name['ParameterOperatorType']
ParameterOperatorType = enum_type_wrapper.EnumTypeWrapper(_PARAMETEROPERATORTYPE)
INVALID = 0
IN_PROGRESS = 1
SUCCESSFUL = 2
FAILED = 3
REMOTE_BUILD_INITIALIZING = 4
REMOTE_BUILD_CANCELLED = 5
REMOTE_BUILD_TIMED_OUT = 6
REMOTE_BUILD_UNKNOWN = 7
SYNCING_ENVIRONMENTS = 8
FINISHED_SYNCING = 9
METRIC_OPERATOR_TYPE_INVALID = 0
METRIC_OPERATOR_TYPE_EQUALS = 1
METRIC_OPERATOR_TYPE_NOT_EQUALS = 2
METRIC_OPERATOR_TYPE_LESS_THAN = 3
METRIC_OPERATOR_TYPE_LESS_THAN_EQUALS = 4
METRIC_OPERATOR_TYPE_GREATER_THAN = 5
METRIC_OPERATOR_TYPE_GREATER_THAN_EQUALS = 6
PARAMETER_OPERATOR_TYPE_INVALID = 0
PARAMETER_OPERATOR_TYPE_EQUALS = 1
PARAMETER_OPERATOR_TYPE_NOT_EQUALS = 2


_MODELSCHEMA = DESCRIPTOR.message_types_by_name['ModelSchema']
_ENTITY = DESCRIPTOR.message_types_by_name['Entity']
_FEATURE = DESCRIPTOR.message_types_by_name['Feature']
_ONTHEFLYFEATURE = DESCRIPTOR.message_types_by_name['OnTheFlyFeature']
_BATCHFEATURE = DESCRIPTOR.message_types_by_name['BatchFeature']
_STREAMINGFEATURE = DESCRIPTOR.message_types_by_name['StreamingFeature']
_EXPLICITFEATURE = DESCRIPTOR.message_types_by_name['ExplicitFeature']
_REQUESTINPUT = DESCRIPTOR.message_types_by_name['RequestInput']
_SOURCEFEATURE = DESCRIPTOR.message_types_by_name['SourceFeature']
_PREDICTION = DESCRIPTOR.message_types_by_name['Prediction']
_INFERENCEOUTPUT = DESCRIPTOR.message_types_by_name['InferenceOutput']
_VALUETYPE = DESCRIPTOR.message_types_by_name['ValueType']
_PARAMETERCATEGORY = DESCRIPTOR.message_types_by_name['ParameterCategory']
_BUILD = DESCRIPTOR.message_types_by_name['Build']
_BUILD_PARAMSENTRY = _BUILD.nested_types_by_name['ParamsEntry']
_BUILD_METRICSENTRY = _BUILD.nested_types_by_name['MetricsEntry']
_AUDIT = DESCRIPTOR.message_types_by_name['Audit']
_BUILDFILTER = DESCRIPTOR.message_types_by_name['BuildFilter']
_METRICFILTER = DESCRIPTOR.message_types_by_name['MetricFilter']
_PARAMETERFILTER = DESCRIPTOR.message_types_by_name['ParameterFilter']
_VALUETYPE_TYPES = _VALUETYPE.enum_types_by_name['Types']
_PARAMETERCATEGORY_CATEGORY = _PARAMETERCATEGORY.enum_types_by_name['Category']
ModelSchema = _reflection.GeneratedProtocolMessageType('ModelSchema', (_message.Message,), {
  'DESCRIPTOR' : _MODELSCHEMA,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ModelSchema)
  })
_sym_db.RegisterMessage(ModelSchema)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
  'DESCRIPTOR' : _ENTITY,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Entity)
  })
_sym_db.RegisterMessage(Entity)

Feature = _reflection.GeneratedProtocolMessageType('Feature', (_message.Message,), {
  'DESCRIPTOR' : _FEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Feature)
  })
_sym_db.RegisterMessage(Feature)

OnTheFlyFeature = _reflection.GeneratedProtocolMessageType('OnTheFlyFeature', (_message.Message,), {
  'DESCRIPTOR' : _ONTHEFLYFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.OnTheFlyFeature)
  })
_sym_db.RegisterMessage(OnTheFlyFeature)

BatchFeature = _reflection.GeneratedProtocolMessageType('BatchFeature', (_message.Message,), {
  'DESCRIPTOR' : _BATCHFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BatchFeature)
  })
_sym_db.RegisterMessage(BatchFeature)

StreamingFeature = _reflection.GeneratedProtocolMessageType('StreamingFeature', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.StreamingFeature)
  })
_sym_db.RegisterMessage(StreamingFeature)

ExplicitFeature = _reflection.GeneratedProtocolMessageType('ExplicitFeature', (_message.Message,), {
  'DESCRIPTOR' : _EXPLICITFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ExplicitFeature)
  })
_sym_db.RegisterMessage(ExplicitFeature)

RequestInput = _reflection.GeneratedProtocolMessageType('RequestInput', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTINPUT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.RequestInput)
  })
_sym_db.RegisterMessage(RequestInput)

SourceFeature = _reflection.GeneratedProtocolMessageType('SourceFeature', (_message.Message,), {
  'DESCRIPTOR' : _SOURCEFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.SourceFeature)
  })
_sym_db.RegisterMessage(SourceFeature)

Prediction = _reflection.GeneratedProtocolMessageType('Prediction', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTION,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Prediction)
  })
_sym_db.RegisterMessage(Prediction)

InferenceOutput = _reflection.GeneratedProtocolMessageType('InferenceOutput', (_message.Message,), {
  'DESCRIPTOR' : _INFERENCEOUTPUT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.InferenceOutput)
  })
_sym_db.RegisterMessage(InferenceOutput)

ValueType = _reflection.GeneratedProtocolMessageType('ValueType', (_message.Message,), {
  'DESCRIPTOR' : _VALUETYPE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ValueType)
  })
_sym_db.RegisterMessage(ValueType)

ParameterCategory = _reflection.GeneratedProtocolMessageType('ParameterCategory', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETERCATEGORY,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ParameterCategory)
  })
_sym_db.RegisterMessage(ParameterCategory)

Build = _reflection.GeneratedProtocolMessageType('Build', (_message.Message,), {

  'ParamsEntry' : _reflection.GeneratedProtocolMessageType('ParamsEntry', (_message.Message,), {
    'DESCRIPTOR' : _BUILD_PARAMSENTRY,
    '__module__' : 'qwak.build.v1.build_pb2'
    # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build.ParamsEntry)
    })
  ,

  'MetricsEntry' : _reflection.GeneratedProtocolMessageType('MetricsEntry', (_message.Message,), {
    'DESCRIPTOR' : _BUILD_METRICSENTRY,
    '__module__' : 'qwak.build.v1.build_pb2'
    # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build.MetricsEntry)
    })
  ,
  'DESCRIPTOR' : _BUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build)
  })
_sym_db.RegisterMessage(Build)
_sym_db.RegisterMessage(Build.ParamsEntry)
_sym_db.RegisterMessage(Build.MetricsEntry)

Audit = _reflection.GeneratedProtocolMessageType('Audit', (_message.Message,), {
  'DESCRIPTOR' : _AUDIT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Audit)
  })
_sym_db.RegisterMessage(Audit)

BuildFilter = _reflection.GeneratedProtocolMessageType('BuildFilter', (_message.Message,), {
  'DESCRIPTOR' : _BUILDFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildFilter)
  })
_sym_db.RegisterMessage(BuildFilter)

MetricFilter = _reflection.GeneratedProtocolMessageType('MetricFilter', (_message.Message,), {
  'DESCRIPTOR' : _METRICFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.MetricFilter)
  })
_sym_db.RegisterMessage(MetricFilter)

ParameterFilter = _reflection.GeneratedProtocolMessageType('ParameterFilter', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETERFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ParameterFilter)
  })
_sym_db.RegisterMessage(ParameterFilter)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021com.qwak.build.v1B\nBuildProtoP\001'
  _BUILD_PARAMSENTRY._options = None
  _BUILD_PARAMSENTRY._serialized_options = b'8\001'
  _BUILD_METRICSENTRY._options = None
  _BUILD_METRICSENTRY._serialized_options = b'8\001'
  _BUILDSTATUS._serialized_start=2793
  _BUILDSTATUS._serialized_end=3025
  _METRICOPERATORTYPE._serialized_start=3028
  _METRICOPERATORTYPE._serialized_end=3316
  _PARAMETEROPERATORTYPE._serialized_start=3319
  _PARAMETEROPERATORTYPE._serialized_end=3455
  _MODELSCHEMA._serialized_start=82
  _MODELSCHEMA._serialized_end=300
  _ENTITY._serialized_start=302
  _ENTITY._serialized_end=368
  _FEATURE._serialized_start=371
  _FEATURE._serialized_end=700
  _ONTHEFLYFEATURE._serialized_start=703
  _ONTHEFLYFEATURE._serialized_end=836
  _BATCHFEATURE._serialized_start=838
  _BATCHFEATURE._serialized_end=909
  _STREAMINGFEATURE._serialized_start=911
  _STREAMINGFEATURE._serialized_end=986
  _EXPLICITFEATURE._serialized_start=988
  _EXPLICITFEATURE._serialized_end=1063
  _REQUESTINPUT._serialized_start=1065
  _REQUESTINPUT._serialized_end=1137
  _SOURCEFEATURE._serialized_start=1140
  _SOURCEFEATURE._serialized_end=1285
  _PREDICTION._serialized_start=1287
  _PREDICTION._serialized_end=1357
  _INFERENCEOUTPUT._serialized_start=1359
  _INFERENCEOUTPUT._serialized_end=1434
  _VALUETYPE._serialized_start=1437
  _VALUETYPE._serialized_end=1598
  _VALUETYPE_TYPES._serialized_start=1500
  _VALUETYPE_TYPES._serialized_end=1598
  _PARAMETERCATEGORY._serialized_start=1600
  _PARAMETERCATEGORY._serialized_end=1706
  _PARAMETERCATEGORY_CATEGORY._serialized_start=1621
  _PARAMETERCATEGORY_CATEGORY._serialized_end=1706
  _BUILD._serialized_start=1709
  _BUILD._serialized_end=2238
  _BUILD_PARAMSENTRY._serialized_start=2145
  _BUILD_PARAMSENTRY._serialized_end=2190
  _BUILD_METRICSENTRY._serialized_start=2192
  _BUILD_METRICSENTRY._serialized_end=2238
  _AUDIT._serialized_start=2241
  _AUDIT._serialized_end=2396
  _BUILDFILTER._serialized_start=2399
  _BUILDFILTER._serialized_end=2546
  _METRICFILTER._serialized_start=2548
  _METRICFILTER._serialized_end=2662
  _PARAMETERFILTER._serialized_start=2664
  _PARAMETERFILTER._serialized_end=2790
# @@protoc_insertion_point(module_scope)

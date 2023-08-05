# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/kube_deployment_captain/feature_set_deployment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from _qwak_proto.qwak.feature_store.features import feature_set_types_pb2 as qwak_dot_feature__store_dot_features_dot_feature__set__types__pb2
from _qwak_proto.qwak.feature_store.entities import entity_pb2 as qwak_dot_feature__store_dot_entities_dot_entity__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9qwak/kube_deployment_captain/feature_set_deployment.proto\x12\x1cqwak.kube.deployment.captain\x1a\x33qwak/feature_store/features/feature_set_types.proto\x1a(qwak/feature_store/entities/entity.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe5\x06\n\x14\x46\x65\x61tureSetDeployment\x12\x17\n\x0f\x66\x65\x61tureset_name\x18\x01 \x01(\t\x12S\n\x15streaming_feature_set\x18\x02 \x01(\x0b\x32\x32.qwak.feature.store.features.StreamingFeatureSetV1H\x00\x12K\n\x11\x62\x61tch_feature_set\x18\x03 \x01(\x0b\x32..qwak.feature.store.features.BatchFeatureSetV1H\x00\x12h\n!streaming_aggregation_feature_set\x18\x04 \x01(\x0b\x32;.qwak.feature.store.features.StreamingAggregationFeatureSetH\x00\x12|\n\x1e\x65xtra_deployment_configuration\x18\x05 \x03(\x0b\x32T.qwak.kube.deployment.captain.FeatureSetDeployment.ExtraDeploymentConfigurationEntry\x12n\n\x17\x65xtra_env_configuration\x18\x06 \x03(\x0b\x32M.qwak.kube.deployment.captain.FeatureSetDeployment.ExtraEnvConfigurationEntry\x12=\n\x06\x65ntity\x18\x07 \x01(\x0b\x32-.qwak.feature.store.entities.EntityDefinition\x12\x15\n\rfeatureset_id\x18\x08 \x01(\t\x12\x1a\n\x12secret_service_url\x18\t \x01(\t\x12\x0e\n\x06run_id\x18\n \x01(\x03\x12&\n\x1eqwak_internal_protocol_version\x18\x0b \x01(\x05\x1a\x43\n!ExtraDeploymentConfigurationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a<\n\x1a\x45xtraEnvConfigurationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\r\n\x0b\x66\x65\x61ture_set\"\x94\x01\n\x0c\x42\x61tchDetails\x12\x38\n\x14\x62\x61tch_execution_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ntry_number\x18\x02 \x01(\x05\x12\x36\n\x12\x62\x61tch_trigger_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x84\x02\n\x18\x46\x65\x61tureSetDeploymentSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x46\n\x08metadata\x18\x03 \x01(\x0b\x32\x34.qwak.kube.deployment.captain.FeatureSetUserMetadata\x12>\n\x06\x65ntity\x18\x04 \x01(\x0b\x32..qwak.kube.deployment.captain.EntityDefinition\x12\x46\n\x10\x66\x65\x61ture_set_type\x18\x05 \x01(\x0b\x32,.qwak.kube.deployment.captain.FeatureSetType\"R\n\x16\x46\x65\x61tureSetUserMetadata\x12\r\n\x05owner\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\t\"d\n\x10\x45ntityDefinition\x12\x11\n\tentity_id\x18\x01 \x01(\t\x12=\n\x0b\x65ntity_spec\x18\x02 \x01(\x0b\x32(.qwak.kube.deployment.captain.EntitySpec\"p\n\x0e\x46\x65\x61tureSetType\x12R\n\x15streaming_feature_set\x18\x01 \x01(\x0b\x32\x31.qwak.kube.deployment.captain.StreamingFeatureSetH\x00\x42\n\n\x08set_type\"]\n\x13StreamingFeatureSet\x12\x46\n\x0b\x64\x61ta_source\x18\x01 \x01(\x0b\x32\x31.qwak.kube.deployment.captain.StreamingDataSource\"\xe6\x01\n\x0bKafkaSource\x12\x16\n\x0e\x63onsumer_topic\x18\x01 \x01(\t\x12!\n\x19\x63onsumer_bootstrap_server\x18\x02 \x01(\t\x12\x18\n\x10\x63onsumer_timeout\x18\x03 \x01(\t\x12\x16\n\x0e\x63onsumer_group\x18\x04 \x01(\t\x12\x18\n\x10\x61uto_offset_type\x18\x05 \x01(\t\x12\x17\n\x0fsecret_username\x18\x06 \x01(\t\x12\x17\n\x0fsecret_password\x18\x07 \x01(\t\x12\x1e\n\x16\x63onsumer_configuration\x18\x08 \x01(\t\"`\n\x13StreamingDataSource\x12\x41\n\x0ckafka_source\x18\x01 \x01(\x0b\x32).qwak.kube.deployment.captain.KafkaSourceH\x00\x42\x06\n\x04type\"z\n\nEntitySpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04keys\x18\x02 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12;\n\nvalue_type\x18\x04 \x01(\x0e\x32\'.qwak.kube.deployment.captain.ValueType*-\n\tValueType\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06STRING\x10\x01\x12\x07\n\x03INT\x10\x02\x42+\n\'com.qwak.ai.kube.deployment.captain.apiP\x01\x62\x06proto3')

_VALUETYPE = DESCRIPTOR.enum_types_by_name['ValueType']
ValueType = enum_type_wrapper.EnumTypeWrapper(_VALUETYPE)
INVALID = 0
STRING = 1
INT = 2


_FEATURESETDEPLOYMENT = DESCRIPTOR.message_types_by_name['FeatureSetDeployment']
_FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY = _FEATURESETDEPLOYMENT.nested_types_by_name['ExtraDeploymentConfigurationEntry']
_FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY = _FEATURESETDEPLOYMENT.nested_types_by_name['ExtraEnvConfigurationEntry']
_BATCHDETAILS = DESCRIPTOR.message_types_by_name['BatchDetails']
_FEATURESETDEPLOYMENTSPEC = DESCRIPTOR.message_types_by_name['FeatureSetDeploymentSpec']
_FEATURESETUSERMETADATA = DESCRIPTOR.message_types_by_name['FeatureSetUserMetadata']
_ENTITYDEFINITION = DESCRIPTOR.message_types_by_name['EntityDefinition']
_FEATURESETTYPE = DESCRIPTOR.message_types_by_name['FeatureSetType']
_STREAMINGFEATURESET = DESCRIPTOR.message_types_by_name['StreamingFeatureSet']
_KAFKASOURCE = DESCRIPTOR.message_types_by_name['KafkaSource']
_STREAMINGDATASOURCE = DESCRIPTOR.message_types_by_name['StreamingDataSource']
_ENTITYSPEC = DESCRIPTOR.message_types_by_name['EntitySpec']
FeatureSetDeployment = _reflection.GeneratedProtocolMessageType('FeatureSetDeployment', (_message.Message,), {

  'ExtraDeploymentConfigurationEntry' : _reflection.GeneratedProtocolMessageType('ExtraDeploymentConfigurationEntry', (_message.Message,), {
    'DESCRIPTOR' : _FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY,
    '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
    # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetDeployment.ExtraDeploymentConfigurationEntry)
    })
  ,

  'ExtraEnvConfigurationEntry' : _reflection.GeneratedProtocolMessageType('ExtraEnvConfigurationEntry', (_message.Message,), {
    'DESCRIPTOR' : _FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY,
    '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
    # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetDeployment.ExtraEnvConfigurationEntry)
    })
  ,
  'DESCRIPTOR' : _FEATURESETDEPLOYMENT,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetDeployment)
  })
_sym_db.RegisterMessage(FeatureSetDeployment)
_sym_db.RegisterMessage(FeatureSetDeployment.ExtraDeploymentConfigurationEntry)
_sym_db.RegisterMessage(FeatureSetDeployment.ExtraEnvConfigurationEntry)

BatchDetails = _reflection.GeneratedProtocolMessageType('BatchDetails', (_message.Message,), {
  'DESCRIPTOR' : _BATCHDETAILS,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.BatchDetails)
  })
_sym_db.RegisterMessage(BatchDetails)

FeatureSetDeploymentSpec = _reflection.GeneratedProtocolMessageType('FeatureSetDeploymentSpec', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETDEPLOYMENTSPEC,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetDeploymentSpec)
  })
_sym_db.RegisterMessage(FeatureSetDeploymentSpec)

FeatureSetUserMetadata = _reflection.GeneratedProtocolMessageType('FeatureSetUserMetadata', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETUSERMETADATA,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetUserMetadata)
  })
_sym_db.RegisterMessage(FeatureSetUserMetadata)

EntityDefinition = _reflection.GeneratedProtocolMessageType('EntityDefinition', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYDEFINITION,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.EntityDefinition)
  })
_sym_db.RegisterMessage(EntityDefinition)

FeatureSetType = _reflection.GeneratedProtocolMessageType('FeatureSetType', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETTYPE,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.FeatureSetType)
  })
_sym_db.RegisterMessage(FeatureSetType)

StreamingFeatureSet = _reflection.GeneratedProtocolMessageType('StreamingFeatureSet', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGFEATURESET,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.StreamingFeatureSet)
  })
_sym_db.RegisterMessage(StreamingFeatureSet)

KafkaSource = _reflection.GeneratedProtocolMessageType('KafkaSource', (_message.Message,), {
  'DESCRIPTOR' : _KAFKASOURCE,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.KafkaSource)
  })
_sym_db.RegisterMessage(KafkaSource)

StreamingDataSource = _reflection.GeneratedProtocolMessageType('StreamingDataSource', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGDATASOURCE,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.StreamingDataSource)
  })
_sym_db.RegisterMessage(StreamingDataSource)

EntitySpec = _reflection.GeneratedProtocolMessageType('EntitySpec', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYSPEC,
  '__module__' : 'qwak.kube_deployment_captain.feature_set_deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.kube.deployment.captain.EntitySpec)
  })
_sym_db.RegisterMessage(EntitySpec)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\'com.qwak.ai.kube.deployment.captain.apiP\001'
  _FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY._options = None
  _FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY._serialized_options = b'8\001'
  _FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY._options = None
  _FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY._serialized_options = b'8\001'
  _VALUETYPE._serialized_start=2355
  _VALUETYPE._serialized_end=2400
  _FEATURESETDEPLOYMENT._serialized_start=220
  _FEATURESETDEPLOYMENT._serialized_end=1089
  _FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY._serialized_start=945
  _FEATURESETDEPLOYMENT_EXTRADEPLOYMENTCONFIGURATIONENTRY._serialized_end=1012
  _FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY._serialized_start=1014
  _FEATURESETDEPLOYMENT_EXTRAENVCONFIGURATIONENTRY._serialized_end=1074
  _BATCHDETAILS._serialized_start=1092
  _BATCHDETAILS._serialized_end=1240
  _FEATURESETDEPLOYMENTSPEC._serialized_start=1243
  _FEATURESETDEPLOYMENTSPEC._serialized_end=1503
  _FEATURESETUSERMETADATA._serialized_start=1505
  _FEATURESETUSERMETADATA._serialized_end=1587
  _ENTITYDEFINITION._serialized_start=1589
  _ENTITYDEFINITION._serialized_end=1689
  _FEATURESETTYPE._serialized_start=1691
  _FEATURESETTYPE._serialized_end=1803
  _STREAMINGFEATURESET._serialized_start=1805
  _STREAMINGFEATURESET._serialized_end=1898
  _KAFKASOURCE._serialized_start=1901
  _KAFKASOURCE._serialized_end=2131
  _STREAMINGDATASOURCE._serialized_start=2133
  _STREAMINGDATASOURCE._serialized_end=2229
  _ENTITYSPEC._serialized_start=2231
  _ENTITYSPEC._serialized_end=2353
# @@protoc_insertion_point(module_scope)

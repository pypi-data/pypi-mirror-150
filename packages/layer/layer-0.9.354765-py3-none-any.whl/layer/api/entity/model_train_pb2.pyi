"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.entity.model_train_status_pb2
import layer.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ModelTrain(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _TrainType:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _TrainTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ModelTrain._TrainType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        TRAIN_TYPE_INVALID: ModelTrain._TrainType.ValueType  # 0
        TRAIN_TYPE_AD_HOC: ModelTrain._TrainType.ValueType  # 1
        TRAIN_TYPE_SCHEDULED: ModelTrain._TrainType.ValueType  # 2
    class TrainType(_TrainType, metaclass=_TrainTypeEnumTypeWrapper):
        pass

    TRAIN_TYPE_INVALID: ModelTrain.TrainType.ValueType  # 0
    TRAIN_TYPE_AD_HOC: ModelTrain.TrainType.ValueType  # 1
    TRAIN_TYPE_SCHEDULED: ModelTrain.TrainType.ValueType  # 2

    ID_FIELD_NUMBER: builtins.int
    MODEL_VERSION_ID_FIELD_NUMBER: builtins.int
    INDEX_FIELD_NUMBER: builtins.int
    URI_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    CREATED_BY_ID_FIELD_NUMBER: builtins.int
    START_TIMESTAMP_FIELD_NUMBER: builtins.int
    END_TIMESTAMP_FIELD_NUMBER: builtins.int
    TRAIN_TYPE_FIELD_NUMBER: builtins.int
    ORGANIZATION_ID_FIELD_NUMBER: builtins.int
    PROJECT_ID_FIELD_NUMBER: builtins.int
    HYPERPARAMETER_TUNING_ID_FIELD_NUMBER: builtins.int
    TRAIN_STATUS_FIELD_NUMBER: builtins.int
    @property
    def id(self) -> api.ids_pb2.ModelTrainId: ...
    @property
    def model_version_id(self) -> api.ids_pb2.ModelVersionId: ...
    index: builtins.int
    uri: typing.Text
    description: typing.Text
    @property
    def created_by_id(self) -> api.ids_pb2.UserId: ...
    start_timestamp: builtins.int
    end_timestamp: builtins.int
    train_type: global___ModelTrain.TrainType.ValueType
    @property
    def organization_id(self) -> api.ids_pb2.OrganizationId: ...
    @property
    def project_id(self) -> api.ids_pb2.ProjectId: ...
    @property
    def hyperparameter_tuning_id(self) -> api.ids_pb2.HyperparameterTuningId: ...
    @property
    def train_status(self) -> api.entity.model_train_status_pb2.ModelTrainStatus: ...
    def __init__(self,
        *,
        id: typing.Optional[api.ids_pb2.ModelTrainId] = ...,
        model_version_id: typing.Optional[api.ids_pb2.ModelVersionId] = ...,
        index: builtins.int = ...,
        uri: typing.Text = ...,
        description: typing.Text = ...,
        created_by_id: typing.Optional[api.ids_pb2.UserId] = ...,
        start_timestamp: builtins.int = ...,
        end_timestamp: builtins.int = ...,
        train_type: global___ModelTrain.TrainType.ValueType = ...,
        organization_id: typing.Optional[api.ids_pb2.OrganizationId] = ...,
        project_id: typing.Optional[api.ids_pb2.ProjectId] = ...,
        hyperparameter_tuning_id: typing.Optional[api.ids_pb2.HyperparameterTuningId] = ...,
        train_status: typing.Optional[api.entity.model_train_status_pb2.ModelTrainStatus] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_by_id",b"created_by_id","hyperparameter_tuning_id",b"hyperparameter_tuning_id","id",b"id","model_version_id",b"model_version_id","organization_id",b"organization_id","project_id",b"project_id","train_status",b"train_status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created_by_id",b"created_by_id","description",b"description","end_timestamp",b"end_timestamp","hyperparameter_tuning_id",b"hyperparameter_tuning_id","id",b"id","index",b"index","model_version_id",b"model_version_id","organization_id",b"organization_id","project_id",b"project_id","start_timestamp",b"start_timestamp","train_status",b"train_status","train_type",b"train_type","uri",b"uri"]) -> None: ...
global___ModelTrain = ModelTrain

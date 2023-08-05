"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.ids_pb2
import layer.api.value.sha256_pb2
import layer.api.value.signature_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ModelVersion(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _ModelFlavor:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _ModelFlavorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ModelVersion._ModelFlavor.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        MODEL_FLAVOR_INVALID: ModelVersion._ModelFlavor.ValueType  # 0
        MODEL_FLAVOR_PYFUNC: ModelVersion._ModelFlavor.ValueType  # 1
        MODEL_FLAVOR_H2O: ModelVersion._ModelFlavor.ValueType  # 2
        MODEL_FLAVOR_KERAS: ModelVersion._ModelFlavor.ValueType  # 3
        MODEL_FLAVOR_PYTORCH: ModelVersion._ModelFlavor.ValueType  # 4
        MODEL_FLAVOR_SKLEARN: ModelVersion._ModelFlavor.ValueType  # 5
        MODEL_FLAVOR_SPARK: ModelVersion._ModelFlavor.ValueType  # 6
        MODEL_FLAVOR_TENSORFLOW: ModelVersion._ModelFlavor.ValueType  # 7
        MODEL_FLAVOR_XGBOOST: ModelVersion._ModelFlavor.ValueType  # 8
        MODEL_FLAVOR_SPACY: ModelVersion._ModelFlavor.ValueType  # 9
        MODEL_FLAVOR_FASTAI: ModelVersion._ModelFlavor.ValueType  # 10
        MODEL_FLAVOR_LIGHTGBM: ModelVersion._ModelFlavor.ValueType  # 11
        MODEL_FLAVOR_CATBOOST: ModelVersion._ModelFlavor.ValueType  # 12
        MODEL_FLAVOR_HUGGINGFACE: ModelVersion._ModelFlavor.ValueType  # 13
    class ModelFlavor(_ModelFlavor, metaclass=_ModelFlavorEnumTypeWrapper):
        pass

    MODEL_FLAVOR_INVALID: ModelVersion.ModelFlavor.ValueType  # 0
    MODEL_FLAVOR_PYFUNC: ModelVersion.ModelFlavor.ValueType  # 1
    MODEL_FLAVOR_H2O: ModelVersion.ModelFlavor.ValueType  # 2
    MODEL_FLAVOR_KERAS: ModelVersion.ModelFlavor.ValueType  # 3
    MODEL_FLAVOR_PYTORCH: ModelVersion.ModelFlavor.ValueType  # 4
    MODEL_FLAVOR_SKLEARN: ModelVersion.ModelFlavor.ValueType  # 5
    MODEL_FLAVOR_SPARK: ModelVersion.ModelFlavor.ValueType  # 6
    MODEL_FLAVOR_TENSORFLOW: ModelVersion.ModelFlavor.ValueType  # 7
    MODEL_FLAVOR_XGBOOST: ModelVersion.ModelFlavor.ValueType  # 8
    MODEL_FLAVOR_SPACY: ModelVersion.ModelFlavor.ValueType  # 9
    MODEL_FLAVOR_FASTAI: ModelVersion.ModelFlavor.ValueType  # 10
    MODEL_FLAVOR_LIGHTGBM: ModelVersion.ModelFlavor.ValueType  # 11
    MODEL_FLAVOR_CATBOOST: ModelVersion.ModelFlavor.ValueType  # 12
    MODEL_FLAVOR_HUGGINGFACE: ModelVersion.ModelFlavor.ValueType  # 13

    ID_FIELD_NUMBER: builtins.int
    MODEL_ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    FLAVOR_FIELD_NUMBER: builtins.int
    SIGNATURE_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    MODEL_TRAIN_IDS_FIELD_NUMBER: builtins.int
    DEFAULT_TRAIN_ID_FIELD_NUMBER: builtins.int
    LATEST_TRAIN_ID_FIELD_NUMBER: builtins.int
    IS_DEFAULT_FIELD_NUMBER: builtins.int
    ORGANIZATION_ID_FIELD_NUMBER: builtins.int
    TRAINING_FILES_HASH_FIELD_NUMBER: builtins.int
    FABRIC_FIELD_NUMBER: builtins.int
    PROJECT_ID_FIELD_NUMBER: builtins.int
    @property
    def id(self) -> api.ids_pb2.ModelVersionId: ...
    @property
    def model_id(self) -> api.ids_pb2.ModelId: ...
    name: typing.Text
    flavor: global___ModelVersion.ModelFlavor.ValueType
    @property
    def signature(self) -> api.value.signature_pb2.Signature: ...
    description: typing.Text
    @property
    def model_train_ids(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[api.ids_pb2.ModelTrainId]: ...
    @property
    def default_train_id(self) -> api.ids_pb2.ModelTrainId: ...
    @property
    def latest_train_id(self) -> api.ids_pb2.ModelTrainId: ...
    is_default: builtins.bool
    @property
    def organization_id(self) -> api.ids_pb2.OrganizationId: ...
    @property
    def training_files_hash(self) -> api.value.sha256_pb2.Sha256: ...
    fabric: typing.Text
    @property
    def project_id(self) -> api.ids_pb2.ProjectId: ...
    def __init__(self,
        *,
        id: typing.Optional[api.ids_pb2.ModelVersionId] = ...,
        model_id: typing.Optional[api.ids_pb2.ModelId] = ...,
        name: typing.Text = ...,
        flavor: global___ModelVersion.ModelFlavor.ValueType = ...,
        signature: typing.Optional[api.value.signature_pb2.Signature] = ...,
        description: typing.Text = ...,
        model_train_ids: typing.Optional[typing.Iterable[api.ids_pb2.ModelTrainId]] = ...,
        default_train_id: typing.Optional[api.ids_pb2.ModelTrainId] = ...,
        latest_train_id: typing.Optional[api.ids_pb2.ModelTrainId] = ...,
        is_default: builtins.bool = ...,
        organization_id: typing.Optional[api.ids_pb2.OrganizationId] = ...,
        training_files_hash: typing.Optional[api.value.sha256_pb2.Sha256] = ...,
        fabric: typing.Text = ...,
        project_id: typing.Optional[api.ids_pb2.ProjectId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["default_train_id",b"default_train_id","id",b"id","latest_train_id",b"latest_train_id","model_id",b"model_id","organization_id",b"organization_id","project_id",b"project_id","signature",b"signature","training_files_hash",b"training_files_hash"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["default_train_id",b"default_train_id","description",b"description","fabric",b"fabric","flavor",b"flavor","id",b"id","is_default",b"is_default","latest_train_id",b"latest_train_id","model_id",b"model_id","model_train_ids",b"model_train_ids","name",b"name","organization_id",b"organization_id","project_id",b"project_id","signature",b"signature","training_files_hash",b"training_files_hash"]) -> None: ...
global___ModelVersion = ModelVersion

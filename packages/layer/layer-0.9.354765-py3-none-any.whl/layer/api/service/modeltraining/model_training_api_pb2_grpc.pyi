"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import layer.api.service.modeltraining.model_training_api_pb2
import grpc

class ModelTrainingAPIStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    GetSourceCodeUploadCredentials: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.GetSourceCodeUploadCredentialsRequest,
        api.service.modeltraining.model_training_api_pb2.GetSourceCodeUploadCredentialsResponse]

    StartModelTraining: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.StartModelTrainingRequest,
        api.service.modeltraining.model_training_api_pb2.StartModelTrainingResponse]
    """model train"""

    CancelModelTraining: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.CancelModelTrainingRequest,
        api.service.modeltraining.model_training_api_pb2.CancelModelTrainingResponse]
    """CancelModelTraining is not guaranteed to succeed and shall return return immediately.
    A client can use the GetModelTrainStatus to know if cancellation eventually succeeds.
    """

    GetModelTrainStatus: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.GetModelTrainStatusRequest,
        api.service.modeltraining.model_training_api_pb2.GetModelTrainStatusResponse]

    StartHyperparameterTuning: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.StartHyperparameterTuningRequest,
        api.service.modeltraining.model_training_api_pb2.StartHyperparameterTuningResponse]
    """hpt model train"""

    CancelHyperparameterTuning: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.CancelHyperparameterTuningRequest,
        api.service.modeltraining.model_training_api_pb2.CancelHyperparameterTuningResponse]
    """CancelHyperparameterTuning is not guaranteed to succeed and shall return return immediately.
    A client can use the GetHyperparameterTuningStatus to know if cancellation eventually succeeds.
    """

    GetHyperparameterTuningStatus: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningStatusRequest,
        api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningStatusResponse]

    CreateHyperparameterTuning: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.CreateHyperparameterTuningRequest,
        api.service.modeltraining.model_training_api_pb2.CreateHyperparameterTuningResponse]

    GetHyperparameterTuning: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningRequest,
        api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningResponse]

    UpdateHyperparameterTuning: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.UpdateHyperparameterTuningRequest,
        api.service.modeltraining.model_training_api_pb2.UpdateHyperparameterTuningResponse]

    StoreHyperparameterTuningMetadata: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.StoreHyperparameterTuningMetadataRequest,
        api.service.modeltraining.model_training_api_pb2.StoreHyperparameterTuningMetadataResponse]

    GetOrCreateLatestPendingHyperparameterTuningId: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_api_pb2.GetOrCreateLatestPendingHyperparameterTuningIdRequest,
        api.service.modeltraining.model_training_api_pb2.GetOrCreateLatestPendingHyperparameterTuningIdResponse]


class ModelTrainingAPIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def GetSourceCodeUploadCredentials(self,
        request: api.service.modeltraining.model_training_api_pb2.GetSourceCodeUploadCredentialsRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.GetSourceCodeUploadCredentialsResponse: ...

    @abc.abstractmethod
    def StartModelTraining(self,
        request: api.service.modeltraining.model_training_api_pb2.StartModelTrainingRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.StartModelTrainingResponse:
        """model train"""
        pass

    @abc.abstractmethod
    def CancelModelTraining(self,
        request: api.service.modeltraining.model_training_api_pb2.CancelModelTrainingRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.CancelModelTrainingResponse:
        """CancelModelTraining is not guaranteed to succeed and shall return return immediately.
        A client can use the GetModelTrainStatus to know if cancellation eventually succeeds.
        """
        pass

    @abc.abstractmethod
    def GetModelTrainStatus(self,
        request: api.service.modeltraining.model_training_api_pb2.GetModelTrainStatusRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.GetModelTrainStatusResponse: ...

    @abc.abstractmethod
    def StartHyperparameterTuning(self,
        request: api.service.modeltraining.model_training_api_pb2.StartHyperparameterTuningRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.StartHyperparameterTuningResponse:
        """hpt model train"""
        pass

    @abc.abstractmethod
    def CancelHyperparameterTuning(self,
        request: api.service.modeltraining.model_training_api_pb2.CancelHyperparameterTuningRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.CancelHyperparameterTuningResponse:
        """CancelHyperparameterTuning is not guaranteed to succeed and shall return return immediately.
        A client can use the GetHyperparameterTuningStatus to know if cancellation eventually succeeds.
        """
        pass

    @abc.abstractmethod
    def GetHyperparameterTuningStatus(self,
        request: api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningStatusRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningStatusResponse: ...

    @abc.abstractmethod
    def CreateHyperparameterTuning(self,
        request: api.service.modeltraining.model_training_api_pb2.CreateHyperparameterTuningRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.CreateHyperparameterTuningResponse: ...

    @abc.abstractmethod
    def GetHyperparameterTuning(self,
        request: api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.GetHyperparameterTuningResponse: ...

    @abc.abstractmethod
    def UpdateHyperparameterTuning(self,
        request: api.service.modeltraining.model_training_api_pb2.UpdateHyperparameterTuningRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.UpdateHyperparameterTuningResponse: ...

    @abc.abstractmethod
    def StoreHyperparameterTuningMetadata(self,
        request: api.service.modeltraining.model_training_api_pb2.StoreHyperparameterTuningMetadataRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.StoreHyperparameterTuningMetadataResponse: ...

    @abc.abstractmethod
    def GetOrCreateLatestPendingHyperparameterTuningId(self,
        request: api.service.modeltraining.model_training_api_pb2.GetOrCreateLatestPendingHyperparameterTuningIdRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_api_pb2.GetOrCreateLatestPendingHyperparameterTuningIdResponse: ...


def add_ModelTrainingAPIServicer_to_server(servicer: ModelTrainingAPIServicer, server: grpc.Server) -> None: ...

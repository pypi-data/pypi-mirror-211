from functools import wraps
from typing import Any, Dict, List, Union

from urllib import request
from loguru import logger

from netspresso.compressor.client import (
    ModelCompressorAPIClient,
    Task,
    Framework,
    CompressionMethod,
    RecommendationMethod,
)
from netspresso.compressor.client.schemas.auth import CreditResponse, LoginRequest, RefreshTokenRequest
from netspresso.compressor.client.schemas.model import UploadModelRequest
from netspresso.compressor.client.schemas.compression import (
    AutoCompressionRequest,
    CompressionRequest,
    GetAvailableLayersRequest,
    CreateCompressionRequest,
    RecommendationRequest,
)
from netspresso.compressor.core.model import CompressedModel, Model
from netspresso.compressor.core.compression import CompressionBase, CompressionInfo
from netspresso.compressor.utils.token import check_jwt_exp


class ModelCompressor:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.client = ModelCompressorAPIClient()
        self.__login()

    def __login(self) -> None:
        try:
            data = LoginRequest(username=self.email, password=self.password)
            response = self.client.login(data)
            self.access_token = response.access_token
            self.refresh_token = response.refresh_token
            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Login failed. Error: {e}")
            raise e

    def validate_token(func) -> None:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not check_jwt_exp(self.access_token):
                self.__reissue_token()
            return func(self, *args, **kwargs)

        return wrapper

    def __reissue_token(self) -> None:
        try:
            data = RefreshTokenRequest(access_token=self.access_token, refresh_token=self.refresh_token)
            response = self.client.refresh_token(data)
            self.access_token = response.access_token
            self.refresh_token = response.refresh_token

        except Exception as e:
            raise e

    @validate_token
    def get_credit(self) -> CreditResponse:
        """Retrieve credit information.

        Raises:
            e: An exception that occurred while retrieving credit information.

        Returns:
            CreditResponse: Credit information response.
        """
        try:
            credit = self.client.get_credit(access_token=self.access_token)
            logger.info(f"Get Credit successful. Credit: {credit.total}")

            return credit

        except Exception as e:
            logger.error(f"Get Credit failed. Error: {e}")
            raise e

    @validate_token
    def upload_model(
        self, model_name: str, task: Task, framework: Framework, file_path: str, input_layers: List = []
    ) -> Model:
        """Upload a model.

        Args:
            model_name (str): Name of the model.
            task (Task): Task type of the model.
            framework (Framework): Framework used for the model.
            file_path (str): File path of the model.
            input_layers (List, optional): List of input layers for the model. Defaults to [].

        Raises:
            e: If an error occurs while uploading the model.

        Returns:
            Model: Uploaded model object.
        """
        try:
            logger.info("Uploading Model...")
            data = UploadModelRequest(
                model_name=model_name,
                task=task.value,
                framework=framework.value,
                file_path=file_path,
                input_layers=input_layers,
            )
            model_info = self.client.upload_model(data=data, access_token=self.access_token)
            model = Model(model_info)
            logger.info(f"Upload model successful. Model ID: {model.model_id}")

            return model

        except Exception as e:
            logger.error(f"Upload model failed. Error: {e}")
            raise e

    @validate_token
    def get_models(self) -> List[Dict[str, Any]]:
        """Retrieve the list of models.

        Raises:
            e: An exception occurred while retrieving the model list.

        Returns:
            List[Dict[str, Any]]: The list of models.
        """
        try:
            logger.info("Getting model list...")
            models = []
            parent_models = self.client.get_parent_models(is_simple=True, access_token=self.access_token)
            uploaded_models = [
                vars(Model(parent_model)) for parent_model in parent_models if parent_model.origin_from == "custom"
            ]
            for uploaded_model in uploaded_models:
                children_models = self.client.get_children_models(
                    model_id=uploaded_model["model_id"], access_token=self.access_token
                )
                uploaded_model["compressed_models"] = [
                    vars(CompressedModel(children_model)) for children_model in children_models
                ]
                models.append(uploaded_model)
            logger.info("Get model list successful.")

            return models

        except Exception as e:
            logger.error(f"Get model list failed. Error: {e}")
            raise e

    @validate_token
    def get_uploaded_models(self) -> List[Dict[str, Any]]:
        """Retrieve the list of uploaded models.

        Raises:
            e: An exception occurred while retrieving the uploaded model list.

        Returns:
            List[Dict[str, Any]]: The list of uploaded models.
        """
        try:
            logger.info("Getting uploaded model list...")
            parent_models = self.client.get_parent_models(is_simple=True, access_token=self.access_token)
            uploaded_models = [
                vars(Model(parent_model)) for parent_model in parent_models if parent_model.origin_from == "custom"
            ]
            logger.info("Get uploaded model list successful.")

            return uploaded_models

        except Exception as e:
            logger.error(f"Get uploaded model list failed. Error: {e}")
            raise e

    @validate_token
    def get_compressed_models(self, model_id: str) -> List[Dict[str, Any]]:
        """Retrieve the list of compressed models for a given model.

        Args:
            model_id (str): The ID of the model.

        Raises:
            e: An exception occurred while retrieving the compressed model list.

        Returns:
            List[Dict[str, Any]]: The list of compressed models.
        """
        try:
            logger.info("Getting compressed model list...")
            children_models = self.client.get_children_models(model_id=model_id, access_token=self.access_token)
            compressed_models = [vars(CompressedModel(children_model)) for children_model in children_models]
            logger.info("Get compressed model list successful.")

            return compressed_models

        except Exception as e:
            logger.error(f"Get compressed model list failed. Error: {e}")
            raise e

    @validate_token
    def get_model(self, model_id: str) -> Union[Model, CompressedModel]:
        """Retrieve a specific model by its ID.

        Args:
            model_id (str): The ID of the model.

        Raises:
            e: An exception occurred while retrieving the model.

        Returns:
            Union[Model, CompressedModel]: The retrieved model.
        """
        try:
            logger.info("Getting model...")
            model_info = self.client.get_model_info(model_id=model_id, access_token=self.access_token)
            if model_info.status.is_compressed:
                model = CompressedModel(model_info)
            else:
                model = Model(model_info)
            logger.info("Get model successful.")

            return model

        except Exception as e:
            logger.error(f"Get model failed. Error: {e}")
            raise e

    @validate_token
    def download_model(self, model_id: str, local_path: str) -> None:
        """Download a specific model to the local file system.

        Args:
            model_id (str): The ID of the model.
            local_path (str): The local path to save the downloaded model.

        Raises:
            e: An exception occurred while downloading the model.
        """
        try:
            logger.info("Downloading model...")
            download_link = self.client.get_download_model_link(model_id=model_id, access_token=self.access_token)
            request.urlretrieve(download_link.url, local_path)
            logger.info(f"Download model successful. Local Path: {local_path}")

        except Exception as e:
            logger.error(f"Download model failed. Error: {e}")
            raise e

    @validate_token
    def delete_model(self, model_id: str, recursive: bool = False) -> None:
        """Delete a model.

        Args:
            model_id (str): The ID of the model to delete.
            recursive (bool, optional): Whether to delete the compressed model for that model. Defaults to False.

        Raises:
            e: An exception occurred while deleting the model.
        """
        try:
            logger.info("Deleting model...")
            children_models = self.client.get_children_models(model_id=model_id, access_token=self.access_token)
            if len(children_models) != 0:
                if not recursive:
                    logger.warning(
                        "Deleting the model will also delete its compressed models. To proceed with the deletion, set the `recursive` parameter to True."
                    )
                else:
                    logger.info("The compressed model for that model will also be deleted.")
                    self.client.delete_model(model_id=model_id, access_token=self.access_token)
                    logger.info("Delete model successful.")
            else:
                logger.info("The model will be deleted.")
                self.client.delete_model(model_id=model_id, access_token=self.access_token)
                logger.info("Delete model successful.")

        except Exception as e:
            logger.error(f"Delete model failed. Error: {e}")
            raise e

    @validate_token
    def select_compression_method(self, model_id: str, compression_method: CompressionMethod) -> CompressionBase:
        """Select a compression method for a model.

        Args:
            model_id (str): The ID of the model.
            compression_method (CompressionMethod): The compression method to use.

        Raises:
            e: An exception occurred while selecting the compression method.

        Returns:
            CompressionBase: The compression information for the selected compression method.
        """
        try:
            logger.info("Selecting compression method...")
            data = GetAvailableLayersRequest(model_id=model_id, compression_method=compression_method.value)
            response = self.client.get_available_layers(data=data, access_token=self.access_token)
            compression_info = CompressionBase(compression_method.value, response.available_layers, model_id)
            logger.info("Select compression method successful.")

            return compression_info

        except Exception as e:
            logger.error(f"Select compression method failed. Error: {e}")
            raise e

    @validate_token
    def get_compression(self, compression_id: str) -> CompressionInfo:
        """Get information about a compression.

        Args:
            compression_id (str): The ID of the compression.

        Raises:
            e: An exception occurred while getting the compression information.

        Returns:
            CompressionInfo: The information about the compression.
        """
        try:
            logger.info("Getting compression...")
            compression_info = CompressionInfo(
                self.client.get_compression_info(compression_id=compression_id, access_token=self.access_token)
            )
            logger.info("Get compression successful.")

            return compression_info

        except Exception as e:
            logger.error(f"Get compression failed. Error: {e}")
            raise e

    @validate_token
    def compress_model(self, compression: CompressionInfo, model_name: str, output_path: str) -> CompressedModel:
        """Compress a model using the provided compression information.

        Args:
            compression (CompressionInfo): Information about the compression.
            model_name (str): Name of the compressed model.
            output_path (str): Local path to save the compressed model.

        Raises:
            e: An exception occurred while compressing the model.

        Returns:
            CompressedModel: The compressed model.
        """
        try:
            logger.info("Compressing model...")
            data = CreateCompressionRequest(
                model_id=compression.model_id,
                model_name=model_name,
                compression_method=compression.compression_method,
            )
            compression_info = self.client.create_compression(data=data, access_token=self.access_token)

            for available_layers in compression.available_layers:
                if available_layers.values != [""]:
                    available_layers.use = True

            data = CompressionRequest(
                compression_id=compression_info.compression_id,
                compression_method=compression.compression_method,
                layers=compression.available_layers,
                compressed_model_id=compression_info.new_model_id,
            )
            self.client.compress_model(data=data, access_token=self.access_token)
            self.download_model(model_id=compression_info.new_model_id, local_path=output_path)
            compressed_model = self.get_model(model_id=compression_info.new_model_id)
            logger.info(f"Compress model successful. Compressed Model ID: {compressed_model.model_id}")
            logger.info("50 credits have been consumed.")

            return compressed_model

        except Exception as e:
            logger.error(f"Compress model failed. Error: {e}")
            raise e

    @validate_token
    def recommendation_compression(
        self,
        model_id: str,
        model_name: str,
        compression_method: CompressionMethod,
        recommendation_method: RecommendationMethod,
        recommendation_ratio: float,
        output_path: str,
    ) -> CompressedModel:
        """Compress a recommendation-based model using the specified compression and recommendation methods.

        Args:
            model_id (str): The ID of the model to be compressed.
            model_name (str): The name of the compressed model.
            compression_method (CompressionMethod): The compression method to be used.
            recommendation_method (RecommendationMethod): The recommendation method to be used.
            recommendation_ratio (float): The compression ratio recommended by the recommendation method.
            output_path (str): The local path to save the compressed model.

        Raises:
            e: An exception occurred while performing recommendation compression.

        Returns:
            CompressedModel: The compressed model.
        """
        try:
            logger.info("Compressing recommendation-based model...")
            data = CreateCompressionRequest(
                model_id=model_id,
                model_name=model_name,
                compression_method=compression_method.value,
            )
            compression_info = self.client.create_compression(data=data, access_token=self.access_token)

            data = RecommendationRequest(
                model_id=model_id,
                compression_id=compression_info.compression_id,
                recommendation_method=recommendation_method.value,
                recommendation_ratio=recommendation_ratio,
            )
            recommendation_result = self.client.get_recommendation(data=data, access_token=self.access_token)

            for available_layer, recommended_info in zip(
                compression_info.available_layers, recommendation_result.recommended_layers
            ):
                available_layer.use = True
                available_layer.values = recommended_info.values

            data = CompressionRequest(
                compression_id=compression_info.compression_id,
                compression_method=compression_method.value,
                layers=compression_info.available_layers,
                compressed_model_id=compression_info.new_model_id,
            )
            self.client.compress_model(data=data, access_token=self.access_token)
            self.download_model(model_id=compression_info.new_model_id, local_path=output_path)
            compressed_model = self.get_model(model_id=compression_info.new_model_id)
            logger.info(f"Recommendation compression successful. Compressed Model ID: {compressed_model.model_id}")
            logger.info("50 credits have been consumed.")

            return compressed_model

        except Exception as e:
            logger.error(f"Recommendation compression failed. Error: {e}")
            raise e

    @validate_token
    def automatic_compression(
        self, model_id: str, model_name: str, compression_ratio: float, output_path: str
    ) -> CompressedModel:
        """Compress a model automatically based on the specified compression ratio.

        Args:
            model_id (str): The ID of the model to be compressed.
            model_name (str): The name of the compressed model.
            compression_ratio (float): The target compression ratio for automatic compression.
            output_path (str): The local path to save the compressed model.

        Raises:
            e: An exception occurred while performing automatic compression.

        Returns:
            CompressedModel: The compressed model.
        """
        try:
            logger.info("Compressing automatic-based model...")
            data = AutoCompressionRequest(
                model_id=model_id,
                model_name=model_name,
                recommendation_ratio=compression_ratio,
                save_path=output_path,
            )
            model_info = self.client.auto_compression(data=data, access_token=self.access_token)
            self.download_model(model_id=model_info.model_id, local_path=output_path)
            compressed_model = CompressedModel(model_info)
            logger.info(f"Automatic compression successful. Compressed Model ID: {compressed_model.model_id}")
            logger.info("25 credits have been consumed.")

            return compressed_model

        except Exception as e:
            logger.error(f"Automatic compression failed. Error: {e}")
            raise e

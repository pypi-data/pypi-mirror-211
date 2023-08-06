import json
from typing import List, Any
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator, HttpUrl
from loguru import logger

from .common import TASK, FRAMEWORK, ORIGIN_FROM


class InputLayer(BaseModel):
    batch: Any = Field(0, description="Input Batch")
    channel: int = Field(0, description="Input Channel")
    dimension: List[int] = Field([0], description="Input Diemension")


class UploadModelRequest(BaseModel):
    model_name: str = Field(..., description="Model Name")
    description: str = Field("", description="Description")
    task: TASK = Field(..., description="Task")
    framework: FRAMEWORK = Field(..., description="Framework")
    input_layers: List[InputLayer] = Field(None, description="Input Layers")
    file_path: str = Field(..., description="Model Path")
    # metric_unit: str = Field("", description="Metric Unit")
    # metric_value: float = Field(0, description="Metric Value")

    @validator("input_layers")
    def validate_input_layers(cls, value):
        if value:
            input_layers = []
            for v in value:
                if any((v.batch == 0, v.channel == 0, v.dimension == [0])):
                    return None
                input_layers.append(v.dict())
            return json.dumps(input_layers)
        else:
            return None

    @root_validator(pre=True, skip_on_failure=True)
    def validate_input_shape(cls, values):
        framework = values.get("framework")
        input_layers = values.get("input_layers")

        if framework == "pytorch" and input_layers is None:
            logger.info("Please fill in Input Layers fields.")

        return values


class Spec(BaseModel):
    input_layers: List[InputLayer] = Field([], description="Input Layers")
    model_size: float = Field(0, description="Model Size")
    flops: float = Field(0, description="FLOPs")
    trainable_parameters: float = Field(0, description="Trainable Parameters")
    non_trainable_parameters: float = Field(0, description="Non Trainable Parameters")
    number_of_layers: int = Field(0, description="Number of Layers")


class Status(BaseModel):
    is_convertible: bool = Field(False, description="Convertible Status")
    is_packageable: bool = Field(False, description="Packageable Status")
    is_compressible: bool = Field(False, description="Compressible Status")
    is_visible: bool = Field(False, description="Visible Status")
    is_compressed: bool = Field(False, description="Compressed Status")
    is_trained: bool = Field(False, description="Trained Status")
    is_downloadable: bool = Field(False, description="Downloadable Status")
    is_retrainable: bool = Field(False, description="Retrainable Status")


class Metric(BaseModel):
    metric_unit: str = Field("", description="Metric Unit")
    metric_value: float = Field(None, description="Metric Value")


class Device(BaseModel):
    name: str = Field("", description="Device Name")
    total_latency: float = Field(0, description="Total Latency of Model")
    performance: List = Field([], description="Metric Value")
    spec: List = Field([], description="Metric Value")
    layers: List = Field([], description="Metric Value")


class ModelResponse(BaseModel):
    model_id: UUID = Field(..., description="Model ID")
    model_name: str = Field(..., description="Model Name")
    description: str = Field("", description="Description")
    original_model_id: str = Field(..., description="Original Model ID")
    original_compression_id: str = Field("", description="Compression ID")
    task: TASK = Field(..., description="Task")
    framework: FRAMEWORK = Field(..., description="Framework")
    origin_from: ORIGIN_FROM = Field(..., description="Origin From(Model Source)")
    target_device: str = Field("", description="Target Device")
    metric: Metric = Field(..., description="Metric")
    spec: Spec = Field(..., description="Spec")
    status: Status = Field(..., description="Status")
    devices: List[Device] = Field([], description="Devices")
    # edges: List = Field([], description="Edges")
    # nodes: List = Field([], description="Nodes")


class GetDownloadLinkResponse(BaseModel):
    url: HttpUrl = Field(..., description="Model Path")

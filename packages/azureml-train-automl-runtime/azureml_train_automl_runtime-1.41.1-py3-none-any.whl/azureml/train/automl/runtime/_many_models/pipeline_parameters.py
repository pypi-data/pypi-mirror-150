# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict
from abc import ABC
from azureml.automl.core.shared.exceptions import ConfigException
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import DNNNotSupportedForManyModel
from azureml.automl.core.shared.reference_codes import ReferenceCodes


class TrainPipelineParameters(ABC):
    def __init__(self, automl_settings: Dict[str, Any]):
        self.automl_settings = automl_settings

    def validate(self):
        if self.automl_settings.get("enable_dnn", False):
            raise ConfigException._with_error(
                AzureMLError.create(
                    DNNNotSupportedForManyModel,
                    reference_code=ReferenceCodes._VALIDATE_DNN_ENABLED_MANY_MODELS))


class InferencePipelineParameters(ABC):
    def __init__(self):
        pass

    def validate(self):
        pass

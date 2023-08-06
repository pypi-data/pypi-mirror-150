from typing import Union, List, Optional
from datetime import datetime, timedelta

import pandas as pd
from pydantic import BaseModel, validator, StrictStr, StrictBool, StrictInt, StrictFloat

from .. import api

__all__ = [
    "ModelExecution",
    "get_default_model_execution",
    "set_default_model_execution",
]


# Credentials
class BasicAuthCredentials(BaseModel):
    baseUrl: StrictStr
    login: StrictStr
    pwd: StrictStr

    def to_object(self):
        return api.OIAnalyticsAPICredentials(
            base_url=self.baseUrl, login=self.login, pwd=self.pwd
        )


class TokenCredentials(BaseModel):
    baseUrl: StrictStr
    token: StrictStr

    def to_object(self):
        return api.OIAnalyticsAPICredentials(base_url=self.baseUrl, token=self.token)


Credentials = Union[BasicAuthCredentials, TokenCredentials]


# Triggers
class CronTrigger(BaseModel):
    type: StrictStr
    cron: StrictStr

    @validator("type")
    def check_type(cls, value):
        if value != "cron-trigger":
            raise ValueError("Trigger type should be 'cron-trigger'")
        return value


Trigger = Union[CronTrigger]


# Model inputs & outputs
class StringParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[StrictStr]

    @validator("type")
    def validate_type(cls, value):
        if value != "STRING":
            raise ValueError("'type' should be 'STRING'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class BooleanParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[StrictBool]

    @validator("type")
    def validate_type(cls, value):
        if value != "BOOLEAN":
            raise ValueError("'type' should be 'BOOLEAN'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class NumericParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[Union[StrictInt, StrictFloat]]

    @validator("type")
    def validate_type(cls, value):
        if value != "NUMERIC":
            raise ValueError("'type' should be 'NUMERIC'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class FileParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[StrictStr]

    @validator("type")
    def validate_type(cls, value):
        if value != "FILE":
            raise ValueError("'type' should be 'FILE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class PeriodParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[timedelta]

    @validator("type")
    def validate_type(cls, value):
        if value != "PERIOD":
            raise ValueError("'type' should be 'PERIOD'")
        return value

    @validator("value", pre=True)
    def parse_value(cls, value):
        if value is None:
            return None
        else:
            return pd.Timedelta(value).to_pytimedelta()

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class DurationParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[timedelta]

    @validator("type")
    def validate_type(cls, value):
        if value != "DURATION":
            raise ValueError("'type' should be 'DURATION'")
        return value

    @validator("value", pre=True)
    def parse_value(cls, value):
        if value is None:
            return None
        else:
            return pd.Timedelta(value, unit="ms").to_pytimedelta()

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class InstantParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[datetime]

    @validator("type")
    def validate_type(cls, value):
        if value != "INSTANT":
            raise ValueError("'type' should be 'INSTANT'")
        return value

    @validator("value", pre=True)
    def parse_value(cls, value):
        if value is None:
            return None
        else:
            return pd.to_datetime(value).to_pydatetime()

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value


class UnitValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class UnitParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[UnitValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "UNIT":
            raise ValueError("'type' should be 'UNIT'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class MeasurementValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class MeasurementParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[MeasurementValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "MEASUREMENT":
            raise ValueError("'type' should be 'MEASUREMENT'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class TagKeyValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class TagKeyParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[TagKeyValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "TAG_KEY":
            raise ValueError("'type' should be 'TAG_KEY'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class TagValueValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class TagValueParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[TagValueValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "TAG_VALUE":
            raise ValueError("'type' should be 'TAG_VALUE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class DataUnit(BaseModel):
    id: StrictStr
    label: StrictStr


class DataValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr
    dataType: StrictStr
    unit: DataUnit
    aggregationFunction: Optional[StrictStr]


class DataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[DataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "DATA":
            raise ValueError("'type' should be 'DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class StoredContinuousDataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[DataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "STORED_CONTINUOUS_DATA":
            raise ValueError("'type' should be 'STORED_CONTINUOUS_DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class BatchType(BaseModel):
    id: StrictStr
    name: StrictStr


class BatchDataValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr
    dataType: StrictStr
    unit: DataUnit
    aggregationFunction: Optional[StrictStr]
    batchType: BatchType


class StoredBatchDataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[BatchDataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "STORED_BATCH_DATA":
            raise ValueError("'type' should be 'STORED_BATCH_DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class ComputedContinuousDataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[DataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "COMPUTED_CONTINUOUS_DATA":
            raise ValueError("'type' should be 'COMPUTED_CONTINUOUS_DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class ComputedBatchDataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[BatchDataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "COMPUTED_BATCH_DATA":
            raise ValueError("'type' should be 'COMPUTED_BATCH_DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class BatchTimeDataParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[BatchDataValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "BATCH_TIME_DATA":
            raise ValueError("'type' should be 'BATCH_TIME_DATA'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class BatchPredicateBatchType(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class BatchPredicateValue(BaseModel):
    type: StrictStr
    batchType: BatchPredicateBatchType


class BatchPredicateParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[BatchPredicateValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "BATCH_PREDICATE":
            raise ValueError("'type' should be 'BATCH_PREDICATE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.batchType.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.batchType.id


class BatchStructureValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class BatchStructureParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[BatchStructureValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "BATCH_STRUCTURE":
            raise ValueError("'type' should be 'BATCH_STRUCTURE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class BatchTagKeyParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[TagKeyValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "BATCH_TAG_KEY":
            raise ValueError("'type' should be 'BATCH_TAG_KEY'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class BatchTagValueParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[TagValueValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "BATCH_TAG_VALUE":
            raise ValueError("'type' should be 'BATCH_TAG_KEY'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class EventTypeValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class EventTypeParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[EventTypeValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "EVENT_TYPE":
            raise ValueError("'type' should be 'EVENT_TYPE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class EventTagKeyValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class EventTagKeyParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[EventTagKeyValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "EVENT_TAG_KEY":
            raise ValueError("'type' should be 'EVENT_TAG_KEY'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


class EventTagValueValue(BaseModel):
    type: StrictStr
    id: StrictStr
    reference: StrictStr


class EventTagValueParameter(BaseModel):
    type: StrictStr
    sourceCodeName: StrictStr
    value: Optional[EventTagValueValue]

    @validator("type")
    def validate_type(cls, value):
        if value != "EVENT_TAG_VALUE":
            raise ValueError("'type' should be 'EVENT_TAG_VALUE'")
        return value

    @property
    def readable_value(self):
        if self.value is None:
            return None
        else:
            return self.value.reference

    @property
    def technical_value(self):
        if self.value is None:
            return None
        else:
            return self.value.id


InstanceParameter = Union[
    StringParameter,
    BooleanParameter,
    NumericParameter,
    FileParameter,
    PeriodParameter,
    DurationParameter,
    InstantParameter,
    UnitParameter,
    MeasurementParameter,
    TagKeyParameter,
    TagValueParameter,
    DataParameter,
    StoredContinuousDataParameter,
    StoredBatchDataParameter,
    ComputedContinuousDataParameter,
    ComputedBatchDataParameter,
    BatchTimeDataParameter,
    BatchPredicateParameter,
    BatchStructureParameter,
    BatchTagKeyParameter,
    BatchTagValueParameter,
    EventTypeParameter,
    EventTagKeyParameter,
    EventTagValueParameter,
]


# Model instance
class ModelInstance(BaseModel):
    id: StrictStr
    trigger: Trigger
    active: StrictBool
    dataExchangeMode: StrictStr
    inputParameters: List[InstanceParameter]
    outputParameters: List[InstanceParameter]

    def find_inputs_by_types(self, input_types: Optional[List[str]] = None):
        if input_types is None:
            return self.inputParameters
        else:
            return [
                param for param in self.inputParameters if param.type in input_types
            ]

    def find_input_by_sourcecodename(self, source_code_name: str):
        for param in self.inputParameters:
            if param.sourceCodeName == source_code_name:
                return param
            raise KeyError(
                f"No input parameter is referenced by the source code name {source_code_name}"
            )

    def find_outputs_by_types(self, output_types: Optional[List[str]] = None):
        if output_types is None:
            return self.outputParameters
        else:
            return [
                param for param in self.outputParameters if param.type in output_types
            ]

    def find_output_by_sourcecodename(self, source_code_name: str):
        for param in self.outputParameters:
            if param.sourceCodeName == source_code_name:
                return param
            raise KeyError(
                f"No output parameter is referenced by the source code name {source_code_name}"
            )

    def get_input_dict(
        self, input_types: Optional[List[str]] = None, mode: str = "object"
    ):
        input_params = self.find_inputs_by_types(input_types)
        if mode == "reference":
            return {
                param.sourceCodeName: param.readable_value for param in input_params
            }
        elif mode == "id":
            return {
                param.sourceCodeName: param.technical_value for param in input_params
            }
        elif mode == "object":
            return {param.sourceCodeName: param.value for param in input_params}
        else:
            raise ValueError(f"Unknown value for 'mode': {mode}")

    def get_output_dict(
        self, output_types: Optional[List[str]] = None, mode: str = "object"
    ):
        output_params = self.find_outputs_by_types(output_types)
        if mode == "reference":
            return {
                param.sourceCodeName: param.readable_value for param in output_params
            }
        elif mode == "id":
            return {
                param.sourceCodeName: param.technical_value for param in output_params
            }
        elif mode == "object":
            return {param.sourceCodeName: param.value for param in output_params}
        else:
            raise ValueError(f"Unknown value for 'mode': {mode}")


# Model execution
class ModelExecution(BaseModel):
    testMode: StrictBool
    credentials: Optional[Credentials]
    lastSuccessfulExecutionInstant: datetime
    currentExecutionInstant: datetime
    pythonModelInstance: ModelInstance

    def set_as_default_model_execution(self):
        set_default_model_execution(self)

    @property
    def execution_kwargs(self):
        return {
            "model_instance_id": self.pythonModelInstance.id,
            "test_mode": self.testMode,
            "current_execution_date": self.currentExecutionInstant,
            "last_execution_date": self.lastSuccessfulExecutionInstant,
            "input_parameters": self.pythonModelInstance.get_input_dict(mode="object"),
            "input_parameter_references": self.pythonModelInstance.get_input_dict(
                mode="reference"
            ),
            "input_parameter_ids": self.pythonModelInstance.get_input_dict(mode="id"),
            "output_parameters": self.pythonModelInstance.get_output_dict(
                mode="object"
            ),
            "output_parameter_references": self.pythonModelInstance.get_output_dict(
                mode="reference"
            ),
            "output_parameter_ids": self.pythonModelInstance.get_output_dict(mode="id"),
        }

    def get_execution_argument_value(self, argument_name: str):
        return self.execution_kwargs[argument_name]


# Current event
DEFAULT_EVENT: Optional[ModelExecution] = None


def set_default_model_execution(event: ModelExecution):
    """
    Put an execution event into a global variable, for external use

    Parameters
    ----------
    event: ModelExecution
    """

    global DEFAULT_EVENT
    DEFAULT_EVENT = event


def get_default_model_execution():
    global DEFAULT_EVENT
    return DEFAULT_EVENT

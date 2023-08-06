from typing import Union, Optional
import io
import time

import pandas as pd

from .. import api
from ._dtos import get_default_model_execution

__all__ = ["FileOutput", "TimeValuesOutput", "Delay", "OIModelOutputs"]


# Output classes
class FileOutput:
    def __init__(self, file_name: str, content: Union[io.StringIO, io.BytesIO]):
        self.output_type = "file"
        self.file_name = file_name
        self.content = content

    @classmethod
    def from_pandas(
        cls,
        data: Union[pd.Series, pd.DataFrame],
        file_name: str,
        file_type: str = "csv",
        writing_kwargs: Optional[dict] = None,
    ):
        # Init
        if writing_kwargs is None:
            writing_kwargs = {}

        bio = io.BytesIO()

        # Write data
        if file_type == "excel":
            data.to_excel(bio, **writing_kwargs)
        elif file_type == "csv":
            data.to_csv(bio, **writing_kwargs)
        else:
            raise NotImplementedError(f"Unsupported file_type: {file_type}")
        bio.seek(0)

        # Create object
        return cls(file_name=file_name, content=bio)

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        return api.endpoints.files.upload_file(
            file_content=self.content,
            file_name=self.file_name,
            api_credentials=api_credentials,
        )


class TimeValuesOutput:
    def __init__(
        self,
        data: Union[pd.Series, pd.DataFrame],
        units: Optional[dict] = None,
        rename_data: bool = True,
    ):
        self.output_type = "time_values"
        self.data = data.to_frame() if isinstance(data, pd.Series) else data
        self.units = units
        self.rename_data = rename_data

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        # Rename data if specified
        if self.rename_data is True:
            event = get_default_model_execution()
            if event is None:
                raise ValueError(
                    "Data can't be renamed without a current event set globally"
                )

            output_dict = event.pythonModelInstance.get_output_dict(
                output_types=["DATA", "STORED_CONTINUOUS_DATA"], mode="reference"
            )
            data_to_send = self.data.rename(columns=output_dict)
        else:
            data_to_send = self.data

        # Send data
        return api.insert_time_values(
            data=data_to_send,
            units=self.units,
            use_external_reference=False,
            api_credentials=api_credentials,
        )


class Delay:
    def __init__(self, duration=5):
        self.output_type = "delay"
        self.duration = duration

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        time.sleep(self.duration)


class OIModelOutputs:
    def __init__(self):
        self.output_type = "outputs_queue"
        self.model_outputs = []

    def add_output(self, output_object: Union[FileOutput, TimeValuesOutput, Delay]):
        self.model_outputs.append(output_object)

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        for model_output in self.model_outputs:
            model_output.send_to_oianalytics(api_credentials=api_credentials)

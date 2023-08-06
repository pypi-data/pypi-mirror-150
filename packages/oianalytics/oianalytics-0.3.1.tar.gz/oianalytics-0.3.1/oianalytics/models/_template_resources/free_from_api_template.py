from oianalytics import api, models

from datetime import datetime


def load_data(
    model_instance_id: str,
    test_mode: bool,
    current_execution_date: datetime,
    last_execution_date: datetime,
    input_parameters: dict,
    input_parameter_references: dict,
    input_parameter_ids: dict,
    output_parameters: dict,
    output_parameter_references: dict,
    output_parameter_ids: dict,
    **kwargs,
):
    # Get data ID from input parameters and query data
    time_data = api.get_time_values(
        data_id=input_parameter_ids["my_timedata_sourcecodename"],
        start_date=last_execution_date,
        end_date=current_execution_date,
        aggregation="RAW_VALUES",
    )

    # Return data to be used in 'process_data' in the 'data' argument
    return time_data


def load_resources(
    model_instance_id: str,
    test_mode: bool,
    current_execution_date: datetime,
    last_execution_date: datetime,
    input_parameters: dict,
    input_parameter_references: dict,
    input_parameter_ids: dict,
    output_parameters: dict,
    output_parameter_references: dict,
    output_parameter_ids: dict,
    **kwargs,
):
    # Get the BytesIO from the resource content
    my_resource = models.get_resource_file(
        resource_file_id=input_parameter_ids["my_resource_sourcecodename"]
    )

    # Return resources to be used in 'process_data' in the 'resources' argument
    return my_resource


def process_data(
    data,
    resources,
    model_instance_id: str,
    test_mode: bool,
    current_execution_date: datetime,
    last_execution_date: datetime,
    input_parameters: dict,
    input_parameter_references: dict,
    input_parameter_ids: dict,
    output_parameters: dict,
    output_parameter_references: dict,
    output_parameter_ids: dict,
    **kwargs,
):
    # Create a model output object
    outputs = models.outputs.OIModelOutputs()

    # Declare a file output, built from a pandas series
    outputs.add_output(
        models.outputs.FileOutput.from_pandas(
            data=data, file_name="my_time_values.csv", writing_kwargs={"sep": ";"}
        )
    )

    # Return outputs
    return outputs

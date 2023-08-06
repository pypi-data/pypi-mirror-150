# Overview
This library contains useful wrappers around the Tonic.ai API.

## Usage

Instantiate the API wrapper using the following code:

```
from tonic_api.api import TonicApi

# Do not include trailing backslash in TONIC_URL
api = TonicApi(TONIC_URL, API_KEY)
```

Once instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.

```
TonicApi:
    get_workspace(workspace_id) => Workspace

Workspace:
    id => string
    name => string
    models => Model[]

    train(force_train) => existing or new job ID (if force_train or no Completed jobs)
    get_most_recent_training_job(with_status) => TrainingJob (by default any status)
    get_most_recent_training_job_by_model_id(model_id) => TrainingJob
    get_most_recent_training_job_by_model_name(model_name) => TrainingJob
    get_training_job_by_id(job_id) => TrainingJob
    get_historical_training_jobs() => TrainingJob[]

    describe() => debugger helper for printing fields

Model:
    id => string
    name => string
    query => string
    parameters => {}
    encodings => {}

    describe() => debugger helper for printing fields

TrainingJob:
    id => string
    published_time => string

    get_training_status() => TrainingStatus
    tail_training_status() => tails and prints status updates on training
    get_trained_models() => TrainedModel[]
    get_trained_model_by_model_id(model_id) => TrainedModel
    get_trained_model_by_model_name(model_name) => TrainedModel

    describe() => debugger helper for printing fields

TrainedModel:
    id => string
    model => Model

    sample(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided)
    sample_source(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided). Note: NOT randomized. Upper limit is limited to row count in source.

    get_numeric_columns() => string[]
    get_categorical_columns() => string[]

    describe() => debugger helper for printing fields
```

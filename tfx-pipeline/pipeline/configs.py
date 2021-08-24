# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFX taxi template configurations.

This file defines environments for a TFX  pipeline.
"""

import os

# Pipeline name will be used to identify this pipeline.
PIPELINE_NAME = 'tfx-pipeline'

# GCP related configs.
# Following code will retrieve your GCP project. You can choose which project
# to use by setting GOOGLE_CLOUD_PROJECT environment variable.
try:
  import google.auth  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error
  try:
    _, GOOGLE_CLOUD_PROJECT = google.auth.default()
  except google.auth.exceptions.DefaultCredentialsError:
    GOOGLE_CLOUD_PROJECT = ''
except ImportError:
  GOOGLE_CLOUD_PROJECT = ''

# Specify your GCS bucket name here. You have to use GCS to store output files
# when running a pipeline with Kubeflow Pipeline on GCP or when running a job
# using Dataflow. Default is '<gcp_project_name>-kubeflowpipelines-default'.
# This bucket is created automatically when you deploy KFP from marketplace.
GCS_BUCKET_NAME = GOOGLE_CLOUD_PROJECT + '-kubeflowpipelines-default'

GOOGLE_CLOUD_REGION = 'us-central1'

# Following image will be used to run pipeline components run if Kubeflow Pipelines used.
# This image will be automatically built by CLI if we use --build-image flag.
PIPELINE_IMAGE = f'gcr.io/{GOOGLE_CLOUD_PROJECT}/{PIPELINE_NAME}'

PREPROCESSING_FN = 'models.preprocessing.preprocessing_fn'
RUN_FN = 'models.keras_model.model.run_fn'

PREPROCESSING_MODULE = f'gs://{GCS_BUCKET_NAME}/modules/preprocessing.py'
TRAINING_MODULE = f'gs://{GCS_BUCKET_NAME}/modules/model.py'

TRAIN_NUM_STEPS = 1000
EVAL_NUM_STEPS = 150

# Change this value according to your use cases.
EVAL_ACCURACY_THRESHOLD = 0.6

GCP_AI_PLATFORM_TRAINING_ARGS = {
    'project': GOOGLE_CLOUD_PROJECT,
    'region': GOOGLE_CLOUD_REGION,
    'scaleTier': 'BASIC_GPU',
    'masterConfig': {
      'imageUri': PIPELINE_IMAGE
    },
}

GCP_AI_PLATFORM_SERVING_ARGS = {
    'model_name': PIPELINE_NAME.replace('-','_'),  # '-' is not allowed.
    'project_id': GOOGLE_CLOUD_PROJECT,
    # The region to use when serving the model. See available regions here:
    # https://cloud.google.com/ml-engine/docs/regions
    # Note that serving currently only supports a single region:
    # https://cloud.google.com/ml-engine/reference/rest/v1/projects.models#Model  # pylint: disable=line-too-long
    'regions': [GOOGLE_CLOUD_REGION],
}
# Chứa các hằng số của model

import os


ARTIFACTS_DIR: str = "artifacts"

"""
DATA INGESTION related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_DOWNLOAD_URL: str = "https://github.com/NgocSon-AI/mydata/raw/refs/heads/main/SignLanguageData.zip"

"""
DATA VALIDATION related constant start with DATA_VALIDATION var name
"""


DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE = "status.txt"

DATA_VALIDATION_ALL_REQUIRED_FILES = ["train", "test", "data.yaml"]


"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"

MODEL_TRAINER_PRETRAINED_WEIGHT_NAME: str = "yolov5s.pt"

MODEL_TRAINER_NO_EPOCHS: int = 10

MODEL_TRAINER_BATCH_SIZE: int = 16

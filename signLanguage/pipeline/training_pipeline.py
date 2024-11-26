import os
import sys

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.entity.config_entity import (DataIngestionConfig, DataValidationConfig, ModelTrainerConfig)
from signLanguage.entity.artifacts_entity import (DataIngestionArtifact, DataValidationArtifact, ModelTrainerArtifact)


from signLanguage.components.data_ingestion import DataIngestion
from signLanguage.components.data_validation import DataValidation
from signLanguage.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.mode_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Entered to start_data_ingestion method of TrainPipeline class")
            logging.info("Get data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got data from URL")
            logging.info("Exited to start_data_ingestion method of TrainPipeline class")

            return data_ingestion_artifact
        
        except Exception as e:
            raise SignException(e, sys)
    
    def start_data_validation(
            self,
            data_ingestion_artifact: DataIngestionArtifact
        )-> DataValidationArtifact:
        logging.info("Entered to start_data_validation method of TrainPipeline class")
        try:
            data_validaion = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )
            data_validaion_artifact = data_validaion.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validaion_artifact
        except Exception as e:
            raise SignException(e, sys)

    def start_model_trainer(self) -> ModelTrainerConfig:
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.mode_trainer_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SignException(e, sys)

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact= data_ingestion_artifact
            )
            if data_validation_artifact.validation_status == True:
                model_trainer_artifact = self.start_model_trainer()
            else:
                raise Exception("Your data is not in correct format")
        except Exception as e:
            raise SignException(e, sys)
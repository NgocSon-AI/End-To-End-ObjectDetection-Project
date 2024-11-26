import os
import sys
import shutil

from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import DataValidationConfig
from signLanguage.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
#from signLanguage.components.data_ingestion import DataIngestion

class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise SignException(e, sys)


    def validate_all_file_exist(self)->bool:
        try:
            #validation_status = None    # Dùng để kiểm tra trạng thái tệp
            
            # Lấy tất cả các file trong thư mục với đường dẫn self.data_ingestion_artifact.feature_store_path  [test, train, data.yaml]
            all_file = os.listdir(self.data_ingestion_artifact.feature_store_path + "/SignLanguageData")
            #print("all_file: ", all_file)
            all_file_exist = True
            for require_file in self.data_validation_config.required_file_list:
                #print("require_file: ", require_file)
                if require_file not in all_file:

                    all_file_exist = False
                    break
            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            #all_file_exist = True
            with open(self.data_validation_config.valid_status_file_dir, "w") as f:
                f.write(f"Validation status: {all_file_exist}")
            return all_file_exist
            # for file in all_file: # [test, train, data.yaml]
            #     if file not in self.data_validation_config.required_file_list:      # Kiểm tra xem nó có trong danh sách các file yêu cầu hay không?
            #         print
            #           # Nếu không có thì...gán..
            #         validation_status = False
            #         # Tạo thư mục 
            #         os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            #         # Mở tệp và ghi trạng thái kiểm tra vào tệp
            #         with open(self.data_validation_config.valid_status_file_dir, "w") as f:
            #             f.write(f"Validation status: {validation_status}")
            #     else:
            #         # Nếu tìm thấy tệp gán = True và tạo tệp + ghi trạng thái.
            #         validation_status = True
            #         os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            #         with open(self.data_validation_config.valid_status_file_dir, "w") as f:
            #             f.write(f"Validation status: {validation_status}")
            # return validation_status
        except Exception as e:
            raise SignException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entered the initiate_data_validation method of DataValidationArtifact class")
        try:
            status = self.validate_all_file_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status
            )
            print("data_validation_artifact: ", data_validation_artifact)
            logging.info("Exited initiate_data_validation method of DataValidationArtifact class")
            logging.info(f"Data validaiton artifact: {data_validation_artifact}")
            if status == True:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())
            return data_validation_artifact
        
        except Exception as e:
            raise SignException(e, sys)


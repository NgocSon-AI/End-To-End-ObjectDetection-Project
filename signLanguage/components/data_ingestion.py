import os
import sys
from six.moves import urllib

import zipfile

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(
        self,
        data_ingestion_config: DataIngestionConfig = DataIngestionConfig(),
        #data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact()
    ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SignException(e, sys)
        
    def download_data(self)-> str:
        '''
        Fetch data from the url
        Trả về chuỗi đường dẫn đến file data mới được tải về
        '''
        try:
            # url của tập dữ liệu lấy từ thuộc tính data_ingestion_config của lớp DataIngestionConfig
            dataset_url = self.data_ingestion_config.data_download_url
            
            # Nơi file zip được lưu lấy từ thuộc tính data_ingestion_config của lớp DataIngestionConfig
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(zip_download_dir, exist_ok=True)
            
            # Tên cơ sở của tập tin được trích suất từ url
            data_file_name = os.path.basename(dataset_url)
            
            # Đường dẫn đầy đủ nơi tập tin được lưu (Được tạo nên bằng cách kết hợp thư mục tải xuống và tên tệp tin)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
            
            # Tải tập tin về path 
            urllib.request.urlretrieve(dataset_url, zip_file_path)

            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            
            # Trả về đường dẫn nơi tập tin được tải xuống.
            return zip_file_path

        except Exception as e:
            raise SignException(e, sys)


    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            # Đường dẫn 
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            
            # Tạo thư mục theo đường dẫn vừa lấy
            os.makedirs(feature_store_path, exist_ok=True)
            
            # Đọc file zip
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Giải nén
                zip_ref.extractall(feature_store_path)
            

            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")
            # Trả về đường dẫn nơi tập được giải nén.
            return feature_store_path

        except Exception as e:
            raise SignException(e, sys)

    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the initiate_data_ingestion of DataIngestion class")
        try:
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path=zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path= zip_file_path,
                feature_store_path= feature_store_path
            )

            logging.info("Exited the initiate_data_ingestion of DataIngestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact

        except Exception as e:
            raise SignException(e, sys)
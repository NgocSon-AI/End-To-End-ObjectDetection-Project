import os
import sys
import yaml
import subprocess
import logging
import shutil
from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifacts_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            # Giải nén tệp ZIP bằng PowerShell
            subprocess.run(["powershell", "-Command", "Expand-Archive -Path 'SignLanguageData.zip' -DestinationPath '.'"], check=True)
            
            # Xóa tệp ZIP
            os.remove("SignLanguageData.zip")

            # Đọc số lượng lớp từ tệp YAML
            with open("SignLanguageData/data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            # Đọc cấu hình mô hình
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)

            # Ghi lại cấu hình mới
            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # Chạy lệnh huấn luyện
            subprocess.run([
                "python", "train.py", 
                "--img", "416", 
                "--batch", str(self.model_trainer_config.batch_size), 
                "--epochs", str(self.model_trainer_config.no_epochs), 
                "--data", "data.yaml", 
                "--cfg", f"./models/custom_{model_config_file_name}.yaml", 
                "--weights", self.model_trainer_config.weight_name, 
                "--name", "yolov5s_results", 
                "--cache"
            ], cwd="yolov5", check=True)

            # Sao chép tệp trọng số tốt nhất
            best_pt_path = "yolov5/runs/train/yolov5s_results/weights/best.pt"
            if os.path.exists(best_pt_path):
                os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
                shutil.copy(best_pt_path, self.model_trainer_config.model_trainer_dir)

            # Dọn dẹp
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            shutil.rmtree("train", ignore_errors=True)
            shutil.rmtree("test", ignore_errors=True)
            os.remove("data.yaml")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt"),
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SignException(e, sys)
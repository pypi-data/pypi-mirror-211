from abc import ABC, abstractmethod
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.constant import Task,Model
from ailab.atp_finetuner.build import TrainerRg

class AILabTrainer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, **kwargs):
        pass

    @abstractmethod
    def train(self):
        pass
    
    @abstractmethod
    def postprocess(self):
        pass

    @classmethod
    def from_task_model(cls, task:Task, model_name:Model, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, **kwargs):
        auto_trainer = TrainerRg.get_cls((task, model_name))()
        if auto_trainer is None:
            raise TypeError(f'auto_trainer is None')
        auto_trainer.preprocess(dataset, model, preprocessor, data_collator, metric, **kwargs)
        return auto_trainer
    
    @property
    def accelerator(self):
        return self._accelerator

    @accelerator.setter
    def accelerator(self, value):
        self._accelerator = value
        
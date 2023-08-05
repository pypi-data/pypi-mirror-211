from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.constant import Framework, Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.trainer import AILabTrainer
from ailab.atp_finetuner.accelerator import AILabAccelerator


class AILabFinetuner:
    def __init__(self, task: Task, framework: Framework.Pytorch, \
                 dataset: AILabDataset, model_name: Model, **args):
        is_accelerate = args.get('accelerator', False)
        accelerator = None
        if is_accelerate:
            accelerator = AILabAccelerator.from_project_config(**args)
        preprocessor = AILabPreprocessor.from_pretrained(task, model_name, dataset)
        preprocessor.accelerator = accelerator
        tokenized_dataset = preprocessor.forward()

        model = AILabModel.from_pretrained('cuda', task, model_name, **args)
        model.accelerator = accelerator
        model.forward()

        data_collator = AILabDataCollator.from_task_model(task, model_name, framework, preprocessor)
        metrics = AILabMetric.from_task_model(task, model_name)
        trainer = AILabTrainer.from_task_model(task, model_name, tokenized_dataset, model, preprocessor, data_collator,
                                               metrics, **args)
        trainer.accelerator = accelerator

        self._trainer = trainer

    def finetuner(self):
        self._trainer.train()

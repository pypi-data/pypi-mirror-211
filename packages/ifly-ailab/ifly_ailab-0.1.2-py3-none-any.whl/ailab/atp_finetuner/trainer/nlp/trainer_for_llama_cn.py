import torch
from transformers import TrainingArguments, Trainer
from peft import get_peft_model_state_dict
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model

@TrainerRg.register((Task.question_answering_cn, Model.llama))
class Vicunatrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, **kwargs):
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 1e-5)
        num_train_epochs = train_args.get('num_train_epochs', 2)

        now_max_steps = max((len(dataset.to_hf_dataset()["train"]) - 200) // 128 * num_train_epochs, num_train_epochs)
        MAX_STEPS = 5000
        GRADIENT_ACCUMULATION_STEPS = 128 // 4

        training_args=TrainingArguments(
            per_device_train_batch_size=4,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
            warmup_steps=100,
            num_train_epochs=num_train_epochs,
            max_steps=MAX_STEPS,
            learning_rate=learning_rate,
            fp16=True,
            logging_steps=20,
            evaluation_strategy="steps",
            save_strategy="steps",
            eval_steps=200,
            save_steps=200,
            output_dir=output_dir,
            save_total_limit=30,
            load_best_model_at_end=True,
            ddp_find_unused_parameters=None,
            report_to=[],
            ignore_data_skip=False,
        )

        trainer = Trainer(
            model=model.model_ins,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            data_collator=data_collator.datacollator_ins,
        )
        self.trainer = trainer
        self.model = model.model_ins
        self.output_dir = output_dir
    
    def train(self):
        model = self.model
        model.config.use_cache = False
        old_state_dict = model.state_dict
        model.state_dict = (
            lambda self, *_, **__: get_peft_model_state_dict(
                self, old_state_dict()
            )
        ).__get__(model, type(model))
        model = torch.compile(model)

        self.trainer.train()
        model.save_pretrained(self.output_dir)

    def postprocess(self):
        self.trainer.evaluate()




import os
import torch
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from transformers.integrations import TensorBoardCallback
from transformers import TrainingArguments, Trainer

from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model

class CastOutputToFloat(nn.Sequential):
    def forward(self, x):
        return super().forward(x).to(torch.float32)
    
class ModifiedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        return model(
            input_ids=inputs["input_ids"],
            labels=inputs["labels"],
        ).loss

    def save_model(self, output_dir=None, _internal_call=False):
        from transformers.trainer import TRAINING_ARGS_NAME
        os.makedirs(output_dir, exist_ok=True)
        torch.save(self.args, os.path.join(output_dir, TRAINING_ARGS_NAME))
        saved_params = {
            k: v.to("cpu") for k, v in self.model.named_parameters() if v.requires_grad
        }
        torch.save(saved_params, os.path.join(output_dir, "adapter_model.bin"))

@TrainerRg.register((Task.question_answering, Model.chatglm_6b))
class ChatGlmTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, **kwargs):
        os_model = model.model_ins
        os_model.gradient_checkpointing_enable()
        os_model.enable_input_require_grads()
        os_model.is_parallelizable = True
        os_model.model_parallel = True
        os_model.lm_head = CastOutputToFloat(os_model.lm_head)
        os_model.config.use_cache = (
            False  # silence the warnings. Please re-enable for inference!
        )
        from peft import get_peft_model, LoraConfig, TaskType
        # setup peft
        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=8,
            lora_alpha=32,
            lora_dropout=0.1,
        )
        os_model = get_peft_model(os_model, peft_config)
        writer = SummaryWriter()

        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 1e-5)
        num_train_epochs = train_args.get('num_train_epochs', 2)

        training_args = TrainingArguments(
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=6,
            gradient_accumulation_steps=1,
            max_steps=52000,
            save_steps=1000,
            save_total_limit=2,
            learning_rate=learning_rate,
            fp16=True,
            remove_unused_columns=False,
            logging_steps=50,
            output_dir=output_dir,
        )
        print(f'dataset {dataset.to_hf_dataset()}')

        trainer = ModifiedTrainer(
            model=os_model,
            train_dataset=dataset.to_hf_dataset(),
            args=training_args,
            callbacks=[TensorBoardCallback(writer)],
            data_collator=data_collator.datacollator_ins,
        )
        
        self.os_model = os_model
        self.writer = writer
        self.training_args = training_args
        self.trainer = trainer
    
    def train(self):
        self.trainer.train()
        self.writer.close()
        self.os_model.save_pretrained(self.training_args.output_dir)

    def postprocess(self):
        self.trainer.evaluate()




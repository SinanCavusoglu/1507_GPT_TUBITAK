import argparse
from transformers import AutoTokenizer, GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import wandb
from transformers import AdamW, TrainerCallback
"""
# chatgptye yazdırdım kontrol et, youtubede video var bak ona
class PushToHubCallback(TrainerCallback):
    def __init__(self, trainer=None):
        super().__init__()
        self.trainer = trainer
        self.best_loss = float('inf')

    def on_evaluate(self, args, state, control, **kwargs):
        logs = kwargs.get('logs', {})
        current_loss = logs.get('eval_loss', None)
        if current_loss is not None and current_loss < self.best_loss:
            self.best_loss = current_loss
            # Modeli kaydet
            self.trainer.save_model()
            # Hub'a yükle
            if self.trainer.args.push_to_hub:
                self.trainer.push_to_hub()
"""
def get_model_size_dict(size):
    if size == 'gpt2':
        return dict(n_layer=12, n_head=12, n_embd=768)  # 124M params
    elif size == 'gpt2-medium':
        return dict(n_layer=24, n_head=16, n_embd=1024)  # 350M params
    elif size == 'gpt2-large':
        return dict(n_layer=36, n_head=20, n_embd=1280)  # 774M params
    elif size == 'gpt2-xl':
        return dict(n_layer=48, n_head=25, n_embd=1600)  # 1558M params

def initialize_model(tokenizer, config):
    model_config_dict = get_model_size_dict(config.size)
    model_config = GPT2Config(**model_config_dict)
    model = GPT2LMHeadModel(model_config)
    tokenizer.pad_token = tokenizer.eos_token
    return model

def load_data(dataset):
    dataset = load_dataset(dataset)
    return dataset['train'], dataset['validation']

def setup_trainer(model, tokenizer, train_dataset, eval_dataset, config):
    optimizer = AdamW(model.parameters(), lr=config.learning_rate)
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        evaluation_strategy="steps",
        eval_steps=config.eval_interval,
        push_to_hub=True,
        hub_model_id="YourModelID",  # sonra gir
        hub_token="YourHuggingFaceToken",  # sonra gir
        logging_steps=config.log_interval,
        save_steps=config.eval_interval,
        warmup_steps=config.warmup_iters,
        max_steps=config.max_iters,
        lr_scheduler_type="cosine" if config.decay_lr else "constant",
        weight_decay=config.weight_decay,
        logging_dir='./logs',
        report_to="wandb",
        gradient_checkpointing=True,
        max_grad_norm=config.grad_clip,
        block_size=config.block_size,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        #callbacks=[PushToHubCallback(trainer)]  # youtubede video var bak bozuk olabilir
    )

    return trainer

def main(args):
    wandb.init(project="gpt2_tuning", config=vars(args))
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    model = initialize_model(tokenizer, args)
    train_dataset, eval_dataset = load_data(args.dataset)
    trainer = setup_trainer(model, tokenizer, train_dataset, eval_dataset, args)
    trainer.train()
    wandb.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", type=str, help="Huggingface tokenizer URL")
    parser.add_argument("--dataset", type=str, help="Huggingface dataset URL")
    parser.add_argument("--size", choices=['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'], required=True,
                        help="Model size (124M params, 350M params, 774M params, 1558M params)")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=12)
    parser.add_argument("--block_size", type=int, default=1024)
    parser.add_argument("--gradient_accumulation", type=int, default=8)
    parser.add_argument("--eval_interval", type=int, default=2000)
    parser.add_argument("--log_interval", type=int, default=1)
    parser.add_argument("--warmup_iters", type=int, default=2000)
    parser.add_argument("--max_iters", type=int, default=600000)
    parser.add_argument("--weight_decay", type=float, default=0.1)
    parser.add_argument("--decay_lr", type=bool, default=True)
    parser.add_argument("--grad_clip", type=float, default=1.0)
    parser.add_argument("--learning_rate", type=float, default=5e-5, help="Initial learning rate for AdamW optimizer")
    args = parser.parse_args()

    main(args)

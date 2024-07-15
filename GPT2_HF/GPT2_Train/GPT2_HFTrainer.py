import argparse
from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import wandb

def initialize_model(tokenizer):
    model_config = GPT2Config()
    model = GPT2LMHeadModel(model_config)
    tokenizer.pad_token = tokenizer.eos_token
    return model

def load_data():
    dataset = load_dataset('wikitext', 'wikitext-103-raw-v1')
    return dataset['train'], dataset['validation']

def setup_trainer(model, tokenizer, train_dataset, eval_dataset, config):
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        warmup_steps=config.warmup_steps,
        weight_decay=config.weight_decay,
        logging_dir='./logs',
        evaluation_strategy="steps",
        eval_steps=500,
        logging_steps=500,
        report_to="wandb"
    )

    return Trainer(
        model=model,
        args=training_args,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )

def main(args):
    wandb.init(project="gpt2_tuning", config=args)
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = initialize_model(tokenizer)
    train_dataset, eval_dataset = load_data()
    trainer = setup_trainer(model, tokenizer, train_dataset, eval_dataset, args)
    trainer.train()
    wandb.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_size", type=str, )
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--per_device_eval_batch_size", type=int, default=8)
    parser.add_argument("--warmup_steps", type=int, default=500)
    parser.add_argument("--weight_decay", type=float, default=0.01)

    args = parser.parse_args()
    
    main(args)

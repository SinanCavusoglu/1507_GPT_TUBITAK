import os
import json


import argparse
import wandb
from transformers import GPT2Tokenizer

from model_utils import initialize_model
from data_utils import load_data
from training_utils import setup_trainer



def parse_args_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            args_dict = json.load(f)
        return args_dict
    else:
        return {}


def main(args):
    
    wandb.init(project=args.project_name, name=args.size,config=vars(args))
    tokenizer = GPT2Tokenizer.from_pretrained(args.tokenizer)
    model = initialize_model(tokenizer, args)
    train_dataset, eval_dataset = load_data(args.dataset_path)
    #train_dataset = train_dataset.shuffle(seed=42).select(range(1000000))
    #eval_dataset = eval_dataset.shuffle(seed=42).select(range(10000))
    trainer = setup_trainer(model, tokenizer, train_dataset, eval_dataset, args)
    if args.checkpoint_bool:

        trainer.train(resume_from_checkpoint=args.checkpoint)
    else:
        trainer.train()
    wandb.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, help="Path to JSON config file", default=None)
    args, unknown = parser.parse_known_args()

    config_args = {}
    if args.config_file:
        config_args = parse_args_from_file(args.config_file)

    parser.add_argument("--output_dir", type=str, help="Save Weights Directory", default='./results')
    parser.add_argument("--tokenizer", type=str, help="Huggingface tokenizer URL")
    parser.add_argument("--dataset_path", type=str, help="tokenizer.py output in local(./tokenized_law)")
    parser.add_argument("--size", choices=['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'],
                        help="Model size (124M params, 350M params, 774M params, 1558M params)")
    parser.add_argument("--batch_size", type=int, default=12)
    parser.add_argument("--block_size", type=int, default=1024)
    parser.add_argument("--gradient_accumulation", type=int, default= 5*2) 
    parser.add_argument("--eval_interval", type=int, default=1000)                                                                                                                                                                                                                                                                         
    parser.add_argument("--log_interval", type=int, default=10)
    parser.add_argument("--warmup_iters", type=int, default=2000)
    parser.add_argument("--max_iters", type=int, default=600000)
    parser.add_argument("--weight_decay", type=float, default=0.1)
    parser.add_argument("--decay_lr", type=bool, default=True)
    parser.add_argument("--grad_clip", type=float, default=1.0)
    parser.add_argument("--learning_rate", type=float, default=5e-5, help="Initial learning rate for AdamW optimizer")
    #parser.add_argument("--dropout", type=float, default=)
    parser.add_argument("--project_name", type=str, default="hf_training", help="Project Name for Wandb")
    parser.add_argument("--checkpoint_bool", type=bool, default=False)
    parser.add_argument("--checkpoint", type=str, default = "results/")
    parser.set_defaults(**config_args)
    args = parser.parse_args(unknown)
    main(args)

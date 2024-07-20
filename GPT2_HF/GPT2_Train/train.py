import argparse
import wandb
from transformers import GPT2Tokenizer

from model_utils import initialize_model
from data_utils import load_data
from training_utils import setup_trainer

def main(args):
    wandb.init(project="gpt2_tuning", config=vars(args))
    tokenizer = GPT2Tokenizer.from_pretrained(args.tokenizer)
    model = initialize_model(tokenizer, args)
    train_dataset, eval_dataset = load_data(args.dataset)
    trainer = setup_trainer(model, tokenizer, train_dataset, eval_dataset, args)
    trainer.train()
    wandb.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, help="Save Weights Directory", default='./results')
    parser.add_argument("--tokenizer", type=str, help="Huggingface tokenizer URL")
    parser.add_argument("--dataset_path", type=str, help="tokenizer.py output in local(./tokenized_law)")
    parser.add_argument("--size", choices=['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'], required=True,
                        help="Model size (124M params, 350M params, 774M params, 1558M params)")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=12)
    parser.add_argument("--block_size", type=int, default=1024)
  # bunun gpu başına mı  #parser.add_argument("--gradient_accumulation", type=int, default= 4*2) 2=gpu's number #When using gradient accumulation, one step is counted as one step with backward pass. Therefore, logging, evaluation, save will be conducted every gradient_accumulation_steps * xxx_step training examples.
    parser.add_argument("--eval_interval", type=int, default=1000)
    parser.add_argument("--log_interval", type=int, default=10)
    parser.add_argument("--warmup_iters", type=int, default=2000)
    parser.add_argument("--max_iters", type=int, default=600000)
    parser.add_argument("--weight_decay", type=float, default=0.1)
    parser.add_argument("--decay_lr", type=bool, default=True)
    parser.add_argument("--grad_clip", type=float, default=1.0)
    parser.add_argument("--learning_rate", type=float, default=5e-5, help="Initial learning rate for AdamW optimizer")
    #parser.add_argument("--dropout", type=float, default=)
    args = parser.parse_args()
    main(args)

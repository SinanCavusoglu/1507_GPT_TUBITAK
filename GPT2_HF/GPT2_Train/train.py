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
    # Add all required arguments
    args = parser.parse_args()
    main(args)

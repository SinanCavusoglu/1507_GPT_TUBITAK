from datasets import load_dataset
from transformers import GPT2Tokenizer
import os

def tokenize_and_save_data(dataset_name, tokenizer_name, save_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_name)
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token

    dataset = load_dataset(dataset_name)

    def tokenize_function(examples):
        return tokenizer(examples['text'], truncation=True, max_length=1024, padding="max_length")

    tokenized_datasets = dataset.map(tokenize_function, batched=True, load_from_cache_file=False, num_proc=12)

    tokenized_datasets.save_to_disk(save_path)
    print(f"Tokenized datasets saved to {save_path}")

    return tokenized_datasets

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

import argparse

def main(args):
    ensure_dir(args.save_path)
    tokenize_and_save_data(args.dataset, args.tokenizer, args.save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", type=str, required=True, help="Pretrained tokenizer model name")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset to load and tokenize")
    parser.add_argument("--save_path", type=str, required="True", help="Path to save the tokenized dataset")
    
    args = parser.parse_args()
    main(args)


# python tokenizer.py --tokenizer sergeantson/1507_Law_Tokenizer --dataset sergeantson/1507_law_dataset --save_path ./tokenized_law

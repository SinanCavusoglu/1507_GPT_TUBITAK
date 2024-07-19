# First Run tokenizer.py

from datasets import load_from_disk

def load_data(dataset_path):
    dataset = load_from_disk(dataset_path)
    return dataset["train"], dataset["validation"]
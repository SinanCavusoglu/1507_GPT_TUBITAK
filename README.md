# [Dataset and Tokenizer (LAW)](https://drive.google.com/drive/folders/1YCQuvKK57yGSKz5oE891AU3i8oodMDXC?usp=sharing)

# [Dataset HF (Law)](https://huggingface.co/datasets/sergeantson/1507_law_dataset)

# [Tokenizer (LAW)](https://huggingface.co/sergeantson/1507_Law_Tokenizer)

# Trainer inside GPT2_HF/GPT2_Train

## Install

datasets 2.19.0

transformers 4.40.1

wandb 0.16.6

## 1) Tokenizer

First, run the tokenizer script. It creates tokenized_law folder. I set the num_proc to 6 and It can be increased by CPU

```bash
python tokenizer.py --tokenizer sergeantson/1507_Law_Tokenizer --dataset sergeantson/1507_law_dataset --save_path ./tokenized_law
```

## 2) Trainer

To run trainer
```bash
python train.py --config_file args.json 
```

Please check the args.json file. I set the `batch_size = 1` and `gradient_accumulation = 1` to fit the GPU. You can increase the `batch_size =12` and  `gradient_accumulation = 5 * (total gpu number)`

To train with checkpoint

```bash
python train.py --config_file args.json --project_name Law --checkpoint_bool True --checkpoint C:\tubitak_1507\1507_GPT_TUBITAK\GPT2_HF\GPT2_Train\results\checkpoint-19000
```


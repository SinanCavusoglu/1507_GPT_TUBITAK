from transformers import GPT2Config, GPT2LMHeadModel

def get_model_size_dict(size):
    size_dict = {
        'gpt2': {'n_layer': 12, 'n_head': 12, 'n_embd': 768},   # 124M params
        'gpt2-medium': {'n_layer': 24, 'n_head': 16, 'n_embd': 1024},   # 350M params
        'gpt2-large': {'n_layer': 36, 'n_head': 20, 'n_embd': 1280},   # 774M params
        'gpt2-xl': {'n_layer': 48, 'n_head': 25, 'n_embd': 1600}   # 1558M params
    }
    return size_dict.get(size, None)

def initialize_model(tokenizer, config):
    model_config_dict = get_model_size_dict(config.size)
    if not model_config_dict:
        raise ValueError("Unsupported model size.")
    model_config = GPT2Config(**model_config_dict)
    model = GPT2LMHeadModel(model_config)
    tokenizer.pad_token = tokenizer.eos_token  # Ensure that the tokenizer's pad token is set
    return model

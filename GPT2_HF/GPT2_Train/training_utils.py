from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling, AdamW, get_scheduler

def setup_trainer(model, tokenizer, train_dataset, eval_dataset, config):
    
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="steps",
        eval_steps=config.eval_interval,
        logging_dir='logs',
        logging_steps=config.log_interval,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation,
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay,
        adam_beta1=0.9,
        adam_beta2=0.95,  
        max_steps=config.max_iters,
        max_grad_norm=config.grad_clip,
        warmup_steps=config.warmup_iters,
        lr_scheduler_type='linear',
        fp16=True,
        fp16_backend='auto',
        save_strategy='steps',
        save_steps=config.eval_interval,
        report_to='wandb',
        wandb_run_name=config.size,
        seed=42,
        dataloader_num_workers= 4,
        metric_for_best_model='loss',
        gradient_checkpointing=True,
        #push_to_hub= True,  
        #hub_model_id= "asdf",  # Değişkenleri sonra gir !!!
        #hub_token= "asdf"      # Değişkenleri sonra gir !!! Gerekmiyor sanırım en son yükleriz
    )
    
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
        )
    return trainer

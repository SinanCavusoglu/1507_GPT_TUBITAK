from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling, AdamW, get_scheduler

def setup_trainer(model, tokenizer, train_dataset, eval_dataset, config):
    optimizer = AdamW(model.parameters(), lr=config.learning_rate, betas=(0.9, 0.95), eps=1e-8, weight_decay=config.weight_decay)
    scheduler = get_scheduler("cosine" if config.decay_lr else "constant", optimizer=optimizer, num_warmup_steps=config.warmup_iters, num_training_steps=config.max_iters)
    
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        evaluation_strategy="steps",
        eval_steps=config.eval_interval,
        logging_steps=config.log_interval,
        save_steps=config.eval_interval,
        warmup_steps=config.warmup_iters,
        max_steps=config.max_iters,
        report_to="wandb",
        gradient_checkpointing=True,
        max_grad_norm=config.grad_clip,
        fp16=True
    )
    
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        optimizers=(optimizer, scheduler)
    )
    return trainer

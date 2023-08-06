import numpy as np
import torch
from transformers import TimeSeriesForcaster, TimeSeriesDataset, Trainer, TrainingArguments

# Generate some fake time series data
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
train_data = [(x[i:i+10], y[i+10]) for i in range(80)]
test_data = [(x[i:i+10], y[i+10]) for i in range(80, 90)]

# Define a time series model using Transformers
class TimeSeriesModel(torch.nn.Module):
    def __init__(self):
        super(TimeSeriesModel, self).__init__()
        self.transformer = TimeSeriesForcaster(num_time_series=1, hidden_size=16, num_attention_heads=2, num_layers=2)
        self.linear = torch.nn.Linear(16, 1)

    def forward(self, x):
        outputs = self.transformer(x)
        logits = self.linear(outputs)
        return logits

# Create a time series dataset
train_dataset = TimeSeriesDataset(train_data)
test_dataset = TimeSeriesDataset(test_data)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=5,              # total number of training epochs
    per_device_train_batch_size=4,   # batch size per device during training
    per_device_eval_batch_size=4,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=50,
)

# Create the trainer and train the model
model = TimeSeriesModel()
trainer = Trainer(
    model=model,                         # the instantiated model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=test_dataset            # evaluation dataset
)
trainer.train()

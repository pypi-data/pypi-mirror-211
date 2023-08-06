# this looks like a working project
from transformers import pipeline

# Load the sentiment analysis model
model = pipeline('sentiment-analysis')

# Test the model on a sample text
result = model("I really like this product!, just kidding I wish I can say that")
print(result)


#```python
from huggingface_hub import hf_hub_download
import torch
from transformers import TimeSeriesTransformerModel

file = hf_hub_download(
     repo_id="kashif/tourism-monthly-batch", filename="train-batch.pt", repo_type="dataset")
batch = torch.load(file)
batch
model = TimeSeriesTransformerModel.from_pretrained("huggingface/time-series-transformer-tourism-monthly")
model
# during training, one provides both past and future values
# as well as possible additional features
outputs = model(
    past_values=batch["past_values"],
    past_time_features=batch["past_time_features"],
    past_observed_mask=batch["past_observed_mask"],
    static_categorical_features=batch["static_categorical_features"],
    static_real_features=batch["static_real_features"],
    future_values=batch["future_values"],
    future_time_features=batch["future_time_features"] )
outputs
last_hidden_state = outputs.last_hidden_state
last_hidden_state
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from transformers import TimeSeriesTransformerModel
from transformers import TimesformerModel


# Generate some fake time series data
np.random.seed(42)
time_steps = 100
X = np.arange(time_steps)
y = np.sin(X) + np.random.normal(scale=0.1, size=time_steps)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train.reshape(-1, 1)).flatten()
X_test = scaler.transform(X_test.reshape(-1, 1)).flatten()

# Create the transformer
transformer = TimeSeriesTransformerModel(
    sequence_length=10,
    output_length=1,
    num_input_series=1,
    num_output_series=1,
    num_encoder_layers=2,
    num_decoder_layers=2,
    d_model=64,
    nhead=4,
    dim_feedforward=128,
    dropout=0.1,
)

# Reshape the training data for the transformer
X_train_transformed, y_train_transformed = transformer.fit_transform(X_train.reshape(-1, 1), y_train.reshape(-1, 1))

# Build the model
model = Sequential([
    transformer,
    Dense(32, activation='relu'),
    Dropout(0.1),
    Dense(1),
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=1e-3), loss='mse')

# Train the model
history = model.fit(
    X_train_transformed,
    y_train_transformed,
    epochs=100,
    batch_size=32,
)

# Evaluate the model on the test data
X_test_transformed, y_test_transformed = transformer.transform(X_test.reshape(-1, 1), y_test.reshape(-1, 1))
y_pred = model.predict(X_test_transformed)
y_pred = y_pred.flatten()
y_test = y_test_transformed.flatten()
mae = mean_absolute_error(y_test, y_pred)
print('MAE:', mae)

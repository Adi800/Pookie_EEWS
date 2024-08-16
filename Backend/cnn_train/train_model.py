import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten

# Load datasets
data = pd.concat([
    pd.read_csv('earthquake_1995-2023.csv'),
    pd.read_csv('earthquake_data.csv')
], ignore_index=True)

# Preprocess the data
features = data[['magnitude', 'depth', 'latitude', 'longitude']]
labels = data['alert']  # Assuming 'alert' is your target column

# Convert labels to numerical values if needed
labels = labels.astype('category').cat.codes

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Reshape the data for CNN input
X_train_cnn = X_train_scaled.reshape(X_train_scaled.shape[0], X_train_scaled.shape[1], 1)
X_test_cnn = X_test_scaled.reshape(X_test_scaled.shape[0], X_test_scaled.shape[1], 1)

# Build the CNN model
model = Sequential()
model.add(Conv1D(32, kernel_size=2, activation='relu', input_shape=(X_train_cnn.shape[1], 1)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(len(np.unique(labels)), activation='softmax'))  # Change according to your number of classes

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_cnn, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Save the model
model.save('cnn_model.h5')

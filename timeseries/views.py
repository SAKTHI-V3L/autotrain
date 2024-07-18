import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from .forms import DatasetForm, TrainingParametersForm
from .models import Dataset, TrainingParameters
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam, SGD
from keras.losses import MeanSquaredError
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from datetime import datetime

def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('timeseries:train_model')
    else:
        form = DatasetForm()
    return render(request, 'timeseries/upload_dataset.html', {'form': form})

def preprocess_data(data, input_columns, output_column):
    encoded_columns = []

    for col in input_columns:
        if np.issubdtype(data[col].dtype, np.number):
            # Scale numerical data
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            # Extract date features
            data[col] = pd.to_datetime(data[col])
            data[col + '_year'] = data[col].dt.year
            data[col + '_month'] = data[col].dt.month
            data[col + '_day'] = data[col].dt.day
            data[col + '_hour'] = data[col].dt.hour
            data[col + '_minute'] = data[col].dt.minute
            encoded_columns += [col + '_year', col + '_month', col + '_day', col + '_hour', col + '_minute']
            data = data.drop(col, axis=1)
        else:
            # Encode categorical data
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col])
    
    # Encode the datetime features if any
    for col in encoded_columns:
        encoder = LabelEncoder()
        data[col] = encoder.fit_transform(data[col])
    
    # Separate input and output variables
    X = data[input_columns + encoded_columns].values
    y = data[output_column].values
    
    # Reshape data for LSTM
    X = X.reshape((X.shape[0], X.shape[1], 1))  # Assuming each column is a feature, and each sample is one time step
    y = y.reshape((y.shape[0], 1))
    
    return X, y

def train_model(request):
    if request.method == 'POST':
        form = TrainingParametersForm(request.POST)
        if form.is_valid():
            params = form.save(commit=False)
            
            # Get the last uploaded dataset
            latest_dataset = Dataset.objects.latest('id')
            params.dataset = latest_dataset
            params.save()

            dataset = params.dataset
            data = pd.read_csv(dataset.file.path)

            input_columns = [col.strip() for col in params.input_variables.split(',')]
            output_column = params.output_variable

            # Preprocess data
            X, y = preprocess_data(data, input_columns, output_column)

            model = Sequential()
            for _ in range(params.num_layers):
                model.add(LSTM(params.num_units, activation=params.activation_function, return_sequences=True))
            model.add(Dense(1))

            if params.optimizer == 'adam':
                optimizer = Adam()
            elif params.optimizer == 'sgd':
                optimizer = SGD()

            model.compile(optimizer=optimizer, loss=MeanSquaredError())
            model.fit(X, y, epochs=params.epochs, batch_size=32)

            accuracy = model.evaluate(X, y)

            return render(request, 'timeseries/model_result.html', {'accuracy': accuracy})
    else:
        form = TrainingParametersForm()
    return render(request, 'timeseries/train_model.html', {'form': form})

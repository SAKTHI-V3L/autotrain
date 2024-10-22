from django.shortcuts import render, redirect
from .forms import DatasetForm, TrainingParametersForm, PredictionForm
from .models import Dataset, TrainingParameters
from keras.models import load_model
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from django.conf import settings
import pandas as pd
import numpy as np

def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('timeseries:train_model')
    else:
        form = DatasetForm()
    return render(request, 'timeseries/upload_dataset.html', {'form': form})

def preprocess_data(data, input_columns, output_columns):
    # Remove columns with names like "Unnamed: 0" or any unwanted pattern
    columns_to_remove = [col for col in data.columns if 'Unnamed' in col]
    data = data.drop(columns=columns_to_remove, errors='ignore')

    encoded_columns = []

    for col in input_columns:
        if col not in data.columns:
            continue
        if np.issubdtype(data[col].dtype, np.number):
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            data[col] = pd.to_datetime(data[col])
            data[col + '_year'] = data[col].dt.year
            data[col + '_month'] = data[col].dt.month
            data[col + '_day'] = data[col].dt.day
            data[col + '_hour'] = data[col].dt.hour
            data[col + '_minute'] = data[col].dt.minute
            encoded_columns += [col + '_year', col + '_month', col + '_day', col + '_hour', col + '_minute']
            data = data.drop(col, axis=1)
        else:
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col])

    for col in encoded_columns:
        if col in data.columns:
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col])

    
    output_columns = [col for col in output_columns if col in data.columns]
    
    X = data[input_columns + encoded_columns].values
    y = data[output_columns].values  

    X = X.reshape((X.shape[0], X.shape[1], 1))
    y = y.reshape((y.shape[0], len(output_columns)))   

    return X, y


def train_model(request):
    accuracy = None
    output_columns = None

    dataset = Dataset.objects.last()
    data = pd.read_csv(dataset.file.path) if dataset else pd.DataFrame()

    if request.method == 'POST':
        form = TrainingParametersForm(request.POST, dataset_columns=data.columns)
        if form.is_valid():
            params = form.save(commit=False)
            params.dataset = dataset
            params.save()

            input_columns = []
            output_columns = []
            for col in data.columns:
                value = form.cleaned_data[f'col_{col}']
                if value == 'input':
                    input_columns.append(col)
                elif value == 'output':
                    output_columns.append(col)

            input_columns = ','.join(input_columns)
            output_columns = ','.join(output_columns)
            
            params.input_variables = input_columns
            params.output_variables = output_columns
            params.save()

            X, y = preprocess_data(data, input_columns.split(','), output_columns.split(','))

            model = Sequential()
            for _ in range(params.num_layers - 1):
                model.add(LSTM(params.num_units, activation=params.activation_function, return_sequences=True))
            model.add(LSTM(params.num_units, activation=params.activation_function))  
            model.add(Dense(len(output_columns.split(','))))

            if params.optimizer == 'adam':
                optimizer = Adam()
            elif params.optimizer == 'sgd':
                optimizer = SGD()
            elif params.optimizer == 'rmsprop':
                optimizer = RMSprop()
            elif params.optimizer == 'adagrad':
                optimizer = Adagrad()
            elif params.optimizer == 'adadelta':
                optimizer = Adadelta()

            model.compile(optimizer=optimizer, loss=MeanSquaredError())
            model.fit(X, y, epochs=params.epochs, batch_size=32)

            model_path = settings.BASE_DIR / 'timeseries' / 'models' / 'trained_model.h5'
            model.save(model_path)

            accuracy = model.evaluate(X, y)

            return render(request, 'timeseries/model_result.html', {'accuracy': accuracy, 'output_columns': output_columns.split(',')})
    else:
        form = TrainingParametersForm(dataset_columns=data.columns)

    return render(request, 'timeseries/train_model.html', {'form': form, 'dataset': dataset})

        
def model_result(request):
    input_data = None
    predictions = None
    output_columns = None
    zipped_results = None

    if request.method == 'POST':
        dataset = Dataset.objects.last()
        data = pd.read_csv(dataset.file.path)
        training_params = TrainingParameters.objects.last()

        input_columns = [col.strip() for col in training_params.input_variables.split(',')]
        output_columns = [col.strip() for col in training_params.output_variables.split(',')]

        form = PredictionForm(request.POST, input_columns=input_columns)
        if form.is_valid():
            input_data = form.cleaned_data

            
            processed_input_data = {}
            for col, value in input_data.items():
                try:
                    processed_input_data[col] = float(value) 
                except ValueError:
                    processed_input_data[col] = value  

            input_data_df = pd.DataFrame([processed_input_data])
            X, _ = preprocess_data(data, input_columns, output_columns)

        
            model_path = settings.BASE_DIR / 'timeseries' / 'models' / 'trained_model.h5'
            model = load_model(model_path)


            predictions = model.predict(X).tolist()

            
            zipped_results = list(zip(output_columns, predictions[0]))

    else:
        form = PredictionForm()

    return render(request, 'timeseries/model_result.html', {
        'input_data': input_data,
        'predictions': predictions,
        'form': form,
        'output_columns': output_columns,
        'zipped_results': zipped_results
    })
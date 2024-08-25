# Django Timeseries and Regression Project

## Overview
Autotrain is a Django-based web application designed to streamline the process of creating LSTM regression models. The app includes:

Data Preprocessing:

Normalizes numerical features
Encodes categorical variables
Extracts datetime features (e.g., year, month, day, hour, minute) for timeseries data
Feature Engineering:

Automates the preparation and transformation of data to make it suitable for modeling
Model Training:

Configures and trains LSTM models with customizable settings:
Number of LSTM units
Number of LSTM layers
Activation functions (e.g., ReLU)
Optimizers (e.g., Adam)
Number of epochs
Prediction:

Provides functionality to make predictions using the trained LSTM model based on user input


## Features

- **Dataset Upload**: Upload datasets in CSV format through a user-friendly interface.
- **Dynamic Form Generation**: Automatically generate forms based on dataset columns to select input and output variables.
- **Model Training**: Train models with configurable parameters including:
  - Number of LSTM units
  - Number of LSTM layers
  - Activation function 
  - Optimizer 
  - Number of epochs
- **Prediction**: Use trained models to make predictions based on user-provided input values.


## Setup and Installation

### Prerequisites

- Python 3.8+
- Django 4.2+
- Keras
- TensorFlow
- pandas
- scikit-learn

### Install Dependencies

1. **Install the required Python packages**:

    ```bash
    pip install Django>=4.2 Keras>=2.13.0 tensorflow>=2.14.0 pandas>=2.0.2 scikit-learn>=1.3.1
    ```

2. **Setup Django**

    1. **Migrate the Database**:

        ```bash
        python manage.py migrate
        ```

    2. **Create a Superuser (Optional)**:

        ```bash
        python manage.py createsuperuser
        ```

    3. **Run the Development Server**:

        ```bash
        python manage.py runserver
        ```

    4. **Access the Application**

        Open a web browser and navigate to `http://127.0.0.1:8000/` to use the application.



#Uploading a Dataset

1. Navigate to the upload page (`/upload_dataset/`).
2. Select and upload a CSV file.
3. The uploaded dataset will be available for model training.

# Training a Model

1. Go to the train model page (`/train_model/`).
2. Configure the following training parameters:
   - Input variables
   - Output variables
   - Number of LSTM units
   - Number of LSTM layers
   - Activation function
   - Optimizer
   - Number of epochs
3. Click "Train" to start the model training process.

#Making Predictions

1. Navigate to the model result page (`/model_result/`).
2. Enter the input values for prediction.
3. Click "Predict" to view the prediction results.

# Directory Structure

- regression/: Django application folder.
  - migrations/: Database migrations.
  - static/: Static files (CSS).
  - templates/: HTML templates.
    - `upload_dataset.html`
    - `train_model.html`
    - `model_result.html`
  - models.py: Defines the dataset and training parameters models.
  - forms.py: Contains forms for dataset upload, training parameters, and predictions.
  - views.py: Contains the view logic for dataset upload, model training, and predictions.
  - urls.py: Defines URL routing for the application.
  - manage.py: Django management script.





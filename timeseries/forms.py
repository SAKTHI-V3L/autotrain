from django import forms
from .models import Dataset, TrainingParameters

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']

ACTIVATION_FUNCTION_CHOICES = [
    ('relu', 'ReLU'),
    ('tanh', 'Tanh'),
    ('sigmoid', 'Sigmoid'),
    ('softmax', 'Softmax'),
    ('linear', 'Linear'),
]

OPTIMIZER_CHOICES = [
    ('adam', 'Adam'),
    ('sgd', 'SGD'),
    ('rmsprop', 'RMSprop'),
    ('adagrad', 'Adagrad'),
    ('adadelta', 'Adadelta'),
]

CHOICES = [
    ('none', 'None'),
    ('input', 'Input'),
    ('output', 'Output')
]

class TrainingParametersForm(forms.ModelForm):
    activation_function = forms.ChoiceField(choices=ACTIVATION_FUNCTION_CHOICES, required=True)
    optimizer = forms.ChoiceField(choices=OPTIMIZER_CHOICES, required=True)

    class Meta:
        model = TrainingParameters
        fields = ['num_units', 'num_layers', 'activation_function', 'epochs', 'optimizer']

    def __init__(self, *args, **kwargs):
        dataset_columns = kwargs.pop('dataset_columns', [])
        super().__init__(*args, **kwargs)
        for col in dataset_columns:
            self.fields[f'col_{col}'] = forms.ChoiceField(choices=CHOICES, label=col, initial='none')

class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        input_columns = kwargs.pop('input_columns', [])
        super(PredictionForm, self).__init__(*args, **kwargs)
        for col in input_columns:
            self.fields[col] = forms.CharField(label=col)

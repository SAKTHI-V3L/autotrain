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

class TrainingParametersForm(forms.ModelForm):
    activation_function = forms.ChoiceField(choices=ACTIVATION_FUNCTION_CHOICES, required=True)
    optimizer = forms.ChoiceField(choices=OPTIMIZER_CHOICES, required=True)

    class Meta:
        model = TrainingParameters
        fields = ['input_variables', 'output_variables', 'num_units', 'num_layers', 'activation_function', 'epochs', 'optimizer']



class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        input_columns = kwargs.pop('input_columns', [])
        super(PredictionForm, self).__init__(*args, **kwargs)
        for col in input_columns:
            # Use CharField to accept any type of input, then convert in view
            self.fields[col] = forms.CharField(label=col)




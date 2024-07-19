from django import forms
from .models import Dataset, TrainingParameters

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']

class TrainingParametersForm(forms.ModelForm):
    class Meta:
        model = TrainingParameters
        fields = [
            'input_variables', 
            'output_variables',  # Changed from output_variable to output_variables
            'num_units', 
            'num_layers', 
            'activation_function', 
            'epochs', 
            'optimizer'
        ]

class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        input_columns = kwargs.pop('input_columns', [])
        super(PredictionForm, self).__init__(*args, **kwargs)
        for col in input_columns:
            self.fields[col] = forms.FloatField(label=col)



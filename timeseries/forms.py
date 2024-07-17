from django import forms
from .models import Dataset, TrainingParameters

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']

class TrainingParametersForm(forms.ModelForm):
    class Meta:
        model = TrainingParameters
        fields = ['dataset', 'input_variables', 'output_variable', 'num_units', 'num_layers', 'activation_function', 'epochs', 'optimizer']
        widgets = {
            'input_variables': forms.TextInput(attrs={'placeholder': 'Comma-separated column names'}),
        }


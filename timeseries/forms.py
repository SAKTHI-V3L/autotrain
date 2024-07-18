from django import forms
from .models import Dataset, TrainingParameters

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']

class TrainingParametersForm(forms.ModelForm):
    class Meta:
        model = TrainingParameters
        fields = ['input_variables', 'output_variable', 'num_units', 'num_layers', 'activation_function', 'epochs', 'optimizer']
        widgets = {
            'input_variables': forms.TextInput(attrs={'placeholder': 'Comma-separated column names'}),
        }


class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        input_columns = kwargs.pop('input_columns', [])
        super(PredictionForm, self).__init__(*args, **kwargs)

        for col in input_columns:
            self.fields[col] = forms.CharField(label=col)

    def clean(self):
        cleaned_data = super().clean()
        # Perform additional validation if needed
        return cleaned_data



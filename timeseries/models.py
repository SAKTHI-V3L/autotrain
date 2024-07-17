from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='datasets/')

class TrainingParameters(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    input_variables = models.TextField()  # Comma-separated column names
    output_variable = models.CharField(max_length=100)
    num_units = models.IntegerField()
    num_layers = models.IntegerField()
    activation_function = models.CharField(max_length=50)
    epochs = models.IntegerField()
    optimizer = models.CharField(max_length=50)



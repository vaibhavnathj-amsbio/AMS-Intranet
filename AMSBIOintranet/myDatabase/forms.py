from .models import ProductRecords, ProductRecordsTech
from django import forms


# Django class for generating model form for 'ProductRecords' table
class EditProductForm(forms.ModelForm): 

    class Meta:
        model = ProductRecords
        fields = '__all__'


# Django class for generating model form for 'ProductRecordsTech' table
class EditTechDetailsForm(forms.ModelForm):

    class Meta:
        model = ProductRecordsTech
        fields = '__all__'
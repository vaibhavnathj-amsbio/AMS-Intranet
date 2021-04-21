from .models import ProductRecords, ProductRecordsTech
from django import forms

class EditProductForm(forms.ModelForm):

    class Meta:
        model = ProductRecords
        fields = '__all__'

class EditTechDetailsForm(forms.ModelForm):

    class Meta:
        model = ProductRecordsTech
        fields = '__all__'
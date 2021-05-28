from .models import ProductRecords, ProductRecordsTech
from django import forms


# Django class for generating model form for 'ProductRecords' table
class EditProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class' : 'form-control', 'rows':'0', 'cols':'10'})

    class Meta:
        model = ProductRecords
        fields = '__all__'


# Django class for generating model form for 'ProductRecordsTech' table
class EditTechDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditTechDetailsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class' : 'form-control', 'rows':'0', 'cols':'5'})

    class Meta:
        model = ProductRecordsTech
        fields = '__all__'
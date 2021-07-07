from .models import ProductRecords, ProductRecordsTech
from django import forms


# Django class for generating model form for 'ProductRecords' table
class EditProductForm(forms.ModelForm):
    sell_price_rest_of_world_usd = forms.CharField(max_length=64, disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {'class': 'form-control', 'rows': '0', 'cols': '10'})

    class Meta:
        model = ProductRecords
        fields = ["product_code",
                  "supplier_product_code",
                  "description",
                  "long_description",
                  "packsize",
                  "purchase_nett_price",
                  "supplier_list_price",
                  "sell_price_gbp",
                  "sell_price_eur",
                  "sell_price_chf",
                  "sell_price_usd",
                  "sell_price_rest_of_world_usd",
                  "storage_conditions",
                  "shipping_temperature",
                  "commodity_code",
                  "category_1",
                  "category_2",
                  "research_area_1",
                  "research_area_2",
                  "research_area_3",
                  "research_area_4",
                  "supplier_category_1",
                  "supplier_category_2",
                  "supplier_category_3",
                  "supplier_lead_time",
                  "ct_supplier_id",
                  "delete_flag",
                  "listing_precedence",
                  "last_updated_user",
                  "last_change_date",
                  "price_calculation_type",
                  "website_flag",
                  "new_product_flag",
                  "previous_purchase_price",
                  "price_change_flag",
                  "price_change_percent",
                  "is_in_website",
                  "is_in_odoo",
                  "special_shipping"]


# Django class for generating model form for 'ProductRecordsTech' table
class EditTechDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditTechDetailsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {'class': 'form-control', 'rows': '0', 'cols': '5'})

    class Meta:
        model = ProductRecordsTech
        fields = '__all__'
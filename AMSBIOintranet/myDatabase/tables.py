from .models import MasterCurrencies, ProductRecords
import django_tables2 as tables
from django_tables2.utils import A 


class CurrencyTable(tables.Table):
    From_col = tables.Column(accessor='symbolfrom',verbose_name='From', order_by='from_currency_id')
    To_col = tables.Column(accessor='symbolto',verbose_name='To',order_by='to_currency_id')
    exchange_rate = tables.Column(verbose_name='Exchange Rate')
    # live_rate = tables.Column(verbose_name='Live Rate', accessor='liverate', orderable=False) 
    # diff = tables.Column(accessor='diff', verbose_name='Difference', orderable=False)

    class Meta:
        model = MasterCurrencies
        fields = ['From_col','To_col','exchange_rate']
        # fields = fields + ['live_rate', 'diff']
        attrs = {"thead": {"position": "fixed;"}}
    

class ProductRecordsTable(tables.Table):
    sup_col = tables.Column(accessor='suppliername',verbose_name='Supplier')
    cat_1 = tables.Column(accessor='cat1', verbose_name='Category 1')
    cat_2 = tables.Column(accessor='cat2', verbose_name='Category 2')
    rsearch1 = tables.Column(accessor='research1', verbose_name='Research area 1')
    rsearch2 = tables.Column(accessor='research2', verbose_name='Research area 2')
    rsearch3 = tables.Column(accessor='research3', verbose_name='Research area 3')
    rsearch4 = tables.Column(accessor='research4', verbose_name='Research area 4')
    attrs = tables.TemplateColumn(template_name='button.html',verbose_name='Attribute')
    product_code = tables.Column(attrs={"td": {"style": "font-weight: bold;"}})

    class Meta:
        model = ProductRecords
        fields = ["attrs","product_code", "supplier_product_code", "description", "long_description", "packsize", "purchase_nett_price", "supplier_list_price", "sell_price_gbp", "sell_price_eur", "sell_price_chf", 
                    "sell_price_usd", "storage_conditions", "shipping_temperature", "commodity_code", "cat_1", "cat_2", "rsearch1", "rsearch2", "rsearch3", 
                        "rsearch4", "supplier_lead_time", "sup_col", "delete_flag", "listing_precedence", "last_updated_user", "last_change_date", "price_calculation_type", "website_flag", "new_product_flag", 
                            "previous_purchase_price", "price_change_flag", "price_change_percent", "special_shipping", ]
        orderable = False
        attrs = {"thead": {"style": "color: #fff; background-color: #f1594a;"}, "class": "table table-striped table-responsive"}
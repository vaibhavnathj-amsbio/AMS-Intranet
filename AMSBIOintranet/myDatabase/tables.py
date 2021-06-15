from .models import (MasterCurrencies, NwAttributes11Biorepository, NwAttributes12Molecularbiology, 
                    NwAttributes13Antibodies, NwAttributes14Proteinspeptides, NwAttributes15Cellscellculture, 
                    NwAttributes16Reagentslabware, NwAttributes17Kitsassays, NwAttributes18Bioseparationelectrophoresis, ProductRecords, ProductRecordsTech)
import django_tables2 as tables


# Django class for generating table for 'Currency value' page
class CurrencyTable(tables.Table):
    From_col = tables.Column(accessor='symbolfrom',verbose_name='From', order_by='from_currency_id')
    To_col = tables.Column(accessor='symbolto',verbose_name='To',order_by='to_currency_id')
    exchange_rate = tables.Column(verbose_name='Exchange Rate')
    live_rate = tables.Column(verbose_name='Live Rate', accessor='liverate', orderable=False) 
    diff = tables.Column(accessor='diff', verbose_name='Difference', orderable=False)

    class Meta:
        model = MasterCurrencies
        fields = ['From_col','To_col','exchange_rate']
        fields = fields + ['live_rate', 'diff']
        attrs = {"thead": {"position": "fixed;"}}
    

# Django class for generating table for 'search database' page
class ProductRecordsTable(tables.Table):
    sup_col = tables.Column(accessor='suppliername',verbose_name='Supplier')
    cat_1 = tables.Column(accessor='cat1', verbose_name='Category 1')
    cat_2 = tables.Column(accessor='cat2', verbose_name='Category 2')
    rsearch1 = tables.Column(accessor='research1', verbose_name='Research area 1')
    rsearch2 = tables.Column(accessor='research2', verbose_name='Research area 2')
    rsearch3 = tables.Column(accessor='research3', verbose_name='Research area 3')
    rsearch4 = tables.Column(accessor='research4', verbose_name='Research area 4')
    attrs = tables.TemplateColumn(template_name='button.html',verbose_name='Attribute')
    product_code = tables.Column(linkify=("similarProducts", [tables.A("product_code")]), attrs={"a": {"id": "similarProduct"}})

    class Meta:
        model = ProductRecords
        fields = ["attrs","product_code", "supplier_product_code", "description", "long_description", "packsize", "purchase_nett_price", "supplier_list_price", "sell_price_gbp", "sell_price_eur", "sell_price_chf", 
                    "sell_price_usd", "storage_conditions", "shipping_temperature", "commodity_code", "cat_1", "cat_2", "rsearch1", "rsearch2", "rsearch3", 
                        "rsearch4", "supplier_lead_time", "sup_col", "delete_flag", "listing_precedence", "last_updated_user", "last_change_date", "price_calculation_type", "website_flag", "new_product_flag", 
                            "previous_purchase_price", "price_change_flag", "price_change_percent", "special_shipping", ]
        orderable = False
        attrs = {"thead": {"style": "color: #fff; background-color: #f1594a;"}, "class": "table table-striped table-responsive"}


class TechRecords_Base(tables.Table):
    product_code = tables.Column(accessor='product_code__product_code')
    Owner = tables.Column(accessor='product_code__suppliername', verbose_name='Owner')
    Supplier_product_code = tables.Column(accessor='product_code__supplier_product_code', verbose_name='Supplier Product Code')
    Pack_Size = tables.Column(accessor='product_code__packsize', verbose_name='Pack Size')
    sell_price_gbp = tables.Column(accessor='product_code__sell_price_gbp', verbose_name='Selling Price GBP')

    class Meta:
        model = ProductRecords
        fields = ["product_code", "Owner", "Supplier_product_code", "Pack_Size", "sell_price_gbp"]
        orderable = False
        sequence = ["product_code", "Owner", "Supplier_product_code", "Pack_Size", "sell_price_gbp", "..."]
        attrs = {"thead": {"style": "color: #fff; background-color: #f1594a;"}, 
                "class": "table table-striped table-responsive", 
                "style": "margin: 0 auto; width: fit-content;"}


class TechRecordsTable_Biorepository(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes11Biorepository
        fields = [
            "name",
            "species",
            "tissue_type",
            "disease",
            "format",
            "cell_line"]


class TechRecordsTable_Molecularbiology(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes12Molecularbiology
        fields = ["accession_no",
            "tag",
            "aa_sequence",
            "species",
            "selection_marker",
            "promoter",
            "tag_position",
            "purification"]


class TechRecordsTable_Antibodies(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes13Antibodies
        fields = ["host_species",
            "species_reactivity",
            "immunogen",
            "isotype",
            "clone_number",
            "application",
            "label_conjugate",
            "epitope",
            "target",
            "species"]


class TechRecordsTable_Proteinspeptides(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes14Proteinspeptides
        fields = [
            "name",
            "cell_line",
            "accession_no",
            "species",
            "expression_host",
            "aa_sequence",
            "tag",
            "label_conjugate",
            "tag_position"]


class TechRecordsTable_CellsCellCulture(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes15Cellscellculture
        fields = [
            "name",
            "cell_line",
            "protein",
            "accession_no",
            "species",
            "tag",
            "aa_sequence",
            "tag_position",
            "serotype",
            "promoter",
            "selection_marker"]


class TechRecordsTable_Reagentslabware(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes16Reagentslabware
        fields = [
                "name",
                "cas_no",
                "expression_host",
                "activity",
                "species",
                "carbohydrate_type",
                "oligosaccharide_length"]


class TechRecordsTable_Kitsassays(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes17Kitsassays
        fields = [
            "species_reactivity",
            "detection_range",
            "sensitivity",
            "sample_type",
            "elisa_format",
            "cross_reactivity",
            "specificity"]


class TechRecordsTable_Bioseparationelectrophoresis(TechRecords_Base, tables.Table):

    class Meta(TechRecords_Base.Meta):
        model = NwAttributes18Bioseparationelectrophoresis
        fields = [
            "format_of_drug",
            "bead_size"]
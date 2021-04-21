# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import requests
import json

class Currencies(models.Model):
    # Field name made lowercase.
    currencyid = models.AutoField(db_column='CurrencyID', primary_key=True)
    # Field name made lowercase.
    descriptive = models.CharField(db_column='Descriptive', max_length=16)
    # Field name made lowercase.
    comments = models.CharField(db_column='Comments', max_length=45)
    dimmensions_currency_symbol = models.CharField(max_length=4)

    def __str__(self):
        return self.descriptive
        

    class Meta:
        managed = False
        db_table = 'currencies'
        verbose_name_plural = "Currencies"
    

class DataOwners(models.Model):
    dat_id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    owner = models.CharField(db_column='Owner', max_length=64)
    # Field name made lowercase.
    supplierpurchasecurrency = models.CharField(
        db_column='SupplierPurchaseCurrency', max_length=4, blank=True, null=True)
    productpurchasebrand = models.PositiveIntegerField(
        db_column='ProductPurchaseBrand', blank=True, null=True)  # Field name made lowercase.
    productsellingbrand = models.PositiveIntegerField(
        db_column='ProductSellingBrand', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dimmensionssuppliercode = models.CharField(
        db_column='DimmensionsSupplierCode', max_length=10, blank=True, null=True)
    dimmensionsproductgroup = models.PositiveIntegerField(
        db_column='DimmensionsProductGroup', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    msaccessdatid = models.PositiveIntegerField(
        db_column='MsAccessDatId', blank=True, null=True)
    # Field name made lowercase.
    datasheetsuffix = models.CharField(
        db_column='DatasheetSuffix', max_length=4, blank=True, null=True)
    logo_url = models.CharField(max_length=128, blank=True, null=True)
    web_site_sql_id = models.PositiveIntegerField(blank=True, null=True)
    precedence_listing = models.PositiveIntegerField(blank=True, null=True)
    web_site_url = models.CharField(max_length=45, blank=True, null=True)
    ik_flag_id = models.PositiveIntegerField(blank=True, null=True)
    currencyid = models.PositiveIntegerField(blank=True, null=True)
    usa_market_flag_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.owner

    class Meta:
        db_table = 'data_owners'
        verbose_name_plural = "Data Owners"
    


class MasterCurrencies(models.Model):
    mstr_cur_id = models.AutoField(primary_key=True)
    from_currency_id = models.PositiveIntegerField()
    to_currency_id = models.PositiveIntegerField()
    exchange_rate = models.FloatField()

    def symbolfrom(self):
        symbol = [1,2,3,4,6,7]
        if self.from_currency_id in symbol:
                return Currencies.objects.get(pk=self.from_currency_id).descriptive

    def symbolto(self):
        symbol = [1,2,3,4,6,7]
        if self.to_currency_id in symbol:
                return Currencies.objects.get(pk=self.to_currency_id).descriptive

    def liverate(self):
        url = "https://currency-exchange.p.rapidapi.com/exchange"

        querystring = {"from": self.symbolfrom() , "to": self.symbolto()}

        headers = {
            'x-rapidapi-key': "bbd68be6d5mshec3a954fdacc16fp100d26jsn431dde547552",
            'x-rapidapi-host': "currency-exchange.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        return float(response.text)
    
    def diff(self):
        return round(self.liverate() - self.exchange_rate,3)
           
    class Meta:
        managed = False
        db_table = 'master_currencies'
        verbose_name_plural = "Master Currencies"


class ProductRecords(models.Model):
    product_code = models.CharField(primary_key=True, max_length=64)
    supplier_product_code = models.CharField(
        max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    packsize = models.CharField(max_length=256, blank=True, null=True)
    purchase_nett_price = models.FloatField(blank=True, null=True)
    supplier_list_price = models.FloatField(blank=True, null=True)
    sell_price_gbp = models.FloatField(blank=True, null=True)
    sell_price_eur = models.FloatField(blank=True, null=True)
    sell_price_chf = models.FloatField(blank=True, null=True)
    sell_price_usd = models.FloatField(blank=True, null=True)
    storage_conditions = models.TextField(blank=True, null=True)
    shipping_temperature = models.TextField(blank=True, null=True)
    commodity_code = models.TextField(blank=True, null=True)
    category_1 = models.IntegerField(blank=True, null=True)
    category_2 = models.IntegerField(blank=True, null=True)
    research_area_1 = models.IntegerField(blank=True, null=True)
    research_area_2 = models.IntegerField(blank=True, null=True)
    research_area_3 = models.IntegerField(blank=True, null=True)
    research_area_4 = models.IntegerField(blank=True, null=True)
    supplier_category_1 = models.TextField(blank=True, null=True)
    supplier_category_2 = models.TextField(blank=True, null=True)
    supplier_category_3 = models.TextField(blank=True, null=True)
    supplier_lead_time = models.TextField(blank=True, null=True)
    ct_supplier_id = models.IntegerField(blank=True, null=True)
    delete_flag = models.IntegerField(blank=True, null=True)
    listing_precedence = models.IntegerField(blank=True, null=True)
    last_updated_user = models.CharField(max_length=64, blank=True, null=True)
    last_change_date = models.DateTimeField(blank=True, null=True)
    price_calculation_type = models.PositiveIntegerField(blank=True, null=True)
    website_flag = models.IntegerField(blank=True, null=True)
    new_product_flag = models.IntegerField(blank=True, null=True)
    previous_purchase_price = models.FloatField(blank=True, null=True)
    price_change_flag = models.IntegerField(blank=True, null=True)
    price_change_percent = models.FloatField(blank=True, null=True)
    is_in_website = models.IntegerField(blank=True, null=True)
    is_in_odoo = models.IntegerField(blank=True, null=True)
    special_shipping = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_records'

    def suppliername(self):
        return DataOwners.objects.get(pk=self.ct_supplier_id).owner
    
    def cat1(self):
        lev1 = NwCategoryLowestNodes.objects.get(pk=self.category_1).level1
        lev2 = NwCategoryLowestNodes.objects.get(pk=self.category_1).level2
        lev3 = NwCategoryLowestNodes.objects.get(pk=self.category_1).level3
        if lev2 == 0:
            return NwCategoryIds.objects.get(pk=lev1).category_name
        elif lev3 == 0 and lev2 != 0:
            return str(NwCategoryIds.objects.get(pk=lev1).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev2).category_name)  
        else:
            return str(NwCategoryIds.objects.get(pk=lev1).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev2).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev3).category_name)
    
    def cat2(self):
        lev1 = NwCategoryLowestNodes.objects.get(pk=self.category_2).level1
        lev2 = NwCategoryLowestNodes.objects.get(pk=self.category_2).level2
        lev3 = NwCategoryLowestNodes.objects.get(pk=self.category_2).level3
        if lev2 == 0:
            return NwCategoryIds.objects.get(pk=lev1).category_name
        elif lev3 == 0 and lev2 != 0:
            return str(NwCategoryIds.objects.get(pk=lev1).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev2).category_name)  
        else:
            return str(NwCategoryIds.objects.get(pk=lev1).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev2).category_name) + " >> " + str(NwCategoryIds.objects.get(pk=lev3).category_name)        
    
    def research1(self):
        return NwResearchAreaIds.objects.get(pk=self.research_area_1).research_area

    def research2(self):
        return NwResearchAreaIds.objects.get(pk=self.research_area_2).research_area

    def research3(self):
        return NwResearchAreaIds.objects.get(pk=self.research_area_3).research_area

    def research4(self):
        return NwResearchAreaIds.objects.get(pk=self.research_area_4).research_area


class ProductRecordsTech(models.Model):
    product_code = models.CharField(primary_key=True, max_length=64)
    species = models.TextField(blank=True, null=True)
    tissue_type = models.TextField(blank=True, null=True)
    disease = models.TextField(blank=True, null=True)
    format_of_drug = models.TextField(verbose_name="Format", blank=True, null=True,db_column='format')
    cell_line = models.TextField(blank=True, null=True)
    accession_no = models.TextField(blank=True, null=True)
    gene_id = models.TextField(blank=True, null=True)
    gene_symbol = models.TextField(blank=True, null=True)
    gene_synonyms = models.TextField(blank=True, null=True)
    gene_description = models.TextField(blank=True, null=True)
    locus_id = models.TextField(blank=True, null=True)
    protein_families = models.TextField(blank=True, null=True)
    protein_pathways = models.TextField(blank=True, null=True)
    vector = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    sequence_data = models.TextField(blank=True, null=True)
    aa_sequence = models.TextField(blank=True, null=True)
    application = models.TextField(blank=True, null=True)
    cas_no = models.TextField(blank=True, null=True)
    selection_marker = models.TextField(blank=True, null=True)
    promoter = models.TextField(blank=True, null=True)
    tag_position = models.TextField(blank=True, null=True)
    purification = models.TextField(blank=True, null=True)
    vector_type = models.TextField(blank=True, null=True)
    sample_type = models.TextField(blank=True, null=True)
    concentration = models.TextField(blank=True, null=True)
    bead_size = models.TextField(blank=True, null=True)
    cell_type = models.TextField(blank=True, null=True)
    host_species = models.TextField(blank=True, null=True)
    species_reactivity = models.TextField(blank=True, null=True)
    immunogen = models.TextField(blank=True, null=True)
    isotype = models.TextField(blank=True, null=True)
    clone_number = models.TextField(blank=True, null=True)
    formulation = models.TextField(blank=True, null=True)
    preservative = models.TextField(blank=True, null=True)
    label_conjugate = models.TextField(blank=True, null=True)
    clonality = models.TextField(blank=True, null=True)
    type_of_drug = models.TextField(verbose_name="Type", blank=True, null=True, db_column='type')
    epitope = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    uniprot_id = models.TextField(blank=True, null=True)
    expression_host = models.TextField(blank=True, null=True)
    predicted_mw = models.TextField(blank=True, null=True)
    determined_mw = models.TextField(blank=True, null=True)
    activity = models.TextField(blank=True, null=True)
    purity = models.TextField(blank=True, null=True)
    endotoxin = models.TextField(blank=True, null=True)
    labeling_method = models.TextField(blank=True, null=True)
    target_specificity = models.TextField(blank=True, null=True)
    components = models.TextField(blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)
    protocol_usage = models.TextField(blank=True, null=True)
    dimensions = models.TextField(blank=True, null=True)
    serotype = models.TextField(blank=True, null=True)
    protein_type = models.TextField(blank=True, null=True)
    protein = models.TextField(blank=True, null=True)
    mycoplasma_testing = models.TextField(blank=True, null=True)
    license_requirement = models.TextField(blank=True, null=True)
    expression = models.TextField(blank=True, null=True)
    tumorigenic = models.TextField(blank=True, null=True)
    mw = models.TextField(blank=True, null=True)
    alternative_names = models.TextField(blank=True, null=True)
    activity_definition = models.TextField(blank=True, null=True)
    carbohydrate_type = models.TextField(blank=True, null=True)
    oligosaccharide_length = models.TextField(blank=True, null=True)
    detection_range = models.TextField(blank=True, null=True)
    sensitivity = models.TextField(blank=True, null=True)
    elisa_format = models.TextField(blank=True, null=True)
    cross_reactivity = models.TextField(blank=True, null=True)
    specificity = models.TextField(blank=True, null=True)
    assay_time = models.TextField(blank=True, null=True)
    intra_assay_cv = models.TextField(blank=True, null=True)
    inter_assay_cv = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_records_tech'


class NwCategoryIds(models.Model):
    cat_id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='Category_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nw_category_ids'


class NwCategoryLowestNodes(models.Model):
    lowest_node = models.IntegerField(primary_key=True)
    level1 = models.IntegerField(blank=True, null=True)
    level2 = models.IntegerField(blank=True, null=True)
    level3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nw_category_lowest_nodes'


class NwResearchAreaIds(models.Model):
    research_id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    research_area = models.CharField(db_column='Research_Area', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nw_research_area_ids'
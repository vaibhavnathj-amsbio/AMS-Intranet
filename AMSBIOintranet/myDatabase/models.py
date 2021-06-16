# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import regex as re
from .cron import live_rate_dict


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
        db_table = 'currencies'
        app_label = 'myDatabase'
        verbose_name_plural = "Currencies"
    

class DataOwners(models.Model):
    dat_id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    owner = models.CharField(db_column='Owner', max_length=64)
    # Field name made lowercase.
    supplierpurchasecurrency = models.CharField(
        db_column='SupplierPurchaseCurrency', max_length=4, blank=True, null=True)
    productpurchasebrand = models.PositiveIntegerField(
        db_column='ProductPurchaseBrand', blank=True, null=True, default=1)  # Field name made lowercase.
    productsellingbrand = models.PositiveIntegerField(
        db_column='ProductSellingBrand', blank=True, null=True, default=1)  # Field name made lowercase.
    # Field name made lowercase.
    dimmensionssuppliercode = models.CharField(
        db_column='DimmensionsSupplierCode', max_length=10, blank=True, null=True)
    dimmensionsproductgroup = models.PositiveIntegerField(
        db_column='DimmensionsProductGroup', blank=True, null=True, default=1)  # Field name made lowercase.
    # Field name made lowercase.
    msaccessdatid = models.PositiveIntegerField(
        db_column='MsAccessDatId', blank=True, null=True, default=1)
    # Field name made lowercase.
    datasheetsuffix = models.CharField(
        db_column='DatasheetSuffix', max_length=4, blank=True, null=True, default=1)
    logo_url = models.CharField(max_length=128, blank=True, null=True, default=1)
    web_site_sql_id = models.PositiveIntegerField(blank=True, null=True, default=1)
    precedence_listing = models.PositiveIntegerField(blank=True, null=True, default=1)
    web_site_url = models.CharField(max_length=45, blank=True, null=True, default=1)
    ik_flag_id = models.PositiveIntegerField(blank=True, null=True, default=1)
    currencyid = models.PositiveIntegerField(blank=True, null=True)
    usa_market_flag_id = models.PositiveIntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return self.owner

    class Meta:
        db_table = 'data_owners'
        app_label = 'myDatabase'
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
        return live_rate_dict[self.symbolfrom()][self.symbolto()]
    
    def diff(self):
        return round(self.liverate() - self.exchange_rate, 3)
           
    class Meta:
        db_table = 'master_currencies'
        app_label = 'myDatabase'
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
        db_table = 'product_records'
        app_label = 'myDatabase'

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

    def purchasePriceGbp(self):
        global live_rate_dict
        currency = DataOwners.objects.get(pk=self.ct_supplier_id).supplierpurchasecurrency
        return round(self.purchase_nett_price*live_rate_dict[currency]["GBP"],3)

    def ug_ps(self):
        mlr = 1
        ps = self.packsize.replace('µ','u')
        outp = 0
        if 'x' in ps.lower():
            if '/ml' in ps.lower():
                ps = re.sub(r'([0-9\.]+) ?([mu]?g) ?/ ?ml ?x ?([0-9\.]+) ?ml',r'\1 x \3 \2',ps,re.IGNORECASE)
            mlr = float(re.findall('([0-9\.]{1,2}) ?x ?',ps,re.IGNORECASE)[0])
            ps = re.sub('[0-9]{1,2} ?x ?','',ps,re.IGNORECASE)

        if 'mg' in ps.lower():
            outp = mlr * float(re.findall('([0-9\.]{1,4}) ?mg',ps,re.IGNORECASE)[0]) * 1000
        elif re.match('^[0-9] ?g$',ps,re.IGNORECASE):
            outp = mlr * float(re.findall('([0-9\.]{1,4}) ?g',ps,re.IGNORECASE)[0]) * 1000000
        elif 'ug' in ps.lower():
            outp = mlr * float(re.findall('([0-9\.]{1,4}) ?ug',ps,re.IGNORECASE)[0])
        return round(self.purchasePriceGbp()/outp, 3)


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
        db_table = 'product_records_tech'
        app_label = 'myDatabase'


class NwCategoryIds(models.Model):
    cat_id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='Category_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nw_category_ids'
        app_label = 'myDatabase'


class NwCategoryLowestNodes(models.Model):
    lowest_node = models.IntegerField(primary_key=True)
    level1 = models.IntegerField(blank=True, null=True)
    level2 = models.IntegerField(blank=True, null=True)
    level3 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'nw_category_lowest_nodes'
        app_label = 'myDatabase'


class NwResearchAreaIds(models.Model):
    research_id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    research_area = models.CharField(db_column='Research_Area', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nw_research_area_ids'
        app_label = 'myDatabase'


class NwAttributes11Biorepository(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    species = models.CharField(max_length=256)
    tissue_type = models.CharField(max_length=256)
    disease = models.CharField(max_length=256)
    format = models.CharField(max_length=256)
    cell_line = models.CharField(max_length=256)
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_11_biorepository'
        app_label = 'myDatabase'
    

class NwAttributes12Molecularbiology(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    accession_no = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    locus_id = models.TextField()
    protein_families = models.TextField()
    protein_pathways = models.TextField()
    vector = models.TextField()
    tag = models.TextField()
    sequence_data = models.TextField()
    aa_sequence = models.TextField()
    application = models.TextField()
    species = models.TextField()
    cas_no = models.TextField()
    selection_marker = models.TextField()
    promoter = models.TextField()
    tag_position = models.TextField()
    purification = models.TextField()
    vector_type = models.TextField()
    sample_type = models.TextField()
    concentration = models.TextField()
    bead_size = models.TextField()
    cell_type = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_12_molecularbiology'
        app_label = 'myDatabase'


class NwAttributes13Antibodies(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    accession_no = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    locus_id = models.TextField()
    protein_families = models.TextField()
    protein_pathways = models.TextField()
    host_species = models.TextField()
    species_reactivity = models.TextField()
    immunogen = models.TextField()
    isotype = models.TextField()
    clone_number = models.TextField()
    formulation = models.TextField()
    preservative = models.TextField()
    concentration = models.TextField()
    purification = models.TextField()
    format = models.TextField()
    application = models.TextField()
    label_conjugate = models.TextField()
    clonality = models.TextField()
    type = models.TextField()
    epitope = models.TextField()
    target = models.TextField()
    species = models.TextField()
    tissue_type = models.TextField()
    cell_line = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_13_antibodies'
        app_label = 'myDatabase'


class NwAttributes14Proteinspeptides(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    accession_no = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    locus_id = models.TextField()
    protein_families = models.TextField()
    protein_pathways = models.TextField()
    uniprot_id = models.TextField()
    species = models.TextField()
    expression_host = models.TextField()
    predicted_mw = models.TextField()
    determined_mw = models.TextField()
    concentration = models.TextField()
    aa_sequence = models.TextField()
    activity = models.TextField()
    format = models.TextField()
    purity = models.TextField()
    endotoxin = models.TextField()
    tag = models.TextField()
    formulation = models.TextField()
    labeling_method = models.TextField()
    target_specificity = models.TextField()
    components = models.TextField()
    preparation = models.TextField()
    application = models.TextField()
    tissue_type = models.TextField()
    disease = models.TextField()
    cell_line = models.TextField()
    protocol_usage = models.TextField()
    bead_size = models.TextField()
    label_conjugate = models.TextField()
    tag_position = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_14_proteinspeptides'
        app_label = 'myDatabase'


class NwAttributes15Cellscellculture(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    accession_no = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    locus_id = models.TextField()
    protein_families = models.TextField()
    protein_pathways = models.TextField()
    species = models.TextField()
    tissue_type = models.TextField()
    format = models.TextField()
    application = models.TextField()
    cell_line = models.TextField()
    dimensions = models.TextField()
    type = models.TextField()
    cell_type = models.TextField()
    vector = models.TextField()
    tag = models.TextField()
    sequence_data = models.TextField()
    aa_sequence = models.TextField()
    tag_position = models.TextField()
    vector_type = models.TextField()
    uniprot_id = models.TextField()
    disease = models.TextField()
    serotype = models.TextField()
    formulation = models.TextField()
    expression_host = models.TextField()
    promoter = models.TextField()
    protein_type = models.TextField()
    protein = models.TextField()
    mycoplasma_testing = models.TextField()
    license_requirement = models.TextField()
    expression = models.TextField()
    tumorigenic = models.TextField()
    components = models.TextField()
    preparation = models.TextField()
    selection_marker = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_15_cellscellculture'
        app_label = 'myDatabase'


class NwAttributes16Reagentslabware(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    protein_families = models.TextField()
    protein_pathways = models.TextField()
    cas_no = models.TextField()
    purity = models.TextField()
    mw = models.TextField()
    alternative_names = models.TextField()
    expression_host = models.TextField()
    application = models.TextField()
    concentration = models.TextField()
    activity = models.TextField()
    species = models.TextField()
    activity_definition = models.TextField()
    tissue_type = models.TextField()
    carbohydrate_type = models.TextField()
    oligosaccharide_length = models.TextField()
    label_conjugate = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_16_reagentslabware'
        app_label = 'myDatabase'


class NwAttributes17Kitsassays(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    accession_no = models.TextField()
    gene_id = models.TextField()
    gene_symbol = models.TextField()
    gene_synonyms = models.TextField()
    gene_description = models.TextField()
    species_reactivity = models.TextField()
    detection_range = models.TextField()
    sensitivity = models.TextField()
    application = models.TextField()
    preservative = models.TextField()
    components = models.TextField()
    sample_type = models.TextField()
    format = models.TextField()
    elisa_format = models.TextField()
    cross_reactivity = models.TextField()
    specificity = models.TextField()
    assay_time = models.TextField()
    intra_assay_cv = models.TextField()
    inter_assay_cv = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_17_kitsassays'
        app_label = 'myDatabase'


class NwAttributes18Bioseparationelectrophoresis(models.Model):
    product_code = models.OneToOneField(ProductRecords, primary_key=True, max_length=64, db_constraint=False, db_column='product_code', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    application = models.TextField()
    format = models.TextField()
    bead_size = models.TextField()
    type = models.TextField()
    product_flag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nw_attributes_18_bioseparationelectrophoresis'
        app_label = 'myDatabase'
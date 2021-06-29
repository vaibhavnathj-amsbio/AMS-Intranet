import json
import getpass
from datetime import datetime

from .forms import EditProductForm, EditTechDetailsForm
from .tables import (CurrencyTable, ProductRecordsTable, TechRecordsTable_Antibodies, 
                    TechRecordsTable_Bioseparationelectrophoresis,
                    TechRecordsTable_Biorepository, TechRecordsTable_CellsCellCulture, 
                    TechRecordsTable_Kitsassays, TechRecordsTable_Molecularbiology, 
                    TechRecordsTable_Proteinspeptides, TechRecordsTable_Reagentslabware)
from .models import (MasterCurrencies, NwAttributes11Biorepository, NwAttributes12Molecularbiology, 
                    NwAttributes13Antibodies, NwAttributes14Proteinspeptides, NwAttributes15Cellscellculture, 
                    NwAttributes16Reagentslabware, NwAttributes17Kitsassays, NwAttributes18Bioseparationelectrophoresis, ProductRecords,
                    ProductRecordsTech, NwCategoryIds, NwCategoryLowestNodes, DataOwners, Currencies)

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.paginators import LazyPaginator
from django.contrib import messages


def index(request):
    return redirect('/')


def addNewSupplier(request):
    """ Main function for rendering the Add new Supplier page! """
    if request.method == "POST" and len(request.POST['comp_name']) > 0:
        name = request.POST['comp_name']
        code = request.POST['acc_code'].upper()
        curr = request.POST['curr_code']
        if curr == 'USD':
            cur_id = 2    
        else:
            cur_id = Currencies.objects.get(descriptive=curr).currencyid
        DataOwners.objects.create(
            currencyid= cur_id,
            owner= name,
            supplierpurchasecurrency= curr,
            dimmensionssuppliercode= code
        )
        context = {'c_name': name, 'c_code':code, 'cur': curr , 'msg': 'Supplier successfully added!'}
        return JsonResponse(context)
    else:
        return render(request, 'newsupplier.html')


def search(request):
    """ Function to control and render the search page!"""
    obj = ProductRecordsTable(ProductRecords.objects.all()[8:])
    RequestConfig(request, paginate={"paginator_class": LazyPaginator, "per_page": 10}).configure(obj)
    msg = True
    if request.method == "POST":
        code = request.POST['Prod']
        desc = request.POST['Desc']
        if len(code) == 0 and len(desc) == 0:
            msg = False
            obj = "*Please enter a search term!"
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        elif len(code) == 0 and len(desc) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                description__icontains=desc).filter(delete_flag = 0).order_by('product_code')[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        elif len(desc) == 0 and len(code) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(delete_flag = 0).order_by('product_code')[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        else:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(description__icontains=desc).filter(delete_flag = 0).order_by('product_code')[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
    else:
        return render(request, 'search.html', {'obj': obj, 'msg': msg})


def currencyValue(request):
    """ Function to control and render the Current Currency page! """
    obj = CurrencyTable(MasterCurrencies.objects.exclude(exchange_rate=1))
    RequestConfig(request).configure(obj)
    export_format = request.GET.get("_export", None)
    now = datetime.today().strftime("%b-%d-%Y")
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, obj)
        return exporter.response("Currency_{}.{}".format(now, export_format))
    return render(request, 'currencyval.html', {'obj': obj})


def editProductRecords(pk):
    """ Helper function for generating the 'Edit Product' form! """
    ProdForm = EditProductForm()
    Product = ProductRecords.objects.get(pk=pk)
    ProdForm = EditProductForm(instance=Product)
    ProdForm.fields['product_code'].widget.attrs['readonly'] = True
    ProdForm.fields['supplier_product_code'].widget.attrs['readonly'] = True
    ProdForm.fields['last_updated_user'].widget.attrs['readonly'] = True
    ProdForm.fields['last_change_date'].widget.attrs['readonly'] = True
    return ProdForm


def editTechDetails(pk):
    """ Helper function for generating the 'Edit Technical Details' form! """
    TechForm = EditTechDetailsForm()
    TechDetails = ProductRecordsTech.objects.get(pk=pk)
    TechForm = EditTechDetailsForm(instance=TechDetails)
    TechForm.fields['product_code'].widget.attrs['readonly'] = True
    return TechForm


def FormSubmit(request):
    """ Helper function for submitting a form! """
    json_data = json.loads(request.POST['data'])
    form_data = {}
    for ele in json_data:
        temp = list(ele.values())
        form_data[temp[0]] = temp[1]
    form_data.pop('csrfmiddlewaretoken')
    if 'supplier_product_code' in form_data.keys():
        form_data['last_updated_user'] = getpass.getuser().upper()
        form_data['last_change_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Product = ProductRecords.objects.get(pk=form_data['product_code'])
        ProdForm = EditProductForm(form_data,instance=Product)
        if ProdForm.is_valid():
            ProdForm.save()
            return JsonResponse({"msg": "Form Submitted!"})
        else:
            return JsonResponse({"msg": ProdForm.errors})
    else:
        TechRecord = ProductRecordsTech.objects.get(pk=form_data['product_code'])
        TechForm = EditTechDetailsForm(form_data, instance=TechRecord)
        if TechForm.is_valid():
            TechForm.save()
            return JsonResponse({"msg": "Form Submitted!"})
        else:
            return JsonResponse({"msg": TechForm.errors})


def editSingleProduct(request, pk):
    """ Main function for rendering the Edit Product page! """
    flag = True
    nocategory = False
    if request.method == "POST" and 'btnSubmitCode' in request.POST:
        code = request.POST["ProdCode"]
        try:
            if ProductRecords.objects.get(pk=code).category_1 == 0: # Case where no categories are defined.
                ProdForm= editProductRecords(code)
                noTechCategory = "No Categories defined!"
                nocategory = True
                context = {'ProdForm':ProdForm,'NoTechCategory': noTechCategory, 'nocategory' : nocategory}
                return render(request, 'editsingleprod.html', context)
            else:
                cat = loadCategory(code) # generating level 1 category
                attributes = ['id_product_code'] +  ['id_' + ele for ele in list(cat[0].values())[0]]
                ProdForm = editProductRecords(code)
                TechForm = editTechDetails(code)
                flag = False
                TwoCategories = True
                if len(cat) > 1: # check if 2 categories exists
                    attributes2 = ['id_' + ele for ele in list(cat[1].values())[0]]
                    merged_attrs = attributes + list(set(attributes2) - set(attributes))
                    context = {'ProdForm': ProdForm, 'TechForm': TechForm, 'flag': flag, 'cat1': list(cat[0].keys())[0], 
                                'cat2': list(cat[1].keys())[0], 'catflag': TwoCategories, 'attrs': merged_attrs}
                else: 
                    TwoCategories = False
                    context = {'ProdForm': ProdForm, 'TechForm': TechForm, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                                'catflag': TwoCategories, 'attrs': attributes}
                return render(request, 'editsingleprod.html', context)
        except:
            flag = True
            return render(request, 'editsingleprod.html', {'msg': "Enter a valid product code", 'flag': flag})
    else:
        try:
            if ProductRecords.objects.get(pk=pk).category_1 == 0: # Case where no categories are defined.
                ProdForm= editProductRecords(pk)
                noTechCategory = "No Categories defined!"
                nocategory = True
                context = {'ProdForm':ProdForm,'NoTechCategory': noTechCategory, 'nocategory' : nocategory}
                return render(request, 'editsingleprod.html', context)
            else:
                cat = loadCategory(pk) # generating level 1 category
                attributes = ['id_product_code'] +  ['id_' + ele for ele in list(cat[0].values())[0]]
                ProdForm = editProductRecords(pk)
                TechForm = editTechDetails(pk)
                flag = False
                TwoCategories = True
                if len(cat) > 1: # check if 2 categories exists
                    attributes2 = ['id_' + ele for ele in list(cat[1].values())[0]]
                    merged_attrs = attributes + list(set(attributes2) - set(attributes))
                    context = {'ProdForm': ProdForm, 'TechForm': TechForm, 'flag': flag, 'cat1': list(cat[0].keys())[0], 
                                'cat2': list(cat[1].keys())[0], 'catflag': TwoCategories, 'attrs': merged_attrs}
                else: 
                    TwoCategories = False
                    context = {'ProdForm': ProdForm, 'TechForm': TechForm, 'flag': flag, 'cat1': list(cat[0].keys())[0],
                                'catflag': TwoCategories, 'attrs': attributes}
                return render(request, 'editsingleprod.html', context)
        except:
            flag = True
            return render(request, 'editsingleprod.html', {'msg': "Enter a valid product code", 'flag': flag})


def checkCategory(data, flag, cat1, cat2):
    """ Helper function for checking if there exists two level 1 categories for the same product! """
    indexList = [list(ele.keys())[0] for ele in data]
    if cat1 == cat2:
        flag = True
    if flag:
        index = indexList.index(cat1)
        return [data[index]]
    elif not flag:
        index1 = indexList.index(cat1)
        index2 = indexList.index(cat2)
        return [data[index1], data[index2], cat1, cat2]


def loadCategory(id, file='categories.json'):
    """ Helper function for fetching the categories from the DB! """
    obj1 = ProductRecords.objects.get(pk=id).category_1
    cat1_lev1 = NwCategoryLowestNodes.objects.get(pk=obj1).level1
    cat1 = NwCategoryIds.objects.get(pk=cat1_lev1).category_name
    obj2 = ProductRecords.objects.get(pk=id).category_2
    onlyOneCategory = False
    if obj2 != 0 and obj1 != obj2:
        cat2_lev1 = NwCategoryLowestNodes.objects.get(pk=obj2).level1
        cat2 = NwCategoryIds.objects.get(pk=cat2_lev1).category_name
    else:
        onlyOneCategory = True
        cat2 = "Null"
    f = open('myDatabase/' + file)
    data = json.load(f)
    categories = checkCategory(data, onlyOneCategory, cat1, cat2)
    return categories


def loadAttributes(data):
    """ Helper function for loading the attributes for every category! """
    if len(data) > 1:
        attrs1 = [i for i in list(data[0].values())[0]]
        attrs2 = [i for i in list(data[1].values())[0]]
        return [attrs1, attrs2, data[2], data[3]]
    else:
        attrs = [i for i in list(data[0].values())[0]]
        return [attrs]


def techRecords(request):
    """ Sub-function for generating technical records on Search Product page. Rendering is controlled by Ajax in main.js! """
    onlyOneCategory = True
    record_id = request.GET.get('record_id')
    categories = loadCategory(record_id)
    attrs = loadAttributes(categories)
    data = serializers.serialize("json", ProductRecordsTech.objects.filter(product_code=record_id))
    temp = json.loads(data)
    if len(attrs) == 1:
        data1 = {item: val for item, val in temp[0]['fields'].items() if item in attrs[0]}
        context = {'data1': data1, 'data2': None, 'flag': onlyOneCategory}
    else:
        onlyOneCategory = False
        data1 = {item: val for item, val in temp[0]['fields'].items() if item in attrs[0]}
        data2 = {item: val for item, val in temp[0]['fields'].items() if item in attrs[1]}
        context = {'data1': data1, 'data2': data2, 'flag': onlyOneCategory, 'cat_1': attrs[2], 'cat_2': attrs[3]}
    return JsonResponse(context)


def similarProducts(request, pk="3011-100"):
    """ Main Function for rendering the Similar Product page. 
    
    By default the page will render similar products to 3011-100. 
    This is done in order to connect both the POST and click request on search page.

    arguments:  request - Default Object for accepting the Http request made
                pk - The product for which similar products are to be fetched, by default it is "3011-100"
    """
    if request.method == "POST":
        prod_code = request.POST['prod_code']
        try:
            category = list(loadCategory(prod_code)[0].keys())[0]
            return categoryWiseProductSorting(category, prod_code, request)
        except NwCategoryLowestNodes.DoesNotExist:
            return setGeneralContext(request=request, msg='Categories do not exists.')
        except ProductRecords.DoesNotExist:
            return setGeneralContext(request=request, msg='Product does not exist, Enter valid Product Code.')
        except ProductRecordsTech.DoesNotExist:
            return setGeneralContext(request=request, msg='Product does not exist, Enter valid Product Code.')
    else:
        try:
            category = list(loadCategory(pk)[0].keys())[0]
            return categoryWiseProductSorting(category, pk, request)
        except NwCategoryLowestNodes.DoesNotExist:
            return setGeneralContext(request=request, msg='Categories do not exist!')


def setGeneralContext(request, msg='Gene ID not found!'):
    """ Helper Function for generating a default view when an error is encountered  """
    messages.warning(request, msg)
    obj = TechRecordsTable_Biorepository(NwAttributes11Biorepository.objects.filter(species='Just need to return a table'))
    context = {'obj': obj, 'num_of_prods': "-"}
    return render(request, "similarProducts.html", context) 


def innerQuery(pk):
    """ Helper function for generating a queryset to filter the DB based on Level 2 of Category 1.
    
    arguments: pk - Product code for which the similar products are being loaded
    
    """
    obj = ProductRecords.objects.get(pk=pk)
    level2 = NwCategoryLowestNodes.objects.get(pk=obj.category_1).level2
    inner_queryset = NwCategoryLowestNodes.objects.filter(level2=level2).values('lowest_node')
    return inner_queryset, level2


def TableBindings(request, pk, cat):
    """ Sub function for querying the DB when special criteria for filtering the products are not met.
    
    The func will filter the DB based on Level 2 of Categry 1 for the requested Product (pk). 
    Then, if the gene_ID is available for the product it'll further filter the DB based on gene_id o/w return it based on just the previous case.
    
    argument:   request - Object for extending the similarProduct function properly
                pk - Product code for which the similar products are being loaded
                cat - Category 1 of the concerned Product (pk)
    """
    inner_queryset, level2 = innerQuery(pk)
    Table_looker = { "Biorepository": [NwAttributes11Biorepository, TechRecordsTable_Biorepository],
                    "Molecular Biology": [NwAttributes12Molecularbiology, TechRecordsTable_Molecularbiology],
                    "Antibodies": [NwAttributes13Antibodies,TechRecordsTable_Antibodies],
                    "Proteins & Peptides": [NwAttributes14Proteinspeptides, TechRecordsTable_Proteinspeptides],
                    "Cells & Cell Culture": [NwAttributes15Cellscellculture, TechRecordsTable_CellsCellCulture],
                    "Reagents & Labware": [NwAttributes16Reagentslabware, TechRecordsTable_Reagentslabware],
                    "Kits & Assays": [NwAttributes17Kitsassays, TechRecordsTable_Kitsassays],
                    "Bioseparation & Electrophoresis": [NwAttributes18Bioseparationelectrophoresis, TechRecordsTable_Bioseparationelectrophoresis]}

    queryset_base = Table_looker[cat][0].objects.get(product_code=pk)
    lev = NwCategoryIds.objects.get(cat_id=int(level2)).category_name
    try:
        geneID = queryset_base.gene_id
        queryset_geneID = Table_looker[cat][0].objects.select_related('product_code').exclude(gene_id='').filter(product_code__category_1__in=inner_queryset, product_code__delete_flag=0, gene_id=geneID)
        obj = Table_looker[cat][1](queryset_geneID)
        filter_used = {'Gene ID': geneID}
        context = {'obj': obj, 'num_of_prods': queryset_geneID.count(), 'filter': filter_used}
        messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>'+ lev)
        return render(request, "similarProducts.html", context)
    except AttributeError:
        geneID = "N\\a"
        queryset_cat = Table_looker[cat][0].objects.select_related('product_code').filter(product_code__category_1__in=inner_queryset, product_code__delete_flag=0)[:1000]
        obj = Table_looker[cat][1](queryset_cat)
        filter_used = {'Gene ID': geneID}
        context = {'obj': obj, 'num_of_prods': queryset_cat.count(), 'filter': filter_used}
        messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>'+ lev)
        return render(request, "similarProducts.html", context)


def categoryWiseProductSorting(cat, pk, request):
    """ Sub Function for querying the DB based on special Cases. As discussed with James.
    
    If the conditions are met the DB is queried as defined by the respective queryset o/w TableBindings function is called. 
    
    arguments:  request - Object for extending the similarProduct function properly
                pk - Product code for which the similar products are being loaded
                cat - Category 1 of the concerned Product (pk)
    """
    if cat == "Biorepository":
        inner_queryset, level2 = innerQuery(pk)
        queryset_base = NwAttributes11Biorepository.objects.get(product_code=pk)
        species, tissue_type, disease = queryset_base.species, queryset_base.tissue_type, queryset_base.disease
        queryset = NwAttributes11Biorepository.objects.select_related('product_code').filter(species=species,
                                                                                            tissue_type=tissue_type, 
                                                                                            disease=disease,
                                                                                            product_code__category_1__in=inner_queryset, product_code__delete_flag=0)
        lev = NwCategoryIds.objects.get(cat_id=int(level2)).category_name
        obj = TechRecordsTable_Biorepository(queryset)
        context = {'obj': obj, 'num_of_prods': queryset.count(), 'filter': {'Species': species,'Tissue type': tissue_type, 'Disease': disease,}}
        messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>' + lev)
        return render(request, "similarProducts.html", context)
    elif cat == "Cells & Cell Culture":
        inner_queryset, level2 = innerQuery(pk)
        if  level2 in [129, 132]:
            queryset_base = NwAttributes15Cellscellculture.objects.get(product_code=pk)
            if level2 == 129:
                filter_used = {'Cell line': queryset_base.cell_line}
                queryset = NwAttributes15Cellscellculture.objects.select_related('product_code').exclude(cell_line='').filter(cell_line=queryset_base.cell_line, 
                                                                                                                            product_code__category_1__in=inner_queryset, 
                                                                                                                            product_code__delete_flag=0)
                lev = "Cell Lines"
            else:
                filter_used = {'Protein': queryset_base.protein}
                queryset = NwAttributes15Cellscellculture.objects.select_related('product_code').exclude(protein='').filter(protein=queryset_base.protein, 
                                                                                                                            product_code__category_1__in=inner_queryset, product_code__delete_flag=0)
                lev = "3D Cell Culture & Extracellular Matrices"
            obj = TechRecordsTable_CellsCellCulture(queryset)
            context = {'obj': obj, 'num_of_prods': queryset.count(), 'filter': filter_used}
            messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>'+ lev)
            return render(request, "similarProducts.html", context)
        else:
            return TableBindings(request, pk, cat)
    elif cat == "Reagents & Labware":
        inner_queryset, level2 = innerQuery(pk)
        if level2 in [137,138]:
            queryset_base = NwAttributes16Reagentslabware.objects.get(product_code=pk)
            if level2 == 137:
                filter_used = {'Cas Number': queryset_base.cas_no}
                queryset = NwAttributes16Reagentslabware.objects.select_related('product_code').exclude(cas_no='').filter(cas_no=queryset_base.cas_no,
                                                                                                                        product_code__category_1__in=inner_queryset, product_code__delete_flag=0)
                lev = 'Reagents & Consumables'
            else:
                filter_used = {'Carbohydrate Type': queryset_base.carbohydrate_type}
                queryset = NwAttributes16Reagentslabware.objects.select_related('product_code').exclude(carbohydrate_type='').filter(carbohydrate_type=queryset_base.carbohydrate_type, 
                                                                                                                                    product_code__category_1__in=inner_queryset, product_code__delete_flag=0)
                lev = 'Carbohydrates'
            obj = TechRecordsTable_Reagentslabware(queryset)
            context = {'obj': obj, 'num_of_prods': queryset.count(), 'filter': filter_used}
            messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>' + lev)
            return render(request, "similarProducts.html", context)
        else:
            return TableBindings(request, pk, cat)
    elif cat == "Proteins & Peptides":
        inner_queryset, level2 = innerQuery(pk)
        if level2 == 125:
            queryset_base = NwAttributes14Proteinspeptides.objects.get(product_code=pk)
            filter_used = {'Cell line': queryset_base.cell_line}
            queryset = NwAttributes14Proteinspeptides.objects.select_related('product_code').exclude(cell_line='').filter(cell_line=queryset_base.cell_line, 
                                                                                                                        product_code__category_1__in=inner_queryset, product_code__delete_flag=0)
            obj = TechRecordsTable_Proteinspeptides(queryset)
            context = {'obj': obj, 'num_of_prods': queryset.count(), 'filter': filter_used}
            messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>Cell Line Lysates')
            return render(request, "similarProducts.html", context)
        else:
            return TableBindings(request, pk, cat)
    else:
        return TableBindings(request, pk, cat)
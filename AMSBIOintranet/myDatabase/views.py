import json
import getpass
from datetime import datetime

from .forms import EditProductForm, EditTechDetailsForm
from .tables import CurrencyTable, ProductRecordsTable
from .models import (MasterCurrencies,
                     ProductRecords,
                     ProductRecordsTech,
                     NwCategoryIds,
                     NwCategoryLowestNodes,
                     DataOwners,
                     Currencies)

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.paginators import LazyPaginator


def index(request):
    return redirect('/')


def addNewSupplier(request):
    """ Main function for rendering the Add new Supplier page! """
    if request.method == "POST":
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
    RequestConfig(request, paginate={
                  "paginator_class": LazyPaginator, "per_page": 25}).configure(obj)
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
                description__icontains=desc)[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        elif len(desc) == 0 and len(code) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code)[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        else:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(description__icontains=desc)[:100])
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


def editSingleProduct(request):
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
            return render(request, 'editsingleprod.html', {'msg': "*Please enter a valid product code", 'flag': flag})

    return render(request, 'editsingleprod.html', {'msg': " ", 'flag': flag})


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


def loadCategory(id):
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
    f = open('myDatabase/categories.json')
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

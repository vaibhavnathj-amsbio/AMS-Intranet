import json
import getpass
from datetime import datetime

from .forms import EditProductForm, EditTechDetailsForm
from .tables import (CurrencyTable, ProductRecordsTable)
from .models import (MasterCurrencies, ProductRecords, ProductRecordsTech,
                        NwCategoryLowestNodes, DataOwners, Currencies)

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.paginators import LazyPaginator

from .utils import *
from .smlrProdsUtils import *


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
                description__icontains=desc).filter(delete_flag = 0)[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        elif len(desc) == 0 and len(code) > 0:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(delete_flag = 0)[:100])
            return render(request, 'search.html', {'obj': obj, 'msg': msg})
        else:
            # instance limit set to 100
            obj = ProductRecordsTable(ProductRecords.objects.filter(
                product_code__icontains=code).filter(description__icontains=desc).filter(delete_flag = 0)[:100])
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


def FormSubmit(request):
    """ Helper function for submitting a form! | Ajax Call """
    json_data = json.loads(request.POST['data'])
    form_data = {}
    for ele in json_data:
        temp = list(ele.values())
        form_data[temp[0]] = temp[1]
    form_data.pop('csrfmiddlewaretoken')
    if 'supplier_product_code' in form_data.keys():
        form_data['last_updated_user'] = getpass.getuser().upper()
        #form_data['last_updated_user'] = request.user.username
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
        except (ProductRecords.DoesNotExist, ProductRecordsTech.DoesNotExist):
            return setGeneralContext(request=request, msg='Product does not exist, Enter valid Product Code.')

    else:
        try:
            category = list(loadCategory(pk)[0].keys())[0]
            return categoryWiseProductSorting(category, pk, request)
        except NwCategoryLowestNodes.DoesNotExist:
            return setGeneralContext(request=request, msg='Categories do not exist!')

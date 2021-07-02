import json

from django.core import serializers
from django.http.response import JsonResponse
from myDatabase.models import NwCategoryIds, NwCategoryLowestNodes
from .forms import *


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

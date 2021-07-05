from .models import *
from .tables import *


from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render


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

    lev = NwCategoryIds.objects.get(cat_id=int(level2)).category_name
    try:
        geneID = CodeToGeneId.objects.get(product_code=pk).gene_id
        queryset_geneID = Table_looker[cat][0].objects.select_related('product_code').exclude(gene_id='').filter(product_code__category_1__in=inner_queryset, product_code__delete_flag=0, gene_id=geneID)
        obj = Table_looker[cat][1](queryset_geneID)
        gene_info = NcbiGeneInfo.objects.get(gene_id=geneID)
        filter_used = {'Gene ID': geneID, 'Gene Symbol': gene_info.gene_symbol, 'Gene Description': (gene_info.gene_description)}
        context = {'obj': obj, 'num_of_prods': queryset_geneID.count(), 'filter': filter_used}
        messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>'+ lev)
        return render(request, "similarProducts.html", context)
    except NcbiGeneInfo.DoesNotExist:
        geneID = Table_looker[cat][0].objects.get(product_code=pk).gene_id
        queryset_geneID = Table_looker[cat][0].objects.select_related('product_code').exclude(gene_id='').filter(product_code__category_1__in=inner_queryset, product_code__delete_flag=0, gene_id=geneID)
        obj = Table_looker[cat][1](queryset_geneID)
        gene_info = NcbiGeneInfo.objects.get(gene_id=geneID)
        filter_used = {'Gene ID': geneID, 'Gene Symbol': gene_info.gene_symbol, 'Gene Description': (gene_info.gene_description)}
        context = {'obj': obj, 'num_of_prods': queryset_geneID.count(), 'filter': filter_used}
        messages.success(request, 'Showing Products similar to Product code: ' + pk + ' in ' + cat + '>>'+ lev)
        return render(request, "similarProducts.html", context)
    except (AttributeError, ObjectDoesNotExist):
        geneID = "N\\A"
        queryset_cat = Table_looker[cat][0].objects.filter(product_code__category_1__in=inner_queryset, product_code__delete_flag=0, gene_id=geneID).exclude(gene_id='')[:1000]
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
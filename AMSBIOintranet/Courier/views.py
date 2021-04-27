from django.shortcuts import render, redirect

def index(request):
    return redirect('/')

def fedexUK(request):
    return render(request, 'fedex_UK.html')

def fedexUSA(request):
    return render(request, 'fedex_USA.html')


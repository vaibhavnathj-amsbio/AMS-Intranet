from django.shortcuts import render, redirect

def index(request):
    return redirect('/')

def orderdetails(request):
    return render(request, 'orderdetails.html')


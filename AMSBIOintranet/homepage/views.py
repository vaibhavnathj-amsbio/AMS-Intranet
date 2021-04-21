from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if request.method == "POST":
        return redirect(request, 'index.html')
    else:
        return render(request, 'index.html')
from django.shortcuts import render,redirect




# Create your views here.

def home(request):
    
    return render(request,'index.html',locals())


def about(request):
    
    return render(request,'about.html',locals())




from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req,template_name='index.html')

def about(req):
    return render(req,template_name='about.html')

def contacts(req):
    return render(req,template_name='contacts.html')
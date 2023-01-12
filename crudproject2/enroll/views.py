from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StudentRegistration
from .models import User

# Create your views here.
def add_data(request):
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            nm=fm.cleaned_data['name']
            em=fm.cleaned_data['email']
            pw=fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            fm = StudentRegistration()
    else:
        fm = StudentRegistration()
    stud = User.objects.all()
    return render(request,'addinformation.html',{'form':fm})


def show_data(request):
    stud = User.objects.all()
    return render(request,'showinformation.html',{ 'stu':stud})


def delete_data(request,id):
    if request.method == 'POST':
        deleteData = User.objects.get(pk=id)
        deleteData.delete()
        return HttpResponseRedirect('/showinfo')

def update_data(request, id):
    if request.method == "POST":
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(instance=pi)
    return render(request,'updateinformation.html',{'form':fm})    
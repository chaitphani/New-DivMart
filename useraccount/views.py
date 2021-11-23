from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework import generics
from rest_framework import serializers

from .models import *
from useraccount.models import *


def common_login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        user = auth.authenticate(username=username, password=password)
        if user:
            # login_user = LoginUser.objects.filter(user=user)
            # if len(login_user) > 0:
            #     print('login user role-------', login_user[0].role)
            if user.is_superuser:
                auth.login(request,user)
                return redirect('home')
            elif not user.is_superuser:
                auth.login(request,user)
                return redirect('/dashboard/pos/add')
            else:
                return render(request,'useraccount/admin_login.html',{'error':'Please Enter Valid Credentials'})
        else:
            return render(request,'useraccount/admin_login.html',{'error1':'Invalid Login Credentials'})
    else:
        context_data={'u':User.objects.all()}
        return render(request,'useraccount/admin_login.html',context_data)


def admin_logout(request):
    auth.logout(request)
    return redirect("common_login")


# def cashier_logout(request):
#     auth.logout(request)
#     return redirect("common_login")


# def admin_signup(request):
#     if request.method == 'POST':
#         if request.POST.get("pwd1") == request.POST.get("pwd2"):
#             try:
#                 usr = User.objects.get(username=request.POST.get('username'))
#                 return render(request,'useraccount/admin_signup.html',{'error':"Username has been already taken"})
#             except User.DoesNotExist:
#                 email = request.POST.get('email')
#             try:
#                 usr_email = AdminUser.objects.get(email=request.POST.get('email'))
#                 return render(request,'useraccount/admin_signup.html',{'errore':"email already exists"})
#             except:
#                 pass
#                 user = User.objects.create_user(username=request.POST['username'],password=request.POST['pwd1'],email= request.POST.get('email'),is_superuser=True,is_staff=True)
#                 username = request.POST.get('username')
#                 fname = request.POST.get('fname')
#                 lname = request.POST.get('lname')
#                 email = request.POST.get('email')
#                 password  = request.POST.get('pwd1')
#                 conform_password = request.POST.get('pwd2')
#                 phone = request.POST.get('phone')
#                 address = request.POST.get('address')
#                 id_proof_front = request.FILES.get('idfront')
#                 id_proof_back = request.FILES.get('idback')
#                 r_obj = Role.objects.get(title="Admin")
#                 user_obj = AdminUser(user_id=user.id,username=username,password=password,first_name=fname,last_name=lname,id_proof_front=id_proof_front,id_proof_back=id_proof_back,email=email,permanent_address=address,mobile=phone,role=r_obj)
#                 user_obj.save()
#                 return redirect('admin_login')
#         else:
#             return render(request,'useraccount/admin_signup.html',{'mismatch':"Password Did't Match"})
#     return render(request,'useraccount/admin_signup.html')


# def cashier_signup(request):
#     if request.method == 'POST':
#         if request.POST.get("pwd1") == request.POST.get("pwd2"):
#             try:
#                 usr = User.objects.get(username=request.POST.get('username'))
#                 return render(request,'useraccount/cashier_signup.html',{'error':"Username has been already taken"})
#             except User.DoesNotExist:
#                 email = request.POST.get('email')
#             try:
#                 usr_email = StaffUser.objects.get(email=request.POST.get('email'))
#                 return render(request,'useraccount/cashier_signup.html',{'errore':"email already exists"})
#             except:
#                 pass
#                 user = User.objects.create_user(username=request.POST['username'],password=request.POST['pwd1'],email= request.POST.get('email'),is_staff=True)
#                 username = request.POST.get('username')
#                 fname = request.POST.get('fname')
#                 lname = request.POST.get('lname')
#                 email = request.POST.get('email')
#                 password  = request.POST.get('pwd1')
#                 conform_password = request.POST.get('pwd2')
#                 phone = request.POST.get('phone')
#                 address = request.POST.get('address')
#                 id_proof_name = request.FILES.get('idfront')
#                 id_proof_number = request.FILES.get('idback')
#                 cash_obj = StaffUser(user_id=user.id,username=username,password=password,first_name=fname,last_name=lname,id_proof_name=id_proof_name,id_proof_number=id_proof_number,email=email,permanent_address=address,mobile=phone,role="C")
#                 cash_obj.save()
#                 return redirect('cashier_login')
#         else:
#             return render(request,'useraccount/cashier_signup.html',{'mismatch':"Password Did't Match"})
#     return render(request,'useraccount/cashier_signup.html')

# def cashier_login(request):
#     if request.method == "POST":
#         username = request.POST['uname']
#         password = request.POST['pwd']
#         user = auth.authenticate(username=username,password=password)
#         if user is not None:
#             if user.is_staff:
#                 auth.login(request,user)
#                 return redirect('cashier_dashboard')
#             else:
#                 return render(request,'useraccount/cashier_login.html',{'error':'You are not authenticated as admin'})

#         else:
#             return render(request,'useraccount/cashier_login.html',{'errori':'Invalid Login Credentials'})
#     return render(request,'useraccount/cashier_login.html')


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__' 

class ContentTypeView(generics.ListCreateAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    

class PermissionsView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
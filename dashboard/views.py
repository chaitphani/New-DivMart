from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.checks import messages
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, F, Q, Count, aggregates
from django.http import HttpResponse,JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse
from django_filters.filters import DateRangeFilter

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

import os
import csv, io
import barcode
import requests
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw,ImageFont

from .forms import *
from sale.models import *
from dashboard.models import *
from membership.models import *
from useraccount.models import *
from div_settings.models import *


from itertools import groupby
from dateutil.relativedelta import relativedelta

@login_required(login_url='/useraccount/common_login')
def home(request):

    today_date = datetime.datetime.now()

    if request.method == 'POST':
        today = request.POST.get('today')
        week = request.POST.get('week')
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        if today != None:
            purchase_total = Purchase_info.objects.filter(status=True, purchase_date__day=today_date.day, purchase_date__month=today_date.month, purchase_date__year=today_date.year)\
                .aggregate(Sum('purchase_total'))['purchase_total__sum']

            sales_total = Sell.objects.filter(status='F', sale_date__day=today_date.day, sale_date__month=today_date.month, sale_date__year=today_date.year, is_deleted=False)\
                .aggregate(Sum('total_payable'))['total_payable__sum']

            purchase_due = Purchase_info.objects.filter(status=True, purchase_date__day=today_date.day, purchase_date__month=today_date.month, purchase_date__year=today_date.year)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

            sales_due = Sell.objects.filter(status='F', sale_date__day=today_date.day, sale_date__month=today_date.month, sale_date__year=today_date.year, is_deleted=False)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

        elif week != None:

            purchase_total = Purchase_info.objects.filter(status=True, purchase_date__date__week=datetime.date.today().isocalendar()[1])\
                .aggregate(Sum('purchase_total'))['purchase_total__sum']

            sales_total = Sell.objects.filter(status='F', sale_date__date__week=datetime.date.today().isocalendar()[1], is_deleted=False)\
                .aggregate(Sum('total_payable'))['total_payable__sum']

            purchase_due = Purchase_info.objects.filter(status=True, purchase_date__date__week=datetime.date.today().isocalendar()[1])\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

            sales_due = Sell.objects.filter(status='F', sale_date__date__week=datetime.date.today().isocalendar()[1], is_deleted=False)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

        elif month != None:

            purchase_total = Purchase_info.objects.filter(status=True, purchase_date__month=today_date.month, purchase_date__year=today_date.year)\
                .aggregate(Sum('purchase_total'))['purchase_total__sum']

            sales_total = Sell.objects.filter(status='F', sale_date__month=today_date.month, sale_date__year=today_date.year, is_deleted=False)\
                .aggregate(Sum('total_payable'))['total_payable__sum']

            purchase_due = Purchase_info.objects.filter(status=True, purchase_date__month=today_date.month, purchase_date__year=today_date.year)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

            sales_due = Sell.objects.filter(status='F', sale_date__month=today_date.month, sale_date__year=today_date.year, is_deleted=False)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

        elif year != None:
            purchase_total = Purchase_info.objects.filter(status=True, purchase_date__year=today_date.year)\
                .aggregate(Sum('purchase_total'))['purchase_total__sum']

            # today_date = today_date - timedelta(days=30)
            sales_total = Sell.objects.filter(status='F', sale_date__year=today_date.year)\
                .aggregate(Sum('total_payable'))['total_payable__sum']

            purchase_due = Purchase_info.objects.filter(status=True, purchase_date__year=today_date.year)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

            sales_due = Sell.objects.filter(status='F', sale_date__year=today_date.year)\
                .aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']  

    else:
        purchase_total = Purchase_info.objects.filter(status=True).aggregate(Sum('purchase_total'))['purchase_total__sum']
        sales_total = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('total_payable'))['total_payable__sum']
        purchase_due = Purchase_info.objects.filter(status=True).aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']
        sales_due = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']

    revenue_total = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('payment_info__amount'))
    cost_total = Purchase_info.objects.filter(status=True).aggregate(Sum('payment_info__amount'))

    return render(request, 'divmart_dashboard/home.html', {
        'purchase':purchase_total, 'sales':sales_total, 'purchase_due':purchase_due, 'sales_due':sales_due,
        'revenue_total':revenue_total, 'cost_total':cost_total})


######### for user listing (admin and cashier) ###########################
@login_required(login_url='/useraccount/common_login')
def user(request):
    staff_users = StaffUser.objects.all()
    return render(request, 'divmart_dashboard/user.html',{"users":staff_users})


@login_required(login_url='/useraccount/common_login')
def user_detail(request, id):

    staff_user = StaffUser.objects.get(id=id)
    return render(request,'divmart_dashboard/user_view.html',{'usr':staff_user,'rol':staff_user.role})


@login_required(login_url='/useraccount/common_login')
def user_delete(request, id):

    if AdminUser.objects.filter(id=id).exists():
        adm_obj = AdminUser.objects.get(id=id)
        adm_obj.is_deleted = 1
        adm_obj.save()
    elif StaffUser.objects.filter(id=id).exists():
        cash_obj = StaffUser.objects.get(id=id)
        cash_obj.is_deleted = 1
        cash_obj.save()
    return redirect('user')


@login_required(login_url='/useraccount/common_login')
def user_edit(request,id):

    staff_user = StaffUser.objects.get(id=id)
    r_obj = Role.objects.get(id=staff_user.role.id)

    if request.method == "POST":
        entered_role = request.POST.get("role")
        prefix = request.POST.get('Prefix')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        contact = request.POST.get('contact')
        location = request.POST.get('business_location')
        id_proof_front = request.FILES.get('id_proof_front')
        id_proof_back = request.FILES.get('id_proof_back')
        guardain_name= request.POST.get('guardian_name')
        per_address = request.POST.get("permanent_address")
        curr_address = request.POST.get("current_address")
        acc_holder_name = request.POST.get("account_holder_name")
        acc_num = request.POST.get("account_no")
        bank_name = request.POST.get("bank_name")
        branch = request.POST.get("branch")
        taxpid = request.POST.get("tax_payer_id")   
        bank_identifier_code = request.POST.get("bank_identifier_code")

        # if entered_role == "Admin":
        #     r_obj = Role.objects.get(title="Admin")
        #     AdminUser.objects.filter(id=id).update(Prefix= prefix,first_name=fname,last_name=lname,id_proof_front=id_proof_front,id_proof_back=id_proof_back,permanent_address=per_address,current_address=curr_address,mobile=mobile,role=r_obj,account_holder_name=acc_holder_name,account_number=acc_num,bank_name=bank_name,branch=branch,tax_payer_id=taxpid,guardian_name=guardain_name,bank_identifier_code=bank_identifier_code)
        #     return redirect('user')
        # else:
        StaffUser.objects.filter(id=id).update(Prefix= prefix,first_name=fname,last_name=lname,id_proof_front=id_proof_front,id_proof_back=id_proof_back,permanent_address=per_address,current_address=curr_address,mobile=mobile,role=r_obj,account_holder_name=acc_holder_name,account_number=acc_num,bank_name=bank_name,branch=branch,tax_payer_id=taxpid,guardian_name=guardain_name,bank_identifier_code=bank_identifier_code, business_location=location)
        return redirect('user')
    
    business_location = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/admin_user_edit.html',{'usr':staff_user,'rol':staff_user.role, 'locations':business_location})


def sales_commission_agent(request):
    return render(request, 'sales_commissiona_gents.html')


def admin_user_creation(request):
    main_role = Role.objects.all()
    if request.method == 'POST':

        try:
            usr = User.objects.get(username=request.POST.get('username'))
            return render(request,'divmart_dashboard/admin_user_creation.html',{'error':"Username has been already taken"})
        except User.DoesNotExist:
            email = request.POST.get('email')

        try:
            usr_email = AdminUser.objects.get(email=request.POST.get('email'))
            return render(request,'divmart_dashboard/admin_user_creation.html',{'errore':"email already exists"})
        except:
            pass

        entered_role = request.POST.get("role")
        prefix = request.POST.get('prefix')
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password  = request.POST.get('password1')
        conform_password = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        contact = request.POST.get('contact')
        id_proof_front = request.FILES.get('id_proof_front')
        id_proof_back = request.FILES.get('id_proof_back')
        guardain_name= request.POST.get('guardian_name')
        b_day =  request.POST.get('birth_date')
        location = request.POST.get('business_location')
        per_address = request.POST.get("permanent_address")
        curr_address = request.POST.get("current_address")
        acc_holder_name = request.POST.get("account_holder_name")
        acc_num = request.POST.get("account_no")
        bank_name = request.POST.get("bank_name")
        branch = request.POST.get("branch")
        taxpid = request.POST.get("tax_payer_id")   
        bank_identifier_code = request.POST.get("bank_identifier_code")
        location = BusinessLocation.objects.get(id=location)

        r_obj = Role.objects.get(title=entered_role)
        if entered_role == "Admin":
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email= request.POST.get('email'),is_superuser=True,is_staff=True)

                user_obj = AdminUser.objects.create(user=user,Prefix= prefix,username=username,password=password,first_name=fname,last_name=lname,id_proof_front=id_proof_front,id_proof_back=id_proof_back,email=email,permanent_address=per_address,current_address=curr_address,mobile=mobile,role=r_obj,account_holder_name=acc_holder_name,account_number=acc_num,bank_name=bank_name,branch=branch,tax_payer_id=taxpid,guardian_name=guardain_name,bank_identifier_code=bank_identifier_code, business_location=location)
                user_obj.save()
            except Exception as e:
                usercreated = User.objects.last()
                usercreated.delete()
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email= request.POST.get('email'),is_staff=True)

                user_obj = StaffUser.objects.create(user=user,Prefix= prefix,username=username,password=password,first_name=fname,last_name=lname,id_proof_front=id_proof_front,id_proof_back=id_proof_back,email=email,permanent_address=per_address,current_address=curr_address,mobile=mobile, role=r_obj,account_holder_name=acc_holder_name,account_number=acc_num,bank_name=bank_name,branch=branch,tax_payer_id=taxpid,guardian_name=guardain_name,bank_identifier_code=bank_identifier_code,business_location=location)
                user_obj.save()
            except Exception as e:
                usercreated = User.objects.last()
                usercreated.delete()

        messages.success(request, 'User create success...')
        return redirect('user')
    
    business_location = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/admin_user_creation.html',{'main_role':main_role, 'locations':business_location})  


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class RoleView(APIView):

    @method_decorator(login_required(login_url='/useraccount/common_login'))
    def get(self, request):
        cont_obj = ContentType.objects.filter(status=1)
        resp = {}

        for each in cont_obj:
            resp[each.app_label]=[]
            per_obj = each.permission_set.all()

            for each_perm in per_obj:
                resp[each.app_label].append(each_perm.permit)

        return render(request,'divmart_dashboard/add_role.html',{'per_obj':resp})

    @method_decorator(login_required(login_url='/useraccount/common_login'))
    def post(self,request,*args,**kwargs):

        if request.method == "POST":
            role_name = request.POST.get("role")
            req_data_ser = RoleSerializer(data={'title':role_name})

            if(req_data_ser.is_valid()):
                # try:
                r_obj = Role.objects.create(title=role_name)
                content = request.POST.get('content_type')
                for k, v in request.POST.items():
                    key_con  = k.split('#')
                    if v == "on":
                        p_obj = Permission.objects.get(permit=key_con[0], content_type__app_label=key_con[1])
                        r_obj.permissions_provided.add(p_obj)
                messages.success(request, role_name + ' Role create success...')
                return redirect("roles")
                # except:
                #     pass
                #     return redirect('add_role')
            return Response(req_data_ser.errors,status=422)


class RoleUpdateView(APIView):

    @method_decorator(login_required(login_url='/useraccount/common_login'))
    def get(self, request, id, *args, **kwargs):

        per_all_obj = Permission.objects.all()
        cont_obj = ContentType.objects.filter(status=1)
        resp = {}
        r = Role.objects.get(id=id)
        list_per = r.permissions_provided.all()
        final_list = {'id': int(id), 'data':[]}

        list_per_list = list(map(lambda x:x.id,list_per))
        for each in cont_obj:
            per_obj = each.permission_set.all()
            if(len(per_obj)>0):
                resp[each.app_label]=[]
                for each_perm in per_obj:
                    temp = {'per_obj': each_perm}
                    if(each_perm.id in list_per_list):
                        temp['status'] = 1
                        final_list['data'].append(temp)
                        resp[each.app_label].append({'permit':each_perm.permit,'status':1})
                    else:
                        temp['status'] = 0
                        final_list['data'].append(temp)
                        resp[each.app_label].append({'permit':each_perm.permit,'status':0})
                    # resp[each.app_label].append(each_perm.permit)
        return render(request,'divmart_dashboard/add_role.html',{'r':r,'per_obj':per_all_obj,'list_per':list_per, 'final_list': final_list,'resp':resp})
    
    @method_decorator(login_required(login_url='/useraccount/common_login'))
    def post(self,request,id,*args,**kwargs):

        # try:
        role_obj = Role.objects.get(id=id)
        role_obj.title = request.data.get('role')

        already_existed_permissions = list(map(lambda x:x.id, role_obj.permissions_provided.all()))
        new_permissions=[]
        role_obj.save()
        for k,v in request.POST.items():
            key_con = k.split('#')
            if v == "on":
                p_obj = Permission.objects.get(permit=key_con[0], content_type__app_label=key_con[1])
                new_permissions.append(p_obj.id)
                if(p_obj.id not in already_existed_permissions):
                    role_obj.permissions_provided.add(p_obj)
        for each in already_existed_permissions:
            if(each not in new_permissions):
                role_obj.permissions_provided.remove(Permission.objects.get(id=each))

        # return self.get(request,id)
        messages.success(request, role_obj.title + ' updated success...')
        return redirect('roles')

        # except Exception as e:
        #     return Response("something went wrong",status=422)


@login_required(login_url='/useraccount/common_login')
def roles(request):
    main_role = Role.objects.filter(is_deleted=0).order_by('-id')
    return render(request,'divmart_dashboard/roles.html',{'main_role':main_role})  


@login_required(login_url='/useraccount/common_login')
def role_deletion(request,id):

    r_obj = Role.objects.get(id=id)
    r_obj.is_deleted = 1
    r_obj.save()

    messages.success(request, r_obj.title + ' remove success...')
    return redirect('roles')
    

# def add_role(request):
#     per_obj = Permission.objects.all()
#     if request.method == "POST":
#         role_name = request.POST.get("role")
#         r_obj = Role.objects.create(title=role_name)
#         for k,v in request.POST.items():
#             if v == "on":
#                 p_obj = Permission.objects.get(permit=k)
#                 r_obj.permissions_provided.add(p_obj)
#                 return redirect("roles")
#     return render(request,'divmart_dashboard/add_role.html',{'per_obj':per_obj})


# def edit_role(request,id):
#     per_obj = Permission.objects.all()
#     r = Role.objects.get(id=id)
#     list_per = r.permissions_provided.through.objects.all()
#     # final_list = {'id': id, 'data':[]}
#     # for p in per_obj:
#     #     temp = {'per_obj': p}
#     #     if list_per:
#     #         for l in list_per:
#     #             if l.permission_id == p.id:
#     #                 temp['status'] = 1
#     #     final_list['data'].append(temp)

#     # if request.method == "POSt":
#     #     for k,v in request.POST.items():
#     #         if v == "on":
                
#     return render(request,'divmart_dashboard/add_role.html',{'r':r,'per_obj':per_obj,'list_per':list_per, 'final_list': final_list})


@login_required(login_url='/useraccount/common_login')
def add_new_product(request):
    
    unit = Units.objects.filter(status=True)
    brand = Brand.objects.filter(status=True)
    cat = Category.objects.filter(status=True)
    sub_cat = SubCategory.objects.filter(status=True)
    tax_rates = TaxRate.objects.filter(status=True)
    business_location = BusinessLocation.objects.filter(status=True)

    if request.method == 'POST':
        prod_obj = Product.objects.create(product_name=request.POST['product_name'], business_location=BusinessLocation.objects.get(id=request.POST['business_location']), brand=Brand.objects.get(id=request.POST['brand']), unit=Units.objects.get(id=request.POST['unit']), category=Category.objects.get(id=request.POST['category']), sub_category=SubCategory.objects.get(id=request.POST['sub_category']), SKU=request.POST['SKU'], barcode_type='EAN13', alert_quantity=request.POST['alert_quantity'], Product_description=request.POST['Product_description'], product_image=request.FILES['product_image'], weight=request.POST['weight'], applicable_tax=TaxRate.objects.get(rate=request.POST['applicable_tax']), product_type=request.POST['product_type'], sale_mrp=request.POST['sale_mrp'], purchase_price_exc_tax=request.POST['purchase_price_exc_tax'], purchase_price_inc_tax=request.POST['purchase_price_inc_tax'], margin=request.POST['margin'], status=True, selling_price_exc_tax=request.POST['selling_price_exc_tax'])

        prod_obj.selling_price = prod_obj.selling_price_exc_tax
        prod_obj.purchase_price = prod_obj.purchase_price_inc_tax
        prod_obj.prod_mrp = prod_obj.purchase_price_exc_tax
        prod_obj.save()

    #     form = ProductForm(request.POST)
    #     if form.is_valid():
    #         form_save = form.save(commit=False)
    #         form_save.status=True
    #         form_save.barcode_type = 'EAN13'
    #         form_save.selling_price = form_save.selling_price_exc_tax
    #         form_save.purchase_price = form_save.purchase_price_inc_tax
    #         form_save.save()
    #         return redirect('list_products')
    # else:
    #     form = ProductForm()
    
    return render(request,'divmart_dashboard/add_new_product.html',{'unit':unit,'brand':brand,'cat':cat,'sub_cat': sub_cat, 'rates':tax_rates,'business_location':business_location})  


@login_required(login_url='/useraccount/common_login')
def purchase_return_api(request,product_name):
    purhase_item = Purchase.objects.filter(product_name__product_name=product_name)
    data = {'x':0}
    return JsonResponse(data)


@login_required(login_url='/useraccount/common_login')
def add_purchase_return(request):
    return render(request,'divmart_dashboard/add_purchase_return.html') 


############### supplier user listing ################
@login_required(login_url='/useraccount/common_login')
def list_supplier(request):
    supplier_user = SupplierUser.objects.all()
    business_location = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/list_supplier.html',{'supplier_user':supplier_user, 'locations':business_location})
    

#############3 not done yet ##############3333
@login_required(login_url='/useraccount/common_login')
def supplier_detail(request,id):
    if SupplierUser.objects.filter(id=id).exists():
        sup = SupplierUser.objects.get(id=id)

    return render(request,'divmart_dashboard/supplier_detail.html',{'sup':sup}) 


@login_required(login_url='/useraccount/common_login')
def supplier_edit(request, id):
    sup = SupplierUser.objects.get(id=id)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        business_name = request.POST.get("business_name")
        contact_id = request.POST.get("contact_id")
        tax_number = request.POST.get("tax_number")
        opening_balance = request.POST.get("opening_balance")
        pay_term = request.POST.get("pay_term")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        Landline = request.POST.get("Landline")
        alternative_contact = request.POST.get("alternative_contact")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        land_mark = request.POST.get("land_mark")

        SupplierUser.objects.filter(id=id).update(first_name=first_name, business_name=business_name, contact_id=contact_id, tax_number=tax_number, opening_balance=opening_balance, pay_term=pay_term,email=email, mobile=mobile, alternative_contact=alternative_contact, Landline=Landline, city=city, state=state, country=country, land_mark=land_mark)
        return redirect('list_supplier')
    return render(request,'divmart_dashboard/supplier_edit.html',{'sup':sup})


@login_required(login_url='/useraccount/common_login')
def supplier_delete(request,id):
    if  SupplierUser.objects.filter(id=id).exists():
        sup_obj =  SupplierUser.objects.get(id=id)
        sup_obj.is_deleted = 1
        sup_obj.save()
    return redirect('list_supplier')


@login_required(login_url='/useraccount/common_login')
def customer_list(request):
    try:
        staff_user = StaffUser.objects.get(user=request.user)
        customer_user = CustomerUser.objects.filter(is_deleted=0, business_location=staff_user.business_location)
    except:
        staff_user = ''
        customer_user = CustomerUser.objects.filter(is_deleted=0)

    customer_group = CustomerGroups.objects.filter(is_deleted=0)
    business_location = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/customer_list.html',{'customer_user':customer_user,'customer_group': customer_group, 'locations':business_location})


@login_required(login_url='/useraccount/common_login')
def delete_customer_group(request,id):
    if  CustomerGroups.objects.filter(id=id).exists():
        cg_obj =  CustomerGroups.objects.get(id=id)
        cg_obj.is_deleted = 1
        cg_obj.save()
    return redirect('customer_group_detail')


@login_required(login_url='/useraccount/common_login')
def import_contact(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        # result_list = []
        # title_headers = []
        # int_blacklist = ['id']
        # float_blacklist = []
        with open(csv_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
    #         line_count = 0
            for row in csv_reader:
                print(row)
#             temp = {}
    #             if line_count == 0:
    #                 title_headers = row
    #             else:
    #                 for i in range(len(row)):
    #                     if title_headers[i] in int_blacklist:
    #                         temp[title_headers[i]] = int(row[i])
    #                     else:
    #                         temp[title_headers[i]] = row[i]
    #             line_count += 1
    #             result_list.append(temp)
    # return result_list
    return render(request,'divmart_dashboard/import_contact.html')


def bar_code_generator(product, price, name_choice, busniness_name_choice, product_price, request):

    bar_fil = Barcode_storage.objects.filter(barcode_type="ean13").filter(product_name__product_name=product)

    if bar_fil:
        b_no = bar_fil[0].barcode_no
        file_name = f"media/barcode_preview/combine_image{b_no}.png"
        if os.path.isfile(file_name):
            image_path = os.path.join(settings.BASE_DOMAIN, f"media/barcode_preview/combine_image{b_no}.png")
            return image_path
            # if image_path:
            #     business_name = BusinessLocation.objects.first().name
            #     retun_image_1 = Image.open(f"media/barcode_preview/combine_image{b_no}.png")
            #     draw = ImageDraw.Draw(retun_image_1)
            #     text = ''
            #     if busniness_name_choice == 'on':
            #         sz1 = ImageFont.truetype('arial.ttf', 14)
            #         draw.text((95,30), business_name, font = sz1,align ="center", fill=(0,0,0))
            #     else:
            #         sz1 = ImageFont.truetype('arial.ttf', 14)
            #         draw.text((95,30), '', font = sz1,align ="center", fill=(0,0,0))

            #     if name_choice == None or name_choice == '' or name_choice != 'on':
            #         sz2 = ImageFont.truetype('gotu.ttf', 20)
            #         draw.text((60,44), text, font = sz2,)

            #     elif name_choice == 'on':
            #         sz2 = ImageFont.truetype('gotu.ttf', 20)
            #         draw.text((60,44), product, font = sz2, align ="center", fill=(0,0,0))

            #     if product_price == 'on':
            #         sz3 = ImageFont.truetype('arial.ttf', 13)
            #         draw.text((88,120), price, font = sz3, fill=(0,0,0))
            #     else:
            #         sz3 = ImageFont.truetype('arial.ttf', 13)
            #         draw.text((88,120), '', font = sz3, fill=(0,0,0))

            #     retun_image_1.save(f"media/barcode_preview/combine_image{b_no}.png")
            #     image_path = os.path.join(settings.BASE_DOMAIN, f"media/barcode_preview/combine_image{b_no}.png")
            #     return image_path

    else:
        price = f"Price:{str(price)}"
        try:
            barcode_number = Barcode_storage.objects.filter(barcode_type="ean13").last().barcode_no
        except:
            barcode_number = '978025647962'

        ########## blank image #############
        # img = Image.new("RGB", (280, 180), (255, 255, 255))
        # img.save("blank_sheet1.png", "PNG")
        ############## barcode_image ########
        try:
            number = int(barcode_number) + 1
            barcode_no = str(number)
            barcode_type = "ean13"
            EAN = barcode.get_barcode_class(barcode_type)
            ean = EAN(barcode_no, writer=ImageWriter())
            barcode_image = f'media/barcodes/barcode{barcode_no}'
            # ean.save(barcode_image,options={'text_distance':0.4, 'dpi':150})

            ean.save(barcode_image, options={"font_size":6, 'text_distance':0.5, 'module_height':7, 'dpi':150, "module_width":0.25})
        except Exception as e:
            messages.error(request, e)

        ################ combined_image ########
        try:
            im1 = Image.open('blank_sheet1.png')
            im2 = Image.open(f"media/barcodes/barcode{barcode_no}.png")
            im1.paste(im2,(15,61))
            im1.save(f"media/barcode_preview/combine_image{barcode_no}.png")
        except Exception as e:
            messages.error(request, e)
        ############# text_writing  ######################
        # product = "Nirma Soap"
        try:
            business_name = BusinessLocation.objects.first().name
        except Exception as e:
            print('---exception from business location---', e)
            business_name = 'NA'
        text_write = Image.open(f"media/barcode_preview/combine_image{barcode_no}.png")

        draw = ImageDraw.Draw(text_write)
        if busniness_name_choice == 'on':
            sz1 = ImageFont.truetype('arial.ttf', 14)
            draw.text((95,30), business_name, font = sz1,align ="center", fill=(0,0,0))
        if name_choice == 'on':
            sz2 = ImageFont.truetype('gotu.ttf', 20)
            draw.text((60,44), product, font = sz2, align ="center", fill=(0,0,0))
        if product_price == 'on':
            sz3 = ImageFont.truetype('arial.ttf', 13)
            draw.text((88,120), price, font = sz3, fill=(0,0,0))

        text_write.save(f"media/barcode_preview/combine_image{barcode_no}.png")

        p_obj = Product.objects.get(product_name=product)
        bar_obj = Barcode_storage(barcode_type ="ean13", product_name = p_obj, barcode_no=barcode_no)
        bar_obj.save()

        image_path = os.path.join(settings.BASE_DOMAIN, f"media/barcode_preview/combine_image{barcode_no}.png")
        return image_path


def svg_label_generator():

    barcode_type = 'code128'
    EAN = barcode.get_barcode_class(barcode_type)

    unique_number = '59012888888888'
    business_name = 'business_name'
    product_name = 'product_name'
    product_price = '25'

    names = [unique_number, business_name, product_name,product_price]
    nl = '\n'
    ean = EAN(f"{nl}{nl.join(names)}")

    svg_file = ean.save('media/product1')

    # with open('media/product1.xml', 'r') as f: 
    # data = f.read() 
    # bs_data = BeautifulSoup(data, 'xml') 
    # return render(request, 'divmart_dashboard/print_label.html')
    return None


def svg_file_reader():

    with open('media/product1.svg', 'r') as f: 
        data = f.read() 

    bs_data = BeautifulSoup(data, 'xml')
    add = 0.10

    for tag in bs_data.find_all('text'):
        k = f'{round(add,2)}mm'
        tag['y'] = k
        add += 1

    with open('media/product1.svg', 'w') as f: 
        f.write(bs_data.prettify())
    # return render(request, 'divmart_dashboard/print_label.html')
    return bs_data

    

def list_discount(request):
    return render(request,'divmart_dashboard/list_discount.html')     

def list_subscription(request):
    return render(request,'divmart_dashboard/list_subscription.html')        

def payment_cash_flow(request):
    return render(request,'divmart_dashboard/payment_cash_flow.html')     

def payment_account_detail(request):
    return render(request,'divmart_dashboard/payment_account_detail.html')

def payment_account_book(request):
    return render(request,'divmart_dashboard/payment_account_book.html')


class RegisteredMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredMembers
        fields = '__all__'


def direct_members(request):
    return render(request,'divmart_dashboard/direct_members.html')


def manage_transaction(request):
    return render(request,'divmart_dashboard/manage_transaction.html') 


def all_point_transaction(request):
    return render(request,'divmart_dashboard/all_point_transaction.html')  


# changes done by.........

@login_required(login_url='/useraccount/common_login')
def stock_transfer_list(request):

    if request.method == "POST":
        location = request.POST.get('business_location')
        date_range = request.POST.get('date')
        
        try:
            date_split = date_range.split('T')[0]
            year = date_split.split('-')[0]
            month = date_split.split('-')[1]
            day = date_split.split('-')[2]

            if date_range == '' or date_range == None:
                transfer_list = StockTransfer.objects.filter(location_from__name=location).filter(status=True)
            elif location == '' or location == None:
                transfer_list = StockTransfer.objects.filter(date__year = year, date__month = month, date__day = day).filter(status=True)
            else:
                transfer_list = StockTransfer.objects.filter(Q(location_from__name=location) & Q(date__year = year, date__month = month, date__day = day)).filter(status=True)

        except:
            transfer_list = StockTransfer.objects.filter(location_from__name=location).filter(status=True)

    else:
        transfer_list = StockTransfer.objects.filter(status=True)

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/stock_transfer_list.html', {'transfer_list':transfer_list, 'locations':locations})



@login_required(login_url='/useraccount/common_login')
def add_stock_transfer(request):

    try:
        stock_trans_obj = StockTransfer.objects.last().ref_no
        ref_id_get = stock_trans_obj.split('-')[1]
        ref_id = int(ref_id_get) + 1
    except Exception as e:
        print('-exception in stock transfer---', e)
        ref_id = 'STR-1000' + str(1)
    
    if request.method == 'POST':
        count = request.POST.get('count')
        date = request.POST.get('date')
        location_from = request.POST.get('location_from')
        location_to = request.POST.get('location_to')
        total_amount = request.POST.get('total_amount')
        shipping_charges = request.POST.get('shipping_charges', 0)
        notes = request.POST.get('notes')
        location_obj_1 = BusinessLocation.objects.get(id=location_from)
        location_obj_2 = BusinessLocation.objects.get(id=location_to)
        try:
            stock_obj = StockTransfer(date=date, ref_no=ref_id, location_from=location_obj_1, location_to=location_obj_2, 
                total_amount=total_amount, shipping_charges=shipping_charges, notes=notes, status=True)
            stock_obj.save()

            for v in range(1, int(count)+1):
                prod_name = request.POST.get("nam"+str(v))
                prod_quan = request.POST.get("qan"+str(v))
                prod_price = request.POST.get("usp"+str(v))
                sub_total = request.POST.get("sub"+str(v))
                prod_obj = Product.objects.get(product_name=prod_name)

                stock_prod_trans_obj = StockProdTransfer(stock_transfer=stock_obj, product=prod_obj, quantity=prod_quan, unit_price=prod_price, sub_total=sub_total)
                stock_prod_trans_obj.save()
        except:
            stock_obj.delete()
            messages.error(request, 'Please choose a valid product...')
            return redirect('add_stock_transfer')
        
        messages.success(request, 'stock transfer success...')
        return redirect('stock_transfer_list')

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/add_stock_transfer.html', {'locations':locations})


@login_required(login_url='/useraccount/common_login')
def edit_stock_trasfer(request, id):

    trans_obj = StockTransfer.objects.get(id=id)
    prod_obj = StockProdTransfer.objects.filter(stock_transfer=trans_obj)

    if request.method == 'POST':

        count = request.POST.get('count')
        location_from = request.POST.get('location_from')
        location_to = request.POST.get('location_to')
        total_amount = request.POST.get('total_amount')
        shipping_charges = request.POST.get('shipping_charges', 0)
        notes = request.POST.get('notes')
        location_obj_1 = BusinessLocation.objects.get(id=location_from)
        location_obj_2 = BusinessLocation.objects.get(id=location_to)

        StockTransfer.objects.filter(id=id).update(location_from=location_obj_1, location_to=location_obj_2, 
            total_amount=total_amount, shipping_charges=shipping_charges, notes=notes)

        for v in range(1, int(count)+1):
            prod_name = request.POST.get("nam"+str(v))
            prod_quan = request.POST.get("qan"+str(v))
            prod_price = request.POST.get("usp"+str(v))
            sub_total = request.POST.get("sub"+str(v))
            stock_prod_trans_id = request.POST.get("stctrobj"+str(v))
            prod_obj = Product.objects.get(product_name=prod_name)

            if StockProdTransfer.objects.filter(id=stock_prod_trans_id):
                StockProdTransfer.objects.filter(id=stock_prod_trans_id).update(stock_transfer=trans_obj, product=prod_obj, quantity=prod_quan, unit_price=prod_price, sub_total=sub_total)
            else:
                trans_obj_create = stock_prod_trans_id(stock_transfer=trans_obj, product=prod_obj, quantity=prod_quan, unit_price=prod_price, sub_total=sub_total)
                trans_obj_create.save()

        messages.success(request, trans_obj.ref_no + ' update success...')
        return redirect('stock_transfer_list')

    locations = BusinessLocation.objects.filter(status=True)
    return render(request, 'divmart_dashboard/edit_stock_transfer.html', {'obj':trans_obj, 'locations':locations, 'prod_objs':prod_obj})


@login_required(login_url='/useraccount/common_login')
def delete_stock_transfer(request, id):

    trans_obj = StockTransfer.objects.get(id=id)
    trans_obj.status = False
    messages.success(request, str(trans_obj.ref_no + ' remove success...!'))
    return redirect('stock_transfer_list')


@login_required(login_url='/useraccount/common_login')
def list_stock_adjustment(request):

    if request.method == 'POST':
        location = request.POST.get('business_location')
        type = request.POST.get('adjust_type')
        date_range = request.POST.get('date')

        date_split = date_range.split('T')[0]
        year = date_split.split('-')[0]
        month = date_split.split('-')[1]
        day = date_split.split('-')[2]

        adjustment_list = StockAdjustment.objects.filter(Q(date_of_adjust__year = year, date_of_adjust__month = month, date_of_adjust__day = day) | Q(adjustment_type = type) | Q(business_location__name__icontains = location)
        ).filter(status=True)

    else:
        adjustment_list = StockAdjustment.objects.filter(status=True)

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/list_stock_adjustment.html', {'adjustment_list':adjustment_list, 'locations':locations})


@login_required(login_url='/useraccount/common_login')
def add_stock_adjustment(request):

    try:
        stock_adjst_obj = StockAdjustment.objects.last().ref_no
        ref_id_get = stock_adjst_obj.split('-')[1]
        ref_id = int(ref_id_get) + 1
    except Exception as e:
        print('-exception in stock transfer---', e)
        ref_id = 'STA-1000' + str(1)

    if request.method == 'POST':

        count = request.POST.get('count')
        business_location = request.POST.get('business_location')
        date = request.POST.get('date')
        total_amount_recovered = request.POST.get('total_amount_recovered')
        adjustment_type = request.POST.get('adjustment_type')
        reason = request.POST.get('reason')

        business_location_obj = BusinessLocation.objects.get(id=business_location)

        stock_obj = StockAdjustment(date_of_adjust=date, ref_no=ref_id, business_location=business_location_obj, 
            total_amount_recovered=total_amount_recovered, adjustment_type=adjustment_type, reason=reason, status=True)
        stock_obj.save()

        for v in range(1, int(count)+1):
            prod_name = request.POST.get("nam"+str(v))
            prod_quan = request.POST.get("qan"+str(v))
            prod_price = request.POST.get("usp"+str(v))
            sub_total = request.POST.get("sub"+str(v))
            prod_obj = Product.objects.get(product_name=prod_name)

            stock_prod_trans_obj = StockProdAdjustment(stock_adjustment=stock_obj, product=prod_obj, quantity=prod_quan, unit_price=prod_price, sub_total=sub_total)
            stock_prod_trans_obj.save()
            
        messages.success(request, 'stock adjustment success...')
        return redirect('stock_transfer_list')

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/add_stock_adjustment.html', {'locations':locations})


@login_required(login_url='/useraccount/common_login')
def edit_stock_adjustment(request, id):

    adjst_obj = StockAdjustment.objects.get(id=id)
    prod_objs = StockProdAdjustment.objects.filter(stock_adjustment=adjst_obj)

    if request.method == 'POST':

        count = request.POST.get('count')
        business_location = request.POST.get('business_location')
        adjustment_type = request.POST.get('adjustment_type')
        total_amount_recovered = request.POST.get('total_amount_recovered')
        reason = request.POST.get('reason')
        business_location = BusinessLocation.objects.get(id=business_location)

        StockAdjustment.objects.filter(id=id).update(business_location=business_location, adjustment_type=adjustment_type, 
                                                    total_amount_recovered=total_amount_recovered, reason=reason)

        for v in range(1, int(count)+1):
            prod_name = request.POST.get("nam"+str(v))
            prod_quan = request.POST.get("qan"+str(v))
            prod_price = request.POST.get("usp"+str(v))
            sub_total = request.POST.get("sub"+str(v))
            stock_prod_adjst_id = request.POST.get("stctrobj"+str(v))
            prod_obj = Product.objects.get(product_name=prod_name)

            if StockProdAdjustment.objects.filter(id=stock_prod_adjst_id).exists():
                StockProdAdjustment.objects.filter(id=stock_prod_adjst_id).update(stock_adjustment=adjst_obj, product=prod_obj, quantity=prod_quan, 
                                                                                    unit_price=prod_price, sub_total=sub_total)
            else:
                adjst_obj_create = StockProdAdjustment.objects.create(stock_adjustment=adjst_obj, product=prod_obj, quantity=prod_quan, unit_price=prod_price, sub_total=sub_total)
                adjst_obj_create.save()

        messages.success(request, adjst_obj.ref_no + ' update success...')
        return redirect('list_stock_adjustment')

    locations = BusinessLocation.objects.filter(status=True)
    return render(request, 'divmart_dashboard/edit_stock_adjustment.html', {'obj':adjst_obj, 'locations':locations, 'prod_objs':prod_objs})


@login_required(login_url='/useraccount/common_login')
def delete_stock_adjustment(request, id):

    adjust_obj = StockAdjustment.objects.get(id=id)
    adjust_obj.status = False
    adjust_obj.save()
    messages.success(request, 'Stock Adjustment ' + str(adjust_obj.ref_no) + ' remove success...!')

    return redirect('list_stock_adjustment')


@login_required(login_url='/useraccount/common_login')
def add_sellingprice_group(request):

    if request.method == 'POST':
        form = SellingPriceGroupForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit = False)
            form_save.status = True
            form_save.save()
            messages.success(request, 'Selling price group ' + str(form_save.name) + ' added success...')
            return redirect('selling-price-groups')
    else:
        form = SellingPriceGroupForm()
    
    selling_group_list = SellingPriceGroup.objects.filter(status=True)
    return render(request, 'divmart_dashboard/selling_groups.html', {'form':form, 'selling_group_list': selling_group_list})


@login_required(login_url='/useraccount/common_login')
def edit_sellingprice_group(request, id):

    selling_group_obj = SellingPriceGroup.objects.get(id=id)
    if request.method == 'POST':
        form = SellingPriceGroupForm(request.POST, instance=selling_group_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Selling price group ' + str(selling_group_obj.name) + ' updated success...!')
            return redirect('selling-price-groups')
    else:
        form = SellingPriceGroupForm(instance=selling_group_obj)
    return render(request, 'divmart_dashboard/edit_selling_groups.html', {'form':form, 'obj':selling_group_obj})


@login_required(login_url='/useraccount/common_login')
def delete_sellingprice_group(request, id):

    selling_group_obj = SellingPriceGroup.objects.get(id=id)
    selling_group_obj.status = False
    selling_group_obj.save()
    messages.success(request, 'Selling price group ' + str(selling_group_obj.name) + ' remove success...!')
    return redirect('selling-price-groups')


@login_required(login_url='/useraccount/common_login')
def variations(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variation ' + str(form.variation_name) + ' create success..!')
            return redirect('variations')
    else:
        form = VariationForm()

    variation_list = ProductVariation.objects.all()
    return render(request, 'divmart_dashboard/variations.html', {'form':form, 'list':variation_list})


@login_required(login_url='/useraccount/common_login')
def edit_variations(request, id):

    variation_obj = ProductVariation.objects.get(id=id)
    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variation ' + str(form.variation_name) + ' update success..!')
            return redirect('variations')
    else:
        form = VariationForm(instance=variation_obj)
    return render(request, 'divmart_dashboard/edit_variation.html', {'form':form, 'obj':variation_obj})


@login_required(login_url='/useraccount/common_login')
def delete_variation(request, id):

    variation_obj = ProductVariation.objects.get(id=id)
    variation_obj.delete()
    variation_obj.save()
    messages.success(request, 'Product Variation ' + str(variation_obj.variation_name) + ' remove success..!')
    return redirect('variations')


@login_required(login_url='/useraccount/common_login')
def import_products(request):

    unit_obj = Units.objects.filter(status=True)
    
    if request.method == 'POST':
        file = request.FILES.get('products')
        try:
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)

            for values in csv.reader(io_string):
                for unit in unit_obj:
                    if unit.name == values[1] or unit.short_name == values[1]:
                        prod_obj = Product.objects.create(product_name=values[0], unit=unit, selling_price_tax_type=values[2], product_type=values[3])
                        prod_obj.save()
                        messages.success(request, 'Product add success...!')
            else:
                messages.error(request, 'Error with data in provided file...!')
        except Exception as e:
            print('--exception as e-----', e)
            messages.error(request, 'please provide valid file...')

        # try:
    #         for unit in unit_obj:
    #             if unit.name == values[1] or unit.short_name == values[1]:
    #                 prod_obj = Product.objects.create(product_name=values[0], unit=unit, selling_price_tax_type=values[2], product_type=values[3], 
    #                 brand=values[4], category=values[5], sub_category=values[6], SKU=values[7], barcode_type=values[8], alert_quantity=values[9],   
    #                 Product_description=values[10], product_image=values[11], weight=values[12], applicable_tax=values[13], selling_price=values[14], 
    #                 selling_price_exc_tax=values[15], purchase_price=values[16], purchase_price_exc_tax=values[17], purchase_price_inc_tax=values[18], 
    #                 margin=values[19], current_stock=values[20])
    #                 prod_obj.save()
        #     # return redirect('list_products')

        # except Exception as e:
        #     print('--exception error in product import--', e)

    return render(request,'divmart_dashboard/import_product.html')


@login_required(login_url='/useraccount/common_login')
def import_opening_stock(request):

    brands = Brand.objects.filter(status=True)

    if request.method == 'POST':
        file = request.FILES.get('open_stock')

        try:
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)

            for values in csv.reader(io_string):
                for brand in brands:
                    if brand.brand_name == values[3] and Product.objects.filter(product_name=values[0]):
                        prod_obj = Product.objects.get(product_name=values[0])
                        prod_obj.current_stock += values[1]
                        prod_obj.save()
                        messages.success(request, 'stock updated success..!')
                    else:
                        obj_prod = Product.objects.create(product_name=values[0], current_stock=values[1], brand=Brand.objects.get(brand_name=values[3]))
                        obj_prod.save()
                        messages.success(request, 'Product add success..!')
            else:
                messages.error(request, 'Please check instructions...!')
        except Exception as e:
            print('-exception as e-----', e)
            messages.error(request, 'Please provide a valid file...')
            
    return render(request,'divmart_dashboard/import_opening_stock.html')



@login_required(login_url='/useraccount/common_login')
def add_expenses(request):

    expense_categories = Expenses_category.objects.filter(status=True)
    business_location_list = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/add_expenses.html',{'expense_categories':expense_categories, 'business':business_location_list})


@login_required(login_url='/useraccount/common_login')
def list_expenses(request):

    list_expense = ''
    year_for = ''
    month_for = ''
    day_for = ''

    if request.method == 'POST':
        prod_type = request.POST.get('location')
        prod_cat = request.POST.get('category')
        prod_unit = request.POST.get('date')

        formated = prod_unit.split('T')[0]
        year_for = formated.split('-')[0]
        month_for = formated.split('-')[1]
        day_for = formated.split('-')[2]

        list_expense = Expenses.objects.filter(Q(expenses_date__year = int(year_for), expenses_date__month = int(month_for), expenses_date__day = int(day_for)) | Q(expense_category__id__contains=prod_cat) | Q(business_location__id__contains=prod_type)
        ).filter(status=True)

    else:
        list_expense = Expenses.objects.filter(status=True)

    locations = BusinessLocation.objects.filter(status=True)
    category = Expenses_category.objects.filter(status=True)

    return render(request,'divmart_dashboard/list_expenses.html', {'list_expense':list_expense, 'locations':locations,'category':category,})


@login_required(login_url='/useraccount/common_login')
def add_expenses_category(request):

    if request.method == "POST":
        name = request.POST.get("name")
        cat_code = request.POST.get("category_code")
        cat_id = request.POST.get("cid")
        Expenses_category.objects.filter(id=cat_id).update(name=name,category_code=cat_code)
        messages.success(request, 'Expense Category ' + name + ' create success...!')
    exp_cat = Expenses_category.objects.filter(status=True)
    return render(request,"divmart_dashboard/expenses_category.html",{'exp_cat':exp_cat})


@login_required(login_url='/useraccount/common_login')
def delete_exp_category(request,id):

    u_obj = Expenses_category.objects.get(id=id)
    u_obj.status = False
    u_obj.save()
    messages.success(request, 'Expense Category ' + str(u_obj.name) + ' remove success..!')
    return redirect('add_expenses_category')


@login_required(login_url='/useraccount/common_login')
def search_product_list(request):

    product_list = []
    d = {}

    if not request.user.is_superuser:
        staff_user = StaffUser.objects.get(user=request.user)
        prod = Product.objects.filter(status=True, business_location=staff_user.business_location)
    else:
        prod = Product.objects.filter(status=True)

    for v in prod:
        d['id'] = v.id
        d['name'] = v.product_name
        d['q_name'] = v.current_stock
        d['u_unit'] = v.selling_price

        product_list.append(d)
        d = {}
        
    return JsonResponse({'prod_list': product_list})
                

@login_required(login_url='/useraccount/common_login')
def search_product_with_id(request, id):

    product_list = []
    d = {}

    prod = Product.objects.filter(status=True, id=id)
    for v in prod:
        d['id'] = v.id
        d['name'] = v.product_name
        d['q_name'] = v.current_stock
        d['u_unit'] = v.selling_price

        product_list.append(d)
        d = {}
    return JsonResponse({'prod_list': product_list})


def print_label(request):

    images = ''
    if request.method == "POST":

        count = request.POST.get("count", 0)
        name_choice = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        tax_type = request.POST.get('tax_type')
        busniness_name_choice = request.POST.get('Business_name')

        images = []
        for val in range(1, int(count)+1):
            product = request.POST.get("nam"+str(val))
            labels = request.POST.get("lab"+str(val))

            # try:
            price = 0
            for label in range(1, int(labels)+1):
                
                prod_obj = Product.objects.get(product_name=product)
                if product_price == 'on':
                    if tax_type == "E":
                        price = prod_obj.purchase_price_exc_tax
                    else:
                        price = prod_obj.purchase_price_inc_tax
                product_image = bar_code_generator(product, str(price), name_choice, busniness_name_choice, product_price, request)
                images.append(product_image)
            # except Exception as e:
            #     messages.warning(request, e)

    return render(request,'divmart_dashboard/print_label.html', {'images':images}) 


@login_required(login_url='/useraccount/common_login')
def list_products(request):

    unit = Units.objects.filter(status=True)
    brand = Brand.objects.filter(status=True)
    cat = Category.objects.filter(status=True)
    sub_cat = SubCategory.objects.filter(status=True)
    locations = BusinessLocation.objects.filter(status=True)

    if request.method == 'POST':
        try:
            prod_unit = request.POST.get('prod_unit', 'None')
            prod_tax = request.POST.get('prod_tax', 'None')
            prod_brand = request.POST.get('prod_brand', 'None')
            business_location = request.POST.get('business_location', 'None')

            if business_location != 'none' and prod_brand != 'none' and prod_unit != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(brand__brand_name__icontains=prod_brand) & Q(unit__name__icontains=prod_unit) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            elif business_location != 'none' and prod_brand != 'none' and prod_unit != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(brand__brand_name__icontains=prod_brand) & Q(unit__name__icontains=prod_unit)).filter(status=True)

            elif business_location != 'none' and prod_brand != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(brand__brand_name__icontains=prod_brand) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            elif business_location != 'none' and prod_unit != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(unit__name__icontains=prod_unit) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            elif prod_brand != 'none' and prod_tax != 'none' and prod_unit != 'none':
                prod_search = Product.objects.filter(Q(selling_price_tax_type__icontains=prod_tax) & Q(brand__brand_name__icontains=prod_brand) & Q(unit__name__icontains=prod_unit)).filter(status=True)

            elif business_location != 'none' and prod_brand != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(brand__brand_name__icontains=prod_brand)).filter(status=True)

            elif business_location != 'none' and prod_unit != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(unit__name__icontains=prod_unit)).filter(status=True)
                
            elif business_location != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(business_location__name=business_location) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            elif prod_brand != 'none' and prod_unit != 'none':
                prod_search = Product.objects.filter(Q(brand__brand_name__icontains=prod_brand) & Q(unit__name__icontains=prod_unit)).filter(status=True)

            elif prod_brand != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(brand__brand_name__icontains=prod_brand) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            elif prod_unit != 'none' and prod_tax != 'none':
                prod_search = Product.objects.filter(Q(unit__name__icontains=prod_unit) & Q(selling_price_tax_type__icontains=prod_tax)).filter(status=True)

            else:
                prod_search = Product.objects.filter(Q(unit__name__icontains=prod_unit) | Q(selling_price_tax_type__icontains=prod_tax) | Q(business_location__name=business_location) | Q(brand__brand_name__icontains=prod_brand)).filter(status=True)

        except Exception as e:
            prod_lists = request.POST.getlist('prod_list')
            for prod in prod_lists:
                prod_obj = Product.objects.get(id=prod)
                prod_obj.status = False
                prod_obj.save()
                return redirect('list_products')

    else:
        if request.user.is_superuser:
            prod_search = Product.objects.filter(status=True)
        else:
            prod_search = Product.objects.filter(status=True, business_location=StaffUser.objects.get(user=request.user).business_location)

    return render(request,'divmart_dashboard/list_products.html',{'unit':unit,'brand':brand,'cat':cat,'sub_cat': sub_cat, 'new_prod':prod_search, 'locations':locations})


@login_required(login_url='/useraccount/common_login')
def edit_new_product(request, id):

    prod_obj = Product.objects.get(id=id)
    unit = Units.objects.filter(status=True)
    brand = Brand.objects.filter(status=True)
    cat = Category.objects.filter(status=True)
    sub_cat = SubCategory.objects.filter(status=True)
    tax_rates = TaxRate.objects.filter(status=True)
    business_location = BusinessLocation.objects.filter(status=True)

    if request.method == "POST":

        p_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        unit = request.POST.get('unit')
        location = request.POST.get('business_location')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        sku = request.POST.get('SKU')
        b_type = request.POST.get('barcode_type')
        alert_quantity = request.POST.get('alert_quantity')
        p_discription = request.POST.get('Product_description')
        p_image = request.POST.get('product_image')
        p_weight = request.POST.get('weight')
        applicable_tax = request.POST.get('applicable_tax')
        product_type = request.POST.get('product_type')
        prod_mrp = request.POST.get('prod_mrp')
        sp_tax_type = request.POST.get('selling_price_tax_type')
        ppe_tax = request.POST.get('purchase_price_exc_tax')
        ppi_tax = request.POST.get('purchase_price_inc_tax')
        margin = request.POST.get('margin')
        spe_tax = request.POST.get('selling_price_exc_tax')
        
        Product.objects.filter(id=id).update(product_name=p_name, brand=brand, unit=unit, category=category, sub_category=sub_category, SKU=sku, barcode_type=b_type, alert_quantity=alert_quantity, Product_description=p_discription, product_image=p_image, weight=p_weight, applicable_tax=applicable_tax, product_type=product_type, selling_price_tax_type=sp_tax_type, purchase_price_exc_tax=ppe_tax, purchase_price_inc_tax=ppi_tax, margin=margin, selling_price_exc_tax=spe_tax, selling_price=prod_obj.selling_price, purchase_price=prod_obj.purchase_price, current_stock=prod_obj.current_stock, status=True,
        prod_mrp=prod_mrp, business_location=location)

        messages.success(request, 'Product ' + str(prod_obj.product_name) + ' update success...!')
        return redirect('list_products')

    return render(request,'divmart_dashboard/edit_new_product.html',{'unit':unit,'brand':brand,'cat':cat,'sub_cat': sub_cat,'prod':prod_obj, 'rates':tax_rates, 'locations':business_location})


@login_required(login_url='/useraccount/common_login')
def product_units(request):

    if request.method == 'POST':
        form = UnitsForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.status = True
            form.save()
            messages.success(request, 'Unit ' + str(form_save.name) + ' create success...!')
            return redirect('units-list')

    units_list = Units.objects.filter(status=True)
    return render(request,'divmart_dashboard/product_units.html',{'units_list':units_list})


@login_required(login_url='/useraccount/common_login')
def edit_units(request, id):

    unit_obj = Units.objects.get(id=id)
    if request.method == "POST":
        form = UnitsForm(request.POST, instance=unit_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit ' + str(unit_obj.name) + ' update success...!')
            return redirect('units-list')
    else:
        form = UnitsForm(instance=unit_obj)

    return render(request, 'divmart_dashboard/edit_unit.html', {'form':form, 'unit_obj':unit_obj}) 


@login_required(login_url='/useraccount/common_login')
def unit_delete(request,id):

    unit_obj = Units.objects.get(id=id)
    unit_obj.status = False
    unit_obj.save()
    messages.success(request, 'Unit ' + str(unit_obj.name) + ' remove success..!')
    return redirect('units-list')


@login_required(login_url='/useraccount/common_login')
def categories(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category create success...!')
            return redirect('categories')
    else:
        form = CategoryForm()

    category_list = Category.objects.filter(status=True)
    sub_category_list = SubCategory.objects.filter(status=True)
    return render(request,'divmart_dashboard/categories.html',{"category_list":category_list, 'sub_category_list':sub_category_list, "form":form})


@login_required(login_url='/useraccount/common_login')
def edit_category(request, id):

    category_obj = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category ' + str(category_obj.name) + ' create success..!')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category_obj)

    sub_category_list = SubCategory.objects.filter(status=True)
    return render(request, 'divmart_dashboard/edit_category.html', {'obj':category_obj, 'sub_category_list':sub_category_list})


@login_required(login_url='/useraccount/common_login')
def delete_category(request, id):

    category_obj = Category.objects.get(id=id, status=True)
    category_obj.status = False
    category_obj.save()
    messages.success(request, 'Category ' + str(category_obj.name) + ' remove success...!')
    return redirect('categories') 


@login_required(login_url='/useraccount/common_login')
def brand(request):

    if request.method == 'POST':
        form = BrnadForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.status = True
            save_form.save()
            messages.success(request, 'Brand ' + str(save_form.brand_name) + ' create success')
            return redirect('brand')
    else:
        form = BrnadForm()

    brands = Brand.objects.filter(status=True)

    return render(request, 'divmart_dashboard/brand.html', {'brands':brands})


@login_required(login_url='/useraccount/common_login')
def edit_brand(request, id):

    brand_obj = Brand.objects.get(id=id)
    if request.method == 'POST':
        form = BrnadForm(request.POST, instance=brand_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand ' + str(brand_obj.brand_name) + ' update success..!')
            return redirect('brand')
    else:
        form = BrnadForm(brand_obj)
    return render(request, 'divmart_dashboard/edit_brand.html', {'form':form, 'obj':brand_obj})


@login_required(login_url='/useraccount/common_login')
def sub_category(request):

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.status = True
            save_form.save()
            messages.success(request, 'Sub category ' + str(save_form.name) + ' create sucess..!')
            return redirect('sub-category')
    else:
        form = SubCategoryForm()
    
    sub_categories = SubCategory.objects.filter(status=True)
    return render(request, 'divmart_dashboard/subcategory.html', {'form':form, 'sub_categories':sub_categories})


@login_required(login_url='/useraccount/common_login')
def edit_sub_ctaegory(request, id):

    sub_cat_obj = SubCategory.objects.get(id=id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=sub_cat_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sub category ' + str(sub_cat_obj.name) + ' update success...!')
            return redirect('sub-category')
    else:
        form = SubCategoryForm(instance=sub_cat_obj)
    return render(request, 'divmart_dashboard/subcategory_edit.html', {'form':form, 'obj':sub_cat_obj})


@login_required(login_url='/useraccount/common_login')
def delete_sub_category(request, id):

    sub_cat_obj = SubCategory.objects.get(id=id)
    sub_cat_obj.status = False
    sub_cat_obj.save()
    messages.success(request, 'Sub category ' + str(sub_cat_obj.name) + ' remove success...!')
    return redirect('sub-category')


@login_required(login_url='/useraccount/common_login')
def remove_brand(request, id):

    brand_obj = Brand.objects.get(id=id)
    brand_obj.status = False
    brand_obj.save()
    messages.success(request, 'Brand ' + str(brand_obj.brand_name) + ' remove success...!')
    return redirect('brand')


@login_required(login_url='/useraccount/common_login')
def list_pos(request):

    pos_list = Sell.objects.filter(is_deleted=False)
    if request.method == 'POST':
        try:
            business_location = request.POST.get('locations')
            customer = request.POST.get('customer')
            payment_status = request.POST.get('payment_status')

            if business_location != '':
                pos_list = Sell.objects.filter(business_location__name__icontains = business_location, is_deleted=False)
            elif customer != '':
                pos_list = Sell.objects.filter(customer__first_name__icontains = customer, is_deleted=False)
            elif payment_status != '':
                pos_list = Sell.objects.filter(status__icontains = payment_status, is_deleted=False)

        except Exception as e:
            # print('--exception as e------', e)
            pos_list = Sell.objects.filter(is_deleted=False)
    else:
        pos_list = Sell.objects.filter(is_deleted=False)

    business_location_list = BusinessLocation.objects.filter(status=True)
    customers = CustomerUser.objects.all()

    return render(request,'divmart_dashboard/list_pos.html', {'pos_list':pos_list, 'locations':business_location_list, 'customers':customers})  


@login_required(login_url='/useraccount/common_login')
def dashboard_pos(request):

    sale_obj = ''
    staffuser_obj = ''
    date_now = datetime.datetime.now()

    try:
        sale_last = Sell.objects.last()
        lasr_ref_no =  sale_last.ref_no
        invoice_last = sale_last.invoice_no

        spi_last = lasr_ref_no.split('-')[1]
        lasr_ref_no = int(spi_last) + 1
        str_ref = 'SL-' + str(lasr_ref_no)

        invoice_last = int(invoice_last) + 1
    except Exception as e:
        # print('---exception error in pos---', e)
        str_ref = 'SL-10001'
        invoice_last = 1000
    try:
        staffuser_obj = StaffUser.objects.get(user=request.user)
    except:
        pass

    product_list = Product.objects.filter(status=True)
    business_location_list = BusinessLocation.objects.filter(status=True)

    try:
        staffuser_obj = StaffUser.objects.get(user=request.user)
    except:
        pass

    if request.user.is_superuser:
        customers = CustomerUser.objects.filter(is_deleted=0)
    else:
        customers = CustomerUser.objects.filter(is_deleted=0, business_location=staffuser_obj.business_location)

    try:
        if request.method == 'POST':
            count = request.POST.get('count',)
            location = request.POST.get('business_location')
            customer = request.POST.get('customer')
            total_amount = request.POST.get('total_amount', 0)
            discount_amount = request.POST.get('discount_amount', 0)
            shipping_charges = request.POST.get('shipping_charges', 0)
            payable = request.POST.get('total_payable', 0)

            if not request.user.is_superuser:
                location_obj = BusinessLocation.objects.get(id=staffuser_obj.business_location.id)
            else:
                location_obj = BusinessLocation.objects.get(id=location)
                
            customer_obj = CustomerUser.objects.get(id=customer)

            pay_obj = Add_Payments.objects.create(amount=total_amount, payment_method=0, payment_notes='', payment_due=0.0, payment_status=True)

            if request.POST.get('draft') == 'Draft':
                sale_obj = Sell.objects.create(ref_no=str_ref,business_location=location_obj, customer=customer_obj, sale_date=date_now, total_amount=total_amount, discount_amount=discount_amount, shipping_charges=shipping_charges, total_payable=payable, status='D', invoice_no=invoice_last, payment_info=pay_obj, cashier=staffuser_obj)

            elif request.POST.get('quote') == "Quotation":
                sale_obj = Sell.objects.create(ref_no=str_ref,business_location=location_obj, customer=customer_obj, sale_date=date_now, total_amount=total_amount, discount_amount=discount_amount, shipping_charges=shipping_charges, total_payable=payable, status='Q', invoice_no=invoice_last, payment_info=pay_obj, cashier=staffuser_obj)

            else:
                sale_obj = Sell.objects.create(ref_no=str_ref,business_location=location_obj, customer=customer_obj, sale_date=date_now, total_amount=total_amount, discount_amount=discount_amount, shipping_charges=shipping_charges, total_payable=payable, status='F', invoice_no=invoice_last, payment_info=pay_obj, cashier=staffuser_obj)

            sale_obj.save()
            for v in range(1, int(count)+1):
                prod_name = request.POST.get("nam"+str(v))
                prod_qan = request.POST.get("qan"+str(v))
                unit_price = request.POST.get("usp"+str(v))
                sub_total = request.POST.get("sub"+str(v))
                prod_obj = Product.objects.get(product_name=prod_name)
                
                # try:
                if float(prod_obj.current_stock) >= float(prod_qan):
                    ItemSold.objects.create(sell=sale_obj, items_name=prod_obj, price=unit_price, quantity=prod_qan, sub_total=sub_total, date=date_now)
                    prod_obj.current_stock = float(prod_obj.current_stock) + float(prod_qan)
                    prod_obj.save()
                else:
                    sale_obj.delete()
                    messages.error(request, 'Not much stock available for selected product/products')
                # except Exception as e:
                #     messages.error(request, e)
                #     sale_obj.delete()
                #     return redirect('dashboard_pos')

            messages.success(request, 'sale added successfully...!')
            return redirect(reverse('invoice_view', kwargs={'id':int(sale_obj.id)}))
    except Exception as e:
        messages.error(request, e)
    
    if not request.user.is_superuser:
        pos_list_final = Sell.objects.filter(status='F', business_location=staffuser_obj.business_location, is_deleted=False)[:5]
        pos_list_quotes = Sell.objects.filter(status='Q', business_location=staffuser_obj.business_location, is_deleted=False)[:5]
        pos_list_draft = Sell.objects.filter(status='D', business_location=staffuser_obj.business_location, is_deleted=False)[:5]
    else:
        pos_list_final = Sell.objects.filter(status='F', is_deleted=False)[:5]
        pos_list_quotes = Sell.objects.filter(status='Q', is_deleted=False)[:5]
        pos_list_draft = Sell.objects.filter(status='D', is_deleted=False)[:5]

    customer_group = CustomerGroups.objects.filter(is_deleted=0)

    return render(request,'divmart_dashboard/index_pos.html', {
                        'locations':business_location_list, 'customers':customers, 'prod_list':product_list,
                        'final_list':pos_list_final, 'quotes_list':pos_list_quotes, 'draft_list':pos_list_draft,
                        'customer_group': customer_group, 'obj':sale_obj, 'staff_obj':staffuser_obj,

    })


@login_required(login_url='/useraccount/common_login')
def payment_account(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        account_number = request.POST.get('account_number')
        openning_balance = request.POST.get('openning_balance')
        note = request.POST.get('note')

        pay_obj = PaymentAccount.objects.create(name=name, account_number=account_number, openning_balance=openning_balance, note=note, status=True)
        pay_obj.save()
        messages.success(request, str(pay_obj.name) + ' create success...!')
    payment_account_list = PaymentAccount.objects.filter(status=True)
    return render(request, 'divmart_dashboard/payment_account_detail.html', {'payment_account_list':payment_account_list})


@login_required(login_url='/useraccount/common_login')
def payment_account_edit(request, id):

    pay_acc_obj = PaymentAccount.objects.get(id=id, status=True)
    if request.method == 'POST':
        form = PaymentAccountForm(request.POST, instance=pay_acc_obj)
        if form.is_valid():
            form.save()
            messages.success(request, str(pay_acc_obj.name) + ' update success...!')
            return redirect('payment_accounts')
        
    else:
        form = PaymentAccountForm(instance=pay_acc_obj)

    return render(request, 'divmart_dashboard/payment_account_edit.html', {'obj':pay_acc_obj})


@login_required(login_url='/useraccount/common_login')
def payment_account_remove(request, id):

    pay_acc_obj = PaymentAccount.objects.get(id=id, status=True)
    pay_acc_obj.status=False
    pay_acc_obj.save()
    messages.success(request, str(pay_acc_obj.name) + ' remove success...!')
    return redirect('payment_account_detail')


@login_required(login_url='/useraccount/common_login')
def add_purchase(request):
            
    purchase = Product.objects.filter(status=True)           
    supplier = SupplierUser.objects.all()
    payment_accounts = PaymentAccount.objects.filter(status=True)

    ref_no_new = ''

    if request.method == "POST":
        pay_amt = request.POST.get("amount", 0)
        pay_method = request.POST.get("pay_method")
        pay_account = request.POST.get("pay_account")
        pay_notes = request.POST.get("pay_notes")
        pay_due = request.POST.get("pay_due", 0)
        payment_account_obj = PaymentAccount.objects.get(id=pay_account)

        pay_obj = Add_Payments(amount=pay_amt,payment_method=pay_method,payment_account=payment_account_obj,payment_notes=pay_notes,payment_due=pay_due,payment_status=True)
        pay_obj.save()
        sup = request.POST.get("supplier")

        supp_obj_modify = SupplierUser.objects.get(id=sup)
        supp_obj_modify.total_purchase_due=float(supp_obj_modify.total_purchase_due) + float(pay_due)
        supp_obj_modify.save()

        pur_date = request.POST.get("purchase_date")
        # pur_status = request.POST.get("purchase_status")
        bus_location = request.POST.get("business_location")
        docs = request.FILES.get("documents")
        net_total_amount = request.POST.get("net_total_amt")
        dis_type = request.POST.get("discount_type")
        discount = request.POST.get("discount")
        dis_amt = request.POST.get("discount_amount", 0)
        purchase_tax = request.POST.get("purchase_tax_sel")
        purchase_tax_amt = request.POST.get("purchase_tax", 0)
        shipping_details = request.POST.get("shipping")
        add_shipping_charges = request.POST.get("add_ship_chrages")
        purchase_total = request.POST.get("purchase_total", 0)
        add_notes = request.POST.get("additional_notes")

        sup_obj = SupplierUser.objects.get(id=sup)
        location_obj = BusinessLocation.objects.get(id=bus_location)

        try:
            last_ref_no = Purchase_info.objects.last().ref_no
            spi_last = last_ref_no.split('-')[1]
            sale_last = int(spi_last) + 1
            ref_no_new = 'PRC-' + str(sale_last)
        except Exception as e:
            print('---exception as e in purchase---', e)
            ref_no_new = 'PRC-10001' 

        pur_info_obj = Purchase_info(supplier=sup_obj,payment_info=pay_obj,ref_no=ref_no_new,purchase_date=pur_date,business_location=location_obj,documents=docs,grand_total=net_total_amount,discount_type=dis_type,Discount_amount=dis_amt,discount=discount,purchase_tax=purchase_tax,purchase_tax_amount=purchase_tax_amt,shipping_details=shipping_details,additional_ship_charges=add_shipping_charges,purchase_total=purchase_total,Additional_notes=add_notes)
        pur_info_obj.save()
        count = request.POST.get("count")
        cnt = int(count)

        for v in range(1,cnt+1):
            prod_name = request.POST.get("nam"+str(v))
            prod_qan = request.POST.get("qan"+str(v))
            prod_price = request.POST.get("pp"+str(v))
            discount = request.POST.get("dis"+str(v))
            unit_cost_before_tax = request.POST.get("ucbt"+str(v))
            subtotal_btax = request.POST.get("st"+str(v))
            tax = request.POST.get("tax"+str(v))
            net_cost = request.POST.get("nc"+str(v))
            l_total = request.POST.get("lt"+str(v))
            margin = request.POST.get("margin"+str(v))
            unit_sp = request.POST.get("usp"+str(v))
            prod_obj = Product.objects.get(product_name=prod_name)

            pur_obj = Purchase(product_name=prod_obj,purchase_quantity=prod_qan,purchase_details= pur_info_obj,unit_cost_before_discount=prod_price,unit_cost_before_tax=unit_cost_before_tax,discount_percentage=discount,sub_total=subtotal_btax,product_tax=tax,net_costs=net_cost,line_total=l_total,profit_margin=margin,unit_selling_price=unit_sp)
            pur_obj.save()
            
            prod_obj.current_stock = prod_obj.current_stock + float(prod_qan)
            prod_obj.save()

        messages.success(request, str(pur_info_obj.ref_no) + ' create success..!')
        return redirect('list_purchase')

    business_location_list = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/add_purchase.html',{
        'purchase':purchase,'supplier':supplier, 'location':business_location_list,
        'payment_accounts':payment_accounts,
    }) 


@login_required(login_url='/useraccount/common_login')
def list_purchase(request):

    pur_info = ''
    if request.method == 'POST':
        location = request.POST.get('business_location')
        supplier = request.POST.get('supplier')
        payment_status = request.POST.get('payment_status')

        if location != 'none' and supplier != 'none' and payment_status != 'none':
            pur_info = Purchase_info.objects.filter(Q(business_location__name__icontains = location) & Q(payment_info__payment_status=payment_status) & Q(supplier__business_name__icontains = supplier)).filter(status=True)

        elif location != 'none' and supplier != 'none':
            pur_info = Purchase_info.objects.filter(Q(business_location__name__icontains = location) & Q(supplier__business_name__icontains = supplier)).filter(status=True)

        elif location != 'none' and payment_status != 'none':
            pur_info = Purchase_info.objects.filter(Q(business_location__name__icontains = location) & Q(payment_info__payment_status=payment_status)).filter(status=True)

        elif supplier != 'none' and payment_status != 'none':
            pur_info = Purchase_info.objects.filter(Q(supplier__business_name__icontains = supplier) & Q(payment_info__payment_status=payment_status)).filter(status=True)            

        elif payment_status == 'none':
            pur_info = Purchase_info.objects.filter(Q(business_location__name__icontains = location) | Q(supplier__business_name__icontains = supplier)).filter(status=True)

        else:
            pur_info = Purchase_info.objects.filter(payment_info__payment_status=payment_status).filter(status=True)
    else:
        if request.user.is_superuser:
            pur_info = Purchase_info.objects.filter(status=True)
        else:
            pur_info = Purchase_info.objects.filter(status=True, business_location=StaffUser.objects.get(user=request.user).business_location)

    pay_obj = Add_Payments.objects.filter(payment_status=True)

    business_location_list = BusinessLocation.objects.filter(status=True)
    supplier_users = SupplierUser.objects.filter(is_deleted=0)

    return render(request,'divmart_dashboard/list_purchase.html',
    {'pur_info':pur_info,'pay_obj':pay_obj, 'business_location_list':business_location_list, 'supplier_users':supplier_users}) 


@login_required(login_url='/useraccount/common_login')
def view_purchase(request, id):

    pur_info = Purchase_info.objects.get(id=id, status=True)
    purchase_obj = Purchase.objects.filter(purchase_details=pur_info)
    return render(request, 'divmart_dashboard/purchase_view.html', {'pur_info':pur_info, 'purchases':purchase_obj})


@login_required(login_url='/useraccount/common_login')
def edit_purchase(request, id):

    try:
        per_info = Purchase_info.objects.get(id=id)
        payment_obj = Add_Payments.objects.get(id=per_info.payment_info.id, payment_status=True)
        purchase_obj = Purchase.objects.filter(purchase_details=per_info.id)
        sup_obj = SupplierUser.objects.get(id=per_info.supplier.id) 

        prod_obj = Product.objects.all()
        payment_accounts = PaymentAccount.objects.filter(status=True)
        supplier_users = SupplierUser.objects.all()
        business_location_list = BusinessLocation.objects.filter(status=True)

        if request.method == "POST":
            pay_amt = request.POST.get("amount")
            # pay_method = request.POST.get("pay_method")
            pay_account = request.POST.get("pay_account")
            pay_notes = request.POST.get("pay_notes")
            pay_due = request.POST.get("pay_due")
            pay_id = request.POST.get("payid")

            Add_Payments.objects.filter(id=pay_id).update(amount=pay_amt, payment_method=0, payment_account=pay_account, payment_notes=pay_notes,
                    payment_due=pay_due,payment_status=True)

            sup = request.POST.get("supplier")
            ref_no = request.POST.get("ref_no")

            # pur_date = request.POST.get("purchase_date")
            # pur_status = request.POST.get("purchase_status")

            bus_location = request.POST.get("business_location")
            docs = request.FILES.get("documents")
            net_total_amount = request.POST.get("net_total_amt")
            dis_type = request.POST.get("discount_type")
            discount = request.POST.get("discount")
            dis_amt = request.POST.get("discount_amount")
            purchase_tax = request.POST.get("purchase_tax_sel")
            purchase_tax_amt = request.POST.get("purchase_tax")
            shipping_details = request.POST.get("shipping")
            add_shipping_charges = request.POST.get("add_ship_chrages")
            purchase_total = request.POST.get("purchase_total")
            add_notes = request.POST.get("additional_notes")
            pur_id = request.POST.get("purid")

            Purchase_info.objects.filter(id=pur_id).update(ref_no=ref_no, status=True, 
            # purchase_date=pur_date, 
            business_location=bus_location, documents=docs, grand_total=net_total_amount, discount_type=dis_type, Discount_amount=dis_amt, discount=discount, purchase_tax=purchase_tax,purchase_tax_amount=purchase_tax_amt, shipping_details=shipping_details, additional_ship_charges=add_shipping_charges, purchase_total=purchase_total,Additional_notes=add_notes)

            count = request.POST.get("count")
            cnt = int(count)
            for v in range(1,cnt+1):
                prod_name = request.POST.get("nam"+str(v))
                prod_qan = request.POST.get("qan"+str(v))
                prod_price = request.POST.get("pp"+str(v))
                discount = request.POST.get("dis"+str(v))
                unit_cost_before_tax = request.POST.get("ucbt"+str(v))
                subtotal_btax = request.POST.get("st"+str(v))
                tax = request.POST.get("tax"+str(v))
                net_cost = request.POST.get("nc"+str(v))
                l_total = request.POST.get("lt"+str(v))
                margin = request.POST.get("margin"+str(v))
                unit_sp = request.POST.get("usp"+str(v))
                prod_id = request.POST.get("pobjid"+str(v))

                prod_obj = Product.objects.get(product_name=prod_name)
                if Purchase.objects.filter(id=prod_id):
                    Purchase.objects.filter(id=prod_id).update(product_name=prod_obj,purchase_quantity=prod_qan,unit_cost_before_discount=prod_price,unit_cost_before_tax=unit_cost_before_tax,discount_percentage=discount,sub_total=subtotal_btax,product_tax=tax,net_costs=net_cost,line_total=l_total,profit_margin=margin,unit_selling_price=unit_sp)
                else:
                    pur_info_obj = Purchase_info.objects.get(id=pur_id)
                    pur_obj = Purchase.objects(product_name=prod_obj,purchase_quantity=prod_qan,purchase_details= pur_info_obj,unit_cost_before_discount=prod_price,unit_cost_before_tax=unit_cost_before_tax,discount_percentage=discount,sub_total=subtotal_btax,product_tax=tax,net_costs=net_cost,line_total=l_total,profit_margin=margin,unit_selling_price=unit_sp)
                    pur_obj.save()

            messages.success(request, str(per_info.ref_no) + ' Update success..!')
            return redirect('list_purchase')
        return render(request,'divmart_dashboard/edit_purchase.html',{'per_info':per_info,'payment_obj':payment_obj,'purchase_obj':purchase_obj,'sup_obj':sup_obj,'prod_obj':prod_obj, 'accounts':payment_accounts, 'users':supplier_users, 'locations':business_location_list}) 
    except:
        messages.error(request, 'No data found with provided id')
        return HttpResponse('No data found with provided id')


def new_members(request):
    new_member_objs = RegisteredMembers.objects.filter(status=0)
    return render(request,'divmart_dashboard/new_members.html',{'data':new_member_objs})  


def edit_members(request,id):

    member_objs = RegisteredMembers.objects.get(id=id)
    if request.method == 'POST':
        try:
            member_objs.identity_proof = request.FILES['identity_proof']
        except:
            member_objs.identity_proof = member_objs.identity_proof
        try:
            member_objs.address_proofs = request.FILES['address_proofs']
        except:
            member_objs.address_proofs = member_objs.address_proofs

        member_objs.save()
        RegisteredMembers.objects.filter(id=id).update(member_amount=request.POST['member_amount'], fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'], contact=request.POST['contact'], alt_contact=request.POST['alt_contact'], perminent_address=request.POST['perminent_address'], current_address=request.POST['current_address'], id_proof_name=request.POST['id_proof_name'], id_proof_number=request.POST['id_proof_number'], account_holder_name=request.POST['account_holder_name'], account_no=request.POST['account_no'], bank_name=request.POST['bank_name'], ifsc_code=request.POST['ifsc_code'], branch_name=request.POST['branch_name'], status=request.POST['status'])

        # if member_objs.status == 0:
        #     from_mail = settings.EMAIL_HOST_USER
        #     to_email = member_objs.email
        #     subject = "Membership account Verified - Div Mart"
        #     body = "Your membership account has been verified successfully \n\n"+\
        #             "You can login to user account with the provided credenatials \n\n" +\
        #             "Email\t: {}\n".format(member_objs.email) +\
        #             "password: {}".format(member_objs.password) +\
        #             "\n\n\n\nRegards,\nTeam Divmart."
        #     send_mail(subject, body, from_mail, [to_email], fail_silently=False,)
        #     messages.success(request, 'Member Update success..!')
        #     return redirect('/dashboard/member/manage')

        messages.success(request, 'Member Update success..!')
        return redirect('/dashboard/members')
    return render(request,'divmart_dashboard/edit_members.html',{'obj':member_objs})   


def view_members(request, id):
    member_objs = RegisteredMembers.objects.get(id=id)
    return render(request,'divmart_dashboard/view_members.html', {'obj':member_objs})   


def members(request):
    member_app_list = RegisteredMembers.objects.filter(status=1)
    return render(request,'divmart_dashboard/members.html', {'lists':member_app_list}) 


def member_status_change(request, id):
    member_obj = RegisteredMembers.objects.get(id=id)
    member_obj.status=0
    member_obj.save()
    messages.success(request, str(member_obj.fname) + ' Remove from the list success...!')
    return redirect('new_members')


@login_required(login_url='/useraccount/common_login')
def list_draft(request):
    try:
        staff_user = StaffUser.objects.get(user=request.user)
        draft_list = Sell.objects.filter(status='D', business_location=staff_user.business_location, is_deleted=False)
    except:
        draft_list = Sell.objects.filter(status='D', is_deleted=False)
    return render(request,'divmart_dashboard/list_draft.html', {'drafts':draft_list})


@login_required(login_url='/useraccount/common_login')
def list_quotations(request):
    try:
        staff_user = StaffUser.objects.get(user=request.user)
        quotes_list = Sell.objects.filter(status='Q', business_location=staff_user.business_location, is_deleted=False)
    except:
        quotes_list = Sell.objects.filter(status='Q', is_deleted=False)

    return render(request,'divmart_dashboard/list_quotations.html', {'quotes':quotes_list})


def barcode_data(request):

    # barcode = '978020137963'
    # prod_obj = Barcode_storage.objects.filter(barcode_no = barcode.strip()).last()
    return render(request, 'divmart_dashboard/invoice.html',)
    #  {'prod_obj':prod_obj})


@login_required(login_url='/useraccount/common_login')
def product_informtion_api(request, product):

    try:
        product =  Product.objects.get(product_name=str(product))
        product_info = {}
        product_info["applicable_tax"] = product.applicable_tax.rate
        product_info["sale_mrp"] = product.sale_mrp
        product_info["mrp"] = product.prod_mrp
        product_info["purchase_price_inc_tax"] = product.purchase_price_inc_tax
        product_info["purchase_price_exc_tax"] = product.purchase_price_exc_tax
        product_info["margin"] = product.margin
        product_info["selling_price"] = product.selling_price
        product_info["selling_price_exc_tax"] = product.selling_price_exc_tax
    except:
        product_info = ''
    return JsonResponse({'prod_info': product_info})


# reports part views start here

def payment_account_report(request):
    return render(request,'divmart_dashboard/payment_account_report.html') 

@login_required(login_url='/useraccount/common_login')
def purchase_sales_report(request):

    purchase_total_excl_tax = Purchase_info.objects.filter(status=True).aggregate(total=Sum(F('purchase_total')-F('purchase_tax_amount')))
    purchase_total_inc_tax = Purchase_info.objects.filter(status=True).aggregate(Sum('purchase_total'))
    purchase_total_return = Purchase_info.objects.filter(status=True, purchase_return=1).aggregate(Sum('purchase_total'))

    sale_total = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('total_payable'))
    total_sale_return = Sell.objects.filter(status='F', sale_return=1, is_deleted=False).aggregate(Sum('total_payable'))

    sale_total_fig = sale_total['total_payable__sum'] if sale_total['total_payable__sum'] else 0.00
    sale_return_fig = total_sale_return['total_payable__sum'] if total_sale_return['total_payable__sum'] else 0.00
    purchase_fig = purchase_total_inc_tax['purchase_total__sum'] if purchase_total_inc_tax['purchase_total__sum'] else 0.00
    purchase_return_fig = purchase_total_return['purchase_total__sum'] if purchase_total_return['purchase_total__sum'] else 0.00

    overall_return = (sale_total_fig - sale_return_fig) - (purchase_fig - purchase_return_fig)

    supplier_due_obj = SupplierUser.objects.all().aggregate(Sum('total_purchase_due'))
    purchase_due_obj = CustomerUser.objects.all().aggregate(Sum('total_sales_due'))

    busienss_locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/purchase_sales_report.html', {
                        'locations':busienss_locations, 
                        'purchase_total_incl_tax':purchase_total_inc_tax['purchase_total__sum'], 
                        'purchase_total':purchase_total_excl_tax['total'], 
                        'purchase_total_return':purchase_total_return['purchase_total__sum'],
                        'sale_total':sale_total['total_payable__sum'],
                        'total_sale_return':total_sale_return['total_payable__sum'],
                        'overall_return':overall_return,
                        'supplier_due':supplier_due_obj['total_purchase_due__sum'],
                        'purchase_due':purchase_due_obj['total_sales_due__sum'],

    }) 


@login_required(login_url='/useraccount/common_login')
def profit_loss_report(request):

    opening_stock = Product.objects.filter(status=True).aggregate(total=Sum(F('current_stock')*F('purchase_price')))

    purchase_total = Purchase_info.objects.filter(status=True).aggregate(Sum('purchase_total'))
    purchase_total_discount = Purchase_info.objects.filter(status=True).aggregate(Sum('Discount_amount'))
    total_purchase_shipping = Purchase_info.objects.filter(status=True).aggregate(Sum('additional_ship_charges'))
    purchase_total_return = Purchase_info.objects.filter(status=True, purchase_return=1).aggregate(Sum('purchase_total'))

    stock_total_adjustment = StockAdjustment.objects.filter(status=True).aggregate(Sum('total_amount_recovered'))

    sale_total = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('total_payable'))
    total_selling_discount = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('discount_amount'))
    total_sale_return = Sell.objects.filter(status=1, sale_return=1, is_deleted=False).aggregate(Sum('total_payable'))

    open_stock_fig = opening_stock['total'] if opening_stock['total'] else 0.00
    pur_total_fig = purchase_total['purchase_total__sum'] if purchase_total['purchase_total__sum'] else 0.00
    sale_fig = sale_total['total_payable__sum'] if sale_total['total_payable__sum'] else 0.00

    closing_stock_total = (open_stock_fig + pur_total_fig) - (sale_fig)
    gross_profit_total = (sale_fig) - (pur_total_fig)

    closing_stock_total = closing_stock_total if closing_stock_total else 0.00
    pur_disc_fig = purchase_total_discount['Discount_amount__sum'] if purchase_total_discount['Discount_amount__sum'] else 0.00
    pur_ship_fig = total_purchase_shipping['additional_ship_charges__sum'] if total_purchase_shipping['additional_ship_charges__sum'] else 0.00
    sell_disc_fig = total_selling_discount['discount_amount__sum'] if total_selling_discount['discount_amount__sum'] else 0.00
    pur_return_fig = purchase_total_return['purchase_total__sum'] if purchase_total_return['purchase_total__sum'] else 0.00
    sale_return_fig = total_sale_return['total_payable__sum'] if total_sale_return['total_payable__sum'] else 0.00

    net_profit = (
        closing_stock_total + sale_fig + pur_disc_fig + pur_return_fig) - (open_stock_fig + pur_total_fig + pur_ship_fig + sell_disc_fig + sale_return_fig)

    product_base_profit = Product.objects.select_related('brand', 'category').annotate(fname=F('brand__brand_name'),fname2=F('category__name'))

    for event in product_base_profit:
        print(event.fname, event.fname2)
    
    busienss_locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/profit_loss_report.html', {'locations':busienss_locations, 
                        'total_selling_discount':total_selling_discount['discount_amount__sum'], 'sale_total':sale_total['total_payable__sum'],
                        'purchase_total_return':purchase_total_return['purchase_total__sum'], 'gross_profit_total':gross_profit_total, 'net_profit':net_profit,
                        'total_sale_return':total_sale_return['total_payable__sum'], 'closing_stock_total':closing_stock_total,
                        'opening_stock':opening_stock['total'], 'purchase_total':purchase_total['purchase_total__sum'], 
                        'total_purchase_shipping':total_purchase_shipping['additional_ship_charges__sum'],
                        'total_stock_adjustment':stock_total_adjustment['total_amount_recovered__sum'],
                        'purchase_total_discount':purchase_total_discount['Discount_amount__sum'],
    })


def tax_report(request):
    return render(request,'divmart_dashboard/tax_report.html') 

def customer_supplier_report(request):
    return render(request,'divmart_dashboard/customer_supplier_report.html') 

def customer_groups_report(request):
    return render(request,'divmart_dashboard/customer_groups_report.html') 

class StockReportSerializer(serializers.ModelSerializer):

    prod_sales = serializers.SerializerMethodField()
    prod_trans = serializers.SerializerMethodField()
    prod_adjst = serializers.SerializerMethodField()
    max_prod_sale = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['SKU', 'product_name', 'purchase_price', 'current_stock', 'prod_sales', 'prod_trans', 'prod_adjst', 'max_prod_sale', 'location']

    def get_location(self, obj):

        try:
            stock_adjust_location = StockProdAdjustment.objects.get(product=obj)
            return stock_adjust_location.stock_adjustment.business_location.name
        except:
            pass

    def get_prod_sales(self, obj):
        items = ItemSold.objects.filter(items_name=obj).aggregate(Sum('quantity'))
        sale_obj = items['quantity__sum'] if items['quantity__sum'] else 0.00
        return sale_obj

    def get_prod_trans(self, obj):
        prods = StockProdTransfer.objects.filter(product=obj).aggregate(Sum('quantity'))
        prod_return = prods['quantity__sum'] if prods['quantity__sum'] else 0.00
        return prod_return

    def get_prod_adjst(self, obj):
        prods = StockProdAdjustment.objects.filter(product=obj).aggregate(Sum('quantity'))
        prod_return = prods['quantity__sum'] if prods['quantity__sum'] else 0.00
        return prod_return

    def get_max_prod_sale(self, obj):

        item_list = []
        items = ItemSold.objects.filter(items_name=obj).aggregate(Sum('quantity'))
        for item in items:
            item_list.append(item)
        for tem in items:
            if max(item_list) == tem:
                return obj.product_name


from django_filters.rest_framework import DjangoFilterBackend
class StockReportView(generics.ListAPIView):

    queryset = Product.objects.filter(status=True)
    serializer_class = StockReportSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['product_name_set']

    # @method_decorator(login_required(login_url='/useraccount/common_login'))
    # def get(self, *args, **kwargs):
    #     products = Product.objects.filter(status=True)
    #     serializer = self.serializer_class(products, many=True)
    #     return Response(serializer.data, status=200)


@login_required(login_url='/useraccount/common_login')
def stock_report(request): # need to check

    # if request.method == 'POST':

    #     product = request.POST.get('product')
    #     category = request.POST.get('category')
    #     brand = request.POST.get('brand')

    #     stocks = Product.objects.filter(Q(product_name__icontains = product)) | Q(category__name__icontains = category) | Q(brand__brand_name__icontains = brand).filter(status=True)

    # else:
    #     stocks = Product.objects.filter(status=True)

    # prod_sales = stocks.annotate(no_of_sales = Count('itemsold'))
    # prod_trans = stocks.annotate(no_of_sales = Count('stockprodtransfer'))

    # prod = Product.objects.annotate(no_of_sales = Count('stockprodadjustment'))
    # products = Product.objects.prefetch_related('items_name').filter(status=True)

    url = f'{settings.BASE_DOMAIN}/dashboard/stocks'
    stocks = requests.get(url).json()

    # categories = Category.objects.filter(status=True)
    # brands = Brand.objects.filter(status=True)

    return render(request,'divmart_dashboard/stock_report.html', {'stocks':stocks}) 


@login_required(login_url='/useraccount/common_login')
def lot_report(request): # need to check

    # if request.method == 'POST':
    #     category = request.POST.get('category')
    #     brand = request.POST.get('brand')
    #     product = request.POST.get('product')

    #     if category != '':
    #         products = Product.objects.filter(status=True).filter(category__name__icontains = category)
    #     if brand != '':
    #         products = Product.objects.filter(status=True).filter(brand__brand_name__icontains = brand)
    #     if product != '':
    #         products = Product.objects.filter(status=True).filter(product_name__icontains = product)

    # else:
    #     products = Product.objects.filter(status=True)

    url = f'{settings.BASE_DOMAIN}/dashboard/stocks'
    products = requests.get(url).json()

    # categories = Category.objects.filter(status=True)
    # brands = Brand.objects.filter(status=True)

    return render(request,'divmart_dashboard/lot_report.html', {'products':products}) 


# @login_required(login_url='/useraccount/common_login')
def trending_products_report(request):

    url = f'{settings.BASE_DOMAIN}/dashboard/stocks'
    trending_prods = requests.get(url)
    prods_ = trending_prods.json()
    return render(request,'divmart_dashboard/trending_products_report.html', {'prods':prods_}) 


def stock_adjustment_report(request):

    url = f'{settings.BASE_DOMAIN}/dashboard/stocks'
    stock_adjust_objs = requests.get(url).json()
    stock_adjust = ''

    if request.method == 'POST':
        location = request.POST.get('business_location')
        type = request.POST.get('type')

        # for objs in stock_adjust_objs:
        if location and type in stock_adjust_objs:  
            stock_adjust = requests.get(url).json()

    else:
        stock_adjust = stock_adjust_objs

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/stock_adjustment_report.html', {'stock_adjust':stock_adjust, 'locations':locations}) 


class ItemReportSerializer(serializers.ModelSerializer):

    purchase_date = serializers.SerializerMethodField()
    purchase_quantity = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    purchase_price = serializers.SerializerMethodField()
    sale_date = serializers.SerializerMethodField()
    sale_quantity = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'purchase_date', 'purchase_quantity', 'supplier', 'purchase_price', 'sale_date', 'sale_quantity', 'customer', 'sale_price', 'subtotal']

    def get_purchase_date(self, obj):
        date_obj = Purchase.objects.filter(product_name=obj)
        for date in date_obj:
            obj_date = date.purchase_details.purchase_date
            return obj_date

    def get_purchase_quantity(self, obj):
        quantity_obj = Purchase.objects.filter(product_name=obj)
        for quan in quantity_obj:
            return quan.purchase_quantity

    def get_supplier(self, obj):
        supplier_obj = Purchase.objects.filter(product_name=obj)
        for supp in supplier_obj:
            return supp.purchase_details.supplier.business_name

    def get_purchase_price(self, obj):
        pur_price_obj = Purchase.objects.filter(product_name=obj)
        for pur_price in pur_price_obj:
            return pur_price.unit_cost_before_tax
    
    def get_sale_date(self, obj):
        sale_date_obj = ItemSold.objects.filter(items_name = obj)
        for sale_date in sale_date_obj:
            return sale_date.sell.sale_date

    def get_sale_quantity(self, obj):
        sale_quantity = ItemSold.objects.filter(items_name = obj)
        for quan in sale_quantity:
            return quan.quantity

    def get_customer(self, obj):
        customer_obj = ItemSold.objects.filter(items_name = obj)
        for customer in customer_obj:
            return customer.sell.customer.first_name

    def get_sale_price(self, obj):
        sale_price_obj = ItemSold.objects.filter(items_name = obj)
        for sale_price in sale_price_obj:
            return sale_price.price

    def get_subtotal(self, obj):
        sub_total_obj = ItemSold.objects.filter(items_name = obj)
        for sub_total in sub_total_obj:
            return sub_total.sub_total


class ItemReportView(generics.ListAPIView):

    queryset = Product.objects.filter(status=True)
    serializer_class = ItemReportSerializer
    # filter_backends = [DjangoFilterBackend]
    # search_fields = ['product_name']

    # @method_decorator(login_required(login_url='/useraccount/common_login'))
    # def get(self, *args, **kwargs):
    #     products = Product.objects.filter(status=True)
    #     serializer = self.serializer_class(products, many=True)
    #     return Response(serializer.data, status=200)


@login_required(login_url='/useraccount/common_login')
def items_report(request): # not done yet

    # products = Purchase.objects.filter(status=True)
    # sales = ItemSold.objects.all()
    # prod_sales = zip(products, sales)

    url = f'{settings.BASE_DOMAIN}/dashboard/items'
    url_json = requests.get(url).json()

    supplier_user = SupplierUser.objects.filter(is_deleted=0)
    customer_user = CustomerUser.objects.filter(is_deleted=0)
    return render(request,'divmart_dashboard/items_report.html', {
        # 'clubbed_pur_sale':prod_sales, 
        'products':url_json, 'supplier_users':supplier_user, 'customer_user':customer_user
        # 'sales':sales
    })


@login_required(login_url='/useraccount/common_login')
def product_purchase_report(request):

    if request.method == 'POST':

        supplier = request.POST.get('supplier')
        location = request.POST.get('location')

        if location == '' or location == None:
            purchases = Purchase.objects.filter(Q(purchase_details__supplier__business_name__icontains = supplier) & Q(purchase_details__business_location__name__icontains = location)).filter(status=True)
        else:
            purchases = Purchase.objects.filter(purchase_details__business_location__name__icontains = location).filter(status=True)

    else:
        purchases = Purchase.objects.filter(status=True)

    busienss_locations = BusinessLocation.objects.filter(status=True)
    suppliers = SupplierUser.objects.all()
    return render(request,'divmart_dashboard/product_purchase_report.html', {'purchases':purchases, 'locations':busienss_locations, 'suppliers':suppliers})


@login_required(login_url='/useraccount/common_login')
def product_sell_report(request):

    if request.method == 'POST':
        customer = request.POST.get('customer')
        location = request.POST.get('location')

        prod_sell = ItemSold.objects.filter(Q(sell__customer__first_name__icontains = customer) & Q(sell__business_location__name__icontains = location))

    else:
        prod_sell = ItemSold.objects.all()

    customers = CustomerUser.objects.all()
    busienss_locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/product_sell_report.html', {'prod_sell':prod_sell, 'customers':customers, 'locations':busienss_locations})
     

@login_required(login_url='/useraccount/common_login')
def purchase_payment_report(request): # fine

    if request.method == 'POST':
        supplier = request.POST.get('supplier')
        location = request.POST.get('location')

        purchase_pays = Purchase_info.objects.filter(Q(supplier__business_name__icontains = supplier) & Q(business_location__name__icontains = location)).filter(status=True)

    else:
        purchase_pays = Purchase_info.objects.filter(status=True)

    busienss_locations = BusinessLocation.objects.filter(status=True)
    suppliers = SupplierUser.objects.all()
    return render(request,'divmart_dashboard/purchase_payment_report.html', {'purchases':purchase_pays, 'locations':busienss_locations, 'suppliers':suppliers}) 


@login_required(login_url='/useraccount/common_login')
def sell_payment_report(request): # fine

    if request.method == 'POST':
        location = request.POST.get('location')
        customer = request.POST.get('customer')

        sale_pays = Sell.objects.filter(Q(business_location__name__icontains = location) & Q(customer__first_name__icontains = customer)).filter(status='F', is_deleted=False)

    else:
        sale_pays = Sell.objects.filter(status='F', is_deleted=False)

    customers = CustomerUser.objects.all()
    busienss_locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/sell_payment_report.html', {'sales':sale_pays, 'locations':busienss_locations, 'customers':customers}) 


@login_required(login_url='/useraccount/common_login')
def expense_report(request): # fine

    if request.method == 'POST':
        location = request.POST.get('location')
        category = request.POST.get('category')

        expenses = Expenses.objects.filter(Q(business_location__name__icontains = location) & Q(expense_category__name__icontains = category)).filter(status=True)

    else:
        expenses = Expenses.objects.filter(status=True)

    busienss_locations = BusinessLocation.objects.filter(status=True)
    exp_categories = Expenses_category.objects.filter(status=True)
    return render(request,'divmart_dashboard/expense_report.html', {'expenses':expenses, 'locations':busienss_locations, 'categories':exp_categories}) 


def register_report(request):
    cashiers = StaffUser.objects.filter(Q(role__title='Cashier') | Q(role__title='cashier') | Q(role__title='CASHIER'))
    return render(request,'divmart_dashboard/register_report.html', {'cashiers':cashiers}) 


def stock_transfer_report(request):

    if request.method == "POST":
        location = request.POST.get('business_location')
        date_range = request.POST.get('date')

        try:
            date_split = date_range.split('T')[0]
            year = date_split.split('-')[0]
            month = date_split.split('-')[1]
            day = date_split.split('-')[2]
            
            if date_range == '' or date_range == None:
                transfer_list = StockTransfer.objects.filter(location_from__name=location).filter(status=True)
            else:
                transfer_list = StockTransfer.objects.filter(date__year = year, date__month = month, date__day = day).filter(status=True)
        except:
            transfer_list = StockTransfer.objects.filter(location_from__name=location, status=True).filter(status=True)

    else:
        transfer_list = StockTransfer.objects.filter(status=True)

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/stock_transfer_report.html', {'locations':locations, 'transfer_list': transfer_list})


def sales_representative_report(request):

    if request.method == 'POST':
        user = request.POST.get('cashier')
        location = request.POST.get('location')
        date_range = request.POST.get('date_range')

        try:
            date_split = date_range.split('T')[0]
            year = date_split.split('-')[0]
            month = date_split.split('-')[1]
            day = date_split.split('-')[2]

            sell_objs = Sell.objects.filter(Q(cashier__role__title='cashier') | Q(cashier__role__title='Cashier') | Q(cashier__role__title='CASHIER')).filter(Q(cashier__username=user) | Q(business_location__name=location) | Q(sale_date__year=year, sale_date__month=month, sale_date__day=day)).filter(sale_return=0, status='F', is_deleted=False)
            
        except:
            sell_objs = Sell.objects.filter(Q(cashier__role__title='cashier') | Q(cashier__role__title='Cashier') | Q(cashier__role__title='CASHIER')).filter(Q(cashier__username=user) | Q(business_location__name=location)).filter(sale_return=0, status='F', is_deleted=False)

    else:
        sell_objs = Sell.objects.filter(Q(cashier__role__title='cashier') | Q(cashier__role__title='Cashier') | Q(cashier__role__title='CASHIER')).filter(sale_return=0, status='F', is_deleted=False)

    total_amount_sum = sell_objs.aggregate(Sum('total_amount'))
    total_paid = sell_objs.aggregate(Sum('payment_info__amount'))
    total_due = sell_objs.aggregate(Sum('payment_info__payment_due'))

    staff_users = StaffUser.objects.filter(is_deleted=0).filter(Q(role__title='cashier') | Q(role__title='Cashier') | Q(role__title='CASHIER'))

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/sales_representative_report.html', {'sales_list':sell_objs, 'cashier':staff_users, 'locations':locations, 'total_amount':total_amount_sum['total_amount__sum'], 'total_paid':total_paid['payment_info__amount__sum'], 'total_due':total_due['payment_info__payment_due__sum']}) 


@login_required(login_url='/useraccount/common_login')
def payment_balance_sheet(request):
    suppl_due = SupplierUser.objects.all().aggregate(Sum('total_purchase_due'))
    cust_due = CustomerUser.objects.all().aggregate(Sum('total_sales_due'))
    cust_due = CustomerUser.objects.all().aggregate(Sum('total_sales_due'))

    opening_stock = Product.objects.filter(status=True).aggregate(total=Sum(F('current_stock')*F('purchase_price')))
    purchase_total = Purchase_info.objects.filter(status=True).aggregate(Sum('purchase_total'))
    sale_total = Sell.objects.filter(status='F', is_deleted=False).aggregate(Sum('total_payable'))

    opening_stock_fig = opening_stock['total'] if opening_stock['total'] else 0.00
    purchase_fig = purchase_total['purchase_total__sum'] if purchase_total['purchase_total__sum'] else 0.00
    sales_fig = sale_total['total_payable__sum'] if sale_total['total_payable__sum']else 0.00

    closing_stock_total = (opening_stock_fig + purchase_fig) - (sales_fig)
    return render(request,'divmart_dashboard/payment_balance_sheet.html', {
                                                        'sdue':suppl_due['total_purchase_due__sum'],
                                                        'pdue':cust_due['total_sales_due__sum'],
                                                        'c_s':closing_stock_total,
    }) 


@login_required(login_url='/useraccount/common_login')
def payment_trial_balance(request):

    suppl_due = SupplierUser.objects.all().aggregate(Sum('total_purchase_due'))
    cust_due = CustomerUser.objects.all().aggregate(Sum('total_sales_due'))

    return render(request,'divmart_dashboard/payment_trial_balance.html', {
                                                        'sdue':suppl_due['total_purchase_due__sum'],
                                                        'pdue':cust_due['total_sales_due__sum'],
    })   


@login_required(login_url='/useraccount/common_login')
def payment_account_report(request):

    sale_obj = Sell.objects.filter(status='F', is_deleted=False)
    payment_accounts = PaymentAccount.objects.filter(status=True)
    return render(request,'divmart_dashboard/payment_account_report.html', {'sales':sale_obj, 'accounts':payment_accounts})


@login_required(login_url='/useraccount/common_login')
def register_details(request):

    today = datetime.datetime.now()
    cash_trans = Add_Payments.objects.filter(payment_status=True, payment_method=0, created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).aggregate(Sum('amount'))
    card_trans = Add_Payments.objects.filter(payment_status=True, payment_method=1, created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).aggregate(Sum('amount'))
    cheque_trans = Add_Payments.objects.filter(payment_status=True, payment_method=2, created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).aggregate(Sum('amount'))
    banktrans_obj = Add_Payments.objects.filter(payment_status=True, payment_method=3, created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).aggregate(Sum('amount'))
    other_trans = Add_Payments.objects.filter(payment_status=True, payment_method=4, created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).aggregate(Sum('amount'))

    total_sale_value = ItemSold.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day).aggregate(Sum('sub_total'))
    sales_from_sell = Sell.objects.filter(status='F', sale_date__year=today.year, sale_date__month=today.month, sale_date__day=today.day, is_deleted=False).aggregate(Sum('payment_info__amount'))

    new_list = []
    brands = Brand.objects.all()
    for brand in brands:
        new_dict = {}
        sold = ItemSold.objects.filter(items_name__brand__brand_name=brand, date__year=today.year, date__month=today.month, date__day=today.day).aggregate(Sum('quantity'))
        sub_total_sold = ItemSold.objects.filter(items_name__brand__brand_name=brand, date__year=today.year, date__month=today.month, date__day=today.day).aggregate(Sum('sub_total'))

        new_dict['brand'] = brand.brand_name
        new_dict['sold'] = sold['quantity__sum']
        new_dict['sub_total'] = sub_total_sold['sub_total__sum']

        new_list.append(new_dict)

    staff_users = StaffUser.objects.filter(is_deleted = 0)
    return render(request, 'divmart_dashboard/registerdetails.html', {
                                                'cash':cash_trans['amount__sum'],
                                                'card':card_trans['amount__sum'],
                                                'cheque':cheque_trans['amount__sum'],
                                                'bank':banktrans_obj['amount__sum'],
                                                'other':other_trans['amount__sum'],
                                                'new_dict':new_list,
                                                'total_sale_value':total_sale_value['sub_total__sum'],
                                                'sale_value_from_payments':sales_from_sell['payment_info__amount__sum'],
                                                'staff_users':staff_users,
    })


@login_required(login_url='/useraccount/common_login')
def list_purchase_return(request):

    if request.method == "POST":
        location = request.POST.get('business_location')
        purchase_return_list = Purchase_info.objects.filter(status=True, purchase_return=1, business_location__name=location)

    else:
        purchase_return_list = Purchase_info.objects.filter(status=True, purchase_return=1)

    locations = BusinessLocation.objects.filter(status=True)
    return render(request,'divmart_dashboard/list_purchase_return.html', {'returns':purchase_return_list, 'locations':locations})


@login_required(login_url='/useraccount/common_login')
def list_sell_return(request):
    sell_return_list = Sell.objects.filter(status='F', sale_return=1, is_deleted=False)
    return render(request,'divmart_dashboard/list_sell_return.html', {'returns':sell_return_list}) 


@login_required(login_url='/useraccount/common_login')
# @group_required('Cashier')
def customer_detail(request,id):

    items_sold_of_sales = ''
    cust = CustomerUser.objects.get(id=id)
    sale_of_customer = Sell.objects.filter(customer_id=cust, status='F', is_deleted=False)
    total_sale_value_of_cusotomer = sale_of_customer.aggregate(Sum('total_payable'))['total_payable__sum']
    total_sale_payment_of_cusotomer = sale_of_customer.aggregate(Sum('payment_info__amount'))['payment_info__amount__sum']
    total_sale_due_of_cusotomer = sale_of_customer.aggregate(Sum('payment_info__payment_due'))['payment_info__payment_due__sum']
    sale_return_of_customer = Sell.objects.filter(sale_return=1, is_deleted=False)

    for sale in sale_of_customer:
        items_sold_of_sales = ItemSold.objects.filter(sell=sale)
    return render(request,'divmart_dashboard/customer_detail.html', {
                            'cust':cust, 'sales':sale_of_customer, 'sale_retun':sale_return_of_customer,
                            'sale_value':total_sale_value_of_cusotomer, 'items_sold':items_sold_of_sales,
                            'sale_payment':total_sale_payment_of_cusotomer, 'sale_due':total_sale_due_of_cusotomer,
    })


@login_required(login_url='/useraccount/common_login')
# @group_required('Cashier')
def invoice_view(request, id):

    sell_obj = Sell.objects.get(id=id, is_deleted=False)
    items_sold = ItemSold.objects.filter(sell=sell_obj)

    login_user = User.objects.get(username=request.user.username).username
    return render(request, 'divmart_dashboard/invoice_view.html', {
                                'items_sold':items_sold, 'obj':sell_obj, 'staff':login_user,
    })


@login_required(login_url='/useraccount/common_login')
def customer_group_detail(request):
    customer_group = CustomerGroups.objects.filter(is_deleted=0)
    return render(request,'divmart_dashboard/customer_group_detail.html',{'customer_group':customer_group})


@login_required(login_url='/useraccount/common_login')
# @group_required('Cashier')
def customer_edit(request, id):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        credit_limit = request.POST.get('credit_limit', 0)
        contact_id = request.POST.get('contact_id')
        tax_number = request.POST.get('tax_number')
        opening_balance = request.POST.get('opening_balance')
        pay_term = request.POST.get('pay_term')
        customer_group = request.POST.get('customer_group')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        alternative_contact = request.POST.get('alternative_contact')
        Landline = request.POST.get('Landline')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        land_mark = request.POST.get('land_mark')

        CustomerUser.objects.filter(id=id).update(first_name=first_name, credit_limit=credit_limit, contact_id=contact_id, tax_number=tax_number, opening_balance=opening_balance, pay_term=pay_term, customer_group=customer_group, email=email, mobile=mobile, alternative_contact=alternative_contact, Landline=Landline, city=city, state=state, country=country, land_mark=land_mark)
        
        messages.success(request, 'customer update success...!')
        return redirect('customer_list')

    customer_obj = CustomerUser.objects.get(id=id)
    customer_group = CustomerGroups.objects.filter(is_deleted=0)
    return render(request, 'divmart_dashboard/customer_edit.html', {'obj':customer_obj, 'customer_group':customer_group})


@login_required(login_url='/useraccount/common_login')
def customer_delete(request, id):

    customer_obj = CustomerUser.objects.get(id=id)
    customer_obj.is_deleted = 1
    customer_obj.save()
    return redirect('customer_list')


@login_required(login_url='/useraccount/common_login')
def product_view(request, id):
    prod_obj = Product.objects.get(status=True, id=id)
    return render(request, 'divmart_dashboard/product_view.html', {'obj':prod_obj})


@login_required(login_url='/useraccount/common_login')
def product_delete(request, id):

    product_obj = Product.objects.get(id=id, status=True)
    product_obj.status = False
    product_obj.save()
    return redirect('list_products')


@login_required(login_url='/useraccount/common_login')
def delete_purchase(request, id):
    p_obj = Purchase_info.objects.get(id=id, status=True)
    p_obj.status=False
    p_obj.save()
    messages.success(request, 'Purchase delete success...')
    return redirect('list_purchase')


@login_required(login_url='/useraccount/common_login')
def all_withdrawal_request(request):
    withdraw_requests = WithdrawlTransactionRequests.objects.filter(Q(payment_status='Pending') | Q(payment_status='Rejected'))

    if request.method == "GET" and request.is_ajax():
        with_obj = WithdrawlTransactionRequests.objects.get(id=request.GET.get('id'))
        with_obj.payment_status = request.GET.get('payment_status', None)
        with_obj.save()
        messages.success(request, 'status change success...')
    return render(request,'divmart_dashboard/all_withdrawal_request.html', {'all_list':withdraw_requests})


@login_required(login_url='/useraccount/common_login')
def transaction_history(request):
    withdraw_requests = WithdrawlTransactionRequests.objects.filter(payment_status='Paid')
    return render(request, 'divmart_dashboard/transaction_history.html', {'paid_requests':withdraw_requests})


from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from dashboard.models import Product, Sell
from useraccount.models import CustomerUser
from div_settings.models import *
from sale.models import *
from datetime import datetime
from dashboard.models import *
from membership.crons import CreditedPointsSerializer


# from my side...
@login_required(login_url='/useraccount/common_login')
def sale_list(request):
    sell_list = ''

    if request.method == 'POST':
        location = request.POST.get('business_location')
        # customer = request.POST.get('customer')
        date = request.POST.get('date')

        try:
            date_split = date.split('T')[0]
            year = date_split.split('-')[0]
            month = date_split.split('-')[1]
            day = date_split.split('-')[2]

            if date == '' or date == None:
                if request.user.is_superuser:
                    sell_list = Sell.objects.filter(business_location__name__icontains = location).filter(status='F', is_deleted=False)
                else:
                    sell_list = Sell.objects.filter(status='F', business_location=StaffUser.objects.get(user=request.user).business_location)

            elif location == '' or location == None:
                if request.user.is_superuser:
                    sell_list = Sell.objects.filter(sale_date__year = year, sale_date__month = month, sale_date__day = day).filter(status='F', is_deleted=False)
                else:
                    sell_list = Sell.objects.filter(sale_date__year = year, sale_date__month = month, sale_date__day = day).filter(status='F', business_location=StaffUser.objects.get(user=request.user).business_location)

            else:
                if request.user.is_superuser:
                    sell_list = Sell.objects.filter(Q(sale_date__year = year, sale_date__month = month, sale_date__day = day) & Q(business_location__name__icontains = location)).filter(status='F', is_deleted=False)
                else:
                    sell_list = Sell.objects.filter(sale_date__year = year, sale_date__month = month, sale_date__day = day).filter(status='F', business_location=StaffUser.objects.get(user=request.user).business_location)
              
        except Exception as e:
            # print('---error----', e)
            if request.user.is_superuser:
                sell_list = Sell.objects.filter(business_location__name__icontains = location).filter(status='F', is_deleted=False)
            else:
                sell_list = Sell.objects.filter(status='F', business_location=StaffUser.objects.get(user=request.user).business_location)

    else:
        if request.user.is_superuser:
            sell_list = Sell.objects.filter(status="Final", is_deleted=False)
        else:
            sell_list = Sell.objects.filter(status="Final", business_location=StaffUser.objects.get(user=request.user).business_location, is_deleted=False)

    customers = CustomerUser.objects.filter(is_deleted=0)
    business_locations = BusinessLocation.objects.filter(status=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(sell_list, 5)
    try:
        sell_list = paginator.page(page)
    except PageNotAnInteger:
        sell_list = paginator.page(1)
    except EmptyPage:
        sell_list = paginator.page(paginator.num_pages)

    return render(request,'divmart_dashboard/all_sales_list.html', {'lists':sell_list, 'locations':business_locations, 'customers':customers})


@login_required(login_url='/useraccount/common_login')
# @group_required('Cashier')
def sale_add(request):

    try:
        sale_last = Sell.objects.last()

        last_ref_no = sale_last.ref_no
        last_invoice = sale_last.invoice_no

        spi_last = last_ref_no.split('-')[1]
        last_ref_no = int(spi_last) + 1
        str_ref = 'SL-' + str(last_ref_no)
        last_invoice = int(last_invoice) + 1
    except Exception as e:
        print('---exception in sale-add---', e)
        str_ref = 'SL-10001'
        last_invoice = 10001

    payment_accounts = PaymentAccount.objects.filter(status=True)
    if not request.user.is_superuser:
        staffuser_obj = StaffUser.objects.get(user=request.user)

    if request.method == 'POST':
        count = request.POST.get('count')
        location = request.POST.get('business_location')
        customer = request.POST.get('customer')
        pay_term = request.POST.get('pay_term')
        sale_date = request.POST.get('sale_date')
        status = request.POST.get('status')
        total_amount = request.POST.get('total_amount')
        discount_type = request.POST.get('discount_type')
        discount_amount = request.POST.get('discount_amount', 0)
        shipping_details = request.POST.get('shipping_details', '')
        shipping_charges = request.POST.get('shipping_charges', 0)
        total_payable = request.POST.get('total_payable')
        sell_notes = request.POST.get('sell_notes')
        order_tax = request.POST.get('order_tax')

        pay_amt = request.POST.get("amount", 0)
        pay_method = request.POST.get("pay_method")
        pay_account = request.POST.get("pay_account")

        pay_notes = request.POST.get("pay_notes")
        pay_due = request.POST.get("pay_due", 0)

        bus_locations = BusinessLocation.objects.get(id=location)
        cus_obj = CustomerUser.objects.get(id=customer)
        payment_account_obj = PaymentAccount.objects.get(id=pay_account)

        pay_obj = Add_Payments.objects.create(amount=pay_amt, payment_method=pay_method,payment_account=payment_account_obj, payment_notes=pay_notes,payment_due=pay_due, payment_status=True)

        if pay_method == 3 or pay_method == '3':
            payment_account_obj.openning_balance = float(payment_account_obj.openning_balance) + float(pay_amt)
            payment_account_obj.save()

        cus_obj.total_sales_due = float(cus_obj.total_sales_due) + float(pay_due)
        cus_obj.save()

        # reg_obj = RegisteredMembers.objects.filter(email=cus_obj.email, status=1)
        # product_obj = Product.objects.get(id=id)
        # product_margin = product_obj.margin
        # effected_price = 0

        # if(product_margin >= 1 and product_margin <= 5):
        #     effected_price = 0.10
        # elif(product_margin > 5 and product_margin <= 10):
        #     effected_price = 0.25
        # elif(product_margin > 10 and product_margin <= 15):
        #     effected_price = 0.5
        # elif(product_margin > 15):
        #     effected_price = 1.0

        # final_points = product_obj.selling_price * effected_price
        # data = {'member':reg_obj[0],'points':final_points,'credited_by':'PURCHASE'}
        # ser_obj = CreditedPointsSerializer(data=data)

        # if(ser_obj.is_valid()):
        #     ser_obj.save()

        if not request.user.is_superuser:
            sale_obj = Sell.objects.create(ref_no=str_ref, business_location=bus_locations, customer=cus_obj, pay_term=pay_term, sale_date=sale_date, status=status, total_amount=total_amount, discount_type=discount_type, discount_amount=discount_amount, shipping_details=shipping_details, shipping_charges=shipping_charges, total_payable=total_payable, sell_notes=sell_notes, payment_info=pay_obj, invoice_no=last_invoice, cashier=staffuser_obj, order_tax=order_tax)
        else:
            sale_obj = Sell.objects.create(ref_no=str_ref, business_location=bus_locations, customer=cus_obj, pay_term=pay_term, sale_date=sale_date, status=status, total_amount=total_amount, discount_type=discount_type, discount_amount=discount_amount, shipping_details=shipping_details, shipping_charges=shipping_charges, total_payable=total_payable, sell_notes=sell_notes, payment_info=pay_obj, invoice_no=last_invoice, order_tax=order_tax)

        for v in range(1,int(count)+1):
            prod_name = request.POST.get("nam"+str(v))
            prod_qan = request.POST.get("qan"+str(v))
            unit_price = request.POST.get("usp"+str(v))
            sub_total = request.POST.get("sub"+str(v))
            prod_obj = Product.objects.get(product_name=prod_name)

            if float(prod_obj.current_stock) >= float(prod_qan):
                ItemSold.objects.create(sell=sale_obj, items_name=prod_obj, price=unit_price, quantity=prod_qan, sub_total=sub_total, date=datetime.now())
                prod_obj.current_stock = prod_obj.current_stock - float(prod_qan)
                prod_obj.save()

            else:
                # sale_obj.status = 'D'
                # sale_obj.save()
                sale_obj.delete()

                # pay_obj.payment_status = False
                # pay_obj.save()
                pay_obj.delete()
                
                cus_obj.total_sales_due = float(cus_obj.total_sales_due) - float(pay_due)
                cus_obj.save()
                
                if pay_method == 3 or pay_method == '3':
                    payment_account_obj.openning_balance = float(cus_obj.total_sales_due) - float(pay_due)
                    payment_account_obj.save()

                messages.error(request, 'Not much stock available for selected product/products')
        return redirect('sale_list')

    business_locations = BusinessLocation.objects.filter(status=True)
    customers = CustomerUser.objects.all()

    return render(request,'divmart_dashboard/add_sale.html', {'locations':business_locations, 'customers':customers, 'accounts':payment_accounts})


@login_required(login_url='/useraccount/common_login')
# @group_required("Cashier")
def edit_sales(request, id):

    sale_info = Sell.objects.get(id=id)
    sale_obj = ItemSold.objects.filter(sell=sale_info.id)
    custom_user_obj = CustomerUser.objects.get(id=sale_info.customer.id)
    prod_obj = Product.objects.all()

    try:
        payments_obj = Add_Payments.objects.get(id=sale_info.payment_info.id, payment_status=True)
    except:
        payments_obj = ''

    if request.method == "POST":

        business_location = request.POST.get("business_location")
        customer = request.POST.get("customer")
        pay_term = request.POST.get("pay_term")
        # sale_date = request.POST.get("sale_date", '')
        status = request.POST.get("status")
        total_amount = request.POST.get("total_amount")
        discount_type = request.POST.get("discount_type")
        discount_amount = request.POST.get("discount_amount")
        shipping_details = request.POST.get("shipping_details")
        shipping_charges = request.POST.get("shipping_charges")
        total_payable = request.POST.get("total_payable")
        sell_notes = request.POST.get("sell_notes")

        pay_amt = request.POST.get("amount", 0)
        pay_method = request.POST.get("payment_method")
        pay_account = request.POST.get("payment_account")

        pay_notes = request.POST.get("payment_notes")
        pay_due = request.POST.get("payment_due", 0)
        # payment_account_obj = PaymentAccount.objects.get(id=pay_account)
        pay_id = request.POST.get("payid")

        Add_Payments.objects.filter(id=pay_id).update(amount=pay_amt, payment_method=pay_method, payment_account=pay_account, payment_notes=pay_notes,
                    payment_due=pay_due,payment_status=True)

        bus_locations = BusinessLocation.objects.get(id=business_location)
        cus_obj = CustomerUser.objects.get(id=customer)

        Sell.objects.filter(id=sale_info.id).update(business_location=bus_locations, customer=cus_obj, pay_term=pay_term, status=status, total_amount=total_amount, discount_type=discount_type, discount_amount=discount_amount,shipping_charges=shipping_charges, shipping_details=shipping_details, total_payable=total_payable, sell_notes=sell_notes)
        
        count = request.POST.get("count")
        for v in range(1, int(count) + 1):
            prod_name = request.POST.get("nam"+str(v))
            prod_qan = request.POST.get("qan"+str(v))
            unit_price = request.POST.get("usp"+str(v))
            sub_total = request.POST.get("sub"+str(v))
            sale_id = request.POST.get("sobjid"+str(v))

            items_sold_obj = ItemSold.objects.filter(id=str(sale_id))
            prod_obj = Product.objects.get(product_name=prod_name)

            if items_sold_obj:
                items_sold_obj.update(items_name=prod_obj,quantity=prod_qan,price=unit_price,sub_total=sub_total)
            else:
                pur_info_obj = Sell.objects.get(id=sale_info)
                pur_obj = ItemSold(sell=pur_info_obj, items_name=prod_obj,quantity=prod_qan,price=unit_price,sub_total=sub_total)
                pur_obj.save()

        return redirect('sale_list')

    customer_users = CustomerUser.objects.all()
    business_location_list = BusinessLocation.objects.filter(status=True)
    payment_accounts = PaymentAccount.objects.filter(status=True)

    return render(request,'divmart_dashboard/edit_sales.html',{'per_info':sale_info,'sale_obj':sale_obj,'custom_user_obj':custom_user_obj,'prod_obj':prod_obj, 'users':customer_users, 'locations':business_location_list, 'payments_obj':payments_obj, 'accounts':payment_accounts}) 


def delete_sale(request, id):

    sell_obj = Sell.objects.get(id=id, is_deleted=False)
    sell_obj.is_deleted = True
    sell_obj.save()
    messages.success(request, 'sales remove success...')
    return redirect('/dashboard/sales')


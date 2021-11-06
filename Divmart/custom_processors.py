from dashboard.models import *
from django.db.models import Sum
from django.db.models import F
from datetime import datetime


def custom_data_for_index(request):
    
    today = datetime.now()
    # print('-----today-----', today)

    opening_stock = Product.objects.filter(status=True).aggregate(total=Sum(F('current_stock')*F('purchase_price')))

    purchase_total = Purchase_info.objects.filter(status=True, purchase_date__year=today.year, purchase_date__month=today.month, purchase_date__day=today.day).aggregate(Sum('purchase_total'))
    # print('---purcahse total-----', purchase_total['purchase_total__sum'])

    total_purchase_shipping = Purchase_info.objects.filter(status=True, purchase_date__year=today.year, purchase_date__month=today.month, purchase_date__day=today.day).aggregate(Sum('additional_ship_charges'))

    expense_obj = Expenses.objects.filter(status=True, date__year=today.year, date__month=today.month, date__day=today.day).aggregate(Sum('amount'))

    stock_total_adjustment = StockAdjustment.objects.filter(status=True, date_of_adjust__year=today.year, date_of_adjust__month=today.month, date_of_adjust__day=today.day).aggregate(Sum('total_amount_recovered'))

    sale_total = Sell.objects.filter(status='F', sale_date__year=today.year, sale_date__month=today.month, sale_date__day=today.day).aggregate(Sum('total_payable'))

    opening_stock_fig = opening_stock['total'] if opening_stock['total'] else 0.00
    
    total_purchase_fig = purchase_total['purchase_total__sum'] if purchase_total['purchase_total__sum'] else 0.00
    sale_total_fig = sale_total['total_payable__sum'] if sale_total['total_payable__sum']else 0.00
    
    closing_stock_total = (opening_stock_fig + total_purchase_fig) - (sale_total_fig)

    gross_profit_total = (sale_total_fig) - (total_purchase_fig)

    closing_stock_total = closing_stock_total if closing_stock_total else 0.00
    pur_ship_fig = total_purchase_shipping['additional_ship_charges__sum'] if total_purchase_shipping['additional_ship_charges__sum'] else 0.00

    # total_selling_discount = Sell.objects.filter(status='F', sale_date=today).aggregate(Sum('discount_amount'))
    # total_sale_return = Sell.objects.filter(status=1, sale_return=1, sale_date=today).aggregate(Sum('total_payable'))
    # purchase_total_discount = Purchase_info.objects.filter(status=True, purchase_date=today).aggregate(Sum('Discount_amount'))
    # purchase_total_return = Purchase_info.objects.filter(status=True, purchase_return=1, purchase_date=today).aggregate(Sum('purchase_total'))
    # pur_disc_fig = purchase_total_discount['Discount_amount__sum'] if purchase_total_discount['Discount_amount__sum'] else 0.00
    # sell_disc_fig = total_selling_discount['discount_amount__sum'] if total_selling_discount['discount_amount__sum'] else 0.00
    # pur_return_fig = purchase_total_return['purchase_total__sum'] if purchase_total_return['purchase_total__sum'] else 0.00
    # sale_return_fig = total_sale_return['total_payable__sum'] if total_sale_return['total_payable__sum'] else 0.00

    net_profit = (closing_stock_total + sale_total_fig) - (opening_stock_fig + total_purchase_fig + pur_ship_fig)

    try:
        staff_obj = StaffUser.objects.get(user=request.user)
    except Exception as e:
        # print('error as exception------', e)
        staff_obj = request.user

    return { 
        'opening_stock':opening_stock['total'],
        'purchase':purchase_total['purchase_total__sum'],
        'stock_adjustment':stock_total_adjustment['total_amount_recovered__sum'],
        'shipping_charges':total_purchase_shipping['additional_ship_charges__sum'],
        'closing_stock':closing_stock_total,
        'sales':sale_total['total_payable__sum'],
        'stock_recovered':stock_total_adjustment['total_amount_recovered__sum'],
        'gross':gross_profit_total,
        'net':net_profit,
        'expense':expense_obj['amount__sum'],
        'user':staff_obj,
    }
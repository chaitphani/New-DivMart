from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


# from my side...
@login_required(login_url='/useraccount/common_login')
def business_location_list(request):

    if request.method == 'POST':
        form = BusinessLocationForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.save()
            if form_save.location_id == '' or form_save.location_id == None:
                form_save.location_id = 'LOC-1000' + str(form_save.id)
            form_save.save()
            messages.success(request, 'added a business location ' + str(form_save.name))
            return redirect('business-location')
    else:
        form = BusinessLocationForm()

    list_locations = BusinessLocation.objects.filter(status=True).order_by('-id')
    return render(request, 'divmart_dashboard/business_location_list.html', {'lists':list_locations,'form':form})


@login_required(login_url='/useraccount/common_login')
def business_location_update(request, id):

    loc_obj = BusinessLocation.objects.get(id=id)
    if request.method == 'POST':
        form = BusinessLocationForm(request.POST, instance=loc_obj)
        if form.is_valid():
            form.save()
            messages.success(request, str(loc_obj.name) +' update success...')
            return redirect('business-location')
    else:
        form = BusinessLocationForm(instance=loc_obj)
    
    return render(request, 'divmart_dashboard/business_location_edit.html', {'form':form, 'loc_obj':loc_obj})


@login_required(login_url='/useraccount/common_login')
def business_location_delete(request, id):

    loc_obj = BusinessLocation.objects.get(id=id)
    if loc_obj:
        loc_obj.status = False
        loc_obj.save()
        messages.info(request, str(loc_obj.name) + ' remove success..')
        return redirect('business-location')

@login_required(login_url='/useraccount/common_login')
def add_tax_rate(request):

    if request.method == 'POST':
        form = TaxRateForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.status = True
            form_save.save()
            return redirect('tax-rate')
    else:
        form = TaxRateForm()
    
    tax_rates = TaxRate.objects.filter(status=True)
    return render(request, 'divmart_dashboard/tax_rate.html', {'rates':tax_rates})

@login_required(login_url='/useraccount/common_login')
def edit_tax_rate(request, id):

    tax_rate_obj = TaxRate.objects.get(id=id, status=True)
    if request.method == 'POST':
        form = TaxRateForm(request.POST, instance = tax_rate_obj)
        if form.is_valid():
            form.save()
            return redirect('tax-rate')
    else:
        form = TaxRateForm(instance=tax_rate_obj)
    return render(request, 'divmart_dashboard/tax_rate_edit.html', {'obj':tax_rate_obj})


@login_required(login_url='/useraccount/common_login')
def delete_tax_rate(request, id):
    tax_rate_obj = TaxRate.objects.get(id=id, status=True)
    tax_rate_obj.status = False
    tax_rate_obj.save()
    return redirect('tax-rate')
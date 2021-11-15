from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from membership.decorator import is_authenticated
from membership.models import *


@is_authenticated
def home(request):

    session_val = request.session.get('email')
    mem_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).first()
    ref_link = settings.BASE_DOMAIN + "/member/register?ref_id=" + mem_obj.self_ref_id

    withdraw_trans_points = WithdrawlTransactionRequests.objects.filter(member=mem_obj, payment_status=1)
    if len(withdraw_trans_points) > 0:
        withdraw_trans_points.last()
        
    return render(request,'membership/dashboard.html', {'obj':mem_obj, 'with_points':withdraw_trans_points, 'ref_link':ref_link})


@is_authenticated
def manage_directs(request):

    session_val = request.session.get('email')
    memo_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).filter(status=1).first()

    if request.method == 'POST':
        status = request.POST.get('status')
        resp_obj = RegisteredMembers.objects.filter(sponser_id=memo_obj.self_ref_id, status=status)
    else:
        resp_obj = RegisteredMembers.objects.filter(sponser_id=memo_obj.self_ref_id)
    return render(request,'membership/manage_directs.html',{'resp_data':resp_obj, 'obj':memo_obj})


@is_authenticated
def direct_transaction(request):
    val = True
    li = []

    session_val = request.session.get('email')
    mem_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).first()
    li.append(mem_obj.id)
    if mem_obj:
        while val:
            mem1 = RegisteredMembers.objects.filter(sponser_id=mem_obj.self_ref_id).first()		
            if mem1:
                li.append(mem1.id)
                mem_obj = mem1     
            else:
                val=False
    members = RegisteredMembers.objects.filter(id__in=li)
    
    return render(request,'membership/direct_transaction.html', {'obj':mem_obj, 'resp_data':members})


@is_authenticated
def withdrawal_transaction(request):

    session_val = request.session.get('email')
    mem_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).first()
    withdraw_trans = WithdrawlTransactionRequests.objects.filter(member=mem_obj)

    pending_trans_exist = WithdrawlTransactionRequests.objects.filter(member=mem_obj, payment_status='Pending')
    if len(pending_trans_exist) > 0:
        pending_trans_exist.last()

    return render(request,'membership/withdrawal_transaction.html', {'obj':mem_obj, 'withdraw_trans':withdraw_trans, 'exist':pending_trans_exist})


@is_authenticated
def withdrawal_request(request):

    session_val = request.session.get('email')
    mem_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).first()

    if request.method == 'POST':
        amount_withdraw = request.POST.get('amount', 1.0)
        user_note = request.POST.get('user_note')
        if float(amount_withdraw) >= 100:
            withdraw_obj = WithdrawlTransactionRequests.objects.create(amount=amount_withdraw, user_note=user_note, member=mem_obj)
            messages.success(request, 'Request submitted...')
            return redirect('withdrawal-transaction')
        else:
            messages.error(request, 'requested amount should be greater than 100..')
    return render(request, 'membership/withdrawal_request.html', {'memo_obj':mem_obj})


@is_authenticated
def point_transaction(request):

    session_val = request.session.get('email')
    mem_obj = RegisteredMembers.objects.filter(Q(email=session_val) | Q(self_ref_id=session_val)).first()

    points_trans = PointsTransactionRequests.objects.filter(member=mem_obj)
    return render(request,'membership/point_transaction.html', {'obj':mem_obj, 'points':points_trans}) 

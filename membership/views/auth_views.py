from django.shortcuts import render, redirect
from django.contrib import messages

from membership.models import *
from membership.decorator import is_authenticated


def member_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        try:
            try:
                email_member = RegisteredMembers.objects.get(email=email, password=pwd, status=1)
                if email_member:
                    request.session['email'] = email
                    return redirect('home-member')
            except Exception as e:
                ref_obj = RegisteredMembers.objects.get(self_ref_id=email, password=pwd, status=1)
                if ref_obj:
                    request.session['email'] = email
                    return redirect('home-member')
        except Exception as e:
            print('---error at member-login----', e)
            messages.error(request, 'member not found with the provided details, contact admin...!')
    return render(request, 'membership/member_login.html')


def member_signup(request):
    return render(request,'membership/member_signup.html')

    
@is_authenticated
def member_logout(request):

    try:
        del request.session['email']
    except Exception as e:
        pass
    return redirect('member-login')

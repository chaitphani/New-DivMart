from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import F

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from dateutil.relativedelta import relativedelta

from membership.serializers import *
from membership.crons import CreditedPointsSerializer


class RegisteredMembersView(APIView):

    serializer_class = RegisteredMembersSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if int(serializer.validated_data['member_amount']) >= 10000:
                if len(RegisteredMembers.objects.filter(email=serializer.validated_data.get('email'))) < 1:
                    serialize = serializer.save()

                    # referal logic starts here
                    if request.data.get('ref_id'):
                        # print('----------if ref id------', request.data.get('ref_id'))

                        ref_user = RegisteredMembers.objects.filter(self_ref_id=request.data.get('ref_id'))
                        if len(ref_user) > 0:

                            # print('------if ref user-------')
                            ref_qual_user = RegisteredMembers.objects.get(self_ref_id=request.data.get('ref_id'))
                            # print('--------ref user-------', ref_qual_user.fname)
                            print(serialize.sponser_id)
                            serialize.sponser_id = ref_qual_user.self_ref_id
                            print(ref_qual_user.level, '-------------')
                            serialize.level = ref_qual_user.level + 1
                            serialize.save()
                            print(serialize, '------------')
                            print(serialize.level)
                            print(serialize.sponser_id)

                            if not ref_qual_user.sponser_id == None or not ref_qual_user.sponser_id == "":
                                main_refer = RegisteredMembers.objects.filter(self_ref_id=ref_qual_user.sponser_id)

                                if len(main_refer) > 0:
                                    # print('-------if main ref user------')
                                    main_qual_refer = RegisteredMembers.objects.get(self_ref_id=ref_qual_user.sponser_id)
                                    # print('-----main ref user------', main_qual_refer.fname)

                                    if not main_qual_refer.sponser_id == None or not main_qual_refer.sponser_id == "":
                                        _head_refer = RegisteredMembers.objects.filter(self_ref_id=main_qual_refer.sponser_id)

                                        # if three referers
                                        if len(_head_refer) > 0:
                                            # print('------if heaf ref user-----')
                                            _head_qual_refer = RegisteredMembers.objects.get(self_ref_id=main_qual_refer.sponser_id)
                                            # print('-----head qual ref user-------', _head_qual_refer.fname)

                                            if not _head_qual_refer.sponser_id == None or not _head_qual_refer.sponser_id == "":
                                                _4th_refer = RegisteredMembers.objects.filter(self_ref_id=_head_qual_refer.sponser_id)

                                                if len(_4th_refer) > 0:
                                                    # print('----if 4th level ref user-------')
                                                    _4th_qual_refer = RegisteredMembers.objects.get(self_ref_id=_head_qual_refer.sponser_id)
                                                    # print('----4th qual ref user-----', _4th_qual_refer.fname)

                                                    if not _4th_qual_refer.sponser_id == None or not _4th_qual_refer.sponser_id == "":
                                                        _5th_refer = RegisteredMembers.objects.filter(self_ref_id=_4th_qual_refer.sponser_id)

                                                        if len(_5th_refer) > 0:
                                                            # print('---if 5th ref user------')
                                                            _5th_qual_refer = RegisteredMembers.objects.get(self_ref_id=_4th_qual_refer.sponser_id) 
                                                            # print('-------5th qual ref user------', _5th_qual_refer.fname)

                                                            if not _5th_qual_refer.sponser_id == None or _5th_qual_refer.sponser_id == "":
                                                                _6th_refer = RegisteredMembers.objects.filter(self_ref_id=_5th_qual_refer.sponser_id)

                                                                if len(_6th_refer) > 0:
                                                                    # print('-----if 6th ref user-------')
                                                                    _6th_qual_refer = RegisteredMembers.objects.get(self_ref_id=_5th_qual_refer.sponser_id)
                                                                    # print('-----6th qual ref user------', _6th_qual_refer.fname)
                                                                    
                                                                    _6th_qual_refer.commission += 0.05 * float(request.data.get('member_amount'))
                                                                    # _6th_qual_refer.level = 1
                                                                    # _6th_qual_refer.amount_at_level = 0.05 * float(request.data.get('member_amount'))

                                                                    _5th_qual_refer.commission += 0.04 * float(request.data.get('member_amount'))
                                                                    # _5th_qual_refer.level = 1
                                                                    # _5th_qual_refer.amount_at_level = 0.04 * float(request.data.get('member_amount'))

                                                                    _4th_qual_refer.commission += 0.03 * float(request.data.get('member_amount'))
                                                                    # _4th_qual_refer.level = 2
                                                                    # _4th_qual_refer.amount_at_level = 0.03 * float(request.data.get('member_amount'))

                                                                    _head_qual_refer.commission += 0.02 * float(request.data.get('member_amount'))
                                                                    # _head_qual_refer.level = 3
                                                                    _head_qual_refer.amount_at_level = 0.02 * float(request.data.get('member_amount'))

                                                                    main_qual_refer.commission += 0.01 * float(request.data.get('member_amount'))
                                                                    # main_qual_refer.level = 4
                                                                    # main_qual_refer.amount_at_level = 0.01 * float(request.data.get('member_amount'))

                                                                    ref_qual_user.commission += 0.01 * float(request.data.get('member_amount'))
                                                                    # main_qual_refer.level = 5
                                                                    # main_qual_refer.amount_at_level = 0.01 * float(request.data.get('member_amount'))

                                                                    _6th_qual_refer.save()
                                                                    _5th_qual_refer.save()
                                                                    _4th_qual_refer.save()
                                                                    _head_qual_refer.save()
                                                                    main_qual_refer.save()
                                                                    ref_qual_user.save()

                                                            else:
                                                                print('----inside else of no 6th ref user---')
                                                                _5th_qual_refer.commission += 0.05 * float(request.data.get('member_amount'))
                                                                # _5th_qual_refer.level = 1
                                                                # _5th_qual_refer.amount_at_level = 0.05 * float(request.data.get('member_amount'))

                                                                _4th_qual_refer.commission += 0.04 * float(request.data.get('member_amount'))
                                                                _4th_qual_refer.level = 1
                                                                # _4th_qual_refer.amount_at_level = 0.04 * float(request.data.get('member_amount'))

                                                                _head_qual_refer.commission += 0.03 * float(request.data.get('member_amount'))
                                                                _head_qual_refer.level = 2
                                                                # _head_qual_refer.amount_at_level = 0.03 * float(request.data.get('member_amount'))

                                                                main_qual_refer.commission += 0.02 * float(request.data.get('member_amount'))
                                                                main_qual_refer.level = 3
                                                                # main_qual_refer.amount_at_level = 0.02 * float(request.data.get('member_amount'))

                                                                ref_qual_user.commission += 0.01 * float(request.data.get('member_amount'))
                                                                ref_qual_user.level = 4
                                                                # ref_qual_user.amount_at_level = 0.01 * float(request.data.get('member_amount'))
                                                                
                                                                _5th_qual_refer.save()
                                                                _4th_qual_refer.save()
                                                                _head_qual_refer.save()
                                                                main_qual_refer.save()
                                                                ref_qual_user.save()

                                                        else:
                                                            print('-----inside else of no 5 th ref user-----')
                                                            _4th_qual_refer.commission += 0.05 * float(request.data.get('member_amount'))
                                                            # _4th_qual_refer.level = 1
                                                            # _4th_qual_refer.amount_at_level = 0.05 * float(request.data.get('member_amount'))

                                                            _head_qual_refer.commission += 0.04 * float(request.data.get('member_amount'))
                                                            _head_qual_refer.level = 1
                                                            # _head_qual_refer.amount_at_level = 0.04 * float(request.data.get('member_amount'))

                                                            main_qual_refer.commission += 0.03 * float(request.data.get('member_amount'))
                                                            main_qual_refer.level = 2
                                                            # main_qual_refer.amount_at_level = 0.03 * float(request.data.get('member_amount'))

                                                            ref_qual_user.commission += 0.02 * float(request.data.get('member_amount'))
                                                            ref_qual_user.level = 3
                                                            # ref_qual_user.amount_at_level = 0.02 * float(request.data.get('member_amount'))

                                                            _4th_qual_refer.save()
                                                            _head_qual_refer.save()
                                                            main_qual_refer.save()
                                                            ref_qual_user.save()

                                                else: 
                                                    print('-----inside else of no 4th ref user-----')   
                                                    main_qual_refer.commission += 0.04 * float(request.data.get('member_amount'))
                                                    # main_qual_refer.level = 1
                                                    # main_qual_refer.amount_at_level = 0.04 * float(request.data.get('member_amount'))

                                                    ref_qual_user.commission += 0.05 * float(request.data.get('member_amount'))
                                                    ref_qual_user.level = 1
                                                    # ref_qual_user.amount_at_level = 0.04 * float(request.data.get('member_amount'))

                                                    _head_qual_refer.commission += 0.03 * float(request.data.get('member_amount'))
                                                    _head_qual_refer.level = 2
                                                    # _head_qual_refer.amount_at_level = 0.03 * float(request.data.get('member_amount'))

                                                    main_qual_refer.save()
                                                    ref_qual_user.save()
                                                    _head_qual_refer.save()

                                        else:
                                            print('---inside else of no head ref user--------')
                                            # if dual referers
                                            main_qual_refer.commission += 0.04 * float(request.data.get('member_amount'))
                                            # main_qual_refer.level = 1
                                            # main_qual_refer.amount_at_level = 0.03 * float(request.data.get('member_amount'))

                                            ref_qual_user.commission += 0.05 * float(request.data.get('member_amount'))
                                            ref_qual_user.level = 1
                                            # ref_qual_user.amount_at_level = 0.05 * float(request.data.get('member_amount'))

                                            main_qual_refer.save()
                                            ref_qual_user.save()
                                            
                                else:
                                    print('------inside else of no main ref user------')
                                    # if single referer
                                    ref_qual_user.commission += 0.05 * float(request.data.get('member_amount'))
                                    # ref_qual_user.level = 1
                                    # ref_qual_user.amount_at_level = 0.05 * float(request.data.get('member_amount'))
                                    ref_qual_user.save()
                        else:
                            serialize.sponser_id = ''
                            serialize.level = 0
                            serialize.save()
                    
                    else:
                        serialize.level = 0
                    serialize.save()
                    # referal logic ends here

                    # mail related logic
                    new_obj = RegisteredMembers.objects.get(id = serializer.data.get('id'))
                    statuses = "Active" if new_obj.status == 1 else "Inactive"
                    from_mail = settings.EMAIL_HOST_USER
                    to_email = new_obj.email
                    subject = "Membership account created - Div Mart"
                    body = "Thanks for creating a membership account with Div mart - {} \n\nyour credentials for the same as follow - \n\n".format(new_obj.fname) +\
                            "E-mail : {} \n".format(new_obj.email) +\
                            "Password: {} \n".format(new_obj.password) +\
                            "Amount: {} \n".format(new_obj.member_amount) +\
                            "Status: {} \n\n".format(statuses) +\
                            "Referal ID: {} \n\n".format(new_obj.self_ref_id) +\
                            "Sponser ID: {} \n\n".format(new_obj.sponser_id) +\
                            "Note: You can able to login after the admin verify the account details provided. \nyou will get notified once verification is successful.\n\n\n\n" \
                            "Regards,\nTeam Divmart."
                    send_mail(
                        subject,
                        body,
                        from_mail,
                        [to_email],
                        fail_silently=False,
                    )
                    # mail logic ends here

                    return redirect('member-login')
                else:
                    messages.error(request, 'Email already taken...')
                    return redirect('/member/register')                    
            else:
                messages.error(request, 'Member amount should be higher than 10,000/-')
                return redirect('/member/register')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointTransactionView(generics.ListCreateAPIView):
    queryset = PointsTransactionRequests.objects.all()
    serializer_class = PointsTransactionRequestsSerializer


# testing cron view
# class CronTest(APIView):

#     def get(self, request):

#         today = datetime.date.today()
#         reg_members = RegisteredMembers.objects.filter(status=1).annotate(
#             created_date = F('created__date'),
#             updated_date = F('updated__date')
#         )

#         for each_member in reg_members:
#             created_date = each_member.created_date
#             #months for 4.5 Years => 4*12 = 48 + 6 = 54
#             created_date_after_4_5 = created_date + relativedelta(months=54)
#             points_to_be_credited = 0

#             if(each_member.member_amount == 10000):
#                 points_to_be_credited = 20000
#             elif(each_member.member_amount==25000):
#                 points_to_be_credited = 50000

#             if(today == created_date_after_4_5):

#                 data = {'member':each_member.id, 'points':points_to_be_credited, 'added_by':'CRON'}
#                 ser_obj = CreditedPointsSerializer(data=data)
#                 if(ser_obj.is_valid(raise_exception=True)):
#                     ser_obj.save()
#                     return Response(ser_obj.data, status=200)
#                 else:
#                     return Response({"msg":'nothing'}, status=404)
#             else:
#                 return Response({'msg':'not found'}, status=400)


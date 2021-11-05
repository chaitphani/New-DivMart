from .models import RegisteredMembers,CreditedPoints
import datetime
from django.db.models import F
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


def creditPoints():

    today = datetime.date.today()
    reg_members = RegisteredMembers.objects.filter(status=1).annotate(
        created_date = F('created__date'),
        updated_date = F('updated__date')
    )

    for each_member in reg_members:
        created_date = each_member.created_date
        #months for 4.5 Years => 4*12 = 48 + 6 = 54
        created_date_after_4_5 = created_date + relativedelta(months=54)
        points_to_be_credited = 0

        if(each_member.member_amount == 10000):
            points_to_be_credited = 20000
        elif(each_member.member_amount==25000):
            points_to_be_credited = 50000

        if(today == created_date_after_4_5):
            data = {'member_id':each_member.id, 'points':points_to_be_credited, 'credited_by':'CRON'}
            ser_obj = CreditedPointsSerializer(data=data)
            if(ser_obj.is_valid()):
                ser_obj.save()
                print("POINTS ADDEDD SUCCESSFULLY")
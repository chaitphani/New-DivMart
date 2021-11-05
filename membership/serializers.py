from rest_framework import serializers
from .models import *


class PointsTransactionRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsTransactionRequests
        fields = '__all__'
        extra_kwargs = {
            'status':{
                'read_only':True,
            },
            'created':{
                'read_only':True,
            },
        }


class RegisteredMembersSerializer(serializers.ModelSerializer):
    sponser_id = serializers.CharField(required=False)

    class Meta:
        model = RegisteredMembers
        fields = '__all__'
        extra_kwargs = {
            'sponser_id':{
                'read_only':True,
            },
            'self_ref_id':{
                'read_only':True,
            },
            'created':{
                'read_only':True,
            },
        }

    def validate_sponser_id(self,ob):
        reg_objs = RegisteredMembers.objects.filter(self_ref_id=ob)
        if len(reg_objs) <= 0:
            raise serializers.ValidationError("Sponser id is not valid")
        return ob

class CreditedPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditedPoints
        fields = '__all__'
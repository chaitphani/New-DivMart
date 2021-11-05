from typing import MutableSequence
from django.db import models
# from django.contrib.auth.models import User
import datetime
from enum import IntEnum
from django.utils import timezone


class MemberStatus(IntEnum):
    InActive = 0
    Active = 1


def generate_expiry_date():
    return datetime.datetime.now() + datetime.timedelta(days=4017)


def generate_maturity_date():
    return datetime.datetime.now() + datetime.timedelta(days=1643, hours=12)

# class Member(models.Model):
#     fname = models.CharField(max_length=50)
#     mname = models.CharField(max_length=50)
#     lname = models.CharField(max_length=50)
#     contact = models.CharField(max_length=15)
#     alt_contact = models.CharField(max_length=15, null=True, blank=True) 
#     email = models.EmailField(max_length=50, unique=True)
#     dob = models.DateTimeField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     pin_code = models.CharField(max_length=10)
#     blood_group = models.CharField(max_length=5, null=True, blank=True)
#     pan_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
#     identity_proof_front = models.FileField(upload_to="images/ids")
#     identity_proof_back = models.FileField(upload_to="images/ids")
#     account_holder = models.CharField(max_length=50)
#     account_no = models.CharField(max_length=50)
#     bank_name = models.CharField(max_length=50)
#     bank_branch = models.CharField(max_length=50)


#     def __str__(self):
#         return f"{self.fname} {self.lname}"


# class Card(models.Model):
#     member = models.OneToOneField(Member, on_delete=models.CASCADE)
#     card_ID = models.CharField(max_length=50)
#     created_on = models.DateTimeField(auto_now_add=True)
#     expires_on = models.DateTimeField(default=generate_expiry_date)
#     total_points_earned = models.IntegerField(default=0)
#     redeemable_points = models.IntegerField(default=0)
#     opening_amount = models.IntegerField(default=0)
#     maturity_date = models.DateTimeField(default=generate_maturity_date)
#     maturity_return = models.IntegerField(default=0)
#     cancellation_refund = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.member.fname} - {self.card_ID[-4:]}"


class RegisteredMembers(models.Model):

    id = models.AutoField(primary_key=True)
    sponser_id = models.CharField(max_length=50,blank=True,null=True)
    self_ref_id = models.CharField(max_length=50,blank=True,null=True)
    member_amount = models.BigIntegerField()
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    alt_contact = models.CharField(max_length=15, null=True, blank=True) 
    dob = models.DateTimeField(blank=True, null=True)
    perminent_address = models.TextField()
    current_address = models.TextField(blank=True)

    # city = models.CharField(max_length=50)
    # state = models.CharField(max_length=50)
    # pin_code = models.CharField(max_length=10)
    # blood_group = models.CharField(max_length=5, null=True, blank=True)
    # pan_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    # identity_proof_front = models.FileField(upload_to="images/ids")
    # identity_proof_back = models.FileField(upload_to="images/ids")
    
    id_proof_name = models.CharField(max_length=100)
    id_proof_number = models.CharField(max_length=100)
    identity_proof = models.FileField(upload_to="images/ids")
    address_proofs = models.FileField(upload_to="images/address_proofs")

    account_holder_name = models.CharField(max_length=50)
    account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=MemberStatus.InActive.value)

    # for referals
    commission = models.FloatField(default=0)
    level = models.IntegerField(null=True, blank=True)
    amount_at_level = models.FloatField(null=True, blank=True)

    def update_self_ref_id(self,id):
        # You now have both access to self.id and self.name
        RegisteredMembers.objects.filter(id=id).update(self_ref_id='DG100'+str(id))
        
    def save(self, *args, **kwargs):
        super(RegisteredMembers, self).save(*args, **kwargs)
        self.update_self_ref_id(self.id)

    def __str__(self):
        return '{}-{}-{}'.format(self.fname, self.self_ref_id, self.status)


class PointsTransactionRequests(models.Model):

    amount = models.FloatField()
    note = models.CharField(max_length=100)
    member = models.ForeignKey(RegisteredMembers,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.member.fname, self.amount)


class WithdrawlTransactionRequests(models.Model):

    status_choices = (('Paid', 'Paid'), ('Pending', 'Pending'), ('Rejcted','Rejected'))

    amount = models.FloatField(default=0)
    user_note = models.CharField(max_length=120, null=True, blank=True)
    # admin_note = models.CharField(max_length=120, null=True, blank=True)
    member = models.ForeignKey(RegisteredMembers, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=10, choices=status_choices, default='Pending')

    def __str__(self):
        return '{}-{}'.format(self.member.fname, self.amount)


class CreditedPoints(models.Model):

    member = models.ForeignKey(RegisteredMembers,on_delete=models.CASCADE)
    points = models.IntegerField()
    added_by = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}-{}'.format(self.member.fname, self.points, self.status)
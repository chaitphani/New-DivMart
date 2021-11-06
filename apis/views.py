from django.contrib import messages
from django.shortcuts import render,redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from apis.serializers import *
from useraccount.models import *
from dashboard.models import *


class AdminListCreateView(ListCreateAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = AdminSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            admin_user = serializer.save()
            serializer = self.serializer_class(admin_user)
            return redirect('user')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AdminDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
#     lookup_field = 'id'
#     serializer_class = AdminSerializers
#     queryset = AdminUser.objects.all()

#     def put(self,request,pk,format=None):
#         admin=self.get_object(pk)
#         serializer= self.serializer_class(admin,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)


class AdminDetailUpdateDelView(APIView):
    
    serializer_class = AdminSerializers

    def get(self, request, pk):
        instance = AdminUser.objects.get(id=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = AdminUser.objects.get(id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = AdminUser.objects.get(id=pk)
        instance.delete()
        return Response({"success":"object removed"}, status=status.HTTP_200_OK)



class StaffListCreateView(ListCreateAPIView):
    queryset = StaffUser.objects.all()
    serializer_class = StaffSerializers


# class StaffDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    
#     lookup_field = 'id'
#     serializer_class = StaffSerializers
#     queryset = StaffUser.objects.all()

#     def put(self,request,pk,format=None):
#         cashier = self.get_object(pk)
#         serializer= AdminSerializers(cashier,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)


class StaffDetailUpdateDelView(APIView):
    
    serializer_class = StaffSerializers

    def get(self, request, pk):
        instance = StaffUser.objects.get(id=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = StaffUser.objects.get(id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = StaffUser.objects.get(id=pk)
        instance.delete()
        return Response({"success":"object removed"}, status=status.HTTP_200_OK)


class SupplierListCreateView(ListCreateAPIView):

    authentication_classes = [SessionAuthentication]
    queryset = SupplierUser.objects.all()
    serializer_class = SupplierSerializers

    def post(self, request, *args, **kwargs):
        serializer = SupplierSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'supplier create success....')
            return redirect('list_supplier')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    serializer_class = SupplierSerializers
    queryset = SupplierUser.objects.all()


class CustomerGroupListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = CustomerGroups.objects.all()
    serializer_class = CustomerGroupSerializers

    def post(self, request, *args, **kwargs):
        serializer = CustomerGroupSerializers(data=request.data)
        if serializer.is_valid():
            custg = serializer.save()
            serializer = CustomerGroupSerializers(custg)
            return redirect('customer_group_detail')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerSerializers

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializers(data=request.data)
        if serializer.is_valid():
            cust = serializer.save()
            serializer = CustomerSerializers(cust)
            return redirect('customer_list')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    serializer_class = CustomerSerializers
    queryset = CustomerUser.objects.all()


class BankCreation(CreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Bank.objects.all()
    serializer_class = BankSerializers


class BankDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Bank.objects.all()
    serializer_class = BankSerializers
    lookup_field = 'id'


class CategoryListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            cat = serializer.save()
            serializer = CategorySerializers(cat)
            return redirect('categories')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = 'id'


class BrandListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers

    def post(self, request, *args, **kwargs):
        serializer = BrandSerializers(data=request.data)
        if serializer.is_valid():
            brand = serializer.save()
            serializer = BrandSerializers(brand)
            return redirect('brand')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    lookup_field = 'id'


class UnitsListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Units.objects.all()
    serializer_class = UnitsSerializers

    def post(self, request, *args, **kwargs):
        serializer = UnitsSerializers(data=request.data)
        if serializer.is_valid():
            unit = serializer.save()
            serializer = UnitsSerializers(unit)
            return redirect('product_units')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitsDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Units.objects.all()
    serializer_class = UnitsSerializers
    lookup_field = 'id'


# class ProductListCreateView(ListCreateAPIView):
#     authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers

#     def post(self, request, *args, **kwargs):
#         serializer = ProductSerializers(data=request.data)
#         if serializer.is_valid():
#             prod = serializer.save()
#             prod.status=True
#             prod.ref_no = 'PRC-100' + str(prod.id) 
#             prod.applicable_tax = 
#             prod.save()
#             serializer = ProductSerializers(prod)
#             return redirect('list_products')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubcatListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers


class ProductDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'id'


class PurchaseListCreateView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializers


# class PurchaseReturnUpdateDelView(RetrieveUpdateDestroyAPIView):
#     # queryset = Purchase.objects.all()
#     model = Purchase
#     serializer_class = PurchaseSerializers
#     lookup_field = 'product_name'

#     def get_queryset(self):
#         product_name = self.request.parser_context['kwargs']['product_name']
#         # product = Product.objects.get(product_name=product_name).
#         return Purchase.objects.filter(product_name__product_name=product_name)


class PurchaseDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializers
    lookup_field = 'id'


# class SellListCreateView(ListCreateAPIView):
#     authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = Sell.objects.all()
#     serializer_class = SellSerializers


class SellDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Sell.objects.all()
    serializer_class = SellSerializers
    lookup_field = 'id'
                                                   

class AddExpensesView(ListCreateAPIView):
    
    authentication_classes = [SessionAuthentication]
    queryset = Expenses.objects.all()
    serializer_class = AddExpensesSerializers 

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            exser = serializer.save()
            exser.ref_no = 'EXP0-'+str(exser.id)
            exser.status = True
            exser.save()
            return redirect('list_expenses')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class AddExpensesCategoryView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Expenses_category.objects.all()
    serializer_class = ExpensesCategorySerializers   

    def post(self, request, *args, **kwargs):
        serializer = ExpensesCategorySerializers(data=request.data)
        if serializer.is_valid():
            ex_ct = serializer.save()
            ex_ct.status = True
            ex_ct.save()
            serializer = ExpensesCategorySerializers(ex_ct)
            return redirect('add_expenses_category')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       


class AddExpensesDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Expenses_category.objects.all()
    serializer_class = ExpensesCategorySerializers
    lookup_field = 'id'


class PurchaseInfosDetailUpdateDelView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Purchase_info.objects.all()
    serializer_class = PurchaseInfoSerializers
    lookup_field = 'id'


class PayementView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Add_Payments.objects.all()
    serializer_class = PayementSerializers 
    lookup_field = 'id'


# from my side...

class SellListCreateView(APIView):

    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = SellSerializers

    def get(self, request):
        snippets = Sell.objects.all()
        serializer = self.serializer_class(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            last_invoice = Sell.objects.last().invoice_no
            invoice_no = int(last_invoice) + 1
        except:
            invoice_no = 1000

        if serializer.is_valid(raise_exception=True):
            form_serialize = serializer.save()
            form_serialize.ref_no = 'SL-'+ str(form_serialize.id)
            form_serialize.invoice_no = invoice_no
            form_serialize.save()
            return redirect('sale_list')
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductBarCode(APIView):

    authentication_classes = [SessionAuthentication]
    serializer_class = ProductByBarcodeSerializer

    def get(self, request,):
        
        barcodes = Barcode_storage.objects.all()
        serializer = self.serializer_class(barcodes, many=True)
        return Response(serializer.data)


class ProductsByBarcode(APIView):

    authentication_classes = [SessionAuthentication]
    serializer_class = ProductByBarcodeSerializer

    def get_object(self, barcode_no):
        try:
            return Barcode_storage.objects.get(barcode_no=barcode_no)
        except Barcode_storage.DoesNotExist:
            return None

    def get(self, request, barcode_no):
        
        barcodes_obj = self.get_object(barcode_no)
        serializer = self.serializer_class(barcodes_obj)
        return Response(serializer.data)


from div_settings.models import TaxRate
class ProductListCreateView(APIView):

    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            tax_rate_obj = TaxRate.objects.get(rate=serializer.validated_data.get('applicable_tax'))

            prod = serializer.save()
            prod.applicable_tax = tax_rate_obj.id
            # print('---prod applicable tax----', prod.applicable_tax)
            prod.ref_no = 'PRC-100' + str(prod.id) 
            prod.status = True
            prod.save()
            return redirect('list_products')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
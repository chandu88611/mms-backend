# serializers.py

from rest_framework import serializers
from .models import Bill, BillProduct
from users.models import CustomUser

class BillProductSerializer(serializers.ModelSerializer):
    # Assuming that 'product' is a ForeignKey in the BillProduct model
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = BillProduct
        fields = ['product', 'product_name', 'quantity', 'amount']

class BillSerializer(serializers.ModelSerializer):
    products = BillProductSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'user', 'customer', 'date', 'amount', 'description', 'invoice_number', 'receipt_number', 'is_invoice', 'is_receipt', 'products']

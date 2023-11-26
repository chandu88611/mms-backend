# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Bill, BillProduct
from .serializers import BillSerializer
from customers.models import Customer
from product.models import PharmacyProduct

# views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_bill(request):
    try:
        # Extract data from the request
        data = request.data.copy()
        customer_id = data.get('customer_id')
        product_details = data.get('products')  # Assuming it's a list of dictionaries with product_id, quantity, and amount

        # Get the customer and create a new bill
        customer = Customer.objects.get(id=customer_id)
        bill = Bill.objects.create(user=request.user, customer=customer, date=data['date'], amount=data['amount'], description=data['description'], is_invoice=data['is_invoice'], is_receipt=data['is_receipt'])

        # Iterate through products and create BillProduct instances
        for product_detail in product_details:
            product = PharmacyProduct.objects.get(id=product_detail['product_id'])
            quantity = product_detail['quantity']
            amount = product_detail['amount']

            # Check if there's enough quantity available
            if product.quantity < int(quantity):
                return Response({'status': 'error', 'message': f'Not enough quantity available for {product.name}', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

            # Create BillProduct instance
            BillProduct.objects.create(bill=bill, product=product, quantity=quantity, amount=amount)

            # Reduce product quantity
            product.quantity -= int(quantity)
            product.save()

        serializer = BillSerializer(bill)
        return Response({'status': 'success', 'message': 'Bill generated successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e), 'data': None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

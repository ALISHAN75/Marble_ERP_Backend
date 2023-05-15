from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from inventory.model.Orders import Orders, Order_items
# serializers imports
from inventory.serializers.OrdersSerializer import OrderSerializer, MerchantOrderSerializer, AddOrderSerializer
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer, AddOrderItemsSerializer


class CustomerOrderList(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders',
                                        'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    renderer_classes = [UserRenderer]

    def post(self, request, id=None):  
        try:
           
            if 'MRCHNT_ACCT_ID' in request.data.keys():
                queryset = Orders.objects.filter(MRCHNT_ACCT_ID=request.data['MRCHNT_ACCT_ID'], IS_ACTIVE=1 , DELVRY_STS = 0)
            elif 'CUST_ACCT_ID' in request.data.keys():
                queryset = Orders.objects.filter(CUST_ACCT_ID=request.data['CUST_ACCT_ID'], IS_ACTIVE=1 , DELVRY_STS = 0)
            else:
                return Response({'error': 'Check your account title and try again'  , "error_ur" : "اپنے اکاؤنٹ کا عنوان چیک کریں اور دوبارہ کوشش کریں۔" }, status=400)

        except Orders.DoesNotExist:
            return Response({'error': 'This Account Orders does not exist.'  ,  "error_ur" : "یہ اکاؤنٹ آرڈرز موجود نہیں ہیں۔" }, status=400)
        # read_serializer = OrderSerializer(queryset,many=True)
        # return Response(read_serializer.data, status=200)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=200)

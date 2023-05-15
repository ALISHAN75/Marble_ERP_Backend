from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework.permissions import AllowAny
from datetime import datetime
import math
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
# models imports
from inventory.model.Products import Products
from inventory.model.Inventory import Transaction_Details
# serializers imports
from inventory.serializers.ProductsSerializer import AddProductsSerializer, ProductsSerializer, ProductsDetailSerializer
from inventory.serializers.TransactionDetailsSerializer import TransactionDetailsSerializer
from inventory.utility.AdjustmentUtil import isSectioned

class ProductListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'products.add_products', 'PUT': 'products.change_products',
                                        'DELETE': 'products.delete_products', 'GET': 'products.view_products'})]
    renderer_classes = [UserRenderer]
    ACTIVE_DEFAULT_VALUE = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = Products.objects.get(PRODUCT_ID=id)
            except Products.DoesNotExist:
                return Response({'error': 'The Product does not exist.' , 'error_ur': 'پروڈکٹ موجود نہیں ہے۔'}, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = ProductsDetailSerializer(queryset)

        else:
            if request.query_params:
                params = request.query_params
                queryset = Products.objects.filter(Q(PROD_NM_ID__PROD_NM__icontains=params['search']) | Q(
                    CAT_ID__CAT_NM__icontains=params['search']) | Q(USAGE_ID__USAGE_NM__icontains=params['search']), IS_ACTIVE=self.ACTIVE_DEFAULT_VALUE)
            else:
                queryset = Products.objects.filter(IS_ACTIVE=1)
            read_serializer = ProductsDetailSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #  append security fields
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = AddProductsSerializer(data=request.data)

        if create_serializer.is_valid():
            new_product = create_serializer.save()
            # read_serializer = AddProductsSerializer(new_product)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            product_to_update = Products.objects.get(PRODUCT_ID=id)
        except Products.DoesNotExist:
            return Response({'error': 'The Product does not exist.' , 'error_ur': 'پروڈکٹ موجود نہیں ہے۔'}, status=status.HTTP_400_BAD_REQUEST)

        request.data["REC_ADD_BY"] = product_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = ProductsSerializer(
            product_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_earning = update_serializer.save()
            # read_serializer = ProductsSerializer(updated_earning)
            # return Response(read_serializer.data, status=status.HTTP_200_OK)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            prod_to_delete = Products.objects.get(PRODUCT_ID=id)
        except Products.DoesNotExist:
            return Response({'error': 'The Product does not exist.' , 'error_ur': 'پروڈکٹ موجود نہیں ہے۔'}, status=status.HTTP_400_BAD_REQUEST)

        prod_to_delete.REC_MOD_BY = request.user.id
        prod_to_delete.IS_ACTIVE = 0
        prod_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


#  inventory product
class InventroyProductsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    LAST_REC_DEFAULT = 1
    
    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_CURRENT`(
                        2 -- Type_of_search ,  1: ID
                        , '"""+str(id)+"""' -- search query
                        , 1 -- page number 
                        , 10 --  perPage
                        , 0 -- PROD_NM_ID
                        , 0 -- CAT_ID
                        , 0 -- USAGE_ID
                        , -1 -- IS_SIZED
                        , -1 -- IS_SECTIONED
                        , -1 -- IS_GOLA
                        , -1 -- IS_POLISHED
                        , -1 -- WIDTH
                        , -1 -- LENGHT
                        , -1 -- THICKNESS
                        ); """

                invtry = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if invtry.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" } , status=status.HTTP_400_BAD_REQUEST)
        else:
            # invtry = invtry.fillna('')
            # invtry_data=invtry.to_dict(orient='records')[0]
            # invtry_data['TRANSC_DETALS'] = invtry_items.to_dict(orient='records')
            return Response(invtry.to_dict(orient='records')  , status=status.HTTP_200_OK)
             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_CURRENT`(
                        2 -- Type_of_search ,  1: ID
                        , '' -- search query
                        , 1 -- page number 
                        , 1000000 --  perPage
                        , 0 -- PROD_NM_ID
                        , 0 -- CAT_ID
                        , 0 -- USAGE_ID
                        , -1 -- IS_SIZED
                        , -1 -- IS_SECTIONED
                        , -1 -- IS_GOLA
                        , -1 -- IS_POLISHED
                        , -1 -- WIDTH
                        , -1 -- LENGHT
                        , -1 -- THICKNESS
                        ); """ 


            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" } , status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        q = params.get('q' , '') 
        PROD_NM_ID = params.get('PROD_NM_ID' , 0)
        CAT_ID = params.get('CAT_ID' , 0)
        USAGE_ID = params.get('USAGE_ID' , 0)
        IS_SIZED = params.get('IS_SIZED' , -1)
        IS_SECTIONED = params.get('IS_SECTIONED' , -1)
        IS_GOLA = params.get('IS_GOLA' , -1)
        IS_POLISHED = params.get('IS_POLISHED' , -1)
        WIDTH = params.get('WIDTH' , -1)
        LENGHT = params.get('LENGHT' , -1)
        THICKNESS = params.get('THICKNESS' , -1)      
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_CURRENT`(
                            """+str(is_id_srch)+""" -- Type_of_search ,  1: ID
                            , '"""+str(q)+"""' -- search query
                            , """+str(page)+""" -- page number 
                            ,  """+str(parPage)+""" --  perPage
                            , """+str(PROD_NM_ID)+"""  -- PROD_NM_ID
                            , """+str(CAT_ID)+""" -- CAT_ID
                            , """+str(USAGE_ID)+""" -- USAGE_ID
                            , """+str(IS_SIZED)+""" -- IS_SIZED
                            , """+str(IS_SECTIONED)+""" -- IS_SECTIONED
                            , """+str(IS_GOLA)+""" -- IS_GOLA
                            , """+str(IS_POLISHED)+""" -- IS_POLISHED
                            , """+str(WIDTH)+""" -- WIDTH
                            , """+str(LENGHT)+""" -- LENGHT
                            , """+str(THICKNESS)+""" -- THICKNESS
                            ); """ 
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                    return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        
        if my_data.empty:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()


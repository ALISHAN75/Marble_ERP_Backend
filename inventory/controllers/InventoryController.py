from decimal import Decimal
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.LedgerTransaction import LedgerTransaction
import math
from datetime import datetime
# util
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
from inventory.utility.InventoryUtil import InventoryUtil
# models imports
from inventory.model.Inventory import Inventory_Transactions, Transaction_Details
# serializers imports
from inventory.serializers.InventorySerializer import DelInventorySerializer, DetailedInventorySerializer, AddInvTransactionSerializer
from inventory.serializers.TransactionDetailsSerializer import TransactionDetailsSerializer, AddTransactionDetailsSerializer
from accounts.renderers import UserRenderer

class InventoryListView(
    APIView,
    UpdateModelMixin,
    DestroyModelMixin,
):
    #   permission_classes = [IsUserAllowed({'POST': 'inventory.add_products', 'PUT': 'inventory.change_products', 'DELETE': 'inventory.delete_products', 'GET': 'inventory.view_products'})]
    permission_classes = [AllowAny]
    rec_is_active = 1
    ACTIVE_DEFAULT_VALUE = 1
    renderer_classes = [UserRenderer]

    invDict = {
        "Sectioning": "IS_SECTIONED",
        "Gola": "IS_GOLA",
        "Sizing": "IS_SIZED",
        "Polishing": "IS_POLISHED"
    }

  

    def getOne(self, request, id):
        if id:
            try:
                query = """   
                     CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_TRANS_LIST`(
                        1 -- Type_of_search ,  1: ID
                        , """+str(id)+""" -- search query
                        , 1 -- page number 
                        , 10 --  perPage
                        , '' -- Transaction Type
                        , 0 -- Labour Account ID
                        , '1969-01-01' -- start date
                        , '2099-12-31' -- end date
                        ); 
                        """                
                my_data = pd.read_sql(query, connection)
                query = """   
                     CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_TRANS_LIST`(
                        4 -- Type_of_search ,  ID
                        , """+str(id)+""" -- search query
                        , 1 -- page number 
                        , 10 --  perPage
                        , '' -- Transaction Type
                        , 0 -- Labour Account ID
                        , '1969-01-01' -- start date
                        , '2099-12-31' -- end date
                        ); 
                        """                
                trans_details = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" } , status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            trans_details = trans_details.fillna('')
            invtry_data = my_data.to_dict(orient='records')[0]
            try:
                invtry_data["I_DETAILS"] = trans_details.to_dict(orient='records')[0]
                invtry_data["F_DETAILS"] = trans_details.to_dict(orient='records')[1:]
            except IndexError:
                invtry_data["I_DETAILS"] = {}
                invtry_data["F_DETAILS"] = []
            return Response(invtry_data  , status=status.HTTP_200_OK)

             
    def getAll(self):
        try:
            query = """   
                     CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_TRANS_LIST`(
                        2 -- Type_of_search ,  1: ID
                        , 7 -- search query
                        , 1 -- page number 
                        , 1000000 --  perPage
                        , '' -- Transaction Type
                        , 0 -- Labour Account ID
                        , '1969-01-01' -- start date
                        , '2099-12-31' -- end date
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
        TRANS_TYP = params.get('TRANS_TYP' , '')
        labour_acct = params.get('LABOUR_ACCT' , 0)
        start_date = params.get('start_date' , '01/01/1969') 
        end_date = params.get('end_date'  ,    '31/12/2099')
        q = params.get('q' , '') 
        start_date = dateConversion(start_date)
        end_date = dateConversion(end_date)
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """   
                        CALL `datafunc_Mabrle_ERP_wUrdu`.`INVNTRY_TRANS_LIST`(
                            """+str(is_id_srch)+""" -- Type_of_search ,  1: ID
                            , '"""+str(q)+"""' -- search query
                            , """+str(page)+""" -- page number 
                            , """+str(parPage)+""" --  perPage
                            , '"""+str(TRANS_TYP)+"""' -- Transaction Type
                            , """+str(labour_acct)+""" -- Labour Account ID
                            , '"""+start_date+"""' -- start date
                            , '"""+end_date+"""' -- end date
                            ); 
                            """               
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
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



    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id

        create_serializer = AddInvTransactionSerializer(data=request.data)
        inventoryUtil = InventoryUtil()
        if create_serializer.is_valid():
            new_inventory = create_serializer.save()
            total_volume = 0
            # invRecord
            inventoryUtil.inventoryRec = new_inventory
            # initialAttr
            inventoryUtil.initialAttr = request.data["I_DETAILS"]
            inventoryUtil.user = request.user
            product = inventoryUtil.getOrCreateProduct(productNameID=inventoryUtil.initialAttr["NAME_ID"], categoryID=inventoryUtil.initialAttr["CAT_ID"],
                                                           usageID=inventoryUtil.initialAttr["USAGE_ID"], request_user=request.user)
            inventoryUtil.initialAttr["PROD_ID"] = product.PRODUCT_ID
            inventoryUtil.breakage = request.data["BREAKAGE"]
            intial_product_details = inventoryUtil.insertInitialInventory()
            inventoryUtil.insertInventoryBreakage(initialProduct=intial_product_details)

            for finalInvDetails in request.data["F_DETAILS"]:
                total_volume += Decimal(finalInvDetails["THICKNESS"]) * Decimal(
                    finalInvDetails["QTY_SQFT"])

            inventoryUtil.finalVolume = total_volume
            for finalInvDetails in request.data["F_DETAILS"]:
                # handle size and product
                product = inventoryUtil.getOrCreateProduct(productNameID=finalInvDetails["NAME_ID"], categoryID=finalInvDetails["CAT_ID"],
                                                           usageID=finalInvDetails["USAGE_ID"], request_user=request.user)
                size = inventoryUtil.getOrCreateSize(length=finalInvDetails["LENGTH"],
                                                     width=finalInvDetails["WIDTH"],
                                                     thickness=finalInvDetails["THICKNESS"],
                                                     request_user=request.user)
                finalInvDetails["PROD_ID"] = product.PRODUCT_ID
                finalInvDetails["SIZE_ID"] = size.SIZE_ID

                inventoryUtil.finalAttr = finalInvDetails
                inventoryUtil.insertFinalInventory()

            # add inventory to earning and ledger
            # ledgerTransc = LedgerTransaction(isExpense=False)
            # ledgerTransc.addInventoryToLedger(invRecord=new_inventory)
            inventoryUtil.onInventoryUpdateLedger(inventory_transaction=new_inventory)

            # read_serializer = DetailedInventorySerializer(new_inventory)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            inv_to_delete = Inventory_Transactions.objects.get(INV_TRANS_ID=id)
        except Inventory_Transactions.DoesNotExist:
            return Response({'error': 'This Inventory Transaction item does not exist.' ,  'error_ur': 'یہ انوینٹری ٹرانزیکشن آئٹم موجود نہیں ہے۔'}, status=400)
        inv_serializer = DelInventorySerializer(inv_to_delete)
        updated_serializer = inv_serializer.data
        updated_serializer['LABOUR_COST'] = Decimal(
            -1.00) * Decimal(inv_serializer.data['LABOUR_COST'])
        updated_serializer['LABOUR_SQFT'] = Decimal(
            -1.00) * Decimal(inv_serializer.data['LABOUR_SQFT'])
        updated_serializer["LABOUR_RUN_FT"] = Decimal(
            -1.00) * Decimal(inv_serializer.data["LABOUR_RUN_FT"])

        create_serializer = DelInventorySerializer(data=updated_serializer)
        create_serializer.is_valid(raise_exception=True)
        deleted_inv = create_serializer.save()

        total_volume = 0
        inventoryUtil = InventoryUtil()
        inventoryUtil.inventoryRec = deleted_inv
        inventoryUtil.user = request.user

        # inventoryUtil.initialAttr = request.data["I_DETAILS"]
        # for InvDetails in request.data["TRANSC_DETALS"]:
        # for index, InvDetails in enumerate(request.data["TRANSC_DETALS"]):
        #   if index > 0:
        #     total_volume += Decimal(InvDetails["THICKNESS"]) * Decimal(InvDetails["QTY_SQFT"])
        # inventoryUtil.finalVolume = total_volume

        for invDetail in inv_serializer.data["TRANSC_DETALS"]:
            inventoryUtil.initialAttr = invDetail
            inventoryUtil.deleteInitialInventory()

        # ledgerTransc = LedgerTransaction(isExpense=False)
        # ledgerTransc.addInventoryToLedger(invRecord=deleted_inv)

        # read_serializer = DetailedInventorySerializer(deleted_inv)
        # inv_details_qs = Transaction_Details.objects.filter(INV_TRANS_ID=inv_to_delete.INV_TRANS_ID)

        # inventory_to_delete.REC_MOD_BY = request.user.id
        # inventory_to_delete.IS_ACTIVE = 0
        # inventory_to_delete.save()
        return Response({'success' : "Data is deleted successfully" ,  'success_ur' : "ڈیٹا کامیابی سے حذف ہو گیا ہے۔" } , status=status.HTTP_200_OK)


class NonInventoryProductListView(
    APIView,
    UpdateModelMixin,
    DestroyModelMixin,
):
    #   permission_classes = [IsUserAllowed({'POST': 'inventory.add_products', 'PUT': 'inventory.change_products', 'DELETE': 'inventory.delete_products', 'GET': 'inventory.view_products'})]
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    rec_is_active = 1
    ACTIVE_DEFAULT_VALUE = 1
        
    def get(self, request, id=None):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ORDR_NonInvntryProducts`(); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" } , status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)
from accounts.serializer.UsersSerializer import AccountsSerializer
# from accounts.serializer.AcctLedgerSerializer import AcctLedgerSerializer
from inventory.model.Orders import Order_items


class OrderUtil():

    def __init__(self):
        pass

    def findOrderItem(self, order_item_id):
        try:
            order_item_queryset = Order_items.objects.get(
                ORDR_ITEM_ID=order_item_id)
            return order_item_queryset
        except Order_items.DoesNotExist:
            return None

    def updateOrderQty(self, orderItem, deliveryItemRec, orderAmount):
        remaining_qty = orderItem.REQ_QTY - orderItem.DLVRD_QTY
        deliverd_qty = orderItem.DLVRD_QTY
        unit_cost = orderItem.PROD_TOTL_PRICE

        deliveryQty = deliveryItemRec.PROD_QTY
        deliverySqft = deliveryItemRec.PROD_QTY_SQFT
        orderAmount = orderAmount + (unit_cost * deliverySqft)
        
        # if deliveryQty >= remaining_qty:
        #     orderItem.DLVRD_QTY = deliverd_qty + remaining_qty
        #     orderItem.IS_DLVRD = 1
        #     deliveryQty = deliveryQty - remaining_qty
        # else:
        #     orderItem.DLVRD_QTY = deliverd_qty + deliveryQty
        #     orderAmount = orderAmount + (unit_cost * deliverySqft)
        #     orderItem.IS_DLVRD = 0
        #     deliverd_qty = 0
        orderItem.save()
        return orderAmount

    def saveUnitPriceWDelivery(self, deliveryItem, orderItem):
        deliveryItem.UNIT_PRICE_noDLVRY = round(orderItem.PROD_TOTL_PRICE, 2)
        deliveryItem.UNIT_PRICE_wDLVRY = round(
            orderItem.PROD_TOTL_PRICE + deliveryItem.UNIT_DLVRY, 2)
        deliveryItem.DLVRY_ITEM_TOTAL = round(
            (orderItem.PROD_TOTL_PRICE + deliveryItem.UNIT_DLVRY) * deliveryItem.PROD_QTY_SQFT, 2)
        deliveryItem.save()

        return deliveryItem

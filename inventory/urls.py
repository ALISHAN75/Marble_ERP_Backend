from django.urls import path
# from . import views
from inventory.controllers.ProductNameController import ProductNameListView
from inventory.controllers.ProductCategoryController import ProductCategoryListView
from inventory.controllers.UsageTypeController import UsageTypeListView
from inventory.controllers.UsageSizesController import UsageSizesListView
from inventory.controllers.SizesController import SizesListView
from inventory.controllers.ProductController import ProductListView
from inventory.controllers.PurchaseProductController import MerchantPurchaseProductListView
from inventory.controllers.SaleProductController import CustomerSaleProductListView
from inventory.controllers.PurchaseProductController import PurchaseProductListView
from inventory.controllers.SaleProductController import SaleProductListView
from inventory.controllers.InventoryController import InventoryListView , NonInventoryProductListView
from inventory.controllers.ProductController import InventroyProductsView
from inventory.controllers.BreakageRecoveryController import BreakageRecoveryListView
from inventory.controllers.AdjustmentsController import InventoryAdjustmentView
from inventory.Graphs.SalesGraphController import SalesGraphListView
from inventory.Graphs.OrderGraphController import OrderGraphListView
from inventory.Graphs.ProducInventorytGraphController import ProductInventoryListView
from inventory.controllers.CustomerOrderController import CustomerOrderList
from inventory.Graphs.Confrm_RningOrdersCardController import Confirm_RningOrderCard
from inventory.controllers.InventoryDropdownController import InventroyDropdownView
from inventory.controllers.QuotationsController import QuotationsListView
from inventory.Graphs.InevntoryTransactionGraphController import InevntoryTransactionGraphListView


urlpatterns = [
    # Graphs
    path('Invtry_trans_graph', InevntoryTransactionGraphListView.as_view()),
    path('confirm-orders-card', Confirm_RningOrderCard.as_view()),
    path('sales-graph', SalesGraphListView.as_view()),
    path('order-graph', OrderGraphListView.as_view()),
    path('product-inventory-graph', ProductInventoryListView.as_view()),
    # path('product-name', ProductNameListView.as_view()),
    # path('product-name/<int:id>', ProductNameListView.as_view()),
    # path('product-category', ProductCategoryListView.as_view()),
    # path('product-category/<int:id>', ProductCategoryListView.as_view()),
    # path('product-usage', UsageTypeListView.as_view()),
    # path('product-usage/<int:id>', UsageTypeListView.as_view()),
    # path('product-usage-size', UsageSizesListView.as_view()),
    # path('product-usage-size/<int:id>', UsageSizesListView.as_view()),
    # path('product-size', SizesListView.as_view()),
    # path('product-size/<int:id>', SizesListView.as_view()),
    # path('products', ProductListView.as_view()),
    # path('products/<int:id>', ProductListView.as_view()),
    path('order/quotations', QuotationsListView.as_view()),    
    path('order/quotations/<int:id>', QuotationsListView.as_view()),    
    path('inventory_dropdown', InventroyDropdownView.as_view()),    
    path('product_inventory', InventoryListView.as_view()),    
    path('product_inventory/<int:id>', InventoryListView.as_view()),
    path('order/purchase', PurchaseProductListView.as_view()),
    path('order/purchase/<int:id>', PurchaseProductListView.as_view()),
    path('order/purchase-by-merchant/<int:id>',MerchantPurchaseProductListView.as_view()),
    path('order/sale', SaleProductListView.as_view()),
    path('order/sale/<int:id>', SaleProductListView.as_view()),
    path('non_inv_product', NonInventoryProductListView.as_view()),
    path('adjustment', InventoryAdjustmentView.as_view()),
    path('product/list', InventroyProductsView.as_view()),
    path('product/list/<int:id>', InventroyProductsView.as_view()),

    path('order/sale-by-customer/<int:id>' ,  CustomerSaleProductListView.as_view()),
    path('breakage-recovery', BreakageRecoveryListView.as_view()),
    path('order-by-customer', CustomerOrderList.as_view()),

]

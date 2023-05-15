from django.urls import path
from logistics.controllers.PurchaseDeliveriesController import PurchaseDeliveriesListView
from logistics.controllers.SaleDeliveriesController import SaleDeliveriesListView
from logistics.controllers.SalesGraphController import SalesGraphListView
from logistics.Graphs.ExpenseGraphController import ExpenseGraphListView
from logistics.Graphs.OrderGraphController import OrderGraphListView
from logistics.controllers.ProductInventoryController import ProductInventoryListView
from logistics.controllers.ProductInventoryController import ActiveInactiveOrdersListView


urlpatterns = [
    path('purchase-deliveries', PurchaseDeliveriesListView.as_view()),
    path('purchase-deliveries/<int:id>', PurchaseDeliveriesListView.as_view()),
    path('sale-deliveries', SaleDeliveriesListView.as_view()),
    path('sale-deliveries/<int:id>', SaleDeliveriesListView.as_view()) ,
    path('log_orders', ActiveInactiveOrdersListView.as_view())
]


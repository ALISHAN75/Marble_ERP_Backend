from django.urls import path

# from . import views
from finance.controllers.CurrencyController import CurrencyItemListView
from finance.controllers.EarningTranscController import EarningTransListView
from finance.controllers.ExpenseTransItemController import ExpenseTransItemListView
from finance.controllers.ExpenseTranscController import ExpenseTransListView
from finance.Graphs.ExpenseGraphController import ExpenseGraphListView
from finance.Graphs.EarningGraphController import EarningGraphListView
from finance.Graphs.MonthlyExpenseCardController import ExpenseCardhListView
from finance.Graphs.MonthlyEarningCardController import EarningCardhListView
from finance.Graphs.ClosingBalanceCard import ClosingBalanceCardhListView
from finance.Graphs.RevenueGraphController import RevenueGraphListView
from finance.controllers.IncomeStatementController import IncomeStatementList
from finance.Graphs.RevenueIncomeStatGraphController import RevenueIncomeGraphListView
from finance.Graphs.DashboardCardRevenueController import DashboardCardRevenueSummaryListView
from finance.Graphs.MonthlyCashGraphController import MonthlyCashGraphListView
from finance.Graphs.CurrentMonthCashGraphController import CurrentMonthCashGraphListView
from finance.Graphs.LastMonthClosingBalanceGraphController import LastMonthClosingGraphListView
from finance.Graphs.TopImportedProductsGraphController import TopImportedProductsGraphListView
from finance.Graphs.PayableBalanceCreditsGraphController import PayableBalanceCreditsGraphListView
from finance.Graphs.AccountsTopProductsGraphController import AccountTopProductsGraphListView
from finance.Graphs.PayableExpenseBalanceGraphController import PayableExpenseBalanceGraphListView
from finance.Graphs.ProductsInStockGraphController import ProductsInSockGraphListView
from finance.Graphs.InventoryTransactionSectioningGraphController import InventoryTransactionSectioningGraphListView
from finance.Graphs.ExpenseSummaryCreditServiceGraphController import ExpenseSummaryGraphListView
from finance.Graphs.IncomeDeliveryInOutGraphController import IncomeDeliveryInOutGraphListView
from finance.Graphs.EmployeeSalaryAttendenceGraphController import EmployeeSalaryAttendeceGraphListView


urlpatterns = [
    path('closing-balance-card', ClosingBalanceCardhListView.as_view()),
    path('income-table', IncomeStatementList.as_view()),
    path('expense-card', ExpenseCardhListView.as_view()),
    path('earning-card', EarningCardhListView.as_view()),
    path('earning-graph', EarningGraphListView.as_view()),
    path('expense-graph', ExpenseGraphListView.as_view()),
    path('revenue-graph', RevenueGraphListView.as_view()),
    path('revenue_income_graph', RevenueIncomeGraphListView.as_view()),
    path('dashboard_card_revenue', DashboardCardRevenueSummaryListView.as_view()),
    path('monthly_cash_graph', MonthlyCashGraphListView.as_view()),
    path('current_month_cash_graph', CurrentMonthCashGraphListView.as_view()),
    path('months_closing_blnc_graph', LastMonthClosingGraphListView.as_view()),
    path('top_imported_prod_graphs', TopImportedProductsGraphListView.as_view()),
    path('payable_credit_blnc_graphs', PayableBalanceCreditsGraphListView.as_view()),
    path('accounts_top_prods', AccountTopProductsGraphListView.as_view()),
    path('payable_expns_blnc_graphs', PayableExpenseBalanceGraphListView.as_view()),
    path('top_prods_instock_graph', ProductsInSockGraphListView.as_view()),
    path('inv_trans_summary_graph', InventoryTransactionSectioningGraphListView.as_view()),
    path('expense_trans_summary_graph', ExpenseSummaryGraphListView.as_view()),
    path('income_dlvryInOut_graph', IncomeDeliveryInOutGraphListView.as_view()),
    path('emp_summary_graph', EmployeeSalaryAttendeceGraphListView.as_view()),
    
    path('earning', EarningTransListView.as_view()),
    path('earning/<int:id>', EarningTransListView.as_view()),
    path('expense', ExpenseTransListView.as_view()),
    path('expense/<int:id>', ExpenseTransListView.as_view()),
    #  Just get api
    path('currency', CurrencyItemListView.as_view()), 
    path('currency/<int:id>', CurrencyItemListView.as_view())
]

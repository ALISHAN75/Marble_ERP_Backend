from django.urls import path

from  accounts.controllers.GlobalSearchController import GlobalSearchListView
from accounts.controllers.AccountsController import AccountsListView, AdvanceSearchAccount, AccountsByAcctType
from  accounts.controllers.AcctLedgerController import AcctLedgerListView, LedgerByAcct
from accounts.controllers.CashLedgerController import CashLedgerByAcct, CashLedgerListView
from accounts.controllers.GroupController import GroupListView, GroupPermissionsListView, GroupPermissionsUpdateView, UsersGroupCreateView
from accounts.controllers.PermissionController import PermissionListView
from accounts.controllers.UsersController import UserRegistrationView, SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserPasswordResetView, UserUpdateView, UsersByGroupListView, UsersDetailView, UsersListView
from rest_framework_simplejwt import views as jwt_views
from accounts.controllers.SalePurchaseListController import SalesFactoryListView
from accounts.Graphs.AccountGraphController import AccountGraphListView
from accounts.Graphs.TopProductGraphController import AccountTopProductGraphListView
from accounts.Graphs.ReceivablePayableAmountGraph import ReceivablePayableGraphListView


urlpatterns = [
    path('accounts/list', SalesFactoryListView.as_view(), name='accounts_list'),
    path('accounts/global_search', GlobalSearchListView.as_view(), name='global_search'), 
    path('login', UserLoginView.as_view(), name='login'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('accounts', AccountsListView.as_view()),
    path('accounts/<int:id>', AccountsListView.as_view()),
    path('ledger', AcctLedgerListView.as_view()),
    path('ledger/<int:id>', AcctLedgerListView.as_view()),
    path('ledger_by_account', LedgerByAcct.as_view()),
    path('cash_ledger', CashLedgerListView.as_view()),
    path('cash_ledger/<int:id>', CashLedgerListView.as_view()),
    path('cash_ledger_by_account', CashLedgerByAcct.as_view()) , 
    path('users/list', UsersListView.as_view(), name='users_list'),
    path('user-profile', UserProfileView.as_view(), name='profile'),
    path('users/update/<int:id>', UserUpdateView.as_view(), name='update_user'),
    path('users_by_group/list/<str:group_name>', UsersByGroupListView.as_view(), name='users_by_group_list'),
    path('users/<int:id>', UsersDetailView.as_view(), name='users_details'),
    path('change-password', UserChangePasswordView.as_view(), name='changepassword'),
    path('role/list', GroupListView.as_view(), name='role-group'),
    path('role', UsersGroupCreateView.as_view(), name='role-group'),
    path('role/permissions/<int:id>', GroupPermissionsListView.as_view(), name='role-group'),
    path('role/update-permissions/<int:id>', GroupPermissionsUpdateView.as_view(), name='role-update-group'),
    


    path('permissions', PermissionListView.as_view(), name='permissions'),
    path('permissions/<int:id>', PermissionListView.as_view(), name="permision"),
    path('accounts_by_type/<str:group_name>', AccountsByAcctType.as_view()),
    path('accounts/search/advance', AdvanceSearchAccount.as_view()),
    path('send-reset-password-email', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>', UserPasswordResetView.as_view(), name='reset-password'),
    path('refresh-token', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),



     # Graphs
    path('rec_pay_amnt_graph', ReceivablePayableGraphListView.as_view(), name='rec_pay_amnt_graph'),
    path('accounts/top_prod_graph', AccountTopProductGraphListView.as_view(), name='prod_graph'),
    path('accounts/customer/cuurent-yearr-payables', AccountGraphListView.as_view(), name='accounts_graph'),
    
]

from django.urls import path
# from . import views

# from hrm.controllers.DepartmentController import  DepatmentsCreateView, DepatmentsDeleteView, DepatmentsListView, DepatmentsDetailedFilter, DepatmentsUpdateView
from hrm.controllers.DepartmentController import DepatmentsListView
from hrm.controllers.DesignationController import DesignationsListView
from hrm.controllers.EmployeeTypeController import EmployeeTypeListView
from hrm.controllers.AttendanceController import EmployeeAttendanceListView
from hrm.controllers.EmployeeController import AdvanceSearchEmployee, EmployeeListView
from hrm.controllers.CompensationController import EmployeeCompensationListView
from hrm.Graphs.EmployeSalaryGraphController import EmployeSalarywGraph
from hrm.Graphs.RevenueGraphController import RevenueGraph


urlpatterns = [
    # Graphs
    path('revenue-graph', RevenueGraph.as_view()),
    path('employee-salary-graph', EmployeSalarywGraph.as_view()),


    path('employee', EmployeeListView.as_view()),
    path('employee/<int:id>', EmployeeListView.as_view()),
    path('attendance', EmployeeAttendanceListView.as_view()),
    path('attendance/<int:id>', EmployeeAttendanceListView.as_view()),
    path('departments', DepatmentsListView.as_view()),
    path('departments/<int:id>', DepatmentsListView.as_view()),

    path('employee/search/advance', AdvanceSearchEmployee.as_view()),
    path('employment_type', EmployeeTypeListView.as_view()), 
    path('employment_type/<int:id>', EmployeeTypeListView.as_view()),
    path('designations', DesignationsListView.as_view()),
    path('designations/<int:id>', DesignationsListView.as_view()),
]

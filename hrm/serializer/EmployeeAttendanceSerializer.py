from rest_framework import serializers
# models imports
from hrm.model.Employee_Attendance import Employee_Attendance
# serializers import
from hrm.serializer.EmployeeSerializer import EmployeeSerializer


class EmployeeAttendanceSerializer(serializers.ModelSerializer):

    EMP = EmployeeSerializer(read_only=True)

    class Meta:
        model = Employee_Attendance
        fields = (
            'EMP_ATTND_ID',
            'EMP_ID',
            'EMP',
            'EMP_ATTND_DT',
            'EMP_ATTND_STS',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )
        
        # create and update

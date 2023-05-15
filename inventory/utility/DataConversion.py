from datetime import datetime
import re
from django.db.models import Q

def date_convert(date,input_type):    
    if input_type=="Display":
        if len(date.split("/")[-1])==2:
            return datetime.strptime(date,'%d/%m/%y').strftime('%Y-%m-%d')
        elif len(date.split("/")[-1])==4:
            return datetime.strptime(date,'%d/%m/%Y').strftime('%Y-%m-%d')
        else: return "Error: Incorrect date format. Expecting 'dd/mm/yyyy' format"
    elif input_type=="Save":
        return datetime.strptime(date,'%Y-%m-%d').strftime('%#d/%#m/%y')


def dateConversion(params):
    try:
        if bool(datetime.strptime(params, "%d/%m/%Y" )) :
            params = date_convert(params,input_type="Display")
            return params
    except ValueError:
        try :
            if bool(datetime.strptime(params, "%d/%m/%y" ) ) :
                params = date_convert(params,input_type="Display")
            return params
        except ValueError:
            return params

def acctTypeParams(params):
    if type(params) is list:
        data  = Q()
        for x in params:
            data |= Q(acct_type__ACCT_TYPE_NM__icontains = x)   
        return data
    else:
        return " Expecting a List"

def lisToValues(params):
    if params:   
        return params
    else:
        return ''





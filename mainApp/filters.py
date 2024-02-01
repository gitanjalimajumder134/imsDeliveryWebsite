from sqlite3 import Date
# from tkinter import Widget
import django_filters
from django_filters import FilterSet,DateFilter,CharFilter,DateFromToRangeFilter, ChoiceFilter
from . models import *
from django_filters.widgets import RangeWidget,CSVWidget,DateRangeWidget


# class StockReportFilter(django_filters.FilterSet):
#     startDate = DateFilter(field_name='created_at', label='Date') # widget=forms.SelectDateWidget

#     class Meta:
#         model = Stock
#         fields = '__all__'
#         exclude = ['adminUserID', 'quantity', 'stocktype', 'stockfromSuppliername', 'stockfromHubname', 'stocktoBranchname', 'stocktoHubname', 'receiveddate','created_at', 'stockfrom', 'stockto']


class HubStockReportFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name='created_at', label='Date') # widget=forms.SelectDateWidget

    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ['adminUserID', 'quantity', 'file','stocktype', 'stockfromSuppliername', 'stockfromHubname', 'stocktoBranchname', 'stocktoHubname', 'receiveddate','created_at', 'stockfrom', 'stockto']

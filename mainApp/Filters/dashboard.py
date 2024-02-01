from mainApp import views
from mainApp.models import *
from django.shortcuts import render, redirect
import json
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.db.models import Count
from mainApp.resources import OrderResource
from django.contrib import messages
from tablib import Dataset
from mainApp.filters import *
from .inovicepdf import *
# extra_imports
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.core import serializers

class DashboardView(View):
    def get(self, request):
        Productlabel = []
        ProductData = []
        if request.user.is_superuser:
            queryset = Stock.objects.filter(stockStatus='delivered')
            for product in queryset:
                Productlabel.append(product.productID.productName)
                ProductData.append(product.quantity)

            StocksCount = Stock.objects.all().count()
            UsersCount = User.objects.all().count()
            ProductsCount = Product.objects.all().count()
            OrdersCount = Order.objects.all().count()
        else:
            queryset = Stock.objects.filter(stockStatus='delivered').filter(stocktoBranchname__branch_username = request.user.email)
            for product in queryset:
                Productlabel.append(product.productID.productName)
                ProductData.append(product.quantity)

            StocksCount = Stock.objects.filter(stocktoBranchname__branch_username = request.user.email).all().count()
            UsersCount = User.objects.filter(email = request.user.email).all().count()
            ProductsCount = Product.objects.all().count()
            OrdersCount = Order.objects.filter(branchID__branch_username = request.user.email).all().count()

        salesData = self.getSalesChart(request)
        return render(request, 'admin/index.html', {
            'Productlabels': Productlabel,
            'ProductDatas': ProductData,
            'lables' : salesData['labels'],
            'SalesDatas' : salesData['chartdata'],
            'StocksCount': StocksCount,
            'UsersCount': UsersCount,
            'ProductsCount': ProductsCount,
            'OrdersCount': OrdersCount,
        })

    def getSalesChart(self, request):
        labels = [
            'January',
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July'
            ]
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data ={
                     "labels":labels,
                     "chartdata":chartdata,
             }
        return data
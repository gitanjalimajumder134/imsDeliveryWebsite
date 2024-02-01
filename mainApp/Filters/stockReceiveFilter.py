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
from django.core.files.storage import FileSystemStorage
import datetime as dt
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
import os
from pathlib import Path
from django.conf import settings

base_dir =settings.MEDIA_ROOT  

class StockReceiveView(View):
    def get(self, request):
        if request.user.is_superuser:
            totals =  Stock.objects.filter(stocktype='Transfer', stockto = 'Branch').order_by('id').all()
        else:
            totals = Stock.objects.filter(stocktype='Transfer', stockto = 'Branch').filter(stocktoBranchname__branch_username = request.user.email).all()
        totalStockList = []
        for ttl in totals:
            try:
                stockList = {
                    'id':ttl.id,
                    'ProductName':ttl.productID.productName,
                    'TotalQuantity':ttl.quantity,
                    'StockStatus':ttl.stockStatus,
                    'stockfrom': ttl.stockfrom,
                    'stockfromname': ttl.stockfromHubname.name,
                    'stockto': ttl.stockto,
                    'stocktoname': ttl.stocktoBranchname.branchName,
                    'created_at': ttl.created_at,
                    'receiveddate': ttl.receiveddate if ttl.receiveddate else ''

                }
                totalStockList.append(stockList)
                
            except:
                print('None')

        return render(self.request, 'custom-templates/stock-receive-filter.html', {'totalStockList': totalStockList})

class StockReceiveReportView(View):
    def get(self, request):
        if request.user.is_superuser:
            StockReceivedReportList = "SELECT *, SUM(quantity) as totalQuantity from `mainApp_stock` where stockStatus='Delivered' and stockto = 'Branch' GROUP BY stocktoBranchname_id, productID_id"
            StockReceivedReportList = Stock.objects.raw(StockReceivedReportList)
        else:
            branch = Branch.objects.get(branch_username = request.user.email)
            StockReceivedReportList = "SELECT *, SUM(quantity) as totalQuantity from `mainApp_stock` where stockStatus='Delivered' and stockto = 'Branch' and stocktoBranchname_id = %s GROUP BY stocktoBranchname_id, productID_id" % branch.id
            StockReceivedReportList = Stock.objects.raw(StockReceivedReportList)
        totalStockList = []
        available_stock = 0
        for stock in StockReceivedReportList:
            print('stock', stock.totalQuantity, 'product', stock.productID, 'branch', stock.stocktoBranchname)
            orderedquantity = Order.objects.filter(branchID__id=stock.stocktoBranchname.id, product_id__id = stock.productID.id)
            qty=0
            for order in orderedquantity:
                print("inside for : ", order.quantity)
                qty += int(order.quantity)
            available_stock =int(stock.totalQuantity) -  (qty)
            stockList = {
                'id': stock.id,
                'productID':stock.productID.id,
                'BranchName':stock.stocktoBranchname.branchName,
                'SKU':stock.productID.sku,
                'ProductName':stock.productID.productName,
                'TotalQuantity':stock.totalQuantity,
                'AvailableStock':available_stock,
                'StockStatus':stock.stockStatus,
                'ReceivedDate':stock.receiveddate,
                'Region':stock.stocktoBranchname.region
            }
            totalStockList.append(stockList)
        return render(self.request, 'custom-templates/stock-received-report.html', {'StockReceivedReportList': totalStockList})


class StockReportView(View):
    def get(self, request):
        totalstock = []
        
        if request.user.is_superuser:
            branches = Branch.objects.all()
            hub = Hub.objects.all()
            if request.GET:
                item = request.GET['item']
                branchid = request.GET.getlist('branch') or None
                from_date = request.GET['fromdate']
                to_date =  request.GET['todate']
                hubid = request.GET.getlist('hub') or None
                print('all ', item, branchid, from_date, to_date, hubid)
                if hubid != None  and branchid == None:
                    if 'all' in hubid:
                        totalstock = HubBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
                        print('all', totalstock)
                    else:
                        totalstock = HubBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, hubid__id__in = hubid)
                if branchid != None and hubid == None:
                    if 'all' in branchid: 
                        totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
                    else:
                        totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, branchid__id__in = branchid)
                    
        else:
            if request.GET:
                item = request.GET['item']
                hubid = request.GET['hub'] or None
                branchid = request.GET.getlist['branch'] or None
                from_date = request.GET['fromdate']
                to_date =  request.GET['todate']
                branches = Branch.objects.filter(branch_username = request.user.email).all()
                if branchid != None and hubid == None:
                    if 'all' in branchid: 
                        totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
                    else:
                        totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, branchid__id__in = branchid)
            
        totalStockList = []
        if len(totalstock) != 0:
            print('hlw')
            for ttl in totalstock:
                print('ttl', ttl.openingstock, ttl.id)
                if hubid:
                    if 'all' in hubid:
                        totals = ("SELECT productID_id AS id, stockHub, SUM(CASE WHEN stocktype = 'Opening Stock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) AS total_transfer, SUM(CASE WHEN stocktype = 'Transit' THEN quantity ELSE 0 END) AS total_transit, SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) AS total_decrease,SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END) AS total_increase,(SUM(CASE WHEN stocktype = 'Opening Stock' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transit' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END)) AS total_stock_quantity, productID_id   FROM ( SELECT productID_id, stocktoHubname_id AS stockHub, stocktype, quantity FROM  mainApp_stock WHERE receiveddate >= '{0}' AND receiveddate <= '{1}' AND stockStatus = 'Delivered' and productID_id = {2} UNION ALL SELECT productID_id, stockfromHubname_id AS stockHub, stocktype, quantity FROM  mainApp_stock WHERE receiveddate >= '{3}' AND receiveddate <= '{4}' AND stockStatus = 'Delivered' and productID_id = {5}) AS combined_stock WHERE stockHub IS NOT NULL GROUP BY productID_id, stockHub;".format(from_date, to_date,item,from_date, to_date,item))
                        totals = Stock.objects.raw(totals)
                            
                    else:
                        totals = "SELECT productID_id AS id, stockHub, SUM(CASE WHEN stocktype = 'Opening Stock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) AS total_transfer, SUM(CASE WHEN stocktype = 'Transit' THEN quantity ELSE 0 END) AS total_transit, SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) AS total_decrease,SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END) AS total_increase,(SUM(CASE WHEN stocktype = 'Opening Stock' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transit' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END)) AS total_stock_quantity, productID_id   FROM ( SELECT productID_id, stocktoHubname_id AS stockHub, stocktype, quantity FROM  mainApp_stock WHERE receiveddate >= '{0}' AND receiveddate <= '{1}' AND stockStatus = 'Delivered' AND (stockfromHubname_id IN {2} or stocktoHubname_id IN {3}) and productID_id = {4} UNION ALL SELECT productID_id, stockfromHubname_id AS stockHub, stocktype, quantity FROM  mainApp_stock WHERE receiveddate >= '{5}' AND receiveddate <= '{6}' AND stockStatus = 'Delivered' AND (stockfromHubname_id IN {7} or stocktoHubname_id IN {8}) and productID_id = {9}) AS combined_stock WHERE stockHub IS NOT NULL GROUP BY productID_id, stockHub;".format(from_date, to_date, (str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")),item,from_date, to_date, (str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")),item) 
                        totals = Stock.objects.raw(totals)

                else:
                    if 'all' in branchid: 
                        totals = """SELECT
    productID_id AS id,
    allids,
    stocktoBranchname_id,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate BETWEEN '{0}' AND '{1}' THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate BETWEEN '{2}' AND '{3}' THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate BETWEEN '{4}' AND '{5}' THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND receiveddate BETWEEN '{6}' AND '{7}' THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN receiveddate BETWEEN '{8}' AND '{9}' THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) +  SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END)     
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate < '{18}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate < '{19}' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate < '{20}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' AND receiveddate < '{21}' THEN quantity ELSE 0 END)) AS total_stock_quantity_previous
FROM
    mainApp_stock
WHERE
    (receiveddate BETWEEN '{22}' AND '{23}' OR receiveddate < '{24}')
    AND stockStatus = 'Delivered'
    AND productID_id = {25}
    AND stocktoBranchname_id IS NOT NULL
GROUP BY
    productID_id, stocktoBranchname_id;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, to_date, from_date, item)
                        totals = Stock.objects.raw(totals)    
                    else:
                        print('tp', str(tuple(branchid)))
                        totals = """SELECT
    productID_id AS id,
    allids,
    stocktoBranchname_id,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate BETWEEN '{0}' AND '{1}' THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate BETWEEN '{2}' AND '{3}' THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate BETWEEN '{4}' AND '{5}' THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND receiveddate BETWEEN '{6}' AND '{7}' THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN receiveddate BETWEEN '{8}' AND '{9}' THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) +  SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END)     
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate < '{18}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate < '{19}' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate < '{20}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' AND receiveddate < '{21}' THEN quantity ELSE 0 END)) AS total_stock_quantity_previous
FROM
    mainApp_stock
WHERE
    (receiveddate BETWEEN '{22}' AND '{23}' OR receiveddate < '{24}')
    AND stockStatus = 'Delivered'
    AND productID_id = {25} AND stocktoBranchname_id = {26}
    AND stocktoBranchname_id IS NOT NULL
GROUP BY
    productID_id, stocktoBranchname_id;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, to_date, from_date, item, (str(tuple(branchid)).replace(",)",")")))
                        totals = Stock.objects.raw(totals)   
                for stock in totals:
                    print('ttl2', ttl.openingstock, ttl.id)
                    try:
                        if hubid:
                            product = Product.objects.get(id = stock.id)
                            hubstock = Hub.objects.get(id = stock.stockHub)
                            transitstock = Transit.objects.filter(itemname__id = product.id, stockStatus = 'InTransit', hubname__id = hubstock.id)
                            print('chck', transitstock)
                            transitquantity = 0
                            for transit in transitstock:
                                transitquantity += int(transit.quantity)
                            transferstock = Transfer.objects.filter(transferStatus = 'InTransit', source__id = hubstock.id, transferdate__range = [from_date, to_date])
                            print('chck', transferstock)
                            if transferstock:
                                for transfer in transferstock:
                                    print('chck', transfer)
                                    transferqnty = TransferQuantity.objects.filter(item__id = product.id, transfer__id = transfer.id)
                                    print('qty', transferqnty)
                            stockList = {
                                'BranchName':hubstock.name,
                                'openingstock': ttl.openingstock,
                                'ProductName':product.productName,
                                'closingstock': stock.total_stock_quantity,
                                'transit':transitquantity,
                                'received':stock.total_transit,
                                'transfer': stock.total_transfer,
                                'decreasequantity':stock.total_decrease,
                                'increasequantity':stock.total_increase
                            }
                            totalStockList.append(stockList)
                    
                        else:
                            product = Product.objects.get(id = stock.id)
                            transferstock = Transfer.objects.filter(branchdestination__id = stock.stocktoBranchname_id, transferStatus = 'InTransit').first()
                            print('allids', transferstock)
                            transferquantity = 0
                            branchtransfer = 0
                            if transferstock:
                                
                                transferqty = TransferQuantity.objects.filter(item__id = stock.id,transfer__id = transferstock.id)
                                for transferdata in transferqty:
                                    print('qqty', transferdata.stocktransfered)
                                    branchtransfer += int(transferdata.stocktransfered)
                            branch = Branch.objects.get(id = stock.stocktoBranchname_id)
                            orders = Order.objects.filter(branchID__id = stock.stocktoBranchname_id, product_id__id = stock.id)
                            
                            for order in orders:
                                print('order', order.branchID)
                                transferquantity += int(order.quantity) 
                            stockList = {
                                'BranchName':branch.branchName,
                                'openingstock': ttl.openingstock + stock.total_stock_quantity_previous,
                                'ProductName':product.productName,
                                'closingstock': int(stock.total_closing_stock_current)-int(transferquantity) + stock.total_stock_quantity_previous,
                                'transit':branchtransfer,
                                'received':stock.total_transit,
                                'transfer': transferquantity,
                                'decreasequantity':stock.total_decrease,
                                'increasequantity':stock.total_increase
                            }
                            
                            totalStockList.append(stockList)
                            print('stocktotal', totalStockList)
                    except:
                        print('None')
        else:
            totals = ''
            if request.GET:
                item = request.GET['item']
                branchid = request.GET.getlist('branch') or None
                from_date = request.GET['fromdate']
                to_date =  request.GET['todate']
                hubid = request.GET.getlist('hub') or None
                if hubid:
                    if 'all' in hubid:
                        totals = ("""SELECT
    productID_id AS id,
    stockHub,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{0}' AND receiveddate <= '{1}') THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{2}' AND receiveddate <= '{3}') THEN quantity ELSE 0 END) AS total_transfer,
    SUM(CASE WHEN stocktype = 'Transit' AND (receiveddate >= '{4}' AND receiveddate <= '{5}') THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{6}' AND receiveddate <= '{7}') THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{8}' AND receiveddate <= '{9}') THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transit' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{18}' AND receiveddate <= '{19}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{20}' AND receiveddate <= '{21}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
SUM(
    CASE
        WHEN stocktype = 'OpeningStock' AND receiveddate < '{22}' THEN quantity
        ELSE 0
    END
) - SUM(
    CASE
        WHEN stocktype = 'Transfer' AND receiveddate < '{23}' THEN quantity
        ELSE 0
    END
) + SUM(
    CASE
        WHEN stocktype = 'Transit' AND receiveddate < '{24}' THEN quantity
        ELSE 0
    END
) - SUM(
    CASE
        WHEN stocktype = 'Decrease' AND receiveddate < '{25}' THEN quantity
        ELSE 0
    END
) + SUM(
    CASE
        WHEN stocktype = 'Increase' AND receiveddate < '{26}' THEN quantity
        ELSE 0
    END
) AS total_closing_stock_previous
FROM
    (
        SELECT
            productID_id,
            stocktoHubname_id AS stockHub,
            stocktype,
            quantity,
            receiveddate
        FROM
            mainApp_stock
        WHERE
            (receiveddate >= '{27}' AND receiveddate <= '{28}')
            OR (receiveddate < '{29}') -- Previous month
            AND stockStatus = 'Delivered'
            AND productID_id = {30}

        UNION ALL

        SELECT
            productID_id,
            stockfromHubname_id AS stockHub,
            stocktype,
            quantity,
            receiveddate
        FROM
            mainApp_stock
        WHERE
            (receiveddate >= '{31}' AND receiveddate <= '{32}')
            OR (receiveddate < '{33}') -- Previous month
            AND stockStatus = 'Delivered'
            AND productID_id = {34}
    ) AS combined_stock
WHERE
    stockHub IS NOT NULL
GROUP BY
    productID_id,
    stockHub;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, from_date, to_date,from_date,item,from_date, to_date,from_date,item))
                        totals = Stock.objects.raw(totals)
                        print('ttl stock', totals)    
                    else:
                        totals = """SELECT
    productID_id AS id,
    stockHub,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{0}' AND receiveddate <= '{1}') THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{2}' AND receiveddate <= '{3}') THEN quantity ELSE 0 END) AS total_transfer,
    SUM(CASE WHEN stocktype = 'Transit' AND (receiveddate >= '{4}' AND receiveddate <= '{5}') THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{6}' AND receiveddate <= '{7}') THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{8}' AND receiveddate <= '{9}') THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transit' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{18}' AND receiveddate <= '{19}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{20}' AND receiveddate <= '{21}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
SUM(
    CASE
        WHEN stocktype = 'OpeningStock' AND receiveddate < '{22}' THEN quantity
        ELSE 0
    END
) - SUM(
    CASE
        WHEN stocktype = 'Transfer' AND receiveddate < '{23}' THEN quantity
        ELSE 0
    END
) + SUM(
    CASE
        WHEN stocktype = 'Transit' AND receiveddate < '{24}' THEN quantity
        ELSE 0
    END
) - SUM(
    CASE
        WHEN stocktype = 'Decrease' AND receiveddate < '{25}' THEN quantity
        ELSE 0
    END
) + SUM(
    CASE
        WHEN stocktype = 'Increase' AND receiveddate < '{26}' THEN quantity
        ELSE 0
    END
) AS total_closing_stock_previous
FROM
    (
        SELECT
            productID_id,
            stocktoHubname_id AS stockHub,
            stocktype,
            quantity,
            receiveddate
        FROM
            mainApp_stock
        WHERE
            (receiveddate >= '{27}' AND receiveddate <= '{28}'
            OR receiveddate < '{29}') 
            AND stockStatus = 'Delivered'
            AND productID_id = {30}
       	 	AND (stockfromHubname_id IN {31} or stocktoHubname_id IN {32})

       UNION ALL

        SELECT
            productID_id,
            stockfromHubname_id AS stockHub,
            stocktype,
            quantity,
            receiveddate
        FROM
            mainApp_stock
        WHERE
            (receiveddate >= '{33}' AND receiveddate <= '{34}'
            OR receiveddate < '{35}') 
            AND stockStatus = 'Delivered'
            AND productID_id = {36}
         	AND (stockfromHubname_id IN {37} or stocktoHubname_id IN {38})
    ) AS combined_stock
WHERE
    stockHub IN {39}
GROUP BY
    productID_id,
    stockHub;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, from_date, to_date,from_date, item,(str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")),from_date, to_date,from_date, item,(str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")"))) 
                        totals = Stock.objects.raw(totals)
                        print(totals)    
                else:
                    if 'all' in branchid: 
                        totals = """SELECT
    productID_id AS id,
    allids,
    stocktoBranchname_id,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate BETWEEN '{0}' AND '{1}' THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate BETWEEN '{2}' AND '{3}' THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate BETWEEN '{4}' AND '{5}' THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND receiveddate BETWEEN '{6}' AND '{7}' THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN receiveddate BETWEEN '{8}' AND '{9}' THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) +  SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END)     
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate < '{18}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate < '{19}' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate < '{20}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' AND receiveddate < '{21}' THEN quantity ELSE 0 END)) AS total_stock_quantity_previous
FROM
    mainApp_stock
WHERE
    (receiveddate BETWEEN '{22}' AND '{23}' OR receiveddate < '{24}')
    AND stockStatus = 'Delivered'
    AND productID_id = {25}
    AND stocktoBranchname_id IS NOT NULL
GROUP BY
    productID_id, stocktoBranchname_id;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, to_date, from_date, item)
                        totals = Stock.objects.raw(totals)        
                        print(totals) 
                    else:
                        print('tp', (str(tuple(branchid)).replace(",)",")")))
                        totals = """SELECT
    productID_id AS id,
    allids,
    stocktoBranchname_id,
    SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate BETWEEN '{0}' AND '{1}' THEN quantity ELSE 0 END) AS opening_stock,
    SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate BETWEEN '{2}' AND '{3}' THEN quantity ELSE 0 END) AS total_transit,
    SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate BETWEEN '{4}' AND '{5}' THEN quantity ELSE 0 END) AS total_decrease,
    SUM(CASE WHEN stocktype = 'Increase' AND receiveddate BETWEEN '{6}' AND '{7}' THEN quantity ELSE 0 END) AS total_increase,
    SUM(CASE WHEN receiveddate BETWEEN '{8}' AND '{9}' THEN quantity ELSE 0 END) AS total_stock_quantity_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND (receiveddate >= '{10}' AND receiveddate <= '{11}') THEN quantity ELSE 0 END) +  SUM(CASE WHEN stocktype = 'Transfer' AND (receiveddate >= '{12}' AND receiveddate <= '{13}') THEN quantity ELSE 0 END)     
- SUM(CASE WHEN stocktype = 'Decrease' AND (receiveddate >= '{14}' AND receiveddate <= '{15}') THEN quantity ELSE 0 END)  + SUM(CASE WHEN stocktype = 'Increase' AND (receiveddate >= '{16}' AND receiveddate <= '{17}') THEN quantity ELSE 0 END)) AS total_closing_stock_current,
    (SUM(CASE WHEN stocktype = 'OpeningStock' AND receiveddate < '{18}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' AND receiveddate < '{19}' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' AND receiveddate < '{20}' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' AND receiveddate < '{21}' THEN quantity ELSE 0 END)) AS total_stock_quantity_previous
FROM
    mainApp_stock
WHERE
    (receiveddate BETWEEN '{22}' AND '{23}' OR receiveddate < '{24}')
    AND stockStatus = 'Delivered'
    AND productID_id = {25} AND stocktoBranchname_id = {26}
    AND stocktoBranchname_id IS NOT NULL
GROUP BY
    productID_id, stocktoBranchname_id;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, to_date, from_date, item, (str(tuple(branchid)).replace(",)",")")))
                        totals = Stock.objects.raw(totals)   
                        print('ss', totals)
            for stock in totals:
                
                
                product = Product.objects.get(id = stock.id)
                if hubid:
                    deliveredtransfer = Transfer.objects.filter(transferStatus = 'Delivered', hubdestination__id = stock.stockHub, transferdate__range = (from_date,to_date))
                    print('dlvrd', deliveredtransfer)
                    deliveredtransferqty = TransferQuantity.objects.filter(transfer__id__in = deliveredtransfer)
                    deliveredtransferlist = 0
                    for delivertransfer in deliveredtransferqty:
                        deliveredtransferlist += int(delivertransfer.stocktransfered)
                    print('ccc', deliveredtransferlist)
                    hubstock = Hub.objects.get(id = stock.stockHub)
                    transitstock = Transit.objects.filter(itemname__id = product.id, stockStatus = 'InTransit', hubname__id = hubstock.id)
                    transitquantity = 0
                    for transit in transitstock:
                        transitquantity += int(transit.quantity)
                    
                    transferstock = Transfer.objects.filter(transferStatus = 'InTransit', source__id = hubstock.id, transferdate__range = [from_date, to_date])
                    print('chck', transferstock)
                    transfertransitstock = 0
                    if transferstock:
                        transferqnty = TransferQuantity.objects.filter(item__id = product.id, transfer__id__in = transferstock)
                        for qty in transferqnty:
                            transfertransitstock += int(qty.stocktransfered)
                        
                    stockList = {
                        'BranchName':hubstock.name,
                        'openingstock': stock.opening_stock + stock.total_closing_stock_previous,
                        'ProductName':product.productName,
                        'closingstock': stock.opening_stock + stock.total_transit - (stock.total_transfer - deliveredtransferlist) + stock.total_closing_stock_previous + deliveredtransferlist,
                        'transit':transitquantity,
                        'received':stock.total_transit + deliveredtransferlist,
                        'transferreceived': abs(deliveredtransferlist - stock.total_transfer) ,
                        'transfertransit': transfertransitstock,
                        'decreasequantity':stock.total_decrease,
                        'increasequantity':stock.total_increase
                    }
                    totalStockList.append(stockList)
                else:
                    transferstock = Transfer.objects.filter(branchdestination__id = stock.stocktoBranchname_id, transferStatus = 'InTransit').first()
                    print('allids', transferstock)
                    transferquantity = 0
                    branchtransfer = 0
                    if transferstock:
                        
                        transferqty = TransferQuantity.objects.filter(item__id = stock.id,transfer__id = transferstock.id)
                        for transferdata in transferqty:
                            print('qqty', transferdata.stocktransfered)
                            branchtransfer += int(transferdata.stocktransfered)
                    branch = Branch.objects.get(id = stock.stocktoBranchname_id)
                    orders = Order.objects.filter(branchID__id = stock.stocktoBranchname_id, product_id__id = stock.id)
                    
                    for order in orders:
                        print('order', order.branchID)
                        transferquantity += int(order.quantity) 
                    transfertransitstock = 0
                    stockList = {
                        'BranchName':branch.branchName,
                        'openingstock': stock.opening_stock + stock.total_stock_quantity_previous,
                        'ProductName':product.productName,
                        'closingstock': int(stock.total_closing_stock_current)-int(transferquantity) + stock.total_stock_quantity_previous,
                        'transit':branchtransfer,
                        'received':stock.total_transit,
                        'transferreceived': transferquantity,
                        'transfertransit': transfertransitstock,
                        'decreasequantity':stock.total_decrease,
                        'increasequantity':stock.total_increase
                    }
                    totalStockList.append(stockList)
                    
        print('stcklst', totalStockList)
        items = Product.objects.all()
        itemlist = []
        for itemname in items:
            itemname = {
                'id': itemname.id,
                'name': itemname.productName
            }
            itemlist.append(itemname)
        return render(self.request, 'custom-templates/stock-report.html', {'totalStockList': totalStockList, 'branches': branches, 'itemlist': itemlist, 'hub': hub})
    
class SaleView(View):
    def get(self, request):
        return render(self.request, 'custom-templates/sale.html', context=None)


class PrintInoviceView(View):
    def get(self, request):
        return render(self.request, 'custom-templates/print-invoice.html', context=None)


class DisbursementView(View):
    def get(self, request,id):
        disburselist= Stock.objects.get(id=id)
        # branch = Branch.
        item= Product.objects.get(id=disburselist.productID.id)
        context={'disburselist':disburselist, 'item': item, 'stock': disburselist}
        return redirect('/mainApp/order/add/?branchID='+ str(disburselist.stocktoBranchname.id) + '&'+ 'product_id=' + str(disburselist.productID.id))
    
class printPDFView(View):
    def get(self, request,id):
        invoice = Order.objects.get(id=id)
        printPdf = GenerateInvoicePdf(request, invoice)
        return printPdf
    def post(self, request):
        print("request:",request)
        inv_id = request.POST.get('invoiceID')
        invoice = Order.objects.get(id=inv_id)
        printPdf = GenerateInvoicePdf(request, invoice)
        return printPdf  


class printChalan(View):
    def get(self, request,transferID):  
        chalan = Transfer.objects.filter(id = transferID).first()
        transferqty = TransferQuantity.objects.filter(transfer__id = transferID)
        transferlist = []
        for transfer in transferqty:
            transfer = {
                'itemid': transfer.item.id,
                'cgst': transfer.item.cgst,
                'sgst': transfer.item.sgst,
                'itemname': transfer.item.productName,
                'price': transfer.item.price,

                'transferablestock': transfer.transferablestock,
                'stocktransfered': transfer.stocktransfered,
                'totalcartons': round(int(transfer.stocktransfered) / 4)
            }
            transferlist.append(transfer)
        transferchalan = {
            'sourcefrom': chalan.source.name,
            'sourceaddress': chalan.source.address,
            'sourcephone': chalan.source.phone,
            'BranchID': chalan.branchdestination.id if chalan.branchdestination else '',
            'HubID': chalan.hubdestination.id if chalan.hubdestination else '',
            'branch': chalan.branchdestination.branchName if chalan.branchdestination else '',
            'hub': chalan.hubdestination.name if chalan.hubdestination else '',
            'branchmanager': chalan.branchdestination.branchManager if chalan.branchdestination else '',
            'hubcontactname': chalan.hubdestination.contactname if chalan.hubdestination else '',
            'branchphoneNo': chalan.branchdestination.branchMangerPhoneNo if chalan.branchdestination else chalan.hubdestination.phone,
            'transferlist': transferlist,
            'stock_created': (chalan.transferdate).strftime("%d/%m/%Y"),
            'transferid': chalan.id,
            'delivery_address': chalan.branchdestination.company + " "+ chalan.branchdestination.address + ", "+ chalan.branchdestination.city + ", "+ chalan.branchdestination.region + ", "+ chalan.branchdestination.pincode if chalan.branchdestination else chalan.hubdestination.address
        }
        print('chaln', transferchalan)
        printChalan = GenerateChalanPdf(request,transferchalan)
        return printChalan 

class DisbursementReportView(View):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        if request.user.is_superuser:
            # branch_list = Branch.objects.values_list("branchCode", "branchName" ).distinct().order_by()
            branches = Branch.objects.all()
            branch_list = []
            for branch in branches:
                branch = {
                    'code': branch.branchCode,
                    'name': branch.branchName
                }
                branch_list.append(branch)

        else:
            branches = Branch.objects.filter (branch_username = request.user.email)
            branch_list = []
            for branch in branches:
                branch = {
                    'code': branch.branchCode,
                    'name': branch.branchName
                }
                branch_list.append(branch)
        product_list = Product.objects.values_list("productName" , flat=True).distinct().order_by()
        order_list = Order.objects.values_list("orderDate", flat=True).distinct().order_by()
      
        
        # print('response_list', list(branch_list)[0])
        # branch_list_joined =[]

        # for branch in list(branch_list):
        #     print("SEE BRANCH ", type(branch))
        #     joined = ""
        #     for code in branch:
        #         joined = joined + "-" + code
        #     branch_list_joined.append(joined)
        # print("JOINED LIST ", branch_list_joined)
        response_list = {
            'branch_list': list(branch_list),
            'product_list': list(product_list),
            'order_list': list(order_list)
        }
        return render(self.request, 'custom-templates/disbursement-report.html', context=response_list)
    
    def post(self, request):
        for br_id in request.POST.getlist('brnch_id'):
            if br_id is not None:
                    print("br_id:",br_id)
        br_id = request.POST.getlist('brnch_id')
        pd_id = request.POST.get('pd_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        # for br_id in request.POST.getlist('brnch_id'):
        print('data send', br_id, pd_id,from_date,to_date)
        printexcel = views.download_csv(br_id,pd_id,from_date,to_date)
        return printexcel 
        
    

class ordersImport(View):
    def get(self, request):
        return render(self.request, 'custom-templates/orders-import.html', context=None)

    def post(self, request):
        print('file', request.FILES)
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            excel_file = filename
            empexceldata = pd.read_excel(os.path.join(base_dir,excel_file), na_filter = False)
            print(empexceldata)
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                date = str(dbframe.orderDate)
                date = datetime.datetime.strptime((date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                branchID_id=Branch.objects.filter(branchCode=((dbframe.BranchCode).rstrip())).first()
                product_id_id = Product.objects.filter(productCode=((dbframe.ProductCode).rstrip())).first()
                
                if branchID_id and product_id_id:
                    stocks = "SELECT *, SUM(CASE WHEN (stocktype = 'Decrease') THEN -quantity ELSE quantity END) as totalQuantity from `mainApp_stock` where stockStatus='Delivered' and stockto = 'Branch' and stocktoBranchname_id = '{0}' and productID_id = '{1}' GROUP BY stocktoBranchname_id, productID_id".format(branchID_id.id, product_id_id.id)
                    stocks = Stock.objects.raw(stocks)

                    print('stocks', stocks)
                    if stocks:
                        for stock in stocks:
                        
                            print('stock', stock)
                            orderquantity = Order.objects.filter(branchID__id=stock.stocktoBranchname.id, product_id__id = stock.productID.id)
                            print('ordr', orderquantity)
                            qty=0
                            for order in orderquantity:
                                qty += int(order.quantity)
                            
                            available_stock =int(stock.totalQuantity) -  (qty)
                            
                            if available_stock >= dbframe.Quantity:
                                obj = Order.objects.create(addressState=dbframe.State, branchID_id=branchID_id.id, customerID=dbframe.ClientNo, loanNo=dbframe.LoanNo, customerName=dbframe.ClientName,loan_date=(dbframe.LoanDate).strftime('%d/%m/%Y'), invoiceNo=dbframe.InvoiceNo, loanStatus=dbframe.LoanStatus,  loanType=dbframe.LoanType, orderStatus = dbframe.OrderStatus, product_id_id=product_id_id.id, quantity=dbframe.Quantity, orderDate=date, date_of_delivery=(dbframe.DeliveryDate).strftime('%d/%m/%Y'), address=dbframe.Address)
                                obj.save()
                                messages.success(request, "Successfully Uploaded!")
                            else:
                                messages.error(request, "Quantity is Greater Than the Available Stock Quantity")
                                return render(request,'custom-templates/orders-import.html')
                    else:
                        messages.error(request, "Stcok is not Available")
                    
                else:
                    messages.error(request, "Product or Branch not created...!!!")
            
            return render(request, 'custom-templates/orders-import.html', {
                                    'uploaded_file_url': excel_file
                                })
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class GetLoanData(View):
    def post(self, request):
        oldLoanID = request.POST.get('loanAppNo')
        StockReceivedReportList = Stock.objects.filter(orderID__loanAppNo=oldLoanID)
        stockList = StockReceivedReportList[0]
        stockListArr = {
            'item': stockList.productID.productName,
            'sku' : stockList.productID.sku,
            'quantity': stockList.quantity,
            'invoiceNumber': stockList.orderID.invoiceNo
        }
        print(stockListArr)
        # orderList = Order.objects.filter(loanAppNo=oldLoanID)
        # return HttpResponse(orderList)
        # stockList.orderID.loanAppNo
        # stockList.orderID.invoiceNo
        # stockList.stockBranchID.branchName
        # stockList.orderID.customerID
        # stockList.orderID.customerName
        # stockList.productID.sku
        # stockList.productID.productName
        # stockList.orderID.orderDate
        # stockList.orderID.orderStatus
        # stockList.orderID.EDD
        # stockList.disbursementStatus
        # stockList.orderID.addressState
        # stockList.stockBranchID.region
        # tmpJson = serializers.serialize("json",StockReceivedReportList)
        # tmpObj = json.loads(tmpJson)
        # return JsonResponse({'data' : json.dumps(tmpObj)})
        return JsonResponse({'data' : stockListArr})

class DisburseView(View):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, loanAppNo, format=None):
      
        print("ON POST : ", request.POST['newLoanID'])
        newLoanID = request.POST['newLoanID']
        invoiceNo = request.POST['invoiceNo']
        customerName = request.POST['customerName']
        customerID = request.POST['customerID']
        Phone = request.POST['Phone']
        address = request.POST['address']
        addressState = request.POST['addressState']
        addressZipCode = request.POST['addressZipCode']
        # disbursementDate = request.POST['disbursementDate']
        receiveddate = request.POST['receiveddate']
        order_details=Order.objects.get(loanAppNo=loanAppNo)
        order_details.newLoanID = newLoanID
        order_details.invoiceNo = invoiceNo
        order_details.customerName = customerName
        order_details.customerID = customerID
        order_details.Phone = Phone
        order_details.address = address
        order_details.addressState = addressState
        order_details.addressZipCode = addressZipCode
        order_details.save()

        stockdetails = Stock.objects.get(orderID=order_details.id)
        # stockdetails.disbursementStatus = 'disbursed'
        # stockdetails.disbursementDate = disbursementDate
        stockdetails.receiveddate = receiveddate
        stockdetails.save()
        # disburse = Stock.objects.create(orderID_id=(Order.objects.create(newLoanID=newLoanID, customerName=customerName, Phone=Phone,
        #                 address=address, addressState=addressState, addressZipCode=addressZipCode)).id, disbursementDate=disbursementDate, updatedDate=updatedDate)
        # all_data = request.POST.get
        # print(all_data)
        return JsonResponse({'message': 'Disbursed Successfully'}, status=200)

class printPOPDF(View):
    def get(self, request,id):
        purchaseorder = Purchase.objects.get(id=id)
        supplierqty = Quantity.objects.filter(purchase__id = purchaseorder.id)
        print('supplierqty',supplierqty)
        supplierquantitylist = []
        grandtotal = 0
        hublist = []
        for qty in supplierqty:
            grandtotal += round(float(qty.items.price) * float(qty.quantity),0)
            hubs = HubQuantity.objects.filter(supplier__id = purchaseorder.supplier_name.id, items__id = qty.items.id, purchase__id = purchaseorder.id)
            hublist = []
            for hub in hubs:
                hub = {
                    'hubname': hub.hub.name,
                    'qty': hub.quantity,
                    'contactname': hub.hub.contactname,
                    'address': hub.hub.address,
                    'phone': hub.hub.phone
                    
                }
                hublist.append(hub)
            qty = {
                'items': qty.items.productName,
                'itemsid': qty.items.id,
                'quantity': qty.quantity,
                'itemhsn': qty.items.hsn,
                'price': qty.items.price,
                'totalprice': round(float(qty.items.price) * float(qty.quantity),0),
                'grandtotal': grandtotal,
                'hublist': hublist
            }
            supplierquantitylist.append(qty)
            print('items', supplierquantitylist)
        purchase = {
            'supplier': purchaseorder.supplier_name.suppliername,
            'supplierid': purchaseorder.supplier_name.id,
            'supplieremail': purchaseorder.supplier_name.email,
            'supplierphone': purchaseorder.supplier_name.phone,
            'PoNo': purchaseorder.id,
            'date': purchaseorder.date,
            'supplieraddress': purchaseorder.supplier_name.address,
            'suppliercity': purchaseorder.supplier_name.city,
            'supplierstate': purchaseorder.supplier_name.state,
            'supplierquantitylist': supplierquantitylist,
            'statename': purchaseorder.state.name,
            'stateaddress': purchaseorder.state.address,
            'statecin': purchaseorder.state.cinNumber
            

        }
        printpopdf = GeneratePOPdf(request,purchase)
        return printpopdf 


class RequisitionImport(View):
    def get(self, request):
        return render(self.request, 'custom-templates/requisition-import.html', context=None)

    def post(self, request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            excel_file = filename
            empexceldata = pd.read_excel(os.path.join(base_dir,excel_file), na_filter = False)
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                date = str(dbframe.RequisitionDate)
                
                print('date', type(dbframe.RequisitionDate), date, pd.notnull(date))
                if date == 'NaT':
                    print(True)
                    date = date
                else:
                    print(False)
                    date = datetime.datetime.strptime((date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    print('dates', date)
                branchName_id=Branch.objects.filter(branchCode=((dbframe.BranchCode).rstrip())).first()
                productname_id = Product.objects.filter(productCode=((dbframe.ProductCode).rstrip())).first()
                
                if branchName_id and productname_id:
                    
                    obj = Requisition.objects.create(
                        requisitionNumber=dbframe.RequisitionNumber, 
                        branchName_id=branchName_id.id, 
                        productname_id=productname_id.id, 
                        quantity=dbframe.Quantity, 
                        requisitionDate= datetime.datetime.now() if  date == 'NaT' else date
                        )
                    obj.save()
                    messages.success(request, "Successfully Uploaded!")
                    
                else:
                    messages.error(request, "Product or Branch not created...!!!")
            
            return render(request, 'custom-templates/requisition-import.html', {
                                    'uploaded_file_url': excel_file
                                })
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mainApp.models import *
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.http import HttpResponse
from mainApp.filters import *
# extra_imports
from rest_framework.response import Response
import xlwt
from django.http import HttpResponse, JsonResponse
# from django.core.exceptions import ValidationError
from django.http import QueryDict
from .forms import *
from datetime import datetime,timedelta 
from django.db.models import Sum
from django.db import connection
import calendar
from django.core.files.storage import default_storage
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os

def Home(request):
    return render(request, 'admin-lte/index3.html')


def Index(request):
    return render(request, 'admin-lte/index.html')


def IndexHome(request):
    return render(request, 'admin-lte/index2.html')


def download_csv(br_id,  pd_id, from_date, to_date):
    print('post val', br_id,  pd_id, from_date, to_date) 
    institutionsorderlist = []
    for brnch in br_id:
        print(brnch)
        if brnch != None and pd_id != None and from_date == '' and to_date == '':
            if brnch == 'all':
                institutions = (Order.objects.filter(product_id__productName=pd_id))
                for institution in institutions:
                    ins = {
                        'InvoiceNo': institution.invoiceNo,
                        'InvoiceDate': institution.invoice_date,
                        'LoanNo': institution.loanNo,
                        'CustomerID': institution.customerID,
                        'CustomerName': institution.customerName,
                        'ProductName': institution.product_id.productName,
                        'SKU': institution.product_id.sku,
                        'Region': institution.branchID.region,
                        'BranchCode': institution.branchID.branchCode,
                        'BranchName': institution.branchID.branchName,
                        'OrderDate': institution.orderDate
                    }
                    institutionsorderlist.append(ins)
            else:    
                institutions = (Order.objects.filter(
                    branchID__branchCode=brnch, product_id__productName=pd_id))
                for institution in institutions:
                    ins = {
                        'InvoiceNo': institution.invoiceNo,
                        'InvoiceDate': institution.invoice_date,
                        'LoanNo': institution.loanNo,
                        'CustomerID': institution.customerID,
                        'CustomerName': institution.customerName,
                        'ProductName': institution.product_id.productName,
                        'SKU': institution.product_id.sku,
                        'Region': institution.branchID.region,
                        'BranchCode': institution.branchID.branchCode,
                        'BranchName': institution.branchID.branchName,
                        'OrderDate': institution.orderDate
                    }
                    institutionsorderlist.append(ins)
        elif brnch != None and pd_id != None and from_date != None and to_date != None:
            print('hello')
            if brnch == 'all':
                institutions = Order.objects.filter(
                product_id__productName=pd_id,orderDate__range=(from_date, to_date))
                for institution in institutions:
                    ins = {
                        'InvoiceNo': institution.invoiceNo,
                        'InvoiceDate': institution.invoice_date,
                        'LoanNo': institution.loanNo,
                        'CustomerID': institution.customerID,
                        'CustomerName': institution.customerName,
                        'ProductName': institution.product_id.productName,
                        'SKU': institution.product_id.sku,
                        'Region': institution.branchID.region,
                        'BranchCode': institution.branchID.branchCode,
                        'BranchName': institution.branchID.branchName,
                        'OrderDate': institution.orderDate
                    }
                    institutionsorderlist.append(ins)
            else:
                institutions = Order.objects.filter(
                    branchID__branchCode=brnch, product_id__productName=pd_id,orderDate__range=[from_date, to_date])
                print('data', institutions)
                for institution in institutions:
                    ins = {
                        'InvoiceNo': institution.invoiceNo,
                        'InvoiceDate': institution.invoice_date,
                        'LoanNo': institution.loanNo,
                        'CustomerID': institution.customerID,
                        'CustomerName': institution.customerName,
                        'ProductName': institution.product_id.productName,
                        'SKU': institution.product_id.sku,
                        'Region': institution.branchID.region,
                        'BranchCode': institution.branchID.branchCode,
                        'BranchName': institution.branchID.branchName,
                        'OrderDate': institution.orderDate
                    }
                    institutionsorderlist.append(ins)
                # print('else ins', institutionsorderlist)
    # print('ins', institutionsorderlist)
    orderarraylist = []
    # Convert institutions from query set to iterable(array or dict)
    for orderlist in institutionsorderlist:
        # print('ods', orderlist['InvoiceNo'])
        # print('type', type(orderlist))
        # for orders in orderlist:
            
        order = {
            'InvoiceNo': orderlist['InvoiceNo'],
            'InvoiceDate': orderlist['InvoiceDate'],
            'LoanNo': orderlist['LoanNo'],
            'CustomerID': orderlist['CustomerID'],
            'CustomerName': orderlist['CustomerName'],
            'ProductName': orderlist['ProductName'],
            'SKU': orderlist['SKU'],
            'Region': orderlist['Region'],
            'BranchCode': orderlist['BranchCode'],
            'BranchName': orderlist['BranchName'],
            'OrderDate': orderlist['OrderDate']
        }
        print("OD LIST ", orderlist['OrderDate'])
        orderarraylist.append(order)
        
    ordered_list=["InvoiceNo", "InvoiceDate", "LoanNo", "CustomerID", "CustomerName", "ProductName", "SKU", "Region", "BranchCode", "BranchName", "OrderDate"]
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sale.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in orderarraylist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
            
        row+=1
    wb.save(response)
    return response      
    # response = HttpResponse(content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="Report.xls"'
    # wb = xlwt.Workbook(encoding='utf-8')
    # ws = wb.add_sheet('ProductReports')
    # row__num = 0
    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True
    # columns = ['InvoiceNo', 'LoanNo', 'CustomerID', 'CustomerName', 'ProductName',
    #               'SKU', 'Region', 'BranchCode', 'BranchName', 'OrderDate']
    # for col in range(len(columns)):
    #     ws.write(row__num, col, columns[col], font_style)
    # font_style.font.bold = True

    # for index, institution in enumerate(institutions.values_list('invoiceNo', 'loanNo', 'customerID', 'customerName', 'product_id__productName', 'product_id__sku', 'branchID__region', 'branchID__branchCode', 'branchID__branchName', 'orderDate')):
        
    #     for colNo,inst in enumerate(institution) :
    #         9999
    #         ws.write(index+1, colNo, inst)
    #     # ws.write(institution+1, institution + 1, institution)
    # wb.save(response)
    # return response
    return HttpResponse("response")


def export_excel(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    if '[all]' in queryString:
        print('found')
        queryString = queryString.replace("[all]", '["all"]')
    else:
        print('nnn')
        queryString = queryString
    body = json.loads(queryString)
    print('body', body)
    # check = request.body
    print('check data', body['hubID'])
    item = body['productID']
    print(item)
    hubid = body['hubID'] or None
    branchid = body['branchID'] or None
    from_date = body['fromdate']
    to_date =  body['todate']
    print('show all data', item, hubid, branchid, from_date, to_date)
    if request.user.is_superuser:
        
        if hubid != None and branchid == None:
            if 'all' in hubid:
                totalstock = HubBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
            else:
                totalstock = HubBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, hubid__id__in = hubid)
            
        if branchid != None and hubid == None:
            if 'all' in branchid: 
                totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
            else:
                totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, branchid__id__in = branchid)
            
    else:
        if branchid != None and hubid == None:
            if 'all' in branchid: 
                totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item)
            else:
                totalstock = BranchBalance.objects.filter(created_at__range=(from_date, to_date), item__id = item, branchid__id__in = branchid)
    
    totalStockList = []
    if len(totalstock) != 0:
        for ttl in totalstock:
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
            (receiveddate >= '{27}' AND receiveddate <= '{28}')
            OR (receiveddate < '{29}') -- Previous month
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
            (receiveddate >= '{33}' AND receiveddate <= '{34}')
            OR (receiveddate < '{35}') -- Previous month
            AND stockStatus = 'Delivered'
            AND productID_id = {36}
         	AND (stockfromHubname_id IN {37} or stocktoHubname_id IN {38})
    ) AS combined_stock
WHERE
    stockHub IS NOT NULL
GROUP BY
    productID_id,
    stockHub;""".format(from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date, to_date,from_date,from_date,from_date,from_date,from_date, from_date, to_date,from_date, item,(str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")),from_date, to_date,from_date, item,(str(tuple(hubid)).replace(",)",")")),(str(tuple(hubid)).replace(",)",")")))
                    totals = Stock.objects.raw(totals)

            else:
                if 'all' in branchid: 
                    totals = "SELECT productID_id AS id,allids, stocktoBranchname_id,  SUM(CASE WHEN stocktype = 'OpeningStock' SELECT productID_id AS id, allids, stocktoBranchname_id, SUM(CASE WHEN stocktype = 'Opening Stock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) AS total_transit, SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) AS total_decrease, SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END) AS total_increase, (SUM(CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END)) AS total_stock_quantity, productID_id FROM mainApp_stock WHERE receiveddate >= '{0}' AND receiveddate <= '{1}' AND stockStatus = 'Delivered' AND productID_id = {2} AND stocktoBranchname_id IS NOT NULL GROUP BY productID_id, stocktoBranchname_id;".format(from_date, to_date, item)
                    totals = Stock.objects.raw(totals)    
                else:
                    print('tp', str(tuple(branchid)))
                    totals = "SELECT productID_id AS id, allids, stocktoBranchname_id, SUM(CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) AS total_transit, SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) AS total_decrease, SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END) AS total_increase, (SUM(CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Transfer' THEN quantity ELSE 0 END) - SUM(CASE WHEN stocktype = 'Decrease' THEN quantity ELSE 0 END) + SUM(CASE WHEN stocktype = 'Increase' THEN quantity ELSE 0 END)) AS total_stock_quantity, productID_id FROM mainApp_stock WHERE receiveddate >= '{0}' AND receiveddate <= '{1}' AND stockStatus = 'Delivered' AND productID_id = {2} AND stocktoBranchname_id = {3} AND stocktoBranchname_id IS NOT NULL GROUP BY productID_id, stocktoBranchname_id;".format(from_date, to_date, item, (str(tuple(branchid)).replace(",)",")")))
                    totals = Stock.objects.raw(totals)   
            for stock in totals:
                if hubid:
                    product = Product.objects.get(id = stock.id)
                    hubstock = Hub.objects.get(id = stock.stockHub)
                    transitstock = Transit.objects.filter(itemname__id = product.id, stockStatus = 'InTransit', hubname__id = hubstock.id)
                    print('chck', transitstock)
                    transitquantity = 0
                    for transit in transitstock:
                        print('trnst', transit)
                        transitquantity += int(transit.quantity)
                    stockList = {
                        'HubName':hubstock.name,
                        'OpeningStock': ttl.openingstock,
                        'ProductName':product.productName,
                        'ClosingStock': stock.total_stock_quantity,
                        'Transit':transitquantity,
                        'Received':stock.total_transit,
                        'Transfer': stock.total_transfer,
                        'Decrease':stock.total_decrease,
                        'Increase':stock.total_increase
                    }
                    totalStockList.append(stockList)
            
                else:
                    transferstock = Transfer.objects.filter(branchdestination__id = stock.stocktoBranchname_id, transferStatus = 'InTransit')
                    print('allids', transferstock)
                    if transferstock:
                        for transfer in transferstock:
                            transferqty = TransferQuantity.objects.filter(item__id = stock.id,transfer__id = transfer.id)
                            for transferdata in transferqty:
                                branchtransfer += int(transferdata.transferablestock)
                    branch = Branch.objects.get(id = stock.stocktoBranchname_id)
                    orders = Order.objects.filter(branchID__id = stock.stocktoBranchname_id, product_id__id = stock.id)
                    transferquantity = 0
                    branchtransfer = 0
                    for order in orders:
                        print('order', order.branchID)
                        transferquantity += int(order.quantity) 
                    stockList = {
                        'BranchName':branch.branchName,
                        'OpeningStock': ttl.openingstock,
                        'ProductName':product.productName,
                        'ClosingStock': int(stock.total_stock_quantity)-int(transferquantity),
                        'Transit':branchtransfer,
                        'Received':stock.total_transit,
                        'Transfer': transferquantity,
                        'Decrease':stock.total_decrease,
                        'Increase':stock.total_increase
                    }
                    totalStockList.append(stockList)
    else:
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
            (receiveddate >= '{27}' AND receiveddate <= '{28}')
            OR (receiveddate < '{29}') -- Previous month
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
            (receiveddate >= '{33}' AND receiveddate <= '{34}')
            OR (receiveddate < '{35}') -- Previous month
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

        else:
            if 'all' in branchid: 
                print('yes')
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
                print('ttls', totals)
            else:
                print('no',str(tuple(branchid)))
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
                print('totals', totals)
        for stock in totals:
            if hubid:
                deliveredtransfer = Transfer.objects.filter(transferStatus = 'Delivered', hubdestination__id = stock.stockHub)
                deliveredtransferqty = TransferQuantity.objects.filter(transfer__id__in = deliveredtransfer)
                deliveredtransferlist = 0
                for delivertransfer in deliveredtransferqty:
                    deliveredtransferlist += int(delivertransfer.stocktransfered)
                product = Product.objects.get(id = stock.id)
                hubstock = Hub.objects.get(id = stock.stockHub)
                transitstock = Transit.objects.filter(itemname__id = product.id, stockStatus = 'InTransit', hubname__id = hubstock.id)
                print('chck', transitstock)
                transitquantity = 0
                for transit in transitstock:
                    print('trnst', transit)
                    transitquantity += int(transit.quantity)
                transferstock = Transfer.objects.filter(transferStatus = 'InTransit', source__id = hubstock.id, transferdate__range = [from_date, to_date])
                print('chck', transferstock)
                transfertransitstock = 0
                if transferstock:
                    transferqnty = TransferQuantity.objects.filter(item__id = product.id, transfer__id__in = transferstock)
                    for qty in transferqnty:
                        transfertransitstock += int(qty.stocktransfered)
                stockList = {
                    'HubName':hubstock.name,
                    'OpeningStock': stock.opening_stock + stock.total_closing_stock_previous,
                    'ProductName':product.productName,
                    'ClosingStock': stock.opening_stock + stock.total_transit - (stock.total_transfer - deliveredtransferlist) +
                          stock.total_closing_stock_previous + deliveredtransferlist,
                    'Transit':transitquantity,
                    'Received':stock.total_transit + deliveredtransferlist,
                    'TransferReceived': abs(deliveredtransferlist - stock.total_transfer),
                    'TransferTransit': transfertransitstock,
                    'Decrease':stock.total_decrease,
                    'Increase':stock.total_increase
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
                transfertransitstock = 0
                stockList = {
                    'BranchName':branch.branchName,
                    'OpeningStock': stock.opening_stock + stock.total_stock_quantity_previous,
                    'ProductName':product.productName,
                    'ClosingStock': int(stock.total_closing_stock_current)-int(transferquantity) + stock.total_stock_quantity_previous,
                    'Transit':branchtransfer,
                    'Received':stock.total_transit,
                    'TransferReceived': transferquantity,
                    'TransferTransit': transfertransitstock,
                    'Decrease':stock.total_decrease,
                    'Increase':stock.total_increase
                }
                totalStockList.append(stockList)
    print('total', totalStockList)
    if hubid:
        ordered_list=["SlNo","HubName", "ProductName", "OpeningStock", "Transit", "Received","TransferReceived", "TransferTransit","Decrease", "Increase","ClosingStock"]
    if branchid:
        ordered_list=["SlNo","BranchName", "ProductName", "OpeningStock", "Transit", "Received", "TransferReceived", "TransferTransit","Decrease", "Increase","ClosingStock"]
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="StockReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in totalStockList:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
            
        row+=1
    wb.save(response)
    return response
    print('ppp')
   

def OrderDownload_excel(request):

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sale.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row__num = 0
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    columns = ['State', 'BranchCode', 'ClientNo', 'LoanNo', 'ClientName', 'LoanDate', 'InvoiceNo', 'LoanStatus', 'LoanType', 'OrderStatus', 'ProductCode', 'Quantity', 'orderDate', 'DeliveryDate', 'Address']
    for col in range(len(columns)):
        ws.write(row__num, col, columns[col], date_format)
    date_format.font.bold = True

    wb.save(response)
    return response

def HubAllocation(request, supplier, items, purchase,state):
    print('value found', supplier, items, purchase, state)
    purchaseorder = Purchase.objects.filter(id = purchase, state__id = state).first()
    huballocatelist = []
    print("Purchase ", purchaseorder.id)
    hubdata = HubQuantity.objects.filter(items__id = items, supplier__id = purchaseorder.supplier_name.id, purchase__id = purchaseorder.id)
    print('hubdata', hubdata)
    hublist = []
    for hubs in hubdata:
        hubs = {
            'hubid': hubs.hub.id,
            'hubname': hubs.hub.name,
            'qty': hubs.quantity
        }
        hublist.append(hubs)
        print('hub', hublist)
    # print('hub data', hublist)
    print("IN FOR ", purchaseorder.id , "items ", items)
    suppqty = Quantity.objects.filter(purchase__id = purchaseorder.id, items__id =items)
    print("QTY FOR FR ", suppqty)
    for qty in suppqty:
        # product = Product.objects.filter(id = qty.items.id).first()
        hubs = Hub.objects.filter(state__id = state)
    
        for hub in hubs:
            allocate = {
                'supplier': purchaseorder.supplier_name.suppliername,
                'supplierid': purchaseorder.supplier_name.id,
                'items': qty.items.productName,
                'itemid': qty.items.id,
                'hubname': hub.name,
                'hubid': hub.id,
                'quantity': qty.quantity,
                'remainingstock': qty.remainingquantity,
            }
            huballocatelist.append(allocate)
        print("HELLO AJAX ", huballocatelist)
    return JsonResponse({"allocate" : huballocatelist, 'hublist': hublist})
    # return render(request, 'admin/change_form.html', {"huballocatelist" : huballocatelist},context = None)
    

def hubpost(request):
    
    print("BBBBBBBBBBBBB")
    arradata = request.POST['data']
    datas = json.loads(arradata)
    print(datas)
    
    for data in datas:
        print('loop', data)
        purchase = Purchase.objects.filter(id = data['purchaseorder']).first()
        quantity = Quantity.objects.filter(purchase__id = purchase.id, items__id = data['items'])
        hubquantity = HubQuantity.objects.filter(items__id = data['items'], purchase__id = purchase.id, supplier__id = purchase.supplier_name.id, hub__id = data['hub'])
        print('items get:', data['items'], 'supplier get:', data['supplier'], 'hub:', data['hub'], 'qty:', data['qty'],)
        
        for supplierqty in quantity:
            print('remaining:', supplierqty.remainingquantity)
            for hublist in hubquantity:
                print('hubli', hublist.id)
                hublist.delete()
                supplierqty.remainingquantity = int(supplierqty.remainingquantity) + int(hublist.quantity)
                supplierqty.save()
            HubQuantity.objects.create(items_id = data['items'], quantity = data['qty'], supplier_id = data['supplier'], hub_id = data['hub'], purchase_id = purchase.id)
            supplierqty.remainingquantity = int(supplierqty.remainingquantity) - int(data['qty'])
            supplierqty.save()
    
    return HttpResponse('hello')


def TransitReceive(request):
    arradata = request.POST
    print('reqst', arradata, request.FILES)

    receiveddate = request.POST['date']
    id = request.POST['id']
    file = request.FILES['file']

    receivedstock =  request.POST['receivedstock']
    remarks =  request.POST['remarks']
    transit = Transit.objects.get(id = id)
    if int(transit.quantity) == int(receivedstock):
    
        transit.receiveddate = receiveddate
        transit.stockStatus = 'Delivered'
        transit.file = file
        transit.remarks = remarks
        transit.save()
        Stock.objects.create(stocktype = 'Transit', stockfrom = 'Supplier', stockfromSuppliername_id = transit.suppliername.id, stockto = 'Hub', stocktoHubname_id = transit.hubname.id, productID_id = transit.itemname.id, quantity = transit.quantity, receiveddate = receiveddate, stockStatus = 'Delivered', allids = transit.id)
        
    else :
        qty = int(transit.quantity)-int(receivedstock)
        transit.receiveddate = receiveddate
        transit.stockStatus = 'Delivered'
        transit.file = file
        transit.quantity = receivedstock
        transit.remarks = remarks
        transit.save()
        Stock.objects.create(stocktype = 'Transit', stockfrom = 'Supplier', stockfromSuppliername_id = transit.suppliername.id, stockto = 'Hub', stocktoHubname_id = transit.hubname.id, productID_id = transit.itemname.id, quantity = receivedstock, receiveddate = receiveddate, stockStatus = 'Delivered', allids = transit.id)
        Transit.objects.create(ponumber = transit.ponumber, itemname_id = transit.itemname.id, quantity = qty, stockfrom = transit.stockfrom, suppliername_id = transit.suppliername.id, stockto = transit.stockto, hubname_id = transit.hubname.id, stockStatus = 'InTransit', transitdate = transit.transitdate)
    
    return HttpResponse('hello')


def Deliveredstatus(request, id):
    stock = Transit.objects.get(id = id)
    if(stock.stockStatus == 'Delivered'):
        stock.stockStatus = 'InTransit'
        stock.save()
        stocklist = Stock.objects.filter(stocktype = 'Transit', allids = stock.id)
        stocklist.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def TransferItem(request, id):
    try:
       
        print('get id', id)
        query = "SELECT *, SUM(CASE WHEN stocktype = 'Decrease' then -quantity ELSE quantity END) as adjusted_quantity from `mainApp_stock` where stocktoHubname_id = %s and stockStatus = 'Delivered' and stockto = 'Hub' Group By productID_id" % id
        hubs = Stock.objects.raw(query)
        print('hubs', hubs.query)
        hublist = []
        stocklist = []
        totalstockquantity = 0
        for hub in hubs:
            totalstockquantity = int(hub.adjusted_quantity)

            print('stock list', hub.adjusted_quantity)
            
            transferstock = Stock.objects.filter(stocktype = 'Transfer', productID__id = hub.productID.id, stockfromHubname__id = id)
            totalquantity = totalstockquantity
            print('transferstock', totalquantity)
            for stock in transferstock:
                if stock:
                    quantity = int(stock.quantity) if int(stock.quantity) else 0
                    totalquantity = totalquantity - quantity
            print('totalquantity', totalquantity)
            hub = {
                'itemid': hub.productID.id,
                'itemname': hub.productID.productName,
                'totalstock': totalquantity
            }
            hublist.append(hub)
        print('hub', hublist)
        responseData = {
            'error' : False,
            'message' : "Item Retrieved Successfully"
        }

        return JsonResponse({'data':hublist, 'stocklist': stocklist})


    except:
        responseData = {
            'error' : True,
            'message' : "Cound Not Find Item With ID"
        }

        return Response("Invalid Request")


def TransferStockReceivefileUpload(request):
    receiveddate = request.POST['receivedate'] or None
    id = request.POST['id']
    print("File path ", request.FILES)
    file = request.FILES['file']
    remarks = request.POST['remarks']
    stock = Transfer.objects.get(id = id)
    print('stock get', type(request.FILES['file']))
    if receiveddate != None:
        stock.receiveddate = receiveddate
        stock.file = file
        stock.transferStatus = 'Delivered'
        stock.remarks = remarks
        stock.save()
        transferqty = TransferQuantity.objects.filter(transfer__id = stock.id)
        for qty in transferqty:
            Stock.objects.create(stocktype = 'Transfer', stockfrom = stock.selectfrom, stockfromHubname_id = stock.source.id, stockto = stock.SelectTo, stocktoBranchname_id = stock.branchdestination.id if stock.branchdestination else "", stocktoHubname_id = stock.hubdestination.id if stock.hubdestination else "", productID_id = qty.item.id, quantity = qty.stocktransfered, allids = stock.id, 
                        stockStatus = 'Delivered', receiveddate = stock.receiveddate)
        
    elif receiveddate == '' or receiveddate == None:
        stock.receiveddate = datetime.now().date()
        stock.file = file
        stock.transferStatus = 'Delivered'
        stock.save()
        transferqty = TransferQuantity.objects.filter(transfer__id = stock.id)
        for qty in transferqty:
            Stock.objects.create(stocktype = 'Transfer', stockfrom = stock.selectfrom, stockfromHubname_id = stock.source.id, stockto = stock.SelectTo, stocktoBranchname_id = stock.branchdestination.id if stock.branchdestination else "", stocktoHubname_id = stock.hubdestination.id if stock.hubdestination else "", productID_id = qty.item.id, quantity = qty.stocktransfered, allids = stock.id, 
                             stockStatus = 'Delivered', receiveddate = stock.receiveddate)
    return HttpResponse('hello')


def TransferDeliveredstatus(request, id):
    stock = Transfer.objects.get(id = id)
    if(stock.transferStatus == 'Delivered'):
        stock.transferStatus = 'InTransit'
        stock.receiveddate = datetime.now()
        stock.save()
        stocklist = Stock.objects.filter(stocktype = 'Transfer', allids = stock.id)
        stocklist.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def StocktotalQty(requset):
    this_month = datetime.now()
    
    first = this_month.replace(day=1)
    lastmonth = first - timedelta(days=1)
    
    currentmonth = datetime.today().replace(day=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=lastmonth.day)
  
    balance = HubBalance.objects.filter(created_at=start_day_of_prev_month.date())    
        
    if balance:
        for hubbalance in balance:
            opening_exists = Stock.objects.raw(opening)
            for openingstock in opening_exists:
                closingstock = HubBalance.objects.get(id= hubbalance.id)
                print('closing', closingstock.hubid)
                if closingstock.hubid.id == openingstock.stockTohub and closingstock.item.id == openingstock.product:
                    closingstock.closingstock = int(closingstock.openingstock) + int(openingstock.merged_totalquantity)
                    closingstock.created_at = lastmonth.date()
                    closingstock.save()
                else:
                    closingstock.closingstock = int(closingstock.openingstock) + 0
                    closingstock.created_at = lastmonth.date()
                    closingstock.save()
                HubBalance.objects.create(hubid_id = closingstock.hubid.id, item_id = closingstock.item.id, openingstock = closingstock.closingstock, created_at = currentmonth.date())
                    
    else:
        opening = ("""SELECT
    id,
    stockHub AS hub,
    opening_stock,
    SUM(totalquantity) AS merged_totalquantity
FROM (
    SELECT
        productID_id AS id,
        stocktoHubname_id AS stockHub,
        CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END AS opening_stock,
        CASE WHEN stocktype IN ('Transfer', 'Decrease') THEN -quantity ELSE quantity END AS totalquantity
    FROM
        mainApp_stock
    WHERE
        receiveddate >= '{0}'
        AND receiveddate <= '{1}'
        AND stockStatus = 'Delivered'
        AND stocktoHubname_id IS NOT NULL -- Filter out rows where stocktoHubname_id is null

    UNION ALL

    SELECT
        productID_id AS id,
        stockfromHubname_id AS stockHub,
        0 AS opening_stock,
        CASE WHEN stocktype IN ('Transfer', 'Decrease') THEN -quantity ELSE quantity END AS totalquantity
    FROM
        mainApp_stock
    WHERE
        receiveddate >= '{2}'
        AND receiveddate <= '{3}'
        AND stockStatus = 'Delivered'
        AND stockfromHubname_id IS NOT NULL -- Filter out rows where stockfromHubname_id is null
) AS combined_stock
GROUP BY
    id, stockHub, opening_stock;""".format('2022-11-01', '2022-11-30','2022-11-01', '2022-11-30'))
        
        opening_exists = Stock.objects.raw(opening)
        
        for openingstock in opening_exists:
            
            
            closingstock = HubBalance.objects.create(hubid_id = openingstock.hub, item_id = openingstock.id, openingstock = openingstock.opening_stock, closingstock = openingstock.merged_totalquantity, created_at = '2022-11-30')
            HubBalance.objects.create(hubid_id = closingstock.hubid.id, item_id = openingstock.id, openingstock = closingstock.closingstock, created_at = '2022-12-01')
            
                    

def BranchStocktotalQty(requset):
    this_month = datetime.now()
    
    first = this_month.replace(day=1)
    lastmonth = first - timedelta(days=1)
    
    currentmonth = datetime.today().replace(day=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=lastmonth.day)
    balance = BranchBalance.objects.filter(created_at=start_day_of_prev_month.date())    
    
    if balance:
        for branchbalance in balance:
            opening = ("SELECT t1.product, t1.stockbranch, t1.opening_stock, t1.totalquantity FROM (SELECT *, productID_id AS product, stocktoBranchname_id AS stockbranch, SUM(CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN stocktype = 'Decrease' THEN -quantity ELSE quantity END) AS totalquantity FROM mainApp_stock WHERE receiveddate >= '{0}' AND receiveddate <= '{1}' AND stockStatus = 'Delivered' GROUP BY productID_id, stocktoBranchname_id) t1 JOIN ( SELECT *, productID_id AS product, stocktoBranchname_id AS stockbranch FROM mainApp_stock WHERE receiveddate >= '{2}' AND receiveddate <= '{3}' AND stockStatus = 'Delivered' GROUP BY productID_id, stocktoBranchname_id) t2 ON t1.product = t2.product AND t1.stockbranch = t2.stockbranch;".format(start_day_of_prev_month.date(), lastmonth.date(), start_day_of_prev_month.date(), lastmonth.date()))
            opening_exists = Stock.objects.raw(opening)
            for openingstock in opening_exists:
                closingstock = BranchBalance.objects.get(id= branchbalance.id)
                orderlist = Order.objects.filter(branchID__id = openingstock.stockbranch, product_id__id = openingstock.product)
                orderqty = 0
                if orderlist.count() > 0:
                    for order in orderlist:
                        print('total qty', int(openingstock.totalquantity) - int(order.quantity))
                        orderqty +=  int(order.quantity)
                else:
                    orderqty = 0
                if closingstock.branchid.id == openingstock.stockTohub and closingstock.item.id == openingstock.product:
                    closingstock.closingstock = int(closingstock.openingstock) + int(openingstock.totalquantity) - orderqty
                    closingstock.created_at = lastmonth.date()
                    closingstock.save()
                else:
                    closingstock.closingstock = int(closingstock.openingstock) + 0 - orderqty
                    closingstock.created_at = lastmonth.date()
                    closingstock.save()
                HubBalance.objects.create(hubid_id = closingstock.branchid.id, item_id = closingstock.item.id, openingstock = closingstock.closingstock, created_at = currentmonth.date())
                       
    else:
        opening = ("WITH combinedStock AS (SELECT *, productID_id AS product, stocktoBranchname_id AS stockbranch, SUM(CASE WHEN stocktype = 'OpeningStock' THEN quantity ELSE 0 END) AS opening_stock, SUM(CASE WHEN (stocktype = 'Decrease') THEN -quantity ELSE quantity END) AS totalquantity FROM mainApp_stock WHERE receiveddate >= '2023-07-01' AND receiveddate <= '2023-07-31' AND stockStatus = 'Delivered' GROUP BY productID_id, stocktoBranchname_id) SELECT *, t1.opening_stock, t1.totalquantity, t1.stockbranch, t1.product FROM combinedStock t1 JOIN combinedStock t2 ON t1.stockbranch = t2.stockbranch WHERE t1.product = t2.product and t1.stockbranch = t2.stockbranch GROUP BY t1.stockbranch, t1.product".format(start_day_of_prev_month.date(), lastmonth.date()))
        opening_exists = Stock.objects.raw(opening)
        orderqty = 0    
        for openingstock in opening_exists:
            
            orderlist = Order.objects.filter(branchID__id = openingstock.stockbranch, product_id__id = openingstock.product)
            
            if orderlist.count() > 0:
                for order in orderlist:
                    orderqty +=  int(order.quantity)
            else:
                orderqty = 0

            closingstock = BranchBalance.objects.create(branchid_id = openingstock.stockbranch, item_id = openingstock.product, openingstock = openingstock.opening_stock, closingstock = int(openingstock.totalquantity) - orderqty, created_at = lastmonth.date())
            BranchBalance.objects.create(branchid_id = openingstock.stockbranch, item_id = openingstock.product, openingstock = closingstock.closingstock, created_at = currentmonth.date())



def transferExport(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    body = json.loads(queryString)
    fromdate = body['fromdate']
    todate = body['todate']
    source = body['source']
    stockstatus = body['stockstatus']
    to = body['to']
    print('src', source)
    if source != 'all' and stockstatus != 'all':
        transfer = Transfer.objects.filter(source__id = source, transferStatus = stockstatus, transferdate__range=(fromdate, todate), SelectTo = to)
    elif source == 'all' and stockstatus != 'all':
        transfer = Transfer.objects.filter(transferStatus = stockstatus, transferdate__range=(fromdate, todate), SelectTo = to)
    elif source != 'all' and stockstatus == 'all':
        transfer = Transfer.objects.filter(source__id = source, transferdate__range=(fromdate, todate), SelectTo = to)
    elif source == 'all' and stockstatus == 'all':
        transfer = Transfer.objects.filter(transferdate__range=(fromdate, todate), SelectTo = to)
    print('transferdata', transfer)
    transferlist = []
    for transferdata in transfer:
        transferqty = TransferQuantity.objects.filter(transfer__id = transferdata.id)
        for qty in transferqty:
            if transferdata.SelectTo == 'Hub':
                qty = {
                    'SelectFrom': transferdata.selectfrom,
                    'Source': transferdata.source.name,
                    'SelectTo': transferdata.SelectTo,
                    'HubName': transferdata.hubdestination.name,
                    'Status': transferdata.transferStatus,
                    'ItemCode': qty.item.productCode,
                    'ItemName': qty.item.productName,
                    'QTY': qty.stocktransfered,
                    'TransferDate': transferdata.transferdate,
                    'ReceivedDate': transferdata.receiveddate
                }
                transferlist.append(qty)
            else:
                qty = {
                    'SelectFrom': transferdata.selectfrom,
                    'Source': transferdata.source.name,
                    'SelectTo': transferdata.SelectTo,
                    'BranchCode': transferdata.branchdestination.branchCode,
                    'BranchName': transferdata.branchdestination.branchName,
                    'Status': transferdata.transferStatus,
                    'ItemCode': qty.item.productCode,
                    'ItemName': qty.item.productName,
                    'QTY': qty.stocktransfered,
                    'TransferDate': transferdata.transferdate,
                    'ReceivedDate': transferdata.receiveddate
                }
                transferlist.append(qty)
    print('list', transferlist)
    if to == 'Hub':    
        ordered_list=["SelectFrom", "Source", "SelectTo",  "HubName", "Status", "ItemCode", "ItemName", "QTY", "TransferDate", "ReceivedDate"]
    else:
        ordered_list=["SelectFrom", "Source", "SelectTo",  "BranchCode", "BranchName", "Status", "ItemCode", "ItemName", "QTY", "TransferDate", "ReceivedDate"]
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TransferReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in transferlist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
        row+=1
    wb.save(response)
    return response
    
        

def RequisitionDownload_excel(request):

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Requisition.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row__num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.num_format_str = 'dd-mm-YYYY'
    columns = ['BranchCode', 'ProductCode', 'Quantity', 'RequisitionNumber', 'RequisitionDate']
    for col in range(len(columns)):
        ws.write(row__num, col, columns[col], font_style)
    font_style.font.bold = True

    wb.save(response)
    return response

def ExportOrderExcel(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    body = json.loads(queryString)
    fromdate = body['fromdate']
    todate = body['todate']
    branch = body['branch']
    product = body['item']
    if branch == 'all':
        orders = Order.objects.filter(product_id__id = product, orderDate__range = (fromdate, todate))
    else:
        orders = Order.objects.filter(branchID__id = branch, product_id__id = product, orderDate__range = (fromdate, todate))
    orderlist = []
    for order in orders:
        
        qty = {
            'State': order.branchID.region,
            'BranchCode': order.branchID.branchCode,
            'ClientNo': order.customerID,
            'LoanNo': order.loanNo,
            'ClientName': order.customerName,
            'LoanDate': order.loan_date,
            'InvoiceNo': order.invoiceNo,
            'LoanStatus': order.loanStatus,
            'LoanType': order.loanType,
            'OrderStatus': order.orderStatus,
            'ProductCode': order.product_id.productCode,
            'Quantity' : order.quantity,
            'orderDate': order.orderDate,
            'DeliveryDate': order.date_of_delivery,
            'Address': order.address
        }
        orderlist.append(qty)
        
    ordered_list=["State", "BranchCode", "ClientNo",  "LoanNo", "ClientName", "LoanDate", "InvoiceNo", "LoanStatus", "LoanType", "OrderStatus", "ProductCode", "Quantity", "orderDate", "DeliveryDate", "Address"]
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="OrderReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in orderlist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
        row+=1
    wb.save(response)
    return response

def Itemlist(request):
    items = Product.objects.all()
    itemlist = []
    for item in items:
        list = {
            'id': item.id,
            'name': item.productName
        }
        itemlist.append(list)
    return JsonResponse({"itemlist" : itemlist})

def adjustmentExport(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    body = json.loads(queryString)
    fromdate = body['fromdate']
    todate = body['todate']
    item = body['item']
    adjustment = Adjustment.objects.filter(adjustmentDate__range=(fromdate, todate))
    adjustmentlist = []
    for adjustmentdata in adjustment:
        adjustmentqty = AdjustmentStock.objects.filter(item__id = item, adjust__id = adjustmentdata.id)
        for qty in adjustmentqty:
            if adjustmentdata.adjustmentfor == 'Hub':
                qty = {
                    'AdjustmentFor': adjustmentdata.adjustmentDate,
                    'Adjustable': adjustmentdata.adjustableHub.name,
                    'AdjustmentType': adjustmentdata.adjustmentType,
                    'Item': qty.item.productName,
                    'Stock': qty.stock,
                    'AdjustmentDate': adjustmentdata.adjustmentDate
                }
                adjustmentlist.append(qty)
            else:
                qty = {
                    'AdjustmentFor': adjustmentdata.adjustmentDate,
                    'Adjustable': adjustmentdata.adjustableBranch.branchName,
                    'AdjustmentType': adjustmentdata.adjustmentType,
                    'Item': qty.item.productName,
                    'Stock': qty.stock,
                    'AdjustmentDate': adjustmentdata.adjustmentDate
                }
                adjustmentlist.append(qty)
    print('list', adjustmentlist)
        
    ordered_list=["AdjustmentFor", "Adjustable", "AdjustmentType",  "Item", "Stock", "AdjustmentDate"]
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="AdjustmentReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in adjustmentlist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
        row+=1
    wb.save(response)
    return response
 
def TransitExport(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    body = json.loads(queryString)
    fromdate = body['fromdate']
    todate = body['todate']
    item = body['item']
    stockstatus = body['stockstatus']
    if stockstatus != 'all':
        transit = Transit.objects.filter(itemname__id = item, stockStatus = stockstatus,transitdate__range=(fromdate, todate))
    elif stockstatus == 'all':
        transit = Transit.objects.filter(itemname__id = item, transitdate__range=(fromdate, todate))
    print(transit)
    transitlist = []
    for transitdata in transit:
        transitstock = {
            'PoNumber': transitdata.ponumber,
            'Item': transitdata.itemname.productName,
            'QTY': transitdata.quantity,
            'StockFrom': transitdata.stockfrom,
            'Supplier': transitdata.suppliername.suppliername,
            'StockTo': transitdata.stockto,
            'Hub': transitdata.hubname.name,
            'StockStatus': transitdata.stockStatus,
            'TransitDate': transitdata.transitdate,
            'ReceivedDate': transitdata.receiveddate
        }
        transitlist.append(transitstock)
        
    ordered_list=["PoNumber", "Item", "QTY",  "StockFrom", "Supplier", "StockTo", "Hub", "StockStatus", "TransitDate", "ReceivedDate"]
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TransitReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in transitlist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
        row+=1
    wb.save(response)
    return response
 
def TransferItemlist(request):
    items = Product.objects.all()
    itemlist = []
    for item in items:
        list = {
            'id': item.id,
            'name': item.productName
        }
        itemlist.append(list)
    hubs = Hub.objects.all()
    hublist = []
    for hub in hubs:
        hub = {
            'id': hub.id,
            'name': hub.name
        }
        hublist.append(hub)
    return JsonResponse({"itemlist" : itemlist, "hublist": hublist})

def Requisitionlist(request):
    items = Product.objects.all()
    itemlist = []
    for item in items:
        list = {
            'id': item.id,
            'name': item.productName
        }
        itemlist.append(list)
    branchs = Branch.objects.all()
    branchlist = []
    for branch in branchs:
        branch = {
            'id': branch.id,
            'name': branch.branchName
        }
        branchlist.append(branch)
    return JsonResponse({"itemlist" : itemlist, "branchlist": branchlist})

def RequisitionExport(request):
    queryString =  next(iter(request.POST))
    print('querystring', queryString)
    body = json.loads(queryString)
    fromdate = body['fromdate']
    todate = body['todate']
    item = body['item']
    stockstatus = body['stockstatus']
    branch = body['branch']
    print('req list', branch, stockstatus)
    if branch != 'all' and stockstatus != 'all':
        requisitions = Requisition.objects.filter(productname__id = item, branchName__id = branch, status = stockstatus,requisitionDate__range=(fromdate, todate))
    elif branch == 'all' and stockstatus == 'all':
        requisitions = Requisition.objects.filter(productname__id = item, requisitionDate__range=(fromdate, todate))
        print('all', requisitions)
    elif branch == 'all' and stockstatus != 'all':
        requisitions = Requisition.objects.filter(productname__id = item, status = stockstatus, requisitionDate__range=(fromdate, todate))
        print('branchall', requisitions)
    elif branch != 'all' and stockstatus == 'all':
        requisitions = Requisition.objects.filter(productname__id = item, branchName__id = branch, requisitionDate__range=(fromdate, todate))
        print('stockall', requisitions)
    requisitionlist = []
    for requisitiondata in requisitions:
        if requisitiondata.status == 'Completed':
            hubname = Transfer.objects.get(requisitionno__id = requisitiondata.id)
            hubname = hubname.source.name
        else:
            if requisitiondata.branchName.hubBranch:
                hubname = requisitiondata.branchName.hubBranch.name
            else:
                hubname = ''
        requisitionsstock = {
            'RequisitionNumber': requisitiondata.requisitionNumber,
            'Item': requisitiondata.productname.productName,
            'QTY': requisitiondata.quantity,
            'Branch': requisitiondata.branchName.branchName,
            'Hub': hubname,
            'Status': requisitiondata.status,
            'RequisitionDate': requisitiondata.requisitionDate,
        }
        requisitionlist.append(requisitionsstock)
        
    ordered_list=["RequisitionNumber", "Item", "QTY",  "Branch", "Hub", "Status", "RequisitionDate"]
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="RequisitionReport.xls"'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet("New Sheet")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header)
        ws.write(first_row,col,header)
    row=1
    incrementor = 1
    for StockList in requisitionlist:
        for _key,_value in StockList.items():
            col=ordered_list.index(_key)
            if(_key == "SlNo") :
                ws.write(row,col,incrementor)
                incrementor +=1
            else:
                ws.write(row,col,_value)
        row+=1
    wb.save(response)
    return response

def OrderList(request):
    items = Product.objects.all()
    itemlist = []
    for item in items:
        list = {
            'id': item.id,
            'name': item.productName
        }
        itemlist.append(list)
    branches = Branch.objects.all()
    branchlist = []
    for branch in branches:
        branch = {
            'id': branch.id,
            'name': branch.branchName
        }
        branchlist.append(branch)
    return JsonResponse({"itemlist" : itemlist, "branchlist": branchlist})
from django.http import HttpResponse
from django.views.generic import View

from mainApp.utils import render_to_pdf
import datetime
from num2words import num2words
from django.contrib import messages
from django.shortcuts import render, redirect

# pdf
def GenerateInvoicePdf(request, invoice):
    if invoice.product_id.price != '':
        if invoice.branchID.hubBranch and invoice.salehub:
            if (invoice.branchID.hubBranch.state.id) == (invoice.salehub.state.id):
                print('mTCHED', invoice.branchID.hubBranch.state.name,invoice.salehub.state.name)
                cgstvalue = round(((float(invoice.product_id.price) * float(invoice.quantity)) * float(invoice.product_id.cgst))/100,2)
                sgstvalue = round(((float(invoice.product_id.price) * float(invoice.quantity)) * float(invoice.product_id.sgst))/100,2)
                totalamount = (float(invoice.product_id.price) * float(invoice.quantity)) + cgstvalue + sgstvalue
                totalgst = round(cgstvalue + sgstvalue,2)
                amount = num2words(totalamount)
            else:
                print('not match', invoice.branchID.region,invoice.salehub.state.name)
            
                igstvalue = round(((float(invoice.product_id.price) * float(invoice.quantity)) * float(invoice.product_id.igst))/100,2)
                totalamount = (float(invoice.product_id.price) * float(invoice.quantity)) + igstvalue
                totalgst = round(igstvalue,2)
                amount = num2words(totalamount)
        # else:
        #     messages.error(request, "Select Hub and State")
    else: 
        if invoice.branchID.hubBranch and invoice.salehub:
            if (invoice.branchID.hubBranch.state.id) == (invoice.salehub.state.id):
                cgstvalue = ''
                sgstvalue = ''
                totalamount = ''
                totalgst = ''
                amount = ''
            else:
                igstvalue = ''
                totalamount = ''
                totalgst = ''
                amount = ''
        # else:
        #     messages.error(request, "Select Hub and State")
    if invoice.branchID.hubBranch and invoice.salehub:
        if (invoice.branchID.hubBranch.state.id) == (invoice.salehub.state.id):
            data = {
                    'companyname': invoice.salehub.name,
                    'CIN': invoice.salehub.state.cinNumber,
                    'GSTN': invoice.salehub.state.gst,
                    'regd': invoice.salehub.address,
                    # 'companypincode': '734001',
                    # 'companyPhonenumber': '0353-2504942',
                    'branchstate': (invoice.branchID.hubBranch.state.id),
                    'salehub': (invoice.salehub.state.id),
                    'branchName': invoice.branchID.branchName,
                    'invoice_id': invoice.invoiceNo,
                    'invoicedate': invoice.invoice_date,
                    'orderid': 111111,
                    'loandate': invoice.loan_date,
                    'product': invoice.product_id.productName,
                    'hsn': invoice.product_id.hsn,
                    'cgst': invoice.product_id.cgst,
                    'sgst': invoice.product_id.sgst,
                    'quantity': invoice.quantity,
                    'today': datetime.date.today(), 
                    'customer_name': invoice.customerName,
                    'customerid': invoice.customerID,
                    'orderdate': invoice.orderDate,
                    'invoicedate': invoice.invoice_date,
                    'address': str(invoice.address)+ " " +str(invoice.addressState)+ " " +str(invoice.landmark)+ "," +str(invoice.addressZipCode),
                    'company': invoice.branchID.company,
                    'rate': (float(invoice.product_id.price) * float(invoice.quantity)),
                    'cgst': invoice.product_id.cgst,
                    'sgst': invoice.product_id.sgst,
                    'cgstval': cgstvalue,
                    'sgstval': sgstvalue,
                    'totalamount': totalamount,
                    'amount': amount,
                    'loanno': invoice.loanNo,
                    'totalgst': totalgst,
                }
        else:
            data = {
                'companyname': invoice.salehub.name,
                'CIN': invoice.salehub.state.cinNumber,
                'GSTN': invoice.salehub.state.gst,
                'regd': invoice.salehub.address,
                'branchstate': str(invoice.branchID.region).lower(),
                'salehub': str(invoice.salehub.state.name).lower(),
                'branchName': invoice.branchID.branchName,
                'invoice_id': invoice.invoiceNo,
                'invoicedate': invoice.invoice_date,
                'orderid': 111111,
                'loandate': invoice.loan_date,
                'product': invoice.product_id.productName,
                'hsn': invoice.product_id.hsn,
                'igst': invoice.product_id.igst,
                'quantity': invoice.quantity,
                'today': datetime.date.today(), 
                'customer_name': invoice.customerName,
                'customerid': invoice.customerID,
                'orderdate': invoice.orderDate,
                'invoicedate': invoice.invoice_date,
                'address': str(invoice.address)+ " " +str(invoice.addressState)+ " " +str(invoice.landmark)+ "," +str(invoice.addressZipCode),
                'company': invoice.branchID.company,
                'rate': (float(invoice.product_id.price) * float(invoice.quantity)),
                'igst': invoice.product_id.igst,
                'igstval': igstvalue,
                'totalamount': totalamount,
                'amount': amount,
                'loanno': invoice.loanNo,
                'totalgst': totalgst,
            }
        print(data)
        pdf = render_to_pdf('custom-templates/pdf/invoice.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(invoice)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    else:
        messages.error(request, "Select Hub and State")
        return redirect('/mainApp/order/')
    


def GenerateChalanPdf(request,chalan):
    
    data = {
            'companyname': chalan['sourcefrom'],
            'sourceaddress': chalan['sourceaddress'],
            'sourcephone': chalan['sourcephone'],
            'CIN': 'U51909WB1991PTC053642',
            'GSTN': '19AADCP0333M1ZC',
            'BranchID': chalan['BranchID'],
            'branch': chalan['branch'],
            'HubID': chalan['HubID'],
            'hub': chalan['hub'],
            'branchmanager': chalan['branchmanager'],
            'hubcontactname': chalan['hubcontactname'],
            'branchphoneNo': chalan['branchphoneNo'],
            # 'gst': chalan.productID.gst,
            'transferlist': chalan['transferlist'],
            'stock_created': chalan['stock_created'],
            'orderdate':chalan['stock_created'], 
            # 'product': chalan.productID.productName,
            'stockid': chalan['transferid'],
            # 'quantity': chalan.quantity,
            'today': datetime.date.today(), 
            'dispatch_date': chalan['stock_created'],
            # 'totalcartons': round(int(chalan.quantity) / 4),
            'customer_name': 'Customer name',
            # 'price': float(chalan.productID.price) * float(chalan.quantity),
            'delivery_address': chalan['delivery_address'],
            'order_id': 1233434,
            'regd': '4-B, Dwarika Elegance, Burdwan Road, Siliguri, Darjeeling, WestBengal-734001',
            'penncophoneno': '91-353-2504942',
            'email': 'Accounts.pennco@gmail.com',
            'dispatch': 'PLOT NO 1980,81,82, Vill+PO- Kanduah, PS. Sankrail, Polly Park Dhulagarh- 711302',
    }
    pdf = render_to_pdf('custom-templates/pdf/chalan.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "BranchChalan.pdf" 
        content = "inline; filename=%s" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def GeneratePOPdf(request,purchase):
    suupliergrandtotaltotal = float(purchase['supplierquantitylist'][-1]['grandtotal'])
    data = {
            'supplier': purchase['supplier'],
            'supplierid': purchase['supplierid'],
            'supplieremail': purchase['supplieremail'],
            'PoNo': purchase['PoNo'],
            'date': purchase['date'],
            'supplieraddress': purchase['supplieraddress'],
            'suppliercity': purchase['suppliercity'],
            'supplierstate': purchase['supplierstate'],
            'supplierphone': purchase['supplierphone'],
            'supplierquantitylist': purchase['supplierquantitylist'],
            'suppliergrandtotal': suupliergrandtotaltotal,
            'amountwords': num2words(suupliergrandtotaltotal, lang='en_IN'),
            'statename': purchase['statename'],
            'stateaddress': purchase['stateaddress'],
            'statecin': purchase['statecin']
            # 'hublist': purchase['hublist'],
    }
    pdf = render_to_pdf('custom-templates/pdf/PurchaseOrder.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PurchaseOrder.pdf" 
        content = "inline; filename=%s" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
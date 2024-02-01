from django.contrib import admin
from django.urls import path
from mainApp.Filters.stockReceiveFilter import *
from .forms import *
from .models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from easy_select2 import select2_modelform
from import_export.admin import ImportExportModelAdmin
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from import_export.admin import ExportActionMixin
from import_export import resources
from import_export.fields import Field
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

admin.site.site_url = "http://127.0.0.1:8000/site/dashboard"
print(admin.site.site_url)
 


class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        super().get_queryset(request)
        if request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(email = request.user.email)   
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser','date_joined')
    search_fields = ('email', 'full_name',)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            return not obj.is_superuser

admin.site.register(User, UserAdmin)

class ProductResource(resources.ModelResource):
    productName = Field(attribute='productName', column_name='Product Name')
    productCode = Field(attribute='productCode', column_name='Product Code')
    sku = Field(attribute='sku', column_name='SKU')
    # cgst = Field(attribute='cgst', column_name='CGST')
    # sgst = Field(attribute='sgst', column_name='SGST')
    # cgst = Field(attribute='cgst', column_name='CGST')
    price = Field(attribute='price', column_name='Price')
    hsn = Field(attribute='hsn', column_name='HSN')

    class Meta:
        model = Product
        fields = ('productName', 'productCode', 'sku',  'price', 'hsn')
        export_order = ('productName', 'productCode', 'sku',  'price', 'hsn')

class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    form = ProductForm
    list_display = ('productName', 'productCode', 'sku', 'price')
    search_fields = ('productName', 'sku', 'productCode',)
    resource_class = ProductResource
    list_display_links = None
    
admin.site.register(Product, ProductAdmin)

class BranchResource(resources.ModelResource):
    branchName = Field(attribute='branchName', column_name='Branch Name')
    branchCode = Field(attribute='branchCode', column_name='Branch Code')
    branchManager = Field(attribute='branchManager', column_name='Branch Manager')
    branchMangerPhoneNo = Field(attribute='branchMangerPhoneNo', column_name='Branch Manager Phone Number')
    company = Field(attribute='company', column_name='Company')
    region = Field(attribute='region', column_name='Region')

    class Meta:
        model = Branch
        fields = ('branchName', 'branchCode', 'branchManager', 'branchMangerPhoneNo', 'company', 'region')
        export_order = ('branchName', 'branchCode', 'branchManager', 'branchMangerPhoneNo', 'company', 'region')

class BranchAdmin(ExportActionMixin, admin.ModelAdmin):
    form = BranchForm
    list_display = ('branchName', 'branchCode', 'branchManager', 'branchMangerPhoneNo','company', 'region')
    search_fields = ('branchName', 'branchCode', 'branchManager',)
    resource_class = BranchResource
    def get_queryset(self, request):
        super().get_queryset(request)
        if request.user.is_superuser:
            return Branch.objects.all()
        else:
            return Branch.objects.filter(branch_username = request.user.email)  
    class Media:
        js = (
            ('admin/js/branch.js',)
        )
    
admin.site.register(Branch, BranchAdmin)


class OrderAdmin(admin.ModelAdmin):
    form    = OrderForm
    def add_view(self, request, form_url='', extra_context=None):
        branch = request.GET.get('branchID',None)
        product = request.GET.get('product_id',None)
        if branch != None and product!= None:
            g = request.GET.copy()
        return super(OrderAdmin, self).add_view(request, form_url, extra_context)
    
    def get_queryset(self, request):
        super().get_queryset(request)
        if request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(branchID__branch_username = request.user.email)   

    def download_link(self, obj):
        return format_html(
            '<a href="/site/print/invoice/no/%s">Download</a>' % (obj.id),
            )
        
    download_link.short_description = "Print Invoice"

    def BranchName(self, obj):
        return obj.branchID.branchName
        
    BranchName.short_description = "Branch"

    list_display = ('customerName', 'customerID', 'BranchName', 'product_id', 'salehub', 'download_link', 'orderDate', 'date_of_delivery', 'quantity')
    fields = ('customerName', 'customerID', 'branchID', 'product_id', 'salehub','loan_date', 'loanStatus', 'loanType',  'Phone', 'address', 'addressState', 'addressZipCode', 'landmark',  'invoice_date', 'invoiceNo', 'orderDate', 'date_of_delivery', 'orderStatus', 'loanNo', 'quantity')
    search_fields = ('invoiceNo', 'customerName', 'customerID',)
    # list_filter = (('branchID', RelatedDropdownFilter), ('product_id', RelatedDropdownFilter))

    class Media:
        js = (
             ('admin/js/orders.js', 'admin/js/orderselect.js',)
        )   
        css = {
            'all': ('admin/css/orders.css',)
        }
    
admin.site.register(Order, OrderAdmin)

class StockResource(resources.ModelResource):
    stocktype = Field(attribute='stocktype', column_name='Stock Type')
    stockfrom = Field(attribute='stockfrom', column_name='From')
    stockfromSuppliername = Field(attribute='stockfromSuppliername', column_name='Supplier')
    stockfromHubname = Field(attribute='stockfromHubname', column_name='Stock From Hub')
    stockto = Field(attribute='stockto', column_name='To')
    stocktoBranchname = Field(attribute='stocktoBranchname', column_name='Branch Name')
    stocktoHubname = Field(attribute='stocktoHubname', column_name='HubName')
    productID = Field(attribute='productID', column_name='Item')
    quantity = Field(attribute='quantity', column_name='Quantity')
    created_at = Field(attribute='created_at', column_name='Stock Created')
    receiveddate = Field(attribute='receiveddate', column_name='Stock Received')
    stockStatus = Field(attribute='stockStatus', column_name='Stock Status')

    class Meta:
        model = Stock
        fields = ('stocktype', 'stockfrom', 'stockfromSuppliername', 'stockfromHubname', 'stockto', 'stocktoBranchname','stockStatus', 'stocktoHubname', 'productID', 'quantity', 'created_at', 'receiveddate')
        export_order = ('stocktype', 'stockfrom', 'stockfromSuppliername', 'stockfromHubname', 'stockto', 'stocktoBranchname','stockStatus', 'stocktoHubname', 'productID', 'quantity', 'created_at', 'receiveddate')
class StockAdmin(ExportActionMixin,admin.ModelAdmin):
    form = StockForm
    def get_queryset(self, request):
        super().get_queryset(request)
        if request.user.is_superuser:
            return Stock.objects.all()
        else:
            return Stock.objects.filter(stocktoBranchname__branch_username = request.user.email)

    def Destination(self, obj):
        if obj.stocktype == 'Transit':
            name = obj.stocktoHubname.name
            return name
        if obj.stockto == 'Branch' and obj.stocktype == 'Transfer':
            print('branch', obj.stocktoBranchname)
            name = obj.stocktoBranchname.branchName
            return name
        if obj.stockto == 'Hub' and obj.stocktype == 'Transfer':
            print('hub', obj.stocktoHubname)
            name = obj.stocktoHubname.name
            return name
        if obj.stocktype == 'OpeningStock' and obj.stockto == 'Hub':
            name = obj.stocktoHubname.name
            return name
        if obj.stocktype == 'OpeningStock' and obj.stockto == 'Branch':
            name = obj.stocktoBranchname.branchName
            return name
        if obj.stocktype == 'Increase' and obj.stockto == 'Hub':
            name = obj.stocktoHubname.name
            return name
        if obj.stocktype == 'Increase' and obj.stockto == 'Branch':
            name = obj.stocktoBranchname.branchName
            return name
        if obj.stocktype == 'Decrease' and obj.stockto == 'Hub':
            name = obj.stocktoHubname.name
            return name
        if obj.stocktype == 'Decrease' and obj.stockto == 'Branch':
            name = obj.stocktoBranchname.branchName
            return name
        
    Destination.short_description = "Destination"
    
    resource_class = StockResource
    search_fields = ['productID__productName', 'stocktoBranchname__branchName', 'stocktoHubname__name', 'stockfromHubname__name']
    list_display = ('stocktype', 'stockfrom',  'stockto', 'Destination',  'productID', 'quantity', 'stockStatus', 'receiveddate') 
    list_display_links = None
admin.site.register(Stock, StockAdmin)


class StockReceiveAdmin(admin.ModelAdmin):
    class Media:
        js = (
            ('admin/js/stockreceive.js', )
        )
    change_list_template = 'custom-templates/stock-receive-filter.html'

admin.site.register(StockReceive, StockReceiveAdmin)


class StockReceiveReportAdmin(admin.ModelAdmin):
    change_list_template = 'custom-templates/stock-received-report.html'

admin.site.register(StockReceiveReport, StockReceiveReportAdmin)


class StockReportAdmin(admin.ModelAdmin):
    # class Media:
        # css = {
        #     'all': ('admin/css/stock.css','admin/css/stockreport.css', )
        # }
    change_list_template = 'custom-templates/stock-report.html'

admin.site.register(StockReport, StockReportAdmin)


class SaleAdmin(admin.ModelAdmin):
    change_list_template = 'custom-templates/Sale.html'

admin.site.register(Sale, SaleAdmin)


class PrintInoviceAdmin(admin.ModelAdmin):
    change_list_template = 'custom-templates/print-invoice.html'

admin.site.register(PrintInovice, PrintInoviceAdmin)


class DisbursementReportAdmin(admin.ModelAdmin):
    change_list_template = 'custom-templates/disbursement-report.html'

admin.site.register(DisbursementReport, DisbursementReportAdmin)


class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['suppliername', 'email']
    list_display = ('suppliername', 'email',  'address', 'city', 'state', 'phone',)
    
admin.site.register(Supplier, SupplierAdmin)


class HubAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = HubForm
    list_display = ('name', 'address',)
    class Media:
        js = (
             ('admin/js/hub.js', )
        )
    
admin.site.register(Hub, HubAdmin)


class QuantityInline(admin.StackedInline):
    form = QuantityForm
    model = Quantity
    fields = ['items', 'quantity', 'button']
    readonly_fields = ("button",)
    extra = 0
    verbose_name = "Quantity"
    verbose_name_plural = "Quantity"
    class Media:
        js = (
             ('admin/js/purchase.js', )
        )
    def button (self, obj):
    #   return format_html("<button class='get-item' type='button' >Click Me!</button>")
        # return format_html("<a href='#' class='open_popup btn btn-xs' >Click For Popup</a>")
        return format_html("<button type='button' class='get-item btn btn-success' data-toggle='modal' data-target='.bd-example-modal-xl' id='submit'>Allocate</button>")

    button.allow_tags=True

class HubQuantityInline(admin.ModelAdmin):
    form = HubQuantityForm
    fields = ['supplier', 'items', 'hub', 'quantity']
admin.site.register(HubQuantity, HubQuantityInline)   


class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseForm
    inlines=[QuantityInline]
    def PoNumber(self, obj):
        
        if (obj.status == 'Pending'):
            id = obj.id
            return format_html(
                '<a href="/mainApp/purchase/%s/change">%s</a>' % (obj.id, obj.id),
                )
            
        else:
            id = obj.id
            return id
            
    PoNumber.short_description = 'PO Number'

    def download_PO(self, obj):
        if(obj.status == 'Confirmed'):
            return format_html(
                '<a href="/site/print/PoPDF/%s"><i class="fa fa-print fa-lg"></i></a>' % (obj.id),
                )
        
    download_PO.short_description = "Print Purchase Order"


    search_fields = ('supplier_name__suppliername', 'PoNumber')
    list_display = ('PoNumber','supplier_name', 'status',  'date', 'download_PO')
    list_display_links = None
    class Media:
        
        css = {
            'all': ('admin/css/purchase.css',)
        }
    
admin.site.register(Purchase, PurchaseAdmin)

admin.site.register(Quantity)

class TransitResource(resources.ModelResource):
    ponumber = Field(attribute='ponumber', column_name='Po Number')
    itemname = Field(attribute='itemname', column_name='Item')
    quantity = Field(attribute='quantity', column_name='Quantity')
    stockfrom = Field(attribute='stockfrom', column_name='Stock From')
    suppliername = Field(attribute='suppliername', column_name='Supplier Name')
    stockto = Field(attribute='stockto', column_name='Stock To')
    hubname = Field(attribute='hubname', column_name='Hub Name')
    stockStatus = Field(attribute='stockStatus', column_name='Stock Status')
    transitdate = Field(attribute='transitdate', column_name='Transit Date')
    receiveddate = Field(attribute='receiveddate', column_name='Received Date')

    class Meta:
        model = Transit
        fields = ('ponumber', 'itemname', 'quantity', 'stockfrom', 'suppliername', 'stockto', 'hubname', 'stockStatus', 'transitdate', 'receiveddate')
        export_order = ('ponumber', 'itemname', 'quantity', 'stockfrom', 'suppliername', 'stockto', 'hubname', 'stockStatus', 'transitdate', 'receiveddate')
class TransitAdmin(admin.ModelAdmin):
    def status(self, obj):
        if(obj.stockStatus == 'InTransit'):
            
            return format_html("<button type='button' class='receivestock btn btn-success' id='submitbutton-{0}' data-toggle='modal' data-target='.bd-example-modal-xl'>Accept</button>", obj.id)
            
        if(obj.stockStatus == 'Delivered'):
            html =  format_html(
                '<div>Received</div>',
                )
            html1 =  format_html(
                '<a href="/site/deliveredstatus/%s" class="btn btn-warning">Roll Back</a>' % (obj.id),
                )
            return html + html1
    status.short_description = "Status"
    
    def fileshow(self, obj):
        if obj.stockStatus == 'Delivered':
            file = mark_safe('<div><a href="/media/{0}" target="_blank"/>File</a></div>'.format(obj.file))
            return file
        else:
            file = ''
            return file
    fileshow.short_description = "File"
   

    list_display = ('ponumber', 'itemname', 'quantity', 'stockfrom', 'suppliername', 'stockto', 'hubname', 'transitdate', 'receiveddate', 'fileshow', 'status')
   
    search_fields = ['ponumber', 'itemname__productName', 'hubname__name']
    class Media:
        js = (
             ('admin/js/transitreceive.js',)
        )
        css = {
            'all': ('admin/css/transit.css',)
        }
    def has_add_permission(self, request, obj=None):
        return False
    list_display_links = None
    
admin.site.register(Transit, TransitAdmin)


class TransferQuantityAdmin(admin.StackedInline):
    form = TransferQuantityForm
    model = TransferQuantity
    fields = ['item', 'transferablestock', 'stocktransfered', 'comment']
    extra = 1
    verbose_name = "TransferQuantity"
    verbose_name_plural = "TransferQuantity"
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TransferQuantityAdmin, self).get_form(request, obj, **kwargs)
        item = request.GET.get('item')
        if item and len(item) > 0:
            form.base_fields['item'].initial = item

class TransferResource(resources.ModelResource):
    selectfrom = Field(attribute='selectfrom', column_name='Stock From')
    source = Field(attribute='source', column_name='Source')
    SelectTo = Field(attribute='SelectTo', column_name='Select To')
    branchdestination = Field(attribute='branchdestination', column_name='Branch')
    hubdestination = Field(attribute='hubdestination', column_name='Hub')
    transferStatus = Field(attribute='transferStatus', column_name='Transfer Status')
    transferdate = Field(attribute='transferdate', column_name='Transfer Date')
    

    class Meta:
        model = Transfer
        fields = ('selectfrom', 'source', 'SelectTo', 'branchdestination', 'hubdestination', 'transferStatus', 'transferdate')
        export_order = ('selectfrom', 'source', 'SelectTo', 'branchdestination', 'hubdestination', 'transferStatus', 'transferdate')



class TransferAdmin(admin.ModelAdmin):
    form = TransferForm
    inlines=[TransferQuantityAdmin]
    fields = ('selectfrom', 'source', 'SelectTo', 'branchdestination', 'hubdestination', 'requisitionno', 'transferdate')
    def destination(self, obj):
        destination = ''
        if obj.SelectTo == 'Hub':
            destination = obj.hubdestination.name
        if obj.SelectTo == 'Branch':
            destination = obj.branchdestination.branchName
        return destination
    destination.short_description = "Destination"

    def transferno(self, obj):
        return obj.id
    transferno.short_description = "Transfer No"

    def qty(self, obj):
        stockqty = TransferQuantity.objects.filter(transfer__id = obj.id)
        stockqtylist = []
        for stock in stockqty:
            stock = stock.stocktransfered
            stockqtylist.append(stock)
        return stockqtylist
    qty.short_description = "Quantity"

    def item(self, obj):
        stockqty = TransferQuantity.objects.filter(transfer__id = obj.id)
        stockqtylist = []
        for stock in stockqty:
            stock = stock.item.productName
            stockqtylist.append(stock)
        return stockqtylist
    item.short_description = "Item"

    def download_chalan(self, obj):
        chalan = TransferQuantity.objects.filter(transfer__id = obj.id)
        for chalantransfer in chalan:
            return format_html(
                '<a href="/site/print/chalan/%s">Chalan</a>' % (obj.id),
                )
    download_chalan.short_description = "Print Challan"

    def status(self, obj):
        if(obj.transferStatus == 'InTransit'):
            return format_html("<button type='button' class='get-item btn btn-success' id='submitbutton-{0}' data-toggle='modal' data-target='.bd-example-modal-xl' id='submit'>Accept</button>", obj.id)
           
        if(obj.transferStatus == 'Delivered'):
            html =  format_html(
                '<div>Received</div>',
                )
            html1 =  format_html(
                '<a href="/site/TransferDeliveredstatus/%s" class="btn btn-warning">Roll Back</a>' % (obj.id),
                )
            return html + html1

    search_fields = ['source__name', 'branchdestination__branchName', 'hubdestination__name']

    
    def fileshow(self, obj):
        if obj.transferStatus == 'Delivered':
            file = mark_safe('<div><a href="/media/{0}" target="_blank"/>File</a></div>'.format(obj.file))
            return file
        else:
            file = ''
            return file
    fileshow.short_description = "File"
    list_display = ('transferno','selectfrom', 'source', 'SelectTo', 'destination', 'item', 'qty', 'transferdate', 'receiveddate', 'fileshow', 'download_chalan', 'status')
    class Media:
        js = (
             ('admin/js/transfer.js', 'admin/js/transferselect.js', )
        )
        css = {
            'all': ('admin/css/transfer.css',)
        }

admin.site.register(Transfer, TransferAdmin)
    
admin.site.register(TransferQuantity)

class AdjustmentStockAdmin(admin.StackedInline):
    form = AdjustmentStockForm
    model = AdjustmentStock
    fields = ['item', 'stock']
    extra = 0
    verbose_name = "AdjustmentStockForm"
    verbose_name_plural = "AdjustmentStockForm"


class AdjustmentAdmin(admin.ModelAdmin):
    form = AdjustmentForm
    inlines=[AdjustmentStockAdmin]
    def stockadjust(self, obj):
        stockqty = AdjustmentStock.objects.filter(adjust__id = obj.id)
        stockqtylist = []
        for stock in stockqty:
            stock = stock.stock
            stockqtylist.append(stock)
        return stockqtylist
    stockadjust.short_description = "Adjustment Quantity"
    list_display = ['adjustmentNo', 'adjustmentDate', 'stockadjust', 'adjustmentfor', 'adjustmentType']
    search_fields = ['adjustableHub__name', 'adjustableBranch__branchName']
    class Media:
        js = (
            ('admin/js/adjustment.js','admin/js/adjustmentselect.js',)
        )
        css = {
            'all': ('admin/css/adjustment.css',)
        }
    
admin.site.register(Adjustment, AdjustmentAdmin)


admin.site.register(AdjustmentStock)


class HubBalanceAdmin(admin.ModelAdmin):
    list_display = ('hubid', 'item', 'openingstock', 'closingstock', 'created_at')
    ordering = ['-created_at']
admin.site.register(HubBalance, HubBalanceAdmin)

class BranchBalanceAdmin(admin.ModelAdmin):
    list_display = ('branchid', 'item', 'openingstock', 'closingstock', 'created_at')
    ordering = ['-created_at']
admin.site.register(BranchBalance, BranchBalanceAdmin)

class RequisitionAdmin(admin.ModelAdmin):
    form = RequisitionForm
    def ChalanCreate(self, obj):
        if obj.status == 'Pending':
            
            html =  format_html(
                            '<a href="/mainApp/transfer/add/?SelectTo=%s%sbranchdestination=%s%sitem=%s%srequisitionno=%s%squantity=%s%sselectfrom=%s" class="btn btn-success">Create Transfer Chalan</a>' % ('Branch','&',obj.branchName.id, '&', obj.productname.id, '&', obj.id, '&', obj.quantity, '&', 'Hub'),
                            )
            return html
    def BranchCode(self, obj):
       code = obj.branchName.branchCode
       return code
    BranchCode.short_description = "Branch Code"
    
    def HubName(self, obj):
        if obj.status == 'Completed':
            hub = Transfer.objects.get(requisitionno__id = obj.id)
            hubname = hub.source.name
        else:
            hubname = obj.branchName.hubBranch
        return hubname
    HubName.short_description = "Hub"

    list_display = ('id', 'requisitionNumber', 'status', 'productname', 'quantity', 'BranchCode', 'branchName', 'HubName', 'requisitionDate', 'ChalanCreate')
    ordering = ['-requisitionDate']
    exclude = ['chalanNumber', 'status']
    list_filter = ['status']
    search_fields = ['requisitionNumber', 'productname__productName', 'branchName__branchCode', 'branchName__branchName']
    class Media:
        js = (
            ('admin/js/requisition.js',)
        )
    
admin.site.register(Requisition, RequisitionAdmin)


class StateAdmin(admin.ModelAdmin):
    form = StateForm
    list_display = ('name', 'address', 'gst', 'cinNumber')
    ordering = ['-id']
    search_fields =  ['name']
    
admin.site.register(State, StateAdmin)
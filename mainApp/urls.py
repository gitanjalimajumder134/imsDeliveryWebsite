from django.urls import path
from . import views
from mainApp.Filters.stockReceiveFilter import *
from mainApp.Filters.dashboard import *
# from django.conf.urls import url
from mainApp.views import *
app_name = "site"
urlpatterns = [
    # Class Based Views
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='site-dashboard'),
    path('salesBar', DashboardView.getSalesChart, name='salesBar'),


    
    # path('stockreceive', StockReceiveView.as_view(), name='site-stockreceive'),
    path('stockreceivereport', StockReceiveReportView.as_view(), name='site-stockreceivereport'),
    path('stockreport', StockReportView.as_view(), name='site-stockreport'),
    path('disbursement', DisbursementView.as_view(), name='site-disbursement'),
    # path('disburse/<int:loanAppNo>', DisburseView.as_view(), name='site-disburse'),
    # path('sale', SaleView.as_view(), name='site-sale'),
    path('printinovice', PrintInoviceView.as_view(), name='site-printinovice'),
    path('disbursementreport', DisbursementReportView.as_view(), name='site-disbursementreport'),
    path('import/orders', ordersImport.as_view(), name='site-import-orders'),
    path('print/invoice', printPDFView.as_view(), name='site-print-invoice'),
    path('print/invoice/no/<int:id>', printPDFView.as_view(), name='site-print-invoice-no'),
    path('getold-loan-data',GetLoanData.as_view(), name='site-getold-loan-data'),
    path('print/chalan/<int:transferID>', printChalan.as_view(), name='site-chalan'),
    path('export_excel/', views.export_excel,name="export_excel"),
    path('disburse/<int:id>',DisbursementView.as_view(),name='disburse'),
    path('Orderexport/excel', views.OrderDownload_excel, name='OrderExportexcel'),
    path('hub/allocate/<int:supplier>/<int:items>/<int:purchase>/<int:state>', HubAllocation, name='modal'),
    path('hubpost/allocate', hubpost, name='huballocate'),
    path('print/PoPDF/<int:id>', printPOPDF.as_view(), name='site-PurchaseOrder'),
    path('deliveredstatus/<int:id>', Deliveredstatus, name='site-DeliveredStatus'),
    path('transferitem/<int:id>', TransferItem, name='site-Transferitem'),
    # path('TransferChangeItem/<int:id>', TransferChangeItem, name='site-TransferChangeItem'),
    path('TransferDeliveredstatus/<int:id>', TransferDeliveredstatus, name='site-TransferDeliveredstatus'),
    path('StocktotalQty', StocktotalQty, name='site-StocktotalQty'),
    path('stockreceivefileupload', TransferStockReceivefileUpload, name='site-stockreceivefileupload'),
    path('BranchStocktotalQty', BranchStocktotalQty, name='site-BranchStocktotalQty'),
    path('TransitReceive', TransitReceive, name='site-TransitReceive'),
    path('transfer/export', transferExport, name='transferexport'),
    path('import/requisition', RequisitionImport.as_view(), name='site-import-requisition'),
    path('Requisitionexport/excel', views.RequisitionDownload_excel, name='RequisitionExportexcel'),
    path('order/export', ExportOrderExcel, name='orderexport'),
    path('itemlist', Itemlist, name='itemlist'),
    path('adjustment/export', adjustmentExport, name='adjustmentexport'),
    path('transit/export', TransitExport, name='transitexport'),
    path('transferitemlist', TransferItemlist, name='transferitemlist'),
    path('requisitionlist', Requisitionlist, name='requisitionlist'),
    path('requisition/export', RequisitionExport, name='requisitionexport'),
    path('orderlist', OrderList, name='orderlist'),
]


from pyexpat import model
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
import re
from django.db.models.functions import Length
from datetime import datetime,timedelta 

class UserManager(BaseUserManager):
     
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            # with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise
 
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        return self._create_user(email, password=password, **extra_fields)


# Registered User
class User(AbstractBaseUser, PermissionsMixin):

    date_joined = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, default=email)
    region = models.CharField(max_length=254, blank=True)
    phone = models.CharField(max_length=254, blank=True)
    password = models.CharField(max_length=254)
    userType = models.CharField(max_length=254, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    pass_last_updated = models.CharField(max_length=254, blank=True)
    

    objects = UserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
 
    def save(self, force_insert=False, force_update=False):

        self.username = self.email
        super(User, self).save(force_insert, force_update)


    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def is_mfibranch(self):
        return self.groups.filter(name='MFI_BRANCH').exists()

    def is_mfiho(self):
        return self.groups.filter(name='MFI_HO').exists()

    # def is_admin(self):
    #     return self.filter(is_superuser=True).exists()
    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'User'

    def __str__(self):
        return 'Full Name: {} | Email: {}'.format(self.full_name, self.email,)

# Registered Products
class Product(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True, help_text='date create')
    productName = models.CharField(max_length=100, blank=True, help_text='name a product')
    productCode = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=100, default="")
    cgst = models.CharField(max_length=254, blank=True, db_column='gst')
    sgst = models.CharField(max_length=254, blank=True)
    igst = models.CharField(max_length=254, blank=True)
    price = models.CharField(max_length=254, blank=True)
    hsn = models.CharField(max_length=254, blank=True)


    class Meta:
        ordering = ('-id',)
        verbose_name = 'Product'

    def __str__(self):
        return self.productName

# Registered Branch
class Branch(models.Model):
    branchName = models.CharField(max_length=100, default="", blank=True)
    branchCode = models.CharField(max_length=100, default="", unique=True)
    branchManager = models.CharField(max_length=100, default="", blank=True)
    branchMangerPhoneNo = models.CharField(max_length=100, default="", blank=True,db_column="branchMangerNo")
    company = models.CharField(max_length=100, default="", blank=True)
    address = models.CharField(max_length=254, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    pincode = models.CharField(max_length=100, default="", blank=True)
    region = models.CharField(max_length=100, default="", blank=True)
    branch_username =  models.EmailField(max_length=100, unique=True,default="",blank=True,null = True)
    branch_password = models.CharField(max_length=254,blank=True,default="",null = True)
    hubBranch = models.ForeignKey('Hub', on_delete=models.CASCADE, null = True, related_name='hubBranch', verbose_name='Hub')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Branch'

    def __str__(self):
        return self.branchName

# Registered Order
class Order(models.Model):
    # stockID               = models.ForeignKey('Stock', on_delete=models.CASCADE, blank=True, related_name='stockID', null=True)
    branchID              = models.ForeignKey(Branch, on_delete=models.CASCADE, null = True)
    loan_date             = models.CharField(max_length=100, default="", blank=True, db_column='loan_approval_date')
    loanstatus         = [
        ('Active','Active'),
        ('InActive','InActive')
        ]
    loanStatus            = models.CharField(max_length=100, choices=loanstatus, default="Active")
    loanType              = models.CharField(max_length=100, default="", blank=True)
    customerID            = models.CharField(max_length=100, default="", blank=True)
    customerName          = models.CharField(max_length=100, default="", blank=True)
    husband_name          = models.CharField(max_length=100, default="", blank=True)
    product_id            = models.ForeignKey(Product, on_delete=models.CASCADE, null = True, verbose_name='Product')
    model                 = models.CharField(max_length=100, default="", blank=True)

    member_offer_price    = models.CharField(max_length=100, default="", blank=True)
    vendor_id             = models.CharField(max_length=100, default="", blank=True)
    supplierName         = models.CharField(max_length=100, default="", blank=True, verbose_name= 'Supplier')
    dealer_code           = models.CharField(max_length=100, default="", blank=True)

    phone_regex           = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    Phone                 = models.CharField(validators=[phone_regex], max_length=10, default="", blank=True)
    address               = models.CharField(max_length=100, default="", blank=True)
    addressState          = models.CharField(max_length=100, default="", blank=True)
    addressZipCode        = models.CharField(max_length=6, blank=True)
    landmark              = models.CharField(max_length=100, blank=True)
    village               = models.CharField(max_length=100, blank=True)
    district_name         = models.CharField(max_length=100, blank=True)
    despatch_date         = models.CharField(max_length=100, blank=True)
    serial_number         = models.CharField(max_length=100, blank=True)
    new_product_serial_no = models.CharField(max_length=100, blank=True)
    invoice_date          = models.CharField(max_length=100, blank=True)
    invoiceNo             = models.CharField(max_length=100, default="", blank=True)
    country               = models.CharField(max_length=100, default="", blank=True)
    orderDate             = models.DateField(max_length=100, default="", blank=True, null = True)
    date_of_delivery      = models.CharField(max_length=100, default="", blank=True, verbose_name= "Date of Delivery")
    order_company         = models.CharField(max_length=100, default="", blank=True)
    center_location       = models.CharField(max_length=100, default="", blank=True)
    main_company          = models.CharField(max_length=100, default="", blank=True)
    statusOptions         = [
        ('Pending','Pending'),
        ('Delivered','Delivered')
        ]
    orderStatus           = models.CharField(max_length=100, choices=statusOptions, default="Delivered")
    EDD                   = models.CharField(max_length=100, default="", blank=True)
    loanNo                = models.CharField(max_length=100, default="", blank=True, db_column="loanAppNo")
    quantity              =models.CharField(max_length=100, default="1", blank=True, null=True)
    salehub = models.ForeignKey('Hub', on_delete=models.CASCADE, related_name='Salehub', blank=True, null=True, verbose_name="Sale Hub", db_column="salehuub")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Order'

    def __str__(self):
        return self.customerName


# Registered Stock
class Stock(models.Model):
    stocktype = models.CharField(max_length=100, default="", blank=True, verbose_name= "Type")
    stockfrom = models.CharField(max_length=201, blank=True, default="", verbose_name="From")
    stockfromSuppliername  = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='SupplierID', blank=True, null=True, verbose_name="Name")
    stockfromHubname  = models.ForeignKey('Hub', on_delete=models.CASCADE, related_name='stockHubId', blank=True, null=True, verbose_name="Name")
    stockTochoice = [
    ('Hub','Hub'),
    ('Branch', 'Branch')
    ]
    stockto = models.CharField(max_length=201, blank=True, default="", verbose_name="To", choices=stockTochoice)
    stocktoBranchname  =models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='BranchID', blank=True, null=True, verbose_name="Name")
    stocktoHubname  =models.ForeignKey('Hub', on_delete=models.CASCADE, related_name='HubID', blank=True, null=True, verbose_name="Name")
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productID', null = True, verbose_name='Product')
    quantity = models.CharField(max_length=100, default="", blank=True)
    created_at = models.DateField(auto_now_add=True,blank=True,null = True, verbose_name='Transfer Date')
    receiveddate = models.DateField(auto_now= False, blank=True,null=True)
    stockStatusOptions = [
    ('InTransit','In Transit'),
    ('Delivered','Delivered')
    ]
    stockStatus = models.CharField(max_length=100, default="InTransit", blank=True,choices=stockStatusOptions)
    allids = models.CharField(max_length=201, blank=True,null=True)
    file = models.FileField(blank=True, default="", verbose_name='File')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Stock'

    def __str__(self):
        return str(self.id)


class StockReceive(models.Model):
    pass


class StockReceiveReport(models.Model):
    pass


class StockReport(models.Model):
    pass


class Sale(models.Model):
    pass


class PrintInovice(models.Model):
    pass


class DisbursementReport(models.Model):
    file = models.FileField(blank=True)

class Supplier(models.Model):
    suppliername    = models.CharField(max_length=100, default="", blank=True, verbose_name= 'Supplier Name')
    email    = models.CharField(max_length=100, default="", blank=True)
    address    = models.CharField(max_length=256, default="", blank=True)
    city   = models.CharField(max_length=100, default="", blank=True)
    state   = models.CharField(max_length=100, default="", blank=True)
    phone    = models.CharField(max_length=12, default="", blank=True, verbose_name= 'Phone Number')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Supplier'

    def __str__(self):
        return self.suppliername

class State(models.Model):
    name = models.CharField(max_length=201, blank=True, db_column='Name')
    address = models.CharField(max_length=201, blank=True, db_column='Full Address')
    gst = models.CharField(max_length=201, blank=True, db_column='GST Number')
    cinNumber = models.CharField(max_length=201, blank=True, db_column='CIN Number')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'State'

    def __str__(self):
        return str(self.name)

class Hub(models.Model):
    name = models.CharField(max_length=256, default="", blank=True, verbose_name='Hub Name')
    contactname = models.CharField(max_length=256, default="", blank=True, verbose_name='Contact Name')
    address = models.CharField(max_length=256, default="", blank=True)
    phone    = models.CharField(max_length=12, default="", blank=True, verbose_name= 'Contact Number')
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, related_name='HubState', verbose_name= 'State', null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Hub Master'

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    status  = [
        ('Pending','Pending'),
        ('Confirmed','Confirmed')
        ]
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, related_name='supplier', verbose_name= 'Supplier', null=True)
    status    = models.CharField(max_length=100, choices=status, default="Pending")
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, related_name='PoState', verbose_name= 'State', null=True)
    date  = models.CharField(max_length=201, default="", blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Purchase Order'

    def __str__(self):
        return str(self.supplier_name)
    
@receiver(post_save, sender= Purchase)
def post_save_confirmedstatus(sender, instance, **kwargs):
    print('instance val', instance.status)
    if (instance.status == 'Confirmed'):
        supplierquantity = Quantity.objects.filter(purchase__id = instance.id)
        for supplier in supplierquantity:
            hubquantity = HubQuantity.objects.filter(items__id = supplier.items.id, purchase__id = supplier.purchase.id)
            for hubqty in hubquantity:
                Transit.objects.create(ponumber = hubqty.purchase.id, itemname_id = hubqty.items.id, quantity = hubqty.quantity, stockfrom = 'Supplier', suppliername_id = hubqty.supplier.id, stockto = 'Hub', hubname_id = hubqty.hub.id, transitdate = instance.date)
                
post_save.connect(post_save_confirmedstatus, sender=Purchase)


class Quantity(models.Model):
    items   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', blank=True, null=True, verbose_name="Item Name")
    quantity  = models.CharField(max_length=201, blank=True, default="", verbose_name="Qty")
    purchase  = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase', blank=True, null=True, verbose_name="Purchase")
    remainingquantity = models.CharField(max_length=201, blank=True, default="", verbose_name="Remaining Quantity")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Quantity'

    def __str__(self):
        return str(self.items)
    # def save(self, *args, **kwargs):
    #     print('self quantity', self.quantity)
@receiver(pre_save, sender= Quantity)
def callback_function_presave(sender, instance,*args,**kwargs):
    try:
        if instance.pk is not None:
            instance.old_value = sender.objects.get(pk=instance.pk).quantity
            print('old value', instance.old_value)
        else:
            instance.old_value = 0
            print('old value', instance.old_value)


    except sender.DoesNotExist:
        return
pre_save.connect(callback_function_presave, sender=Quantity)
@receiver(post_save, sender= Quantity)
def post_save_function(sender, instance, **kwargs):
        try:
            print('instance post',instance.id)
            if instance.id:
                if instance.remainingquantity == "":
                        print('found')
                        qty = Quantity.objects.get(id = instance.id)
                        qty.remainingquantity = qty.quantity
                        qty.save()
                else:
                    if (instance.old_value != instance.quantity):
                        print('new value',instance.purchase.id)
                        qty = Quantity.objects.get(id = instance.id,purchase__id = instance.purchase.id)
                        qty.remainingquantity = qty.quantity
                        qty.save()
                        purchase = Purchase.objects.get(id = qty.purchase.id)
                        hubqty = HubQuantity.objects.filter(purchase__id = purchase.id, items__id = qty.items.id)
                        hubqty.delete()
            
        except Exception as error:
            print('Exception occur ', error)
post_save.connect(post_save_function, sender=Quantity)


class HubQuantity(models.Model):
    items   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='itemname', blank=True, null=True, verbose_name="Item Name")
    quantity  = models.CharField(max_length=201, blank=True, default="", verbose_name="Qty")
    supplier  = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_name', blank=True, null=True, verbose_name="Supplier Name")
    # supplierqty  = models.ForeignKey(Quantity, on_delete=models.CASCADE, related_name='supplierqty', blank=True, null=True, verbose_name="Item Name")
    hub  = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub', blank=True, null=True, verbose_name="Hub Name")
    purchase  = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchasename', blank=True, null=True, verbose_name="Purchase")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Hub Quantity'

    def __str__(self):
        return str(self.items)
    

class Transit(models.Model):
    ponumber = models.CharField(max_length=201, blank=True, default="", verbose_name="Po Number")
    itemname   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item', blank=True, null=True, verbose_name="Item Name")
    quantity  = models.CharField(max_length=201, blank=True, default="", verbose_name="Quantity")
    stockfrom = models.CharField(max_length=201, blank=True, default="", verbose_name="From")
    suppliername  = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='suppliers', blank=True, null=True, verbose_name="Name")
    stockto = models.CharField(max_length=201, blank=True, default="", verbose_name="To")
    hubname  = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hubname', blank=True, null=True, verbose_name="Name")
    stockStatusOptions = [
    ('InTransit','In Transit'),
    ('Delivered','Delivered')
    ]
    stockStatus = models.CharField(max_length=100, default="InTransit", blank=True,choices=stockStatusOptions)
    transitdate = models.DateField(auto_now= False, db_column="Po_date", verbose_name = 'Po Date')
    receiveddate = models.DateField(auto_now= False, blank=True,null=True)
    file = models.FileField(blank=True, default="", verbose_name='File')
    remarks = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Transit'

    def __str__(self):
        return str(self.stockStatus)

@receiver(pre_delete, sender=Transit)
def delete_related_journal(sender, instance, **kwargs):
    deleteval = Stock.objects.filter(allids = instance.id, stocktype = 'Transit')
    deleteval.delete()

class Transfer(models.Model):
    FromChoice = [
        ('Hub', 'Hub')
    ]
    selectfrom = models.CharField(max_length=100, default=False, blank=True, choices=FromChoice, verbose_name='From')
    source = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='source', blank=True, null=True)
    ToChoice = [
        ('Hub', 'Hub'),
        ('Branch', 'Branch')
    ]
    SelectTo = models.CharField(max_length=100, default=False, blank=True, choices=ToChoice, verbose_name='To')
    branchdestination =  models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branchnamedestination', blank=True, null=True, verbose_name= 'Destination')
    hubdestination =  models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hubdestination', blank=True, null=True, verbose_name= 'Destination')
    TransferStatusOptions = [
    ('InTransit','In Transit'),
    ('Delivered','Delivered')
    ]
    transferStatus = models.CharField(max_length=100, default="InTransit", blank=True,choices=TransferStatusOptions, db_column='stockStatus')
    requisitionno = models.ForeignKey('Requisition', on_delete=models.CASCADE, related_name='Requisition', blank=True, null=True, verbose_name= 'Requisition')
    transferdate = models.DateField(auto_now= False, blank=True,null=True, editable= True, verbose_name='Tranfer Date')
    receiveddate = models.DateField(auto_now= False, blank=True,null=True)
    file = models.FileField(blank=True, default="", verbose_name='File')
    remarks = models.CharField(max_length=256, blank=True)
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Transfer'

    def __str__(self):
        return str(self.id)
   
@receiver(pre_delete, sender=Transfer)
def delete_related_journal(sender, instance, **kwargs):
    deleteval = Stock.objects.filter(allids = instance.id, stocktype = 'Transfer')
    deleteval.delete()
    if instance.requisitionno != None:
        requisitionstatus = Requisition.objects.get(id = instance.requisitionno.id)
        requisitionstatus.status = 'Pending'
        requisitionstatus.save()

@receiver(post_save, sender= Transfer)
def post_save_transferChalan(sender, instance, created, **kwargs):
        try:
            if created:
                transferid = Requisition.objects.get(id=instance.requisitionno.id)
                transferid.chalanNumber = instance.id
                transferid.status = 'Completed'
                transferid.save()
                
        except Exception as error:
            print('Exception occur ', error)
post_save.connect(post_save_transferChalan, sender=Transfer)  


class TransferQuantity(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Productname', blank=True, null=True)
    transferablestock = models.CharField(max_length=100, default="", blank=True, verbose_name='Transferable Stock')
    stocktransfered = models.CharField(max_length=100, default="", blank=True, verbose_name='Stock to be Transfered')
    comment = models.CharField(max_length=100, default="", blank=True)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='transferid', blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Transfer Quantity'

    def __str__(self):
        return str(self.id)
 
class Adjustment(models.Model):
    adjustmentNo = models.CharField(unique=True, editable=False, max_length=200)
    ToChoice = [
        ('Hub', 'Hub'),
        ('Branch', 'Branch')
    ]
    adjustmentfor = models.CharField(max_length=100, default=False, blank=True, choices=ToChoice, verbose_name='Adjustment For')
    adjustableHub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='adjustableHub', blank=True, null=True, verbose_name="Select Adjustable")
    adjustableBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='adjustableBranch', blank=True, null=True, verbose_name="Select Adjustable")
    Type = [
        ('OpeningStock', 'Opening Stock'),
        ('Increase', 'Increase'),
        ('Decrease', 'Decrease')
    ]
    adjustmentType = models.CharField(max_length=100, default=False, blank=True, choices=Type, verbose_name='Adjustment Type')
    comment = models.CharField(max_length=100, default="", blank=True)
    adjustmentDate = models.CharField(max_length=100, blank=True,null=True, verbose_name="Adjustment Date")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Adjustment'

    def save(self, **kwargs):
        if not self.id:
            max = Adjustment.objects.aggregate(
                id_max=models.Max('adjustmentNo'))['id_max']
            if max is not None:
                pattern = r'\d+'
                max = re.findall(pattern, max)
                max = max[0]
                max = int(max) + 1
            else:
                max = 100001
            self.adjustmentNo = "{}{}".format('ADJN', 
                max)  # id from 100 to start
        if not self.adjustmentDate:
            self.adjustmentDate = datetime.now().date()
        super().save(*kwargs)

    def __str__(self):
        return str(self.id)


class AdjustmentStock(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='adjustmentitem', blank=True, null=True)
    stock = models.CharField(max_length=100, default="", blank=True, verbose_name="Stock To Be Adjusted")
    adjust = models.ForeignKey(Adjustment, on_delete=models.CASCADE, related_name='adjustmentId', blank=True, null=True)


    class Meta:
        ordering = ('-id',)
        verbose_name = 'Adjustment Stock'

    

    def __str__(self):
        return str(self.id)
    
@receiver(post_save, sender= AdjustmentStock)
def post_save_adjustmentStock(sender, instance, created, **kwargs):
        try:
            adjustmentstock = AdjustmentStock.objects.filter(id = instance.id)
            if created:
                
                for stock in adjustmentstock:
                    print('qty', stock)
                    stocklist =  Stock.objects.create(stocktype = stock.adjust.adjustmentType, stockfrom = 'Admin',  stockto = instance.adjust.adjustmentfor, stocktoBranchname_id = instance.adjust.adjustableBranch.id if instance.adjust.adjustableBranch else "", stocktoHubname_id = instance.adjust.adjustableHub.id if instance.adjust.adjustableHub else "", productID_id = stock.item.id, receiveddate = instance.adjust.adjustmentDate, quantity = stock.stock, stockStatus = 'Delivered', allids = instance.id)
                    print('stck', stocklist)
            else:
                for stock in adjustmentstock:
                    stocklist = Stock.objects.get(stocktype = stock.adjust.adjustmentType, allids = instance.id)
                    stocklist.quantity = stock.stock
                    stocklist.save()
        except Exception as error:
            print('Exception occur ', error)
post_save.connect(post_save_adjustmentStock, sender=AdjustmentStock)  



class HubBalance(models.Model):
    # stocktype = models.CharField(max_length=100, default="", blank=True, verbose_name= "Type")
    hubid = models.ForeignKey('Hub', on_delete=models.CASCADE, related_name='HubBalanceId', blank=True, null=True, verbose_name="Name")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='hubItemId', null = True, verbose_name='Item')
    openingstock = models.CharField(max_length=100, default="", blank=True, verbose_name="Opening Stock")
    closingstock = models.CharField(max_length=100, default="", blank=True, verbose_name="Closing Stock")
    created_at = models.DateField(auto_now=False,blank=True,null = True)


    class Meta:
        ordering = ('-id',)
        verbose_name = 'Hub Balance'

    def __str__(self):
        return str(self.id)
    

class BranchBalance(models.Model):
    # stocktype = models.CharField(max_length=100, default="", blank=True, verbose_name= "Type")
    branchid = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branchBalanceId', blank=True, null=True, verbose_name="Name")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='branchItemId', null = True, verbose_name='Item')
    openingstock = models.CharField(max_length=100, default="", blank=True, verbose_name="Opening Stock")
    closingstock = models.CharField(max_length=100, default="", blank=True, verbose_name="Closing Stock")
    created_at = models.DateField(auto_now=False,blank=True,null = True)


    class Meta:
        ordering = ('-id',)
        verbose_name = 'Branch Balance'

    def __str__(self):
        return str(self.id)
    

class Requisition(models.Model):
    requisitionNumber = models.CharField(max_length=100, default="", blank=True, verbose_name="Requisition Number")
    StatusOptions = [
    ('Pending','Pending'),
    ('Completed','Completed')
    ]
    status = models.CharField(max_length=100, default="Pending", blank=True,choices=StatusOptions, db_column='Status')
    productname = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productname', blank=True, null=True, verbose_name="Items")
    branchName = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch', blank=True, null=True, verbose_name="Branch")
    chalanNumber = models.CharField(max_length=201, blank=True, db_column='Chalan Number')
    quantity = models.CharField(max_length=201, blank=True)
    requisitionDate = models.DateField(auto_now=False,blank=True,null = True, verbose_name= "Requisition Date")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Requisition'

    def __str__(self):
        return str(self.id)

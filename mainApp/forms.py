from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import widgets

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customerName'].required = True
        self.fields['loan_date'].required = True
        self.fields['loanStatus'].required = True
        self.fields['invoiceNo'].required = True
        self.fields['orderDate'].required = True
        self.fields['loanNo'].required = True
        self.fields['Phone'].required = True
        self.fields['address'].required = True
        self.fields['addressState'].required = True
        self.fields['addressZipCode'].required = True
        self.fields['landmark'].required = True
        # self.fields['salehub'].required = True
    class Meta:
        model = Order
        fields = '__all__'
        labels = {
            "loan_date": "Loan Date *",
            "loanStatus": "Loan Status *",
            "branchID": "Branch *",
            "customerName": "Customer Name *",
            "product_id": "Product *",
            "invoiceNo": "Invoice No *",
            "orderDate": "Order Date *",
            "loanNo": "Loan No *",
            "Phone": "Phone *",
            "address": "Address *",
            "addressState": "Address State *",
            "addressZipCode": "Zip Code *",
            "landmark": "Landmark *",
            "loanType": "Loan Type",
            "customerID": "Customer No",
            "invoice_date": "Invoice Date",
            # "salehub": "Sale Hub *"
        }
        widgets = {
            'orderDate': widgets.AdminDateWidget,
            'loan_date': widgets.AdminDateWidget,
            'invoice_date': widgets.AdminDateWidget,
            'date_of_delivery': widgets.AdminDateWidget,
            'loanNo': forms.TextInput(attrs={'type':'number'})
        }
        
    # def clean(self):
    #     # stockid = self.cleaned_data['stockID'].id
    #     previousquantity = self.instance.quantity
    #     quantity = self.cleaned_data['quantity']
    #     # stocklist = Stock.objects.get(pk=stockid)
    #     product = self.cleaned_data['product_id'].id
    #     branch = self.cleaned_data['branchID'].id
    #     print('branch value', branch, 'product value', product, 'id', self.instance.pk)
    #     stock = "SELECT *, SUM(quantity) as totalQuantity from `mainApp_stock` where stockStatus='Delivered' and stockto = 'Branch' and productID_id = %s and stocktoBranchname_id = %s GROUP BY stocktoBranchname_id, productID_id" % (product,branch)
    #     stock = Stock.objects.raw(stock)
    #     for stocklist in stock:
    #         print('stocklist', stocklist.totalQuantity)
    #         orderedquantity = Order.objects.filter(branchID__id=branch, product_id__id = product)
    #         qty=0
    #         for order in orderedquantity:
    #             qty += int(order.quantity)
    #         available_stock =int(stocklist.totalQuantity) -  (qty)
            
    #         print('prev', previousquantity)
    #         if(self.instance.pk == None):
                
    #             if(available_stock <= 0 ):
    #                 raise forms.ValidationError('Selected Product has no stock')

    #             if(int(quantity) == 0):
    #                 raise forms.ValidationError('Quantity Should be greater than 0')
    #             # If user makes any changes to the previous quantity 
    #             # if (int(quantity) - int(previousquantity)) != 0:
    #             if (int(previousquantity) == 1) :
    #                 if ((int(quantity) - (int(previousquantity)-1)) > available_stock):
    #                     raise forms.ValidationError('Quantity shoulbe less than Available Stock')   
            


class BranchForm(forms.ModelForm):
    password_2 = forms.CharField(label='Confirm Password',required=False, initial="")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hubBranch'].required = True
    class Meta:
        model = Branch
        fields = ['branchName','branchCode','branchManager','branchMangerPhoneNo','company', 'address', 'city', 'region', 'pincode', 'hubBranch', 'branch_username','branch_password']
        widgets = {
        'branch_password': forms.PasswordInput(render_value = True),
        'branchMangerPhoneNo': forms.TextInput(attrs={'type':'number'}),
        }
        labels = {
            "hubBranch": "Hub *"
        }
    # def clean_branchMangerPhoneNo(self):
    #     branchMangerPhoneNo = self.cleaned_data.get('branchMangerPhoneNo', None)
    #     try:
    #         if int(branchMangerPhoneNo) and not branchMangerPhoneNo.isalpha():
    #             length = 10
                
    #             ph_length = str(branchMangerPhoneNo)
    #             if len(ph_length) >= length:
    #                 raise forms.ValidationError('Phone number length not valid')

    #     except (ValueError, TypeError):
    #         raise forms.ValidationError('Please enter a valid phone number')
    #     return branchMangerPhoneNo
    def clean_email(self):
        '''
        Verify email is available.
        '''
        print("CLEANING EMAIl")
        branch_username = self.cleaned_data.get('branch_username')
        if Branch.objects.filter(branch_username=branch_username).exists():
            raise forms.ValidationError('This username is already taken')
        return branch_username

    def clean(self):
        '''
        Verify both passwords match.
        '''
        previousemail = self.instance.branch_username
        print('prev', previousemail)
        branch_username = self.cleaned_data.get('branch_username')
        if previousemail != branch_username:

            if User.objects.filter(email=branch_username).exists():
                raise forms.ValidationError('This username is already taken')
            cleaned_data = super().clean()
            branch_password = cleaned_data.get("branch_password")
            prevPassword = self.instance.branch_password
            password_2 = cleaned_data.get("password_2")
            if branch_password != prevPassword and password_2 != branch_password :
                self.add_error("password_2", "Your passwords must match")
            if branch_password == prevPassword and (password_2 != branch_password and password_2 != "") :
                self.add_error("password_2", "Your passwords must match")

        
            return cleaned_data

    @receiver(post_save, sender=Branch)
    def create_user(sender, instance, created, **kwargs):
        print("instance :", instance.branch_password,instance.branch_username)
        branch_username = instance.branch_username
        if not User.objects.filter(email=branch_username).exists():
            if created:
                new_branch_manager = User.objects.create_user(email=instance.branch_username, password=instance.branch_password)
                print("NEW BRANCH MANAGER ; ", new_branch_manager.email)
                user = User.objects.get(email=new_branch_manager.email)
                print("user ; ", user)
                created = Group.objects.get(name='BranchManagersGroup')
                created.user_set.add(user)


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cgst'].required = True
        self.fields['sgst'].required = True
        self.fields['igst'].required = True
        self.fields['price'].required = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'cgst': forms.TextInput(attrs={'type':'number'}),
            'sgst': forms.TextInput(attrs={'type':'number'}),
            'igst': forms.TextInput(attrs={'type':'number'}),
        }
        labels = {
            "cgst": "CGST *",
            "sgst": "SGST *",
            "igst": "IGST *",
            "price": "Price *"
        }

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].required = True

    class Meta:
        model = Stock
        fields = '__all__'

        labels = {
            "quantity": "Quantity *",
        }
        widgets = {
            'disbursementDate': widgets.AdminDateWidget,
            'orderDate': widgets.AdminDateWidget,
        }


class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier_name'].required = True
        self.fields['state'].required = True
    class Meta:
        model = Purchase
        fields = '__all__'
        labels = {
            "supplier_name": "Supplier Name *",
            "state": "State *",
        }

        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
        }

class QuantityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuantityForm, self).__init__(*args, **kwargs)
        self.fields['items'].required = True
        self.fields['quantity'].required = True
    class Meta:
        model = Quantity
        fields = ['items', 'quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'type':'number'}),
        }

class HubQuantityForm(forms.ModelForm):
    class Meta:
        model = HubQuantity
        fields = '__all__'

        widgets = {
            'quantity': forms.TextInput(attrs={'type':'number'}),
        }

class TransferQuantityForm(forms.ModelForm):

    class Meta:
        model = TransferQuantity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request',  None )
        super(TransferQuantityForm, self).__init__(*args, **kwargs)


    # def clean(self):
    #     cleaned_data = super(TransferQuantityForm, self).clean()
    #     item = self.cleaned_data.get('item').id
    #     stocktransfered = self.cleaned_data.get('stocktransfered')
    #     transferablestock = self.cleaned_data.get('transferablestock')
    #     previousstock = self.instance.stocktransfered or None
    #     # comment = self.cleaned_data['comment']
    #     print('item:', item, 'transferablestock:', transferablestock, 'stocktransfered:', stocktransfered, 'previous:', previousstock)
    #     if previousstock == None:
    #         if(int(transferablestock) <= 0 ):
    #             raise forms.ValidationError('Selected Item has no stock')

    #         if(int(stocktransfered) == 0):
    #             raise forms.ValidationError('Stock Should be greater than 0')
    #         if(previousstock == ""):
    #             self.cleaned_data['transferablestock'] = int(transferablestock) - int(stocktransfered)
    #             print('transferable stock',  self.cleaned_data['transferablestock'])
    #         if (int(transferablestock)- int(stocktransfered) < 0):
    #             raise forms.ValidationError('Selected Item has no stock')
    #     else:
    #         if(int(stocktransfered)- int(previousstock) == 0):
    #             self.cleaned_data['transferablestock'] = int(transferablestock)
    #             print('previous value equal',  self.cleaned_data['transferablestock'])
    #         if(int(stocktransfered)- int(previousstock) != 0):
    #             if (int(stocktransfered) > int(previousstock)):
    #                 newstock = int(stocktransfered) - int(previousstock)
    #                 self.cleaned_data['transferablestock'] = int(transferablestock) - int(newstock)
    #                 print('stockvalue greater',  self.cleaned_data['transferablestock'])
    #             if (int(stocktransfered) < int(previousstock)):
    #                 newstock = int(previousstock) - int(stocktransfered)
    #                 self.cleaned_data['transferablestock'] = int(transferablestock) + int(newstock)
    #                 print('previous value greater',  self.cleaned_data['transferablestock'])
    #             if ((int(stocktransfered) - (int(previousstock))) > 0):
    #                 raise forms.ValidationError('Stock shoulbe less than Available Stock')
    #     return cleaned_data

class XYZ_DateInput(forms.DateInput):
    input_type = "date"

    
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = '__all__'

        widgets = {
            'transferdate': XYZ_DateInput(),
        }
class AdjustmentStockForm(forms.ModelForm):

    class Meta:
        model = AdjustmentStock
        fields = '__all__'

        widgets = {
            'stock': forms.TextInput(attrs={'type':'number'}),
        }

class AdjustmentForm(forms.ModelForm):

    class Meta:
        model = Adjustment
        fields = '__all__'

        widgets = {
            'adjustmentDate': XYZ_DateInput(),
        }

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'

        widgets = {
            'requisitionDate': XYZ_DateInput(),
            'quantity': forms.TextInput(attrs={'type':'number'}),
        }
    def __init__(self, *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Since the pk is set this is not a new instance
            self.fields['requisitionDate'].widget = forms.HiddenInput()

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

        # widgets = {
        #     'gst': forms.TextInput(attrs={'type':'number'}),
            
        # }

class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = '__all__'

        widgets = {
            'phone': forms.TextInput(attrs={'type':'number'}),
            
        }
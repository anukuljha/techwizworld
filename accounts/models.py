from django.core.validators import MinValueValidator,MinLengthValidator
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Product (models.Model):
    # constants
    CATEGORIES = (
        (0,0),
        (5, 5),
        (12, 12),
        (18, 18),
        
    )

    name = models.CharField(max_length=100)
    #alias = models.CharField(max_length=100)
    #price = models.FloatField(validators=[MinValueValidator(0)])
    #inventory = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    hsn_code = models.CharField(max_length=8, blank=True)
    tax = models.IntegerField(choices=CATEGORIES, default=5)

    def __str__ (self):
        return self.name + "-GST@-"+ str(self.tax)
        
class Client(models.Model):
    name=models.CharField(max_length=150)
    billing_address_line1=models.CharField(max_length=400)
    billing_address_line2=models.CharField(max_length=400)
    billing_address_line3=models.CharField(max_length=400)
    GSTIN=models.CharField(max_length=15,validators=[MinLengthValidator(15)])

    def __str__(self):
        return self.name + "(" + self.billing_address_line3 +")"

class Site(models.Model):
    client=models.ForeignKey(Client)
    name=models.CharField(max_length=150)
    shipping_address_line1=models.CharField(max_length=400)
    shipping_address_line2=models.CharField(max_length=400)
    shipping_address_line3=models.CharField(max_length=400)
    location= models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name+ " (" + self.location + ")" 

class AnnualPriceList(models.Model):
    site=models.ForeignKey(Site)
    valid_from=models.DateField(default=timezone.now)
    valid_to=models.DateField(default=timezone.now)

    def __str__(self):
        return self.site.__str__()

class ProductRate(models.Model):
    UNITS=(
        ("KG","KG"),
        ("Pcs","Pcs"),
        ("Pkt","Pkt"),
        ("Ltr","Ltr"),
        ("Tin","Tin"),
        ("Bottle","Bottle"),
        ("Metre","Metre"),
        ("Box","Box"),
        )
    product=models.ForeignKey(Product)
    rate=models.FloatField(default=0,
                                    validators=[MinValueValidator(0)])
    unit= models.CharField(choices=UNITS,default="KG",max_length=10)
    apl=models.ForeignKey(AnnualPriceList)

    def __str__(self):
        return self.product.name+ " " + self.apl.__str__()


class Inventory (models.Model):
    product = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    source = models.CharField(max_length=100)
    cprice = models.FloatField(validators=[MinValueValidator(0)])
    quantity = models.FloatField(default=1, validators=[MinValueValidator(0)])
    on = models.DateTimeField(default=datetime.now,blank=False)
    def __str__ (self):
        return self.source



class PurchaseBill(models.Model):
    # constant
    COLLECTION = (
        ("1", '(CGST/SGST)'),
        ("2", '(IGST)'),
    )

    purchase_date = models.DateField(default=timezone.now())
    seller = models.CharField(max_length=100)
    seller_address=models.CharField(max_length=100)
    collection = models.CharField(max_length=100, choices=COLLECTION, blank=False, default=1)
    seller_GSTIN=models.CharField(max_length=30)

    def __str__(self):
        return self.seller + " on " +str(self.purchase_date)
    def tax(self):
        return sum([((x.price*x.quantity)*int(x.product.tax)/100) for x in self.purchasedproducts_set.all()])

    def total(self):
        return sum([x.price*x.quantity for x in self.purchasedproducts_set.all()])
    def tax_dict(self):
        res = {
            "0" : 0,
            "5" : 0,
            "12" : 0,
            "18" : 0
            
        }
        for x in self.purchasedproducts_set.all():
            res[str(x.product.tax)] += (x.price*x.product.tax*x.quantity)/100
        return res
    def price_tax_dict(self):
        res = {
            "0" : 0,
            "5" : 0,
            "12" : 0,
            "18" : 0
            
        }
        for x in self.purchasedproducts_set.all():
            res[str(x.product.tax)] += (x.price*x.quantity)
        return res
    def totalQuantity(self):
        return sum([int(x.quantity) for x in self.purchasedproducts_set.all()])
    def grandTotal(self):
        return sum([(x.price*x.quantity) + ((x.price*x.quantity)*int(x.product.tax)/100) for x in self.purchasedproducts_set.all()])


class PurchasedProduct(models.Model):
    UNITS=(
        ("KG","KG"),
        ("Pcs","Pcs"),
        ("Pkt","Pkt"),
        ("Ltr","Ltr"),
        ("Tin","Tin"),
        ("Bottle","Bottle"),
        ("Metre","Metre"),
        ("Box","Box"),
        )
    product=models.ForeignKey(Product)
    rate=models.FloatField(validators=[MinValueValidator(0)])
    unit= models.CharField(choices=UNITS,default="KG",max_length=10)
    quantity=models.FloatField(validators=[MinValueValidator(0)])
    purchase_bill=models.ForeignKey(PurchaseBill)

    def __str__(self):
        return self.product.name



class Bills (models.Model):

    # constant
    COLLECTION = (
        ("1", '(CGST/SGST)'),
        ("2", '(IGST)'),
    )

    invoice_date = models.DateField(default=timezone.now())
    po_date = models.DateField(default=timezone.now())
    invoice_number = models.IntegerField(default=0,unique_for_year="po_date")
    po_number = models.IntegerField(default=0)
    site=models.ForeignKey(Site)
    collection = models.CharField(max_length=100, choices=COLLECTION, blank=False, default=1)


    def __str__(self):
        return self.site.name + " on " + str(self.invoice_date)
    def tax(self):
        return sum([((x.price*x.quantity)*int(x.category)/100) for x in self.billedproducts_set.all()])

    def total(self):
        return sum([x.price*x.quantity for x in self.billedproducts_set.all()])
    def tax_dict(self):
        res = {
            "0" : 0,
            "5" : 0,
            "12" : 0,
            "18" : 0
            
        }
        for x in self.billedproducts_set.all():
            res[str(x.category)] += (x.price*x.category*x.quantity)/100
        l=list()
        keys=["0","5","12","18"]
        for k in keys:
        	l.append(res[k])
        return l
    def price_tax_dict(self):
        res = {
            "0" : 0,
            "5" : 0,
            "12" : 0,
            "18" : 0
            
        }
        for x in self.billedproducts_set.all():
            res[str(x.category)] += (x.price*x.quantity)
        l=list()
        keys=["0","5","12","18"]
        for k in keys:
        	l.append(res[k])
        return l
    def totalQuantity(self):
        return sum([int(x.quantity) for x in self.billedproducts_set.all()])
    def grandTotal(self):
        return sum([(x.price*x.quantity) + ((x.price*x.quantity)*int(x.category)/100) for x in self.billedproducts_set.all()])

class BilledProducts (models.Model):

    # constants
    CATEGORIES = (
        (0, 0),
        (5, 5),
        (12, 12),
        (18, 18)
        
    )

    name = models.CharField(max_length=100)
    quantity = models.FloatField(default=0)
    price = models.FloatField()
    bill = models.ForeignKey(Bills)
    unit= models.CharField(max_length=10)

    category = models.IntegerField(choices = CATEGORIES)
    hsn = models.CharField(max_length=10)

    def taxTotal(self):
        return ((self.price * self.quantity)*self.category)/100

    def total(self):
        return self.price * self.quantity

    def grandTotal(self):
        return self.price * self.quantity + ((self.price * self.quantity)*self.category)/100

    def __str__ (self):
        return self.name

class Tax(models.Model):
    tax = models.FloatField(default=0)

    def __str__(self):
        return self.tax

class SaleSummary(BilledProducts):
    class Meta:
        proxy = True
        verbose_name = 'Sale Summary'
        verbose_name_plural = 'Sales Summary'


class PurchaseSummary(PurchasedProduct):
    class Meta:
        proxy = True
        verbose_name = 'Purchase Summary'
        verbose_name_plural = 'Purchase Summary'
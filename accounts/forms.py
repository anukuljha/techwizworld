from django import forms
from django.core.validators import MinValueValidator
from .models import Product, Tax, Bills, Inventory, Site
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import models


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    #__metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""

        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_save(value)


# create forms here

class LoginForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'hsn_code', 'tax']
        labels = {
            'name' : 'Name',
            
            'hsn_code' : 'HSN Code',
            'tax' : 'Tax Category'
        }

class BillGenForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ['invoice_number', 'po_number','invoice_date','po_date',  'collection']

    names_gst_and_quantities = JSONField()

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['tax', ]

class InventoryAddForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'source', 'cprice', 'quantity']

class SiteSelectForm(forms.ModelForm):
	class Meta:
		model = Site
		fields='__all__'

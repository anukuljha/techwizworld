from django.contrib import admin
from .models import Product,Client,AnnualPriceList,ProductRate,Site,Bills,BilledProducts,SaleSummary,PurchaseSummary ,PurchasedProduct,PurchaseBill
from django.db.models import Sum,F,Value
# Register your models here.
admin.site.register(Product)
#admin.site.register(Inventory)


class ProductRateInline(admin.TabularInline):
    model = ProductRate

class APLAdmin(admin.ModelAdmin):
    save_as = True
    inlines = [
        ProductRateInline,
    ]

class SiteInline(admin.TabularInline):
	model=Site

class ClientAdmin(admin.ModelAdmin):
	inlines=[SiteInline,]

class BillInline(admin.TabularInline):
	model=BilledProducts

class BillAdmin(admin.ModelAdmin):
	inlines=[BillInline,]

class PurchaseInline(admin.TabularInline):
	model=PurchasedProduct

class PurchaseAdmin(admin.ModelAdmin):
	inlines=[PurchaseInline,]

admin.site.register(AnnualPriceList,APLAdmin)
admin.site.register(Client,ClientAdmin)
#admin.site.register(Site)
admin.site.register(Bills,BillAdmin)
admin.site.register(PurchaseBill,PurchaseAdmin)

@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'bill__invoice_date'

    list_filter = ('category',)
    
    def changelist_view(self, request, extra_context=None):
	    response = super().changelist_view(
	        request,
	        extra_context=extra_context,
	    )

	    try:
	        qs = response.context_data['cl'].queryset
	    except (AttributeError, KeyError):
	        return response
	    
	    metrics = {
	        'total': Sum('quantity'),
	        'total_sales': Sum(F('price')*F('quantity')),
	        'total_tax': Sum(F('price')*F('quantity')*F("category")/Value(100)),
	    }

	    response.context_data['summary'] = list(
	        qs
	        .values('name')
	        .annotate(**metrics)
	        .order_by('-total_sales')
	    )
	    
	    response.context_data['summary_total'] = dict(
            qs
            .aggregate(**metrics)
        )

	    return response


@admin.register(PurchaseSummary)
class PurchaseSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/purchase_summary_change_list.html'
    date_hierarchy = 'purchase_bill__purchase_date'

    list_filter = ('product__tax',)
    
    def changelist_view(self, request, extra_context=None):
	    response = super().changelist_view(
	        request,
	        extra_context=extra_context,
	    )

	    try:
	        qs = response.context_data['cl'].queryset
	    except (AttributeError, KeyError):
	        return response
	    
	    metrics = {
	        'total': Sum('quantity'),
	        'total_sales': Sum(F('rate')*F('quantity')),
	        'total_tax': Sum(F('rate')*F('quantity')*F("product__tax")/Value(100)),
	    }

	    response.context_data['summary'] = list(
	        qs
	        .values('product__name')
	        .annotate(**metrics)
	        .order_by('-total_sales')
	    )
	    
	    response.context_data['summary_total'] = dict(
            qs
            .aggregate(**metrics)
        )

	    return response


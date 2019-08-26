from django.conf.urls import url
from . import views

urlpatterns = [
	#view
	url(r'^$', views.index, name='index'),
	url(r'^login/?$', views.login_view, name='login'),
	url(r'^logout/?$', views.logout_view, name='logout'),
	url(r'^products/?$', views.products_view, name='products'),
	url(r'^gen_bill/?$', views.gen_bill_view, name='gen_bills'),
	url(r'^inventory/?$', views.add_inventory, name='inventory'),
	url(r'^view_bill/(?P<id>[0-9]+)/?$', views.view_bill_view, name='view_bills'),
	url(r'^all_bill/?$', views.all_bill_view, name='all_bills'),
	url(r'^select_site/?$', views.select_site, name='select_site'),


	#popup_views
	url(r'^edit_product/(?P<id>[0-9]+)/?$', views.edit_product_view, name='edit_product'),

	#helpers
	url(r'^add_product/?$', views.add_product_helper, name='add_products'),
	url(r'^del_product/(?P<id>[0-9]+)/?$', views.del_product_helper, name='del_products'),

	#apis
	url(r'^search_product/(?P<query>[a-zA-Z0-9\-]+)/?$', views.search_product, name='search_product'),
	url(r'^gen_bill_post/?$', views.gen_bill, name='gen_bill'),
	url(r'^gen_invent/?$', views.gen_invent, name='gen_invent'),
]

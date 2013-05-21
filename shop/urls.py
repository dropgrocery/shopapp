import os.path
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from shop.shop.views import *

from django.contrib import admin
from shop.shop.models import ShoppingList
from django.views.generic import TemplateView
import django.contrib.auth.views


site_media = os.path.join(os.path.dirname(__file__), 'shop/site_media')

urlpatterns = patterns('',
                        ('^admin/', include(admin.site.urls)),
# browsing
  (r'^$', main_page),
  (r'^user/(\w+)/$', user_page),
  (r'^register/$', register_page),
  (r'^products/$', products_page),
  (r'^user/(\w+)/shoppinglist/(\d+)/$', shop_products_page),
  
  #session management
  (r'^login/$', 'django.contrib.auth.views.login'),
  (r'^logout/$', logout_page),
  
  (r'^register/success/$', direct_to_template, 
    { 'template': 'registration/register_success.html' }),
#static content
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
    { 'document_root': site_media }),
                       
                       
 
  # Account management(
  #CREATE
(r'^save/$', shoppinglist_save_page),

(r'^remove/$', shoppinglist_remove_page),
(r'latest/$', shoppinglist_latest),
(r'^user/(\w+)/shoppinglist/(\d+)/remove/$', product_remove_page),
#(r'^shops/$', shops_edit_page),
#(r'^remove/(\d+)/$',shoppinglist_removal_page),

  #INSERT
(r'^user/(\w+)/customproducts/$', custom_product_list),
url(r'^user/(\w+)/customproducts/add/$', create_custom_product),
(r'^user/(\w+)/customproducts/remove/$', custom_products_remove_page),

(r'^user/(\w+)/shoppinglist/(\d+)/insert/$', select_categories_page),
(r'^user/(\w+)/shoppinglist/(\d+)/insert/([\w\|\s]+)/$', select_categories1_page),
(r'^user/(\w+)/shoppinglist/(\d+)/insert/(\w+)/(\w+)/$', select_categories1_page),

#My Products
(r'^user/(\w+)/shoppinglist/(\d+)/insert_myproduct/$', insert_myproduct),

(r'^shops/remove/$', shops_remove_page, {'action': 'remove'}),
(r'^shops/$', ShopList.as_view()),
url(r'^shops/add/$', ShopCreate.as_view(), name='shop_add'),

(r'^products/add/$', product_save_page),

(r'account/$', account_page),
(r'^password_change/$', 'django.contrib.auth.views.password_change',{'template_name':'userpanel/password_change.html'}),
(r'^password_change/done/$',
'django.contrib.auth.views.password_change_done', 
    {'template_name':'userpanel/password_change_done.html'}),
#(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),

(r'^config/$', settings_page),
(r'^config/shoppinglists', config_shoppinglists),

)



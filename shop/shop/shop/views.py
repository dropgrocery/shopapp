from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from shop.shop.forms import *
from shop.shop.models import *
from django.views.generic import ListView
import django.contrib.auth.views

def main_page(request):
  return render_to_response('main_page.html', RequestContext(request))

from django.shortcuts import get_object_or_404
def user_page(request, username):
  
    user = get_object_or_404(User, username=username)
    
    shoppinglists = user.shoppinglist_set.order_by("-id")
    variables = RequestContext(request, {
      'username': username,
      'shoppinglists': shoppinglists,
      'show_products': True
    })
    return render_to_response('user_page.html', variables)


def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')


def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()

  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('registration/register.html', variables)

from django.contrib.auth.decorators import login_required
@login_required
def shoppinglist_save_page(request):
    shops = Shop.objects.all()
    if request.method == 'POST':
        form = ShoppingListSaveForm(request.POST)
        
        if form.is_valid():
            # Create or get shoppinglist
            shoplist, created = ShoppingList.objects.get_or_create(user=request.user,
                        shoppingdate=form.cleaned_data['shoppingdate'],
                        shop=Shop.objects.get(id=form.cleaned_data['shop']))

            # Save shoplist to database.
            shoplist.save()
            return HttpResponseRedirect(
            '/user/%s/' % request.user.username
            )
    else:
        form = ShoppingListSaveForm()
    variables = RequestContext(request, {
            'form': form,
            'shops': shops
        })
    return render_to_response('shoppinglist_save.html', variables)

def shoppinglist_remove_page(request):
    user = request.user
    shoppinglists = user.shoppinglist_set.order_by("-id")
    remove = True
    if request.method == 'POST':
        formfields = request.POST
        for field in formfields:
            s = shoppinglists.get(id=field.split('shoppinglist')[1])
            s.delete()
    variables = RequestContext(request, {
                    'remove': remove,
                    'shoppinglists':shoppinglists})
    return render_to_response('user_page.html', variables)


    

from collections import defaultdict
def product_save_page(request):
    cat0 = Taxonomy.objects.all().values_list('cat0_name', flat=True).distinct()
    cat1 = Taxonomy.objects.all().values_list('cat1_name', 'cat2_name').distinct()
    cat2 = Taxonomy.objects.all().values_list('cat2_name', flat=True).distinct()
    cat1cat2 = defaultdict(list)
    for k, v in sorted(cat1):
        cat1cat2[k].append(v)
    cat1cat2 = dict(cat1cat2)
    keylist = cat1cat2.keys()
    keylist.sort()
    if request.method == 'POST':
        form = ProductSaveForm(request.POST)
        
        if form.is_valid():
            # Create or get shoppinglist
            product, created = Product.objects.get_or_create(name=form.cleaned_data['product_name'],
                        category0=form.cleaned_data['cat0'],
                        category1='test',
                        category2='test')

            # Save shoplist to database.
            product.save()
            return HttpResponseRedirect(
            '/user/%s/' % request.user.username
            )
    else:
        form = ProductSaveForm()
    variables = RequestContext(request, {
            'form': form,
            'cat0': cat0,
            'cat1': cat1,
            'cat2': cat2,
            'cat1cat2': cat1cat2,
            'keylist': keylist,
            
        })
    return render_to_response('product_add.html', variables)

from django.shortcuts import get_list_or_404
@login_required
def shop_products_page(request, username, shoppinglistid):
    shoppinglist = ShoppingList.objects.get(id=shoppinglistid)
    products = shoppinglist.products.all()
    products_list = Shoplist_Product.objects.filter(shoplist=shoppinglistid)
    currentshoplist = {p.product.name:p.amount for p in products_list}    
    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            #import pdb; pdb.set_trace()
            product_name = form.cleaned_data['product_name']
            if str(form.cleaned_data['amount']) == '0':
                pass
            else:
                pass
                
    else:
        form = RemoveProductForm()
    variables = RequestContext(request, {
                'products': products,
                'shoppinglist': shoppinglist,
                'currentshoplist': currentshoplist,
                })
    return render_to_response('shoplist_products.html', variables)

@login_required
def shoppinglist_latest(request):
    shoppinglist= ShoppingList.objects.last()
    products = shoppinglist.products.all()
    products_list = Shoplist_Product.objects.filter(shoplist=shoppinglist.id)
    currentshoplist = {p.product.name:p.amount for p in products_list} 
    variables = RequestContext(request, {
                'products': products,
                'shoppinglist': shoppinglist,
                'currentshoplist': currentshoplist,
                })
    return render_to_response('shoplist_products.html', variables)

@login_required
def product_remove_page(request, username, shoppinglistid):
    user = request.user
    shoppinglist = ShoppingList.objects.get(id=shoppinglistid)
    products = shoppinglist.products.all()
    products_list = Shoplist_Product.objects.filter(shoplist=shoppinglistid)
    remove = True
    if request.method == 'POST':
        #import pdb; pdb.set_trace() 
        formfields = request.POST
        
        for field in formfields:
            s = products.get(id=field)
            s.delete()
    variables = RequestContext(request, {
                'remove': remove,
                'products': products,
                'shoppinglist': shoppinglist,
                })
    return render_to_response('shoplist_products.html', variables)
@login_required
def products_page(request):
    products = Product.objects.all()
    variables = RequestContext(request, {
    'products': products,
    })
    return render_to_response('products_page.html', variables)

@login_required
def shop_products_insert_page(request, username, shoppinglistid):
    shoppinglist = ShoppingList.objects.get(id=shoppinglistid)
    products = shoppinglist.products.all()
    if request.method == 'POST':
        form = ProductSelectForm(request.POST)
    else:
        form = ProductSelectForm()
    variables = RequestContext(request, {
            'form': form,
            'products': products,
            
        })
        
    return render_to_response('product_insert.html', variables)

@login_required
def select_categories_page(request, username, shoppinglistid):
    cat0_names = Taxonomy.objects.values_list('cat0_name', flat=True).order_by('cat0_name').distinct()
    variables = RequestContext(request, {
                    'cat0_names': cat0_names,
                    })
    return render_to_response('cat0_names_page.html', variables)

@login_required
def select_categories1_page(request, username, shoppinglistid, cat0):
    if request.method == 'POST':
        
        form = AmountForm(request.POST)
        
        if form.is_valid():
            
            taxo = Taxonomy.objects.get(id=form.cleaned_data['taxonomy'])
            product, created = Product.objects.get_or_create(name=form.cleaned_data['product_name'],
                        taxonomy=taxo)
            product.save()
            shoplist = ShoppingList.objects.get(id=shoppinglistid)
            product, created = Shoplist_Product.objects.get_or_create(shoplist=shoplist, product=product)
            # import pdb; pdb.set_trace()
            if str(form.cleaned_data['amount']) == '0':
                if created:
                    # product is created, but 0 is selected which is not an option
                    pass
                else:
                    # remove relationship as amount is set to 0
                    product.delete()
            else:
                # add relationship and amount
                product.amount = form.cleaned_data['amount']
                product.save()
            return HttpResponseRedirect(
            '/user/%s/shoppinglist/%s/' % (request.user.username, shoppinglistid)
            )
                
           
    else:
        form = AmountForm()
    taxonomies = Taxonomy.objects.all().filter(cat0_name=cat0).order_by('cat2_name')
    products_list = Shoplist_Product.objects.filter(shoplist=shoppinglistid)
    currentshoplist = {p.product.name:p.amount for p in products_list}
    variables = RequestContext(request, {
                    'form': form,
                    'taxonomies': taxonomies,
                    'shoppinglistid': shoppinglistid,
                    'currentshoplist': currentshoplist,
                    })
    return render_to_response('cat2_names_page.html', variables)

# Shops 
class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class ShopList(LoggedInMixin, ListView):
    """ ShopList view. """
    context_object_name = 'shops'
    action = None
    
    def get_queryset(self):
        # import pdb; pdb.set_trace()
        # self.action = self.args[0]
        return Shop.objects.all()
    



from django.views.generic.edit import CreateView, UpdateView, DeleteView
class ShopCreate(LoggedInMixin, CreateView):
    model = Shop
    success_url = '/shops/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #import pdb; pdb.set_trace()
        #name = form['name'].data
        #Shop
        form.save()
        return HttpResponseRedirect(
            '/shops/'
            )

def shops_remove_page(request, action):
    shops = Shop.objects.all()
    if action:
        remove = True
    if request.method == 'POST':
        formfields = request.POST
        for field in formfields:
            Shop.objects.get(id=str(field)).delete()
            
        remove = False
        #import pdb; pdb.set_trace()
    variables = RequestContext(request, {
                'remove': remove,
                'shops': shops,
                })
    return render_to_response('shop/shop_list.html', variables)

def settings_page(request):
    variables = RequestContext(request, {
                'user': request.user,
                })
    return render_to_response('config.html',variables)

def config_shoppinglists(request):
    variables = RequestContext(request, {
                'navbar': config_shoppinglists,
                })
    return render_to_response('config/shoppinglists.html', variables)

def config_shops(request):
    variables = RequestContext(request, {
                'navbar': config_shops,
                })
    return render_to_response('config/shops.html', variables)

def config_products(request):
    variables = RequestContext(request, {
                'navbar': config_products,
                })
    return render_to_response('config/shops.html', variables)


@login_required
def create_custom_product(request, username):
    if request.method == 'POST':
        form = CustomProductForm(request.POST)
        
        if form.is_valid():    
            customproduct, created = CustomProduct.objects.get_or_create(user=request.user,
                        name=form.cleaned_data['product_name'])
            customproduct.save()
            return HttpResponseRedirect(
            '/user/%s/customproducts/' % request.user.username
            )
    else:
        form = CustomProductForm()
    variables = RequestContext(request, {
                'form': form,
                })
    return render_to_response('shop/customproduct_form.html', variables)

@login_required
def custom_product_list(request, username):
    user = get_object_or_404(User, username=username)
    remove = False
    try:
        customproducts =CustomProduct.objects.filter(user=user)
    except CustomProduct.DoesNotExist:
        customproducts = []
    #if request.method == 'POST':
    #    form = CustomProductForm(request.POST)
    #    
    #    if form.is_valid():    
    #        customproduct, created = CustomProduct.objects.get_or_create(user=request.user,
    #                    name=form.cleaned_data['name'])
    #        customproduct.save()
    #        
    #        return HttpResponseRedirect(
    #        '/user/%s/customproducts/' % request.user.username
    #        )
    variables = RequestContext(request, {
                'remove': remove,
                'customproducts': customproducts,
                })
    
    return render_to_response('shop/customproducts_list.html', variables)
    
def custom_products_remove_page(request, username):
    user = get_object_or_404(User, username=username)
    remove = False
    try:
        customproducts =CustomProduct.objects.filter(user=user)
    except CustomProduct.DoesNotExist:
        customproducts = []
    remove = True
    if request.method == 'POST':
        formfields = request.POST
        for field in formfields:
            CustomProduct.objects.get(id=str(field)).delete()
            
        remove = False
        #import pdb; pdb.set_trace()
    variables = RequestContext(request, {
                'remove': remove,
                'customproducts': customproducts,
                })
    return render_to_response('shop/customproducts_list.html', variables)

@login_required
def account_page(request):
    variables = RequestContext(request, {
                'user': request.user,
                })
    return render_to_response('account.html',variables)




import datetime

from django.db import models

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

import shop.shop

class Shop(models.Model):
    name = models.CharField(max_length=32,unique=True,error_messages={'required': 'Please enter a shop name'})
    
    def get_absolute_url(self):
        return reverse(shop.shop.views.shop_products_page, args=[self.user.username, self.id])
    def __unicode__(self):
        return self.name
    
class ShoppingListManager(models.Manager):
    def completed(self):
        return self.filter(shoppingdate__lt=datetime.date.today())
    def active(self):
        return self.filter(shoppingdate__gte=datetime.date.today())
    def last(self):
        return self.latest('shoppingdate')
   
    
class Taxonomy(models.Model):
    cat0_name = models.CharField(max_length=64, blank=True, null=True)
    cat1_name = models.CharField(max_length=64, blank=True, null=True)
    cat2_name = models.CharField(max_length=64, blank=True, null=True)
    cat3_name = models.CharField(max_length=64, blank=True, null=True)
    cat4_name = models.CharField(max_length=64, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s, %s, %s' % (self.cat0_name, self.cat1_name, self.cat2_name)
    

    
class Product(models.Model):
    name = models.TextField()
    taxonomy = models.ForeignKey(Taxonomy, null=True, blank=True)
    def __unicode(self):
        return u'%s'% self.name
    
class CustomProduct(Product):
    user = models.ForeignKey(User)
    def __unicode(self):
        return u'%s'% self.name

class ShoppingList(models.Model):
    user = models.ForeignKey(User)
    created = models.DateField(auto_now=True)
    description = models.TextField()
    shoppingdate=models.DateField()
    shop = models.ForeignKey(Shop)
    products = models.ManyToManyField(Product, through='Shoplist_Product')
    
    objects = ShoppingListManager()
    
    def get_absolute_url(self):
        return reverse(shop.shop.views.shop_products_page, args=[self.user.username, self.id])
    def __unicode__(self):
        return u'%s, %s, %s' % (self.user.username, self.created, self.shop)
    
class Shoplist_Product(models.Model):
    product = models.ForeignKey(Product)
    shoplist = models.ForeignKey(ShoppingList)
    amount = models.IntegerField(default=1)
    
    def validate_unique(self, exclude=None):
        if Shoplist_Product.objects.exclude(pk=self.pk).filter(product=self.product,shoplist=self.shoplist).exists():
            raise ValidationError("IntegrityError: duplicate product-shoplist not allowed")
        super(Shoplist_Product, self).validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Shoplist_Product, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s-> %s' % (self.shoplist.created, self.product.name)
    
class Recipe(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField()
    instructions = models.TextField()
    def __str__(self):
        return self.name

class Recipe_Product(models.Model):
    product = models.ForeignKey(Product)
    recipe = models.ForeignKey(Recipe)
    amount = models.IntegerField()
    
class ProductTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    product = models.ManyToManyField(Product)
    def __str__(self):
        return self.name
    
class IngredientTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
class Ingredient(models.Model):
    name= models.TextField()
    tag = models.ForeignKey(IngredientTag)


class Profile(models.Model):
    """
    User Profile
    """
    user = models.ForeignKey(User, unique=True)
    onsitedata = models.DateTimeField(auto_now=True, blank=True)
    last_visit = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
            return str(self.user)
    def __unicode__(self):
            return unicode(self.user)
    def save(self, **kwargs):
            if self.pk:
                    if not self.last_visit:
                            self.last_visit = datetime.datetime.now()
                    self.last_visit = self.onsitedata
                    self.onsitedata = datetime.datetime.now()
            super(Profile, self).save(**kwargs)

    
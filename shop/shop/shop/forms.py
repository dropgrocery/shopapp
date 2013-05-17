import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget 
import datetime
from shop.shop.models import Shop,Taxonomy



class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
      label='Password',
      widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
      label='Password (Again)',
      widget=forms.PasswordInput()
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError('Username is already taken.')
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords do not match.')
        
class ShoppingListSaveForm(forms.Form):
    shoppingdate = forms.DateField(initial=datetime.date.today, input_formats=['%d/%m/%Y'])
    description = forms.CharField(required=False)
    shop = forms.ModelChoiceField(queryset = Shop.objects.values_list('id', flat=True))
    
class ProductSaveForm(forms.Form):
    product_name = forms.CharField()
    cat0_name = forms.CharField()
    cat1_name = forms.CharField()
    cat2_name = forms.CharField()
    
class ProductSelectForm(forms.Form):
    products = forms.ModelChoiceField(queryset = Taxonomy.objects.values_list(flat=True))
    
class AmountForm(forms.Form):
    product_name = forms.CharField()
    taxonomy = forms.IntegerField()
    amount = forms.ChoiceField(choices = ((0,'0'),(1,'1',),(2,'2'),(3,'3'),(4,'4'),(5,'5')))

class RemoveProductForm(forms.Form):
    product_id = forms.IntegerField()
    shoppinglist_id = forms.IntegerField()
    
class CustomProductForm(forms.Form):
    product_name = forms.CharField()

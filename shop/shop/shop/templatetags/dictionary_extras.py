'''
Created on 11 Mar 2013

@author: martin
'''

from django import template
register = template.Library()

@register.filter(name='access')
def access(value, arg):
    return value[arg]

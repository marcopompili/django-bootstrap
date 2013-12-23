'''
Created on 22/dic/2013

@author: Marco Pompili
'''

from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.util import flatatt

class BootstrapInput(widgets.Input):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        
        if value is None:
            value = ''
            
        if value != '':
            final_attrs['value'] = force_text(self._format_value(value))
        
        return self.bootstrap_render(name, value, final_attrs)

class BootstrapInputCtrlGroup(BootstrapInput):
    required = False
    input_type = 'text'
    
    def bootstrap_render(self, name, value, final_attrs):
        return format_html('<input{0} class="form-control"/>', flatatt(final_attrs))

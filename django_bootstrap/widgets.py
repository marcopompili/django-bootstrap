'''
Created on 22/dic/2013

@author: Marco Pompili
'''

from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.util import flatatt
from django.forms.widgets import Textarea, TextInput

class BootstrapTextInput(TextInput):
    required = False
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
            
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
            
        return format_html('<input{0} class="form-control"/>', flatatt(final_attrs))


class BootstrapTextarea(Textarea):
    required = False
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
            
        final_attrs = self.build_attrs(attrs, name=name)
        
        return format_html('<textarea{0} class="form-control">\r\n{1}</textarea>',
                           flatatt(final_attrs),
                           force_text(value))

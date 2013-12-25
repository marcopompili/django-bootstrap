'''
Created on 22/dic/2013

@author: Marco Pompili
'''

from django import forms

from django.forms.forms import DeclarativeFieldsMetaclass
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_text


class BootstrapBaseForm(forms.BaseForm):
    
    def _bt_html_output(self, label_attrs, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    # marcs modify: can add attributes to the label tag
                    label = bf.label_tag(label, label_attrs) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': six.text_type(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text': '',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))
    
    def as_bt_ctrl_grp(self):
        "Returns this form rendered as Bootstrap HTML control-group form."
        return self._bt_html_output(
            label_attrs = { 'class' : 'control-label' },
            normal_row='<div class="control-group">%(label)s<div class="controls"><div class="input-group">%(field)s</div>%(help_text)s</div></div>',
            error_row='',
            row_ender='</div>',
            help_text_html='<p class="help-block">%s</p>',
            errors_on_separate_row=False)
    
    def as_bt_grp(self):
        "Returns this form rendered as Bootstrap HTML control-group form."
        return self._html_output(
            normal_row='<div class="form-group">%(label)s%(field)s%(help_text)s</div>',
            error_row='',
            row_ender='</div>',
            help_text_html='<p class="help-block">%s</p>',
            errors_on_separate_row=False)


class BootstrapForm(six.with_metaclass(DeclarativeFieldsMetaclass, BootstrapBaseForm)):
    "A collection of Fields, plus their associated data."
    pass

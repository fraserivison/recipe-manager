from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):
        return mark_safe(field.as_widget(attrs={'class': css_class}))
    return field

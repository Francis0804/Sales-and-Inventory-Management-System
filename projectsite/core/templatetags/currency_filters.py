# core/templatetags/currency_filters.py
from django import template

register = template.Library()

@register.filter
def currency_format(value):
    """Format number as currency with thousand separators"""
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

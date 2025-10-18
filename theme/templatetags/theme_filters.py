from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_price(value):
    """Format price in Indian numbering system with INR symbol"""
    if not value:
        return ""
    
    try:
        price = float(value)
        if price >= 10000000:  # 1 crore
            formatted = price / 10000000
            if formatted == int(formatted):
                return f"{int(formatted)} Cr"
            else:
                return f"{formatted:.2f} Cr"
        elif price >= 100000:  # 1 lakh
            formatted = price / 100000
            if formatted == int(formatted):
                return f"{int(formatted)} Lakh"
            else:
                return f"{formatted:.2f} Lakh"
        else:
            return f"{int(price):,}"
    except (ValueError, TypeError):
        return str(value)

@register.filter
def format_area(value):
    """Format area with proper units"""
    if not value:
        return ""
    return str(value).replace('sq ft', 'sq.ft').replace('sqft', 'sq.ft')

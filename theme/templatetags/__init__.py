from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_price(value):
    """Format price in Indian numbering system"""
    if not value:
        return ""
    
    try:
        price = float(value)
        if price >= 10000000:  # 1 crore
            return f"₹{price / 10000000:.1f} Cr".replace('.0 ', ' ')
        elif price >= 100000:  # 1 lakh
            return f"₹{price / 100000:.1f} L".replace('.0 ', ' ')
        else:
            return f"₹{price:,.0f}"
    except (ValueError, TypeError):
        return str(value)

@register.filter
def format_area(value):
    """Format area with proper units"""
    if not value:
        return ""
    return str(value).replace('sq ft', 'sq.ft').replace('sqft', 'sq.ft')


@register.filter
def human_price(value):
    """Format integer/decimal rupee amounts into readable string.
    Ex: 1800000 -> '18 Lakh', 180000000 -> '18 Cr'
    Accepts value in rupees as integer or Decimal.
    """
    try:
        v = float(value)
    except Exception:
        return value

    lakh = 100000
    crore = 10000000

    if v >= crore:
        val = v / crore
        if val.is_integer():
            return f"{int(val)} Cr"
        return f"{val:.2f} Cr"
    elif v >= lakh:
        val = v / lakh
        if val.is_integer():
            return f"{int(val)} Lakh"
        return f"{val:.2f} Lakh"
    else:
        return f"₹{int(v):,}"

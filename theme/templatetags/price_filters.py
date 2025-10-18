from django import template

register = template.Library()

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

    # values in rupees
    lakh = 100000
    crore = 10000000

    if v >= crore:
        # show in crores with up to 2 decimals, but trim .0
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
        # show with commas
        return f"₹{int(v):,}"

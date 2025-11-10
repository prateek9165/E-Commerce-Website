from django import template
from django.conf import settings

register = template.Library()


_SYMBOL_MAP = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
}


def _get_symbol(code):
    return _SYMBOL_MAP.get(code, code)


@register.filter(name='currency')
def currency(value, code=None):
    """Format a numeric value for a currency code.

    Usage in templates: {{ value|currency:currency_code }}
    Falls back to settings.DEFAULT_CURRENCY if code is falsy.
    """
    if value is None:
        return ''

    # Determine currency code
    cur = code or getattr(settings, 'DEFAULT_CURRENCY', 'USD')
    cur = str(cur)

    # Try to coerce numeric value
    try:
        amount = float(value)
    except Exception:
        # If not numeric, return as-is
        return value

    # Decimal places
    dec = getattr(settings, 'CURRENCY_DECIMAL_PLACES', 2)

    symbol = _get_symbol(cur)
    # Format with thousands separator and fixed decimals
    try:
        formatted = f"{amount:,.{int(dec)}f}"
    except Exception:
        formatted = str(amount)

    return f"{symbol}{formatted}"

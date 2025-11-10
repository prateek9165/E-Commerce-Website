from django.conf import settings


def currencies(request):
    """Expose a CURRENCIES iterable to templates.

    Returns a list of dicts with keys: code, symbol, name.
    The list is built from settings.CURRENCIES. If a code is unknown,
    the code itself is used as symbol and name fallback.
    """
    default_map = {
        'USD': {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'},
        'EUR': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
        'GBP': {'code': 'GBP', 'symbol': '£', 'name': 'British Pound'},
        'INR': {'code': 'INR', 'symbol': '₹', 'name': 'Indian Rupee'},
    }

    cfg = getattr(settings, 'CURRENCIES', [])
    currencies = []
    for code in cfg:
        code_str = str(code)
        entry = default_map.get(code_str, {'code': code_str, 'symbol': code_str, 'name': code_str})
        currencies.append(entry)
    return {'CURRENCIES': currencies}

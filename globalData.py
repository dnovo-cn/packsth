def _init():
    global _global_data
    _global_data = {
        'wife': 'ail1xiya'
    }


def set_value(key, value):
    _global_data[key] = value


def get_value(key, defValue=None):
    try:
        return _global_data[key]
    except KeyError:
        return defValue

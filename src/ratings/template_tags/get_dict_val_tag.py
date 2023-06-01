
from django.template.defaultfilters import register


@register.filter(name = 'get_dict_val_tag' )
def get_dict_val_tag(dictionary, key, key_as_str = True):
        if not isinstance(dictionary, dict):
            return None
        if key_as_str:
            key = f"{key}"
        return dictionary.get(key)
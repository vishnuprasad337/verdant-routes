from django import template

from ..utils.image_utils import build_srcset

register = template.Library()


@register.filter
def srcset(field_file):
    if not field_file:
        return ""
    try:
        return build_srcset(field_file)
    except (ValueError, FileNotFoundError, OSError):
        return ""
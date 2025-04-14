from django import template

register = template.Library()

@register.filter
def status_color(status):
    """
    Returns the appropriate Bootstrap color class for a loan application status.
    """
    color_map = {
        'pending': 'warning',
        'under_review': 'info',
        'approved': 'success',
        'rejected': 'danger',
        'disbursed': 'primary'
    }
    return color_map.get(status, 'secondary') 
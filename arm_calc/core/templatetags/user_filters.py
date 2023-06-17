from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """
    Adds the specified CSS classes to the attributes
    of the given form field widget.
    """
    return field.as_widget(attrs={'class': css})

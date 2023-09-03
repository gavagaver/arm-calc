from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """
    Adds the specified CSS classes to the attributes
    of the given form field widget.
    """
    return field.as_widget(attrs={'class': css})


@register.filter
def multiply(value, arg):
    """
    Multiplies the given value by the given argument.
    """
    return value * arg


@register.filter
def pluralize_ru(value, variants):
    """
    Substitutes the correct declension of a word depending on the number.
    @param value: number.
    @param variants: declension variants of the word.
    Например: 'элемент, элемента, элементов'.
    @return: word in correct declension.
    """
    value = abs(int(value))
    variants = variants.split(', ')

    if value % 10 == 1 and value % 100 != 11:
        index = 0
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        index = 1
    else:
        index = 2

    return variants[index]

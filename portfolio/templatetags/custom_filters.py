from django import template

# Create an instance of the Library class to register custom template filters
register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplies the given value by the argument passed in the template.

    Args:
        value: The first value, typically passed in from the template.
        arg: The multiplier value, passed in from the template.

    Returns:
        The product of value and arg if both are valid numbers.
        Returns an empty string if ValueError or TypeError occurs.
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        # Return an empty string if multiplication fails due to invalid input
        return ''

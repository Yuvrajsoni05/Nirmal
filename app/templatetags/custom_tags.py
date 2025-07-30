from django import template
from datetime import datetime

register  = template.Library()
@register.simple_tag

def render_curreny(value):
    try:
        # Convert the value to a float before formatting
        numeric_value = float(value)
        return "R {:,.2f}".format(numeric_value)
    except (ValueError, TypeError):
        # Handle cases where the input is not a valid number
        return value

@register.simple_tag
def get_data_time():
    return datetime.now().strftime("%m/%d/%Y ,%H:%M:%S")



@register.filter
def indian_currency_format(value):
        
        try:
            # Convert to integer to remove floating point
            num = int(value)
            s = str(num)
            if len(s) <= 3:
                return s
            else:
                last_three = s[-3:]
                remaining = s[:-3]
                formatted_remaining = ""
                # Add commas for lakhs and crores
                while len(remaining) > 0:
                    if len(remaining) > 2:
                        formatted_remaining = remaining[-2:] + "," + formatted_remaining
                        remaining = remaining[:-2]
                    else:
                        formatted_remaining = remaining + "," + formatted_remaining
                        remaining = ""
                return formatted_remaining + last_three
        except (ValueError, TypeError):
            return value

@register.filter
def split_text(value):
    return value.split('+')


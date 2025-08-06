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
       
        num = float(value) 
        
        
        integer_part, decimal_part = str(num).split('.') 
        
    
        formatted_integer = ""
        
     
        formatted_integer = integer_part[-3:]  
        
        
        remaining_integer = integer_part[:-3] 
        
        while len(remaining_integer) > 0:
            if len(remaining_integer) > 2:
                formatted_integer = remaining_integer[-2:] + "," + formatted_integer
                remaining_integer = remaining_integer[:-2]
            else:
                formatted_integer = remaining_integer + "," + formatted_integer
                remaining_integer = ""

     
        if decimal_part:
            return formatted_integer + "." + decimal_part
        else:
            return formatted_integer

    except (ValueError, TypeError):
        return value

@register.filter
def split_text(value):
    return value.split('+')

@register.filter
def remove_white(value):
    return value.split(' ')




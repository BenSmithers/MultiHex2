

def get_cardinal(number:int)->str:
    """
        Returns the cardinal thingy for the end of a number. Used for string formatting, ie, 
            1 --> st
            2 --> nd 
            3 --> rd
            4 --> th
    """
    _number = abs(number)
    if number==0:
        return "th"
    elif _number==1:
        return "st"
    elif _number==2:
        return "nd"
    elif _number ==3:
        return "rd"
    elif _number <20:
        return "th"
    else:
        ones = number % 10

        return get_cardinal(ones)

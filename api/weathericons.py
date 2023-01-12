def get_weathericon(code):
    """
    Method for converting WMO Weather code to letter in the meteoicons font
    """
    if code in [0]:
        return "B"
    elif code in [1, 2]:
        return "H"
    elif code in [3]:
        return "N"
    elif code in [45, 48]:
        return "M"
    elif code in [51, 53, 55, 56, 57, 61, 66, 80]:
        return "Q"
    elif code in [63, 65, 67, 81, 82]:
        return "R"
    elif code in [71]:
        return "U"
    elif code in [73, 75, 86]:
        return "W"
    elif code in [77, 85]:
        return "V"
    elif code in [95, 96, 99]:
        return "Z"
    else:
        return ")"

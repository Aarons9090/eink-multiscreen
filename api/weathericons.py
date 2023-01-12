def get_weathericon(code):
    weathericon = ")"
    match code:
        case 0:
            weathericon = "B"
        case 1 | 2:
            weathericon = "H"
        case 3:
            weathericon = "N"
        case 45 | 48:
            weathericon = "M"
        case 51 | 53 | 55 | 56 | 57 | 61 | 66 | 80:
            weathericon = "Q"
        case 63 | 65 | 67 | 81 | 82:
            weathericon = "R"
        case 71:
            weathericon = "U"
        case 73 | 75 | 86:
            weathericon = "W"
        case 77 | 85:
            weathericon = "V"
        case 95 | 96 | 99:
            weathericon = "Z"
        case _:
            weathericon = ")"
    return weathericon

import pycountry

def convert_639_1_to_2(iso_639_1_code):
    try:
        language = pycountry.languages.get(alpha_2=iso_639_1_code)
        iso_639_2_code = language.alpha_3
        return iso_639_2_code
    except LookupError:
        return None
    
def convert_639_2_to_1(iso_639_2_code):
    try:
        language = pycountry.languages.get(alpha_3=iso_639_2_code)
        iso_639_1_code = language.alpha_2
        return iso_639_1_code
    except LookupError:
        return None
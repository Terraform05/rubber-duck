def highlight_string(input_string):
    highlight_code = '\033[7;97m'
    reset_code = '\033[0m'
    highlighted_string = f"{highlight_code}{input_string}{reset_code}"
    return highlighted_string

def highlight_print(input_string):
    print(highlight_string(input_string))
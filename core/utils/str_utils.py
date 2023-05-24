def check_if_all_digits(string):
    return all(char.isdigit() for char in string)

def extract_numbers(string) -> str:
    return ''.join(filter(str.isdigit, string))

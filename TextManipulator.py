def sarcasticalize(text: str) -> str:

    ret_val = ''

    for index, char in enumerate(text):
        if not char.isalpha():
            ret_val += char
            continue

        if index % 2 == 0:
            char = char.upper()

        ret_val += char

    return ret_val

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Sarcasticalize inputstreams by alternatig between uppercase and lowercase')
    parser.add_argument('inputstream', help='The String to output alternating')

    args = parser.parse_args()
    string: str = args.inputstream.lower()

    print(sarcasticalize(text=string))


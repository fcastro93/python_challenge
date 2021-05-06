import re


def to_text(file):
    ips = re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", file)
    return ips


def open_file(file):
    try:
        ip_file = open(file, 'r')
        text = ip_file.read()
        return text
    except:
        print("Unable to open the file", file)

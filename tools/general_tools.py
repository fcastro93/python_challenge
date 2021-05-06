import re


def to_text(file):
    '''
    Takes out the ip addresses from a text
    Parameters
    ----------
    file : str
    Text that contains the ip addresses

    Returns
    -------
    ips : list
    List that includes the ip addresses
    '''
    ips = re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", file)
    return ips


def open_file(file):
    '''
    Opens a file based on the name
    Parameters
    ----------
    file : str
    Name of the file

    Returns
    -------
    file : bytes file
    Opened file ready to extract info from it
    '''
    try:
        ip_file = open(file, 'r')
        text = ip_file.read()
        return text
    except:
        print("Unable to open the file", file)

import os

def get_parent_dir(directory):

    """
    Gets the base directory of curreny running file/script
    :param directory: Current directory os.getcwd()
    :return: returns the path of the current directory
    """

    return os.path.dirname(directory)

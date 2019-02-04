import os


# FIXME: can rename to more useful method name
# eg if it is used to validate positive floats, could be called positive float validator
def validate(text):
    if not text:
        return 1  # empty -> "incomplete"

    if not text.isdigit():
        return 0  # nondigits -> "invalid"

    if len(text) < 4:
        return 1  # too short -> "incomplete"

    if len(text) > 6:
        return 0  # too long -> "invalid"

    return 2  # Valid text


def get_filename(path, ext=False):
    """Returns filename in given path, strips the extension off is ext is False"""

    fname = path.split(os.sep)[-1]

    if ext:
        return fname

    return fname.split('.')[0]


def get_filename_ext(path):
    """Returns last present extension on filename, if one exists"""

    fname_ext_list = get_filename(path, True).split('.')

    # No extension
    if len(fname_ext_list) < 2:
        return ''

    return fname_ext_list[-1]


def make_unique_directory(directory):
    """Ensures the given directory is unique by appending a unique identifier to it"""

    if os.path.exists(directory):
        uid = 0
        while os.path.exists(directory + str(uid)):
            uid += 1

        directory += str(uid)

    return directory

from PyQt5.QtWidgets import QFileDialog

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


def get_directory(parent, dlg_name='Select Directory'):
    return str(QFileDialog.getExistingDirectory(parent, dlg_name))


def linspace(start, end, number_points):

    # Figure out how much to increment by
    length = end - start
    increment = length / number_points - 1  # There are 19 points to calculate

    # Create list of points
    current = start
    out = [] * number_points
    for i in range(number_points):
        out[i] = current
        current += increment

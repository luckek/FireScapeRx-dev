import os
import subprocess

from PyQt5.QtWidgets import QFileDialog, QDesktopWidget


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


def get_directory(parent, dlg_name='Select Directory'):
    return str(QFileDialog.getExistingDirectory(parent, dlg_name))


def linspace(start, end, number_points, increment=-1):

    # Figure out how much to increment by

    if increment == -1:
        length = end - start
        increment = length / (number_points - 1)  # There are 19 points to calculate

    # Create list of points
    current = start
    out = [0] * number_points
    for i in range(number_points - 1):
        out[i] = current
        current += increment

    out[-1] = end

    return out


def execute(cmd, cwd, out_file):
    """Execute the given command, from within the given current working directory"""

    # Run command via Popen, set stderr and stdout to /dev/null.
    # NOTE: Cannot use subprocess.run because this will wait for the given command to finish, whereas
    # Popen will start the process and just return a process id(pid).
    # FIXME: See if we can replace subprocess.pipe with a file? may run into block-buffering issue again

    subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def meters_per_cell(meters, number_cells):
    """Simple convenience function for calculating FDS mesh sizes"""
    return meters / number_cells


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def center_window(window):

    qt_rectangle = window.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    qt_rectangle.moveCenter(center_point)
    window.move(qt_rectangle.topLeft())

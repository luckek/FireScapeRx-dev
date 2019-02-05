import os
import subprocess

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


def execute(cmd, cwd):
    """Execute the given command, from within the given current working directory"""

    if cwd is None:
        cwd = os.getcwd()

    # Run command via Popen, set stderr and stdout to a new PIPE.
    # This is done because writing directly to a file causes a block buffering issue. However, qApp.processEvents may alleviate this
    # NOTE: Cannot use subprocess.run because this will wait for the given command to finish, whereas
    # Popen will start the process and just return a process id(pid).
    # FIXME: See if we can replace subprocess.pipe with a file? may run into block-buffering issue again
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd=cwd, bufsize=1)

    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

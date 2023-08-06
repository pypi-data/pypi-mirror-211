import os
import shutil
import subprocess

mypid = os.getpid()
f = os.path.normpath(shutil.which("taskkill.exe"))
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW

invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
}


def commit_suicide():
    """
    Terminates the current process in a hidden manner.

    This function terminates the current process by using the 'taskkill.exe'
    command in a subprocess. The termination is performed in a hidden manner,
    without displaying any windows or prompts to the user.

    Note:
        This function is intended for special use cases and should be used with caution.
        Terminating a process abruptly can lead to unexpected results and data loss.

    Raises:
        FileNotFoundError: If the 'taskkill.exe' command is not found on the system.

    Example:
        >>> commit_suicide()
    """
    wholecommand = f'start /min "" {f} /F /T /PID {mypid}'
    p = subprocess.run(wholecommand, capture_output=True, shell=True,  **invisibledict)
    print(p.stdout)
    print(p.stderr)

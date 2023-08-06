# Kills the current process by using 'taskkill.exe'

## pip install suicideproc

#### Tested against Windows 10 / Python 3.10 / Anaconda

```python
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
		from suicideproc import commit_suicide
        commit_suicide()
```
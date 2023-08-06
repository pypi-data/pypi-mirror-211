import ctypes
import os
import sys
from ctypes import wintypes
from ctypes import WinDLL
from ctypes_window_info import get_window_infos
import kthread
from time import perf_counter
import functools
import re
from kthread_sleep import sleep
import psutil
from hackyargparser import add_sysargv

from ctrlchandler import set_console_ctrl_handler


def _exit():
    print("Ending process ...")
    try:
        sys.exit(1)
    finally:
        os._exit(1)


procconf = sys.modules[__name__]
procconf.already_changed = []
procconf.running_threads = {}

kernel32 = WinDLL("kernel32", use_last_error=True)

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

SetPriorityClass = kernel32.SetPriorityClass
SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
SetPriorityClass.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

LOW = 64
BELOW_NORMAL = 16384
NORMAL = 32
ABOVE_NORMAL = 32768
HIGH = 128
REALTIME = 256


@add_sysargv
def constant_check_and_change_priority(
    exe_path: str | None = None,
    priority: int = NORMAL,
    is_regex: int | bool = 1,
    flags: int = re.I,
    delay: float | int = 1.0,
    close_after_first: int | bool = 0,
):
    r"""
    Constantly checks and changes the priority of processes based on the provided parameters.

    Args:
        exe_path (str | None): Path or regular expression pattern of the executable to monitor.
        priority (int): Priority value to set for the processes. Valid options are:
            - LOW = 64
            - BELOW_NORMAL = 16384
            - NORMAL = 32
            - ABOVE_NORMAL = 32768
            - HIGH = 128
            - REALTIME = 256
            Defaults to NORMAL (32).
        is_regex (int | bool): Flag indicating whether the exe_path should be treated as a regular expression pattern.
            Defaults to 1 (True).
        flags (int): Flags to be used with the regular expression pattern. Defaults to re.I (ignore case).
        delay (float | int): Delay in seconds between each check. Defaults to 1.0.
        close_after_first (int | bool): Flag indicating whether to exit the program after the first process is found.
            Defaults to 0 (False).

    Returns:
        Callable: A function that can be used to stop the monitoring thread.

    Example:
        Changing priority of one process - function call:
        This line shows an example of calling the change_priority function to change the priority of a specific process
        with a given PID. In this case, the priority is set to HIGH. The PID used here is 21360.

        change_priority(pid=21360,priority=HIGH)
        #################################################
        Constantly changing priority of processes with exe_path - CLI:
        This line demonstrates how to use the script from the command line interface (CLI)
        to constantly monitor and change the priority of processes based on the specified exe_path parameter.
        The script is invoked using the python command, followed by the script path.
        The CLI arguments are provided using -- followed by the argument name and its corresponding value.
        In this example, the exe_path is set to notepad.exe$, the priority is set to 128 (which corresponds
        to HIGH priority), is_regex is set to 1 (True), flags is set to 2, delay is set to 2.0 seconds,
        and close_after_first is set to 0 (False).

        # adjust the path!
        python .\__init__.py --exe_path notepad.exe$ --priority 128 --is_regex 1 --flags 2 --delay 2.0 --close_after_first 0
        #################################################


        This part showcases an example of using the constant_check_and_change_priority function directly in Python code.
        The function is called with various parameters to monitor and change the priority of processes.
        In this example, the exe_path is set to "notepad.exe$", indicating a regular expression pattern,
        the priority is set to NORMAL, is_regex is set to True, flags is set to re.I (ignore case),
        delay is set to 1.0 second, and close_after_first is set to False.
        constant_check_and_change_priority(
        exe_path="notepad.exe$",
        priority=NORMAL,
        is_regex=True,
        flags=re.I,
        delay=1.0,
        close_after_first=False,
        )
        #################################################

        # To stop the monitoring thread, call the returned function
        stop_monitoring()
    """
    if not exe_path:
        print("No exe_path informed!")
        os._exit(1)
    procname = str(perf_counter())
    procconf.running_threads[procname] = kthread.KThread(
        target=check_and_change_priority,
        name=procname,
        args=(exe_path, priority, is_regex, flags, delay, close_after_first),
    )
    procconf.running_threads[procname].start()
    return functools.partial(killthread, procconf.running_threads[procname])


def check_and_change_priority(
    exe, priority, is_regex, flags=0, delay=1, close_after_first=False
):
    if is_regex:
        exe = re.compile(exe.strip('" '), flags=flags)
    else:
        exe = str(exe).lower()
    print("\n")
    while True:
        for w in get_window_infos():
            proc_ok = False
            if is_regex:
                if exe.search(w.path):
                    proc_ok = True
            else:
                if str(w.path).lower() == exe:
                    proc_ok = True
            if proc_ok:
                try:
                    for chi in [w.pid] + [
                        x.pid for x in psutil.Process(w.pid).children()
                    ]:
                        if chi not in procconf.already_changed:
                            if change_priority(chi, priority):
                                procconf.already_changed.append(chi)
                except Exception as fa:
                    print(fa)

        print(f"\r{procconf.already_changed}", end="")
        if close_after_first:
            try:
                sys.exit(0)
            finally:
                os._exit(0)
        sleep(delay)


def killthread(t):
    try:
        while t.is_alive():
            try:
                t.kill()
            except Exception as fa:
                print(fa)
                continue
    except Exception as fa:
        print(fa)
        return


def change_priority(pid, priority):
    try:
        hProcess = OpenProcess(0x1F0FFF, False, pid)
        if hProcess == 0:
            print("Failed to open the process. Error code:", ctypes.GetLastError())

        if not SetPriorityClass(hProcess, priority):
            print(
                "Failed to set the process priority. Error code:", ctypes.GetLastError()
            )
        CloseHandle(hProcess)
    except Exception as fe:
        print(fe)
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_console_ctrl_handler(returncode=1, func=_exit)
        killfunction = constant_check_and_change_priority()

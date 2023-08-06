import os
import sys
from ctypes_window_info import get_window_infos
import kthread
from time import perf_counter
import functools
import re
from kthread_sleep import sleep
import psutil
from hackyargparser import add_sysargv

from ctrlchandler import set_console_ctrl_handler
from taskkill import taskkill_force_pid_children


def _exit():
    print("Ending process ...")
    try:
        sys.exit(1)
    finally:
        os._exit(1)


procconf = sys.modules[__name__]
procconf.already_changed = []
procconf.running_threads = {}


@add_sysargv
def constant_check_and_kill(
    exe_path: str | None = None,
    is_regex: int | bool = 1,
    flags: int = re.I,
    delay: float | int = 1.0,
    close_after_first: int | bool = 0,
):
    r"""
    Continuously checks for running processes and kills them if they match the specified criteria.

    Args:
        exe_path (str | None): The path or regex pattern of the processes to be killed.
        is_regex (int | bool): Flag indicating if `exe_path` is a regex pattern (default: 1).
        flags (int): Additional flags for the regex pattern matching (default: re.I).
        delay (float | int): Delay in seconds between process checks (default: 1.0).
        close_after_first (int | bool): Flag indicating whether to exit after killing the first matching process (default: 0).

    Returns:
        Callable[[], None]: A partial function that can be used to stop the continuous process checking and killing.

    Raises:
        None

    Example usage:

    Killing one process - function call:
    This example demonstrates how to kill a single process by calling the kill_proc function with the desired process ID (PID).
    The process with the specified PID will be terminated.

    kill_proc(pid=21360)
    ############################################################
    Constantly checking if processes exist and kill them - CLI:
    This example shows how to use the script from the command line to continuously monitor and kill processes that match a
    specific executable path pattern. The command should be executed in the following format:

    python .\constant_kill_procs.py --exe_path "(?:calculator.exe|chrome.exe)$" --is_regex 1 --flags 2 --delay 0.1 --close_after_first 0
    --exe_path: The regular expression pattern specifying the executable path(s) of the target processes.
    --is_regex: A flag indicating whether the exe_path argument should be treated as a regular expression (1 for True, 0 for False).
    --flags: Additional flags for the regular expression pattern matching.
    --delay: The delay in seconds between each process check.
    --close_after_first: A flag indicating whether to exit the script after killing the first matching process (1 for True, 0 for False).
    ############################################################
    Constantly checking if processes exist and kill them - function call:
    This example demonstrates how to continuously monitor and kill processes that match a specific executable path pattern
    by calling the constant_check_and_kill function directly.
    from constant_check_and_kill import constant_check_and_kill

    constant_check_and_kill(
        exe_path="notepad.exe$",
        is_regex=True,
        flags=re.I,
        delay=1.0,
        close_after_first=False,
    )
    exe_path: The regular expression pattern or exact executable path of the target processes.
    is_regex: A flag indicating whether the exe_path argument should be treated as a regular expression (True) or an exact path (False).
    flags: Additional flags for the regular expression pattern matching.
    delay: The delay in seconds between each process check.
    close_after_first: A flag indicating whether to exit the script after killing the first matching process (True) or
    continue monitoring and killing other matching processes (False).

    """
    if not exe_path:
        print("No exe_path informed!")
        os._exit(1)
    procname = str(perf_counter())
    procconf.running_threads[procname] = kthread.KThread(
        target=check_and_kill,
        name=procname,
        args=(exe_path, is_regex, flags, delay, close_after_first),
    )
    procconf.running_threads[procname].start()
    return functools.partial(killthread, procconf.running_threads[procname])


def check_and_kill(exe, is_regex, flags=0, delay=1, close_after_first=False):
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
                        if kill_proc(chi):
                            print(f"\rKilled: {procconf.already_changed}", end="")
                except Exception as fa:
                    continue

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


def kill_proc(pid):
    try:
        results = taskkill_force_pid_children(pids=(pid,))
    except Exception as fe:
        print(fe)
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_console_ctrl_handler(returncode=1, func=_exit)
        killfunction = constant_check_and_kill()

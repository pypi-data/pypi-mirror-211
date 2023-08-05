"""
Launches an interactive shell with an instance of HFSS

omitting the .py in the name of this file hides it from the Electronics Desktop Toolkit menu.
It should be hidden from this menu because the scripts in that menu are meant to be executed using IronPython
cpython_console.py should be run instead of this script.

This file can also serve as a template to modify PyAEDT scripts to take advantage of the command line arguments
provided by the launcher
"""
import atexit
import os
import sys

try:
    import pyaedt
except ImportError:
    # debug only purpose. If Ribbon is added from a github clone then we link pyaedt in personal lib.
    console_setup_dir = os.path.dirname(__file__)
    if "PersonalLib" in console_setup_dir:
        sys.path.append(os.path.join(console_setup_dir, "..", "..", ".."))
    import pyaedt


pyaedt.settings.use_grpc_api = False
from pyaedt import Desktop
from pyaedt.generic.general_methods import active_sessions
from pyaedt.generic.general_methods import is_windows

aedt_process_id = int(sys.argv[1])
version = sys.argv[2]
print("Loading the PyAEDT Console.")


def release(d):
    d.logger.info("Exiting the PyAEDT Console.")

    d.release_desktop(False, False)


sessions = active_sessions(version=version, student_version=False)
session_found = False
port = 0
student_version = False


for session in sessions:
    if session[0] == aedt_process_id and session[1] != -1:
        pyaedt.settings.use_grpc_api = True
        port = session[1]
        session_found = True
        break
    elif session[0] == aedt_process_id:
        session_found = True
        break
if not session_found:
    sessions = active_sessions(version=version, student_version=True)
    for session in sessions:
        if session[0] == aedt_process_id and session[1] != -1:
            pyaedt.settings.use_grpc_api = True
            port = session[1]
            session_found = True
            student_version = True
            break
        elif session[0] == aedt_process_id:
            session_found = True
            student_version = True
            break
error = False
if port:
    desktop = Desktop(
        specified_version=version,
        port=port,
        new_desktop_session=False,
        non_graphical=False,
        close_on_exit=False,
        student_version=student_version,
    )
elif is_windows:
    desktop = Desktop(
        specified_version=version,
        aedt_process_id=aedt_process_id,
        new_desktop_session=False,
        non_graphical=False,
        close_on_exit=False,
        student_version=student_version,
    )
else:
    print("Error. AEDT should be started in GRPC mode in Linux to connect to Pyaedt")
    print("use ansysedt -grpcsrv portnumber command.")
    error = True
if not error:
    print(" ")

    print("\033[92m****************************************************************")
    print("*  ElectronicsDesktop {} Process ID {}".format(version, aedt_process_id))
    print("*  CPython {}".format(sys.version.split(" ")[0]))
    print("*---------------------------------------------------------------")
    print("*  Example: \033[94m hfss = pyaedt.Hfss() \033[92m")
    print("*  Example: \033[94m m2d = pyaedt.Maxwell2d() \033[92m")
    print("*  \033[31mType exit() to close the console and release the desktop.  \033[92m ")
    print("*  desktop object is initialized and available. Example: ")
    print("*  \033[94mdesktop.logger.info('Hello world')\033[92m")
    print("****************************************************************\033[0m")
    print(" ")
    print(" ")
    print(" ")
    atexit.register(release, desktop)

"""
Cloud_Py_Api self install module.
"""

import logging
import platform
import sys
from typing import Union
from argparse import ArgumentParser
from getpass import getuser
from importlib import invalidate_caches
from importlib.metadata import PackageNotFoundError, version, requires
from json import dumps as to_json
from json import loads as from_json
from os import environ, mkdir, path, remove
from re import IGNORECASE, MULTILINE, search, sub
from subprocess import DEVNULL, CalledProcessError, TimeoutExpired, run
from urllib.parse import unquote_plus
from dataclasses import dataclass, field


@dataclass
class Options:
    """Dataclass with runtime properties."""

    app_data: str = ""
    db_config: dict = field(default_factory=dict)
    dev: bool = False
    pip_present: bool = False
    pip_version: tuple = (0, 0, 0)
    pip_local: bool = False

    @property
    def local_dir(self) -> str:
        return str(path.join(self.app_data, ".local"))

    @property
    def python_local(self) -> bool:
        return sys.executable.startswith(self.app_data)


OPTIONS = Options()
EXTRA_PIP_ARGS = []
LOGS_CONTAINER = []
Log = logging.getLogger("pyfrm.install")
Log.propagate = False
logging.addLevelName(30, "WARN")
logging.addLevelName(50, "FATAL")


class InstallLogHandler(logging.Handler):
    """Used when calling this package as a script."""

    __log_levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}

    def emit(self, record):
        self.format(record)
        __content = (
            record.message if record.funcName == "<module>" else record.funcName + ": " + record.message
        )
        if record.exc_text is not None:
            __content += "\n" + record.exc_text
        __log_lvl = self.__log_levels.get(record.levelname)
        __module = record.module if record.name == "root" else record.name
        if OPTIONS.dev:
            LOGS_CONTAINER.append(
                {"log_lvl": __log_lvl, "module": f"{record.filename}:{record.lineno}", "content": __content}
            )
        else:
            LOGS_CONTAINER.append({"log_lvl": __log_lvl, "module": __module, "content": __content})


def update_pip_info() -> None:
    OPTIONS.pip_local = False
    OPTIONS.pip_version = check_pip()
    _pip = OPTIONS.pip_version[0] >= 21
    if _pip:
        _location = get_package_info("pip").get("location", "")
        if _location:
            if _location.startswith(OPTIONS.app_data):
                OPTIONS.pip_local = True
        else:
            Log.warning("Cant determine pip location, assume that it is global.")
    OPTIONS.pip_present = _pip


def init_local_dir() -> None:
    if path.isdir(OPTIONS.local_dir):
        return
    Log.info("Creating local directory: %s", OPTIONS.local_dir)
    try:
        mkdir(OPTIONS.local_dir, mode=0o764)
        if not path.isdir(OPTIONS.local_dir):
            raise ValueError("[REPORT]Local directory missing after create.")
    except OSError as e:
        Log.error("[REPORT]Can not create `local` directory.")
        raise OSError from e


def get_core_userbase() -> str:
    if OPTIONS.python_local:
        return path.dirname(path.dirname(sys.executable))
    return OPTIONS.local_dir


def get_modified_env(userbase: str = "", python_path: str = "") -> dict:
    modified_env = dict(environ)
    modified_env["PYTHONUSERBASE"] = userbase if userbase else get_core_userbase()
    if python_path:
        modified_env["PYTHONPATH"] = python_path
    modified_env["_PIP_LOCATIONS_NO_WARN_ON_MISMATCH"] = "1"
    return modified_env


def get_site_packages(userbase: str = "") -> str:
    _env = get_modified_env(userbase=userbase)
    try:
        _result = run(
            [sys.executable, "-m", "site", "--user-site"],
            capture_output=True,
            check=True,
            env=_env,
        )
        return _result.stdout.decode("utf-8").rstrip("\n")
    except (OSError, ValueError, TypeError, TimeoutExpired, CalledProcessError) as _exception_info:
        Log.exception("Exception %s:", type(_exception_info).__name__)
        return ""


def check_pip() -> tuple:
    _ret = (0, 0, 0)
    try:
        str_version = version("pip")
    except PackageNotFoundError:
        return _ret
    m_groups = search(r"(\d+(\.\d+){0,2})", str_version, flags=MULTILINE + IGNORECASE)
    if m_groups is None:
        return _ret
    pip_version = tuple(map(int, str(m_groups.groups()[0]).split(".")))
    return pip_version if len(pip_version) > 2 else pip_version + (0,)


def remove_pip_warnings(pip_output: str) -> str:
    return sub(r"^\s*WARNING:.*\n?", "", pip_output, flags=MULTILINE + IGNORECASE)


def pip_call(params, userbase: str = "", python_path: str = "", user=False, cache=None) -> [bool, str]:
    Log.debug("pip_call(USERBASE<%s> PATH<%s>)", userbase, python_path)
    try:
        etc = ["--disable-pip-version-check"]
        etc += EXTRA_PIP_ARGS
        _env = get_modified_env(userbase=userbase, python_path=python_path)
        if user:
            etc += ["--user"]
        if cache is False:
            etc += ["--no-cache-dir"]
        elif cache is True:
            etc += ["--cache-dir", _env["PYTHONUSERBASE"]]
        Log.debug("_env=<%s>", _env)
        pip_run_args = [sys.executable, "-m", "pip"] + params + etc
        Log.debug("_args=<%s>", pip_run_args)
        _result = run(pip_run_args, capture_output=True, check=False, env=_env)
        _stderr = _result.stderr.decode("utf-8")
        _stdout = _result.stdout.decode("utf-8")
        if _stderr:
            Log.debug(f"pip.stderr:\n{_stderr}".rstrip("\n"))
        if _stdout:
            Log.debug(f"pip.stdout:\n{_stdout}".rstrip("\n"))
        if not remove_pip_warnings(_stderr):
            return True, _stdout
        return False, _stderr
    except (OSError, ValueError, TypeError, TimeoutExpired) as _exception_info:
        return False, f"Exception {type(_exception_info).__name__}: {str(_exception_info)}"


def add_python_path(_path: str, first: bool = False):
    if not _path:
        return
    try:
        sys.path.pop(sys.path.index(_path))
    except (ValueError, IndexError):
        pass
    if first:
        sys.path.insert(0, _path)
    else:
        sys.path.append(_path)
    invalidate_caches()


def get_package_info(name: str, userbase: str = "", python_path: str = "") -> dict:
    package_info = {}
    if name:
        _call_result, _message = pip_call(
            ["show", name], userbase=userbase, python_path=python_path, cache=True
        )
        if _call_result:
            _pip_show_map = {
                "Version:": "version",
                "Location:": "location",
                "Requires:": "requires",
            }
            for _line in _message.splitlines():
                for key, value in _pip_show_map.items():
                    if _line.startswith(key):
                        package_info[value] = _line[len(key) :].strip()
    return package_info


def get_package_dependencies(name: str) -> Union[dict, None]:
    try:
        dependencies = requires(name)
    except PackageNotFoundError:
        return None
    requires_list = []
    optional_list = []
    for i in dependencies:
        i_info = i.split(";")
        if len(i_info) < 2:
            requires_list.append(i_info[0])
        elif i_info[1].find("optional") != -1:
            optional_list.append(i_info[0])
    return {"requires": requires_list, "optional": optional_list}


def download_file(url: str, out_path: str) -> bool:
    n_download_clients = 2
    for _ in range(2):
        try:
            run(["curl", "-L", url, "-o", out_path], timeout=90, stderr=DEVNULL, stdout=DEVNULL, check=True)
            Log.debug("`%s` finished downloading.", out_path)
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    for _ in range(2):
        try:
            run(["wget", url, "-O", out_path], timeout=90, stderr=DEVNULL, stdout=DEVNULL, check=True)
            Log.debug("`%s` finished downloading.", out_path)
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    if not n_download_clients:
        Log.error("Both curl and wget cannot be found.")
    return False


def install_pip() -> bool:
    Log.info("Start installing local pip.")
    get_pip_path = str(path.join(OPTIONS.local_dir, "get-pip.py"))
    if not download_file("https://bootstrap.pypa.io/get-pip.py", get_pip_path):
        Log.error("Cant download pip installer.")
        return False
    try:
        Log.info("Running get-pip.py...")
        _env = get_modified_env(OPTIONS.local_dir)
        _result = run(
            [
                sys.executable,
                get_pip_path,
                "--user",
                "--cache-dir",
                OPTIONS.local_dir,
                "--no-warn-script-location",
            ],
            capture_output=True,
            check=False,
            env=_env,
        )
        Log.debug("get-pip.stdout:\n%s", _result.stdout.decode('utf-8'))
        full_reply = _result.stderr.decode("utf-8")
        if full_reply:
            Log.debug("get-pip.stderr:\n%s", full_reply)
        if not remove_pip_warnings(full_reply):
            return True
        Log.error("get-pip returned:\n%s", full_reply)
    except (OSError, ValueError, TypeError, TimeoutExpired) as _exception_info:
        Log.exception("Exception %s:", type(_exception_info).__name__)
    finally:
        try:
            remove(get_pip_path)
        except OSError:
            Log.warning("Cant remove `%s`", get_pip_path)
    return False


def update_pip() -> bool:
    if not OPTIONS.pip_present:
        Log.error("No compatible pip found.")
        return False
    if OPTIONS.pip_local:
        _call_result, _message = pip_call(
            ["install", "--upgrade", "pip", "--no-warn-script-location"], user=True, cache=True
        )
        if not _call_result:
            return False
    return True


def app_check(app_name: str = "nc_py_frm") -> [list, list, list]:
    if not OPTIONS.pip_present:
        Log.error("Python pip not found or has too low version.")
        return [], [{"package": "pip3", "location": "", "version": ""}], []
    # TODO: here add path of app
    add_python_path(get_site_packages(), first=True)
    installed_list = []
    not_installed_list = []
    not_installed_opt_list = []
    dependencies = get_package_dependencies(app_name)
    if dependencies is None:
        return [], [{"package": app_name, "location": "", "version": ""}], []
    for dependency in dependencies["requires"] + dependencies["optional"]:
        dependency_info = get_package_info(dependency)
        if dependency_info:
            dependency_info.pop("requires")
            installed_list.append({"package": dependency, **dependency_info})
        elif dependency in dependencies["requires"]:
            not_installed_list.append({"package": dependency, "location": "", "version": ""})
            Log.error("Missing %s.", dependency)
        else:
            not_installed_opt_list.append({"package": dependency, "location": "", "version": ""})
            Log.warning("Missing %s.", dependency)
    return installed_list, not_installed_list, not_installed_opt_list


def frm_install(extra_args=None) -> bool:
    if extra_args is None:
        extra_args = []
    if not OPTIONS.pip_present:
        if not install_pip():
            Log.error("Cant install local pip.")
            return False
        update_pip_info()
        if not OPTIONS.pip_present:
            Log.error("Cant run pip after local install.")
            return False
    import os
    cwd = os.getcwd()
    os.chdir("..")
    cwd = os.getcwd()
    _result, _message = pip_call(
        ["install", "nc_py_frm/.", "--no-warn-script-location", "--no-deps"] + extra_args, user=True, cache=True
        )
    if not _result:
        Log.error("Cant install nc_py_frm. Pip output:\n%s", _message)
    _installed, _not, _not_opt = app_check()
    _installed = [i for i in _installed if not i["location"].startswith(OPTIONS.app_data)]
    _all_dependencies = _installed + _not + _not_opt
    for dependency in _all_dependencies:
        _result, _message = pip_call(
            ["install", dependency["package"], "--no-warn-script-location", "--prefer-binary"] + extra_args,
            user=True,
            cache=True,
        )
        if not _result:
            if dependency in _not_opt:
                Log.warning("Cant install %s. Pip output:\n%s", dependency["package"], _message)
            else:
                Log.error("Cant install %s. Pip output:\n%s", dependency["package"], _message)
                return False
    return True


def frm_perform(action: str) -> bool:
    if action == "delete":
        raise ValueError("Target `framework` can not be specified for delete operation.")
    if action == "install":
        return frm_install()
    if action == "update":
        if not update_pip():
            return False
        return frm_install(["--upgrade"])
    raise ValueError(f"Unknown action: {action}.")


def app_perform(app_id: str, action: str) -> bool:
    return False


def perform_action(target: str, action: str) -> bool:
    if target == "framework":
        return frm_perform(action)
    return app_perform(target, action)


if __name__ == "__main__":
    # from importlib.metadata import requires, metadata, files
    # aa = get_package_dependencies("pillow-heif")
    # abc = requires("pillow-heif")
    # dddabc = metadata("pillow")
    # fff = files("pillow")
    # util.locate
    # METADATA SOURCES.txt
    # sys.exit(0)
    parser = ArgumentParser(
        description="Module for checking/installing packages for NC pyfrm.", add_help=True
    )
    parser.add_argument(
        "--config", dest="config", type=str, help="JSON with loglvl, frmAppData and dbConfig.", required=True
    )
    parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="'framework' or 'AppId' from table `cloud_py_api`(for app).",
        required=True,
    )
    parser.add_argument("--dev", dest="dev", action="store_true", default=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check", dest="check", action="store_true", help="Check installation of specified target."
    )
    group.add_argument(
        "--install",
        dest="install",
        action="store_true",
        help="Perform installation of specified target's packages.",
    )
    group.add_argument(
        "--update", dest="update", action="store_true", help="Perform update of specified target's packages."
    )
    group.add_argument(
        "--delete",
        dest="delete",
        action="store_true",
        help="Perform delete of specified target's packages.",
    )
    args = parser.parse_args()
    OPTIONS.dev = args.dev
    args.target = str(args.target).lower()
    config = from_json(unquote_plus(args.config))
    OPTIONS.app_data = config["frmAppData"]
    OPTIONS.db_config = config["dbConfig"]
    Log.setLevel(level=config["loglvl"])
    Log.addHandler(InstallLogHandler())
    EXIT_CODE = 0
    RESULT = False
    r_installed_list = {}
    r_not_installed_list = {}
    r_not_installed_opt_list = {}
    try:
        try:
            Log.debug("User name: %s", getuser())
        except (AttributeError, ImportError, OSError) as _exception:
            Log.warning("Exception during `getuser`: %s", str(_exception))
        Log.debug("target: %s", args.target)
        Log.debug("Platform: %s", platform.platform())
        init_local_dir()
        update_pip_info()
        Log.debug("app_data: %s", OPTIONS.app_data)
        Log.info("Python: %s : %s", sys.executable, sys.version)
        Log.info("Pip version: %s, local: %r", OPTIONS.pip_version, OPTIONS.pip_local)
        if args.target != "framework":
            r_installed_list, r_not_installed_list, r_not_installed_opt_list = app_check("framework")
            if r_not_installed_list:
                raise ValueError("Install framework before targeting app.")
            r_installed_list.clear()
            r_not_installed_list.clear()
            r_not_installed_opt_list.clear()
        if args.install:
            RESULT = perform_action(args.target, "install")
        elif args.update:
            RESULT = perform_action(args.target, "update")
        elif args.delete:
            RESULT = perform_action(args.target, "delete")
        r_installed_list, r_not_installed_list, r_not_installed_opt_list = app_check(args.target)
        if args.check and not r_not_installed_list:
            RESULT = True
        if not RESULT:
            EXIT_CODE = 1
    except Exception as exception_info:  # pylint: disable=broad-except
        Log.exception("Exception: %s", type(exception_info).__name__)
        EXIT_CODE = 2
    Log.debug("ExitCode: %d", EXIT_CODE)
    if OPTIONS.dev:
        print("Logs:")
        for log_record in LOGS_CONTAINER:
            print(str(log_record["log_lvl"]) + " : " + log_record["module"] + " : " + log_record["content"])
        print(f"Installed:\n{r_installed_list}")
        print(f"NotInstalled:\n{r_not_installed_list}")
        print(f"NotInstalledOpt:\n{r_not_installed_opt_list}")
        print(f"Result: {RESULT}")
    else:
        print(
            to_json(
                {
                    "Result": RESULT,
                    "Installed": r_installed_list,
                    "NotInstalled": r_not_installed_list,
                    "NotInstalledOpt": r_not_installed_opt_list,
                    "Logs": LOGS_CONTAINER,
                }
            )
        )
    sys.exit(EXIT_CODE)

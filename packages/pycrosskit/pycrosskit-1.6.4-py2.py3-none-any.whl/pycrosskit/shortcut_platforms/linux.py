#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
import os
import stat
from pathlib import Path

from pycrosskit.shortcuts import UserFolders

scut_ext = '.desktop'
ico_ext = ('ico', 'svg', 'png')

DESKTOP_FORM = """[Desktop Entry]
Version=1.0
Name={name:s}
Type=Application
Comment={desc:s}
Icon={icon:s}
Terminal=false
Exec={exe:s} {args:s}
"""

_HOME = None


def get_homedir():
    """determine home directory of current user"""
    global _HOME
    if _HOME is not None:
        return _HOME

    home = None
    try:
        home = str(Path.home())
    except:
        pass

    if home is None:
        home = os.path.expanduser("~")
    if home is None:
        home = os.environ.get("HOME", os.path.abspath(".."))
    _HOME = home
    return home


def get_desktop():
    """get desktop location"""
    homedir = get_homedir()
    desktop = os.path.join(homedir, 'Desktop')

    # search for .config/user-dirs.dirs in HOMEDIR
    ud_file = os.path.join(homedir, '.config', 'user-dirs.dirs')
    if os.path.exists(ud_file):
        val = desktop
        with open(ud_file, 'r') as fh:
            text = fh.readlines()
        for line in text:
            if 'DESKTOP' in line:
                line = line.replace('$HOME', homedir)[:-1]
                key, val = line.split('=')
                val = val.replace('"', '').replace("'", "")
        desktop = val
    return desktop


def get_startmenu():
    """get start menu location"""
    homedir = get_homedir()
    return os.path.join(homedir, '.local', 'share', 'applications')


def get_folders():
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def create_shortcut(shortcut_instance,
                    desktop=False, startmenu=False):
    """
    Create Shortcut
    :param shortcut_instance: Shortcut Instance
    :param startmenu: True to create Start Menu Shortcut
    :param desktop: True to create Desktop Shortcut
    :return: desktop icon path, start menu path
    :rtype: str, str
    """
    if shortcut_instance.work_path is None:
        file_content = DESKTOP_FORM.format(name=shortcut_instance.shortcut_name,
                                           desc=shortcut_instance.description,
                                           exe=shortcut_instance.exec_path,
                                           icon=shortcut_instance.icon_path,
                                           args=shortcut_instance.arguments)
    else:
        file_content = DESKTOP_FORM.format(name=shortcut_instance.shortcut_name,
                                           desc=shortcut_instance.description,
                                           exe=f"bash -c "
                                               f"'cd {shortcut_instance.work_path}"
                                               f" && {shortcut_instance.exec_path}'",
                                           icon=shortcut_instance.icon_path,
                                           args=shortcut_instance.arguments)
    user_folders = get_folders()
    desktop_path = Path(user_folders.desktop)
    startmenu_path = Path(user_folders.startmenu)

    if desktop:
        __write_shortcut(desktop_path, shortcut_instance, file_content)

    if startmenu:
        __write_shortcut(startmenu_path, shortcut_instance, file_content)

    return desktop_path, startmenu_path


def __write_shortcut(dest_path: Path, shortcut_instance, file_content):
    """
    Writes shortcut content to destination
    :param dest_path: Path where write file
    :param shortcut_instance: Instance of shortcut that will be used
    :param file_content: Content of future icon from DESKTOP_FORM.format(...)
    """
    if not dest_path.parent.exists():
        os.makedirs(str(dest_path))
    dest = str(dest_path / (shortcut_instance.shortcut_name + scut_ext))
    with open(dest, 'w') as f_out:
        f_out.write(file_content)
    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IEXEC)


def delete_shortcut(shortcut_name, desktop=False, startmenu=False):
    """
    Delete Shortcut
    :param shortcut_name: Name of Shortcut
    :param startmenu: True to create Start Menu Shortcut
    :param desktop: True to create Desktop Shortcut
    :return: desktop icon path, start menu path
    :rtype: str, str
    """
    user_folders = get_folders()
    desktop_path, startmenu_path = "", ""
    if startmenu:
        startmenu_path = user_folders.startmenu + "/" + shortcut_name + scut_ext
        if os.path.exists(startmenu_path):
            os.chmod(startmenu_path, stat.S_IWRITE)
            os.remove(startmenu_path)
    if desktop:
        desktop_path = user_folders.desktop + "/" + shortcut_name + scut_ext
        if os.path.exists(desktop_path):
            os.chmod(desktop_path, stat.S_IWRITE)
            os.remove(desktop_path)
    return desktop_path, startmenu_path

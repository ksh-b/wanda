import os
import subprocess

from wanda.utils.common_utils import command, blank, contains


def screen_orientation():
    return "landscape" if size()[0] > size()[1] else "portrait"


def program_exists(program):
    return subprocess.call(
        ['which', program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ) == 0


def set_wp_win(path):
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def set_wp_linux(path):
    if not os.environ.get("DESKTOP_SESSION"):
        setter = "feh --bg-scale"
    elif os.environ.get("SWAYSOCK"):
        setter = "eval ogurictl output '*' --image"
    elif os.environ.get("DESKTOP_SESSION").lower == "mate":
        setter = "gsettings set org.mate.background picture-filename"
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(), False, ["xfce", "xubuntu"]
    ):
        if program_exists("xfce4-set-wallpaper"):
            setter = "xfce4-set-wallpaper"
        else:
            screens = command("xfconf-query --channel xfce4-desktop -l").split("\n")
            screens = list(filter(lambda it: "/workspace" in it, screens))
            for screen in screens:
                setter = (
                    f"xfconf-query --channel xfce4-desktop --property {screen} --set "
                )
                command(f"{setter} {path}")
            return
    elif os.environ.get("DESKTOP_SESSION").lower() == "lxde":
        setter = "pcmanfm --wallpaper-mode=screen --set-wallpaper"
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(), False, ["plasma", "neon", "kde"]
    ):
        return os.system(
            'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "\n'
            + "var allDesktops = desktops();\n"
            + "print (allDesktops);\n"
            + "for (i=0;i<allDesktops.length;i++) {\n"
            + "d = allDesktops[i];\n"
            + "d.wallpaperPlugin = 'org.kde.image';\n"
            + "d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');\n"
            + f"d.writeConfig('Image', 'file://{path}')\n"
            + '}"'
        )
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(),
            False,
            ["gnome", "pantheon", "ubuntu", "deepin", "pop"],
    ):
        setter = "gsettings set org.gnome.desktop.background picture-uri"
    else:
        setter = "feh --bg-scale"

    command(f"{setter} {path}")


def size():
    import screeninfo  # type: ignore

    if is_android():
        hxw = command("getprop persist.vendor.camera.display.umax")
        if not blank(hxw):
            return int(hxw.split("x")[1]), int(hxw.split("x")[0])
        return 1440, 2960
    try:
        dimensions = screeninfo.get_monitors()[0]  # type: ignore
        return int(dimensions.width), int(dimensions.height)
    except screeninfo.ScreenInfoError:
        return 2560, 1440


def set_wp_android(path, home, lock):
    if home:
        command(f"termux-wallpaper -f {path}")
    if lock:
        command(f"termux-wallpaper -lf {path}")


def is_android():
    return os.environ.get("TERMUX_VERSION") is not None


def is_desktop():
    return not is_android()

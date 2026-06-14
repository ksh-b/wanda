import os
import shlex
import shutil
import subprocess
from pathlib import Path

from wanda.utils.common_utils import command, blank

def program_exists(program):
    return (
        subprocess.call(
            ["which", program],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )


def set_wp_win(path):
    import ctypes

    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

def _cmd_exists(cmd):
    return shutil.which(cmd) is not None

def _run(cmd):
    subprocess.run(cmd, shell=True, check=False)

def set_wp_linux(path):
    path = str(Path(path).expanduser().resolve())
    ds = os.environ.get("DESKTOP_SESSION", "") or ""
    ds_l = ds.lower()
    # Wayland / Sway
    if os.environ.get("SWAYSOCK") or "sway" in ds_l:
        # prefer swaybg or swaymsg, fallback to hyprland method if needed
        if _cmd_exists("swaybg"):
            _run(f'swaybg -o "*" -i {shlex.quote(path)} -m fill &')
            return
        if _cmd_exists("swaymsg"):
            _run(f'swaymsg output "*" background {shlex.quote(path)} fill')
            return
    # KDE / Plasma
    if any(k in ds_l for k in ("plasma", "kde", "neon")):
        # prefer qdbus or qdbus-qt5 or dbus-send approach
        qdbus = shutil.which("qdbus") or shutil.which("qdbus-qt5") or shutil.which("qdbus6") or shutil.which("qdbus-qt6")
        if qdbus:
            script = (
                "var allDesktops = desktops();"
                "for (i=0;i<allDesktops.length;i++) {"
                "d = allDesktops[i];"
                "d.wallpaperPlugin = 'org.kde.image';"
                "d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');"
                f"d.writeConfig('Image', 'file://{path}')"
                "}"
            )
            _run(f'{qdbus} org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "{script}"')
            return
    # XFCE
    if "xfce" in ds_l or "xubuntu" in ds_l:
        if _cmd_exists("xfce4-set-wallpaper"):
            _run(f'xfce4-set-wallpaper --image {shlex.quote(path)}')
            return
        if _cmd_exists("xfconf-query"):
            # set for all workspace images
            proc = subprocess.run("xfconf-query --channel xfce4-desktop -l", shell=True, capture_output=True, text=True)
            for line in proc.stdout.splitlines():
                if "/workspace" in line and "last-image" in line:
                    _run(f'xfconf-query --channel xfce4-desktop --property "{line}" --set {shlex.quote(path)}')
            return
    # MATE
    if "mate" in ds_l:
        if _cmd_exists("gsettings"):
            _run(f"gsettings set org.mate.background picture-filename {shlex.quote(path)}")
            return
    # LXDE / LXQT
    if "lxde" in ds_l:
        if _cmd_exists("pcmanfm"):
            _run(f'pcmanfm --set-wallpaper={shlex.quote(path)} --wallpaper-mode=fit')
            return
    if "lxqt" in ds_l:
        if _cmd_exists("pcmanfm-qt"):
            _run(f'pcmanfm-qt --set-wallpaper {shlex.quote(path)}')
            return
    # GNOME / derivatives (Ubuntu, Pop, Deepin, Pantheon)
    if any(k in ds_l for k in ("gnome", "ubuntu", "pop", "deepin", "pantheon")):
        if _cmd_exists("gsettings"):
            # Use picture-uri for older GNOME, picture-uri or file:// required
            _run(f"gsettings set org.gnome.desktop.background picture-uri 'file://{path}'")
            return
    # fallback to feh (X11)
    if _cmd_exists("feh"):
        _run(f'feh --bg-scale {shlex.quote(path)}')
        return
    # last resort: set with xwallpaper or eog as a crude fallback
    if _cmd_exists("xwallpaper"):
        _run(f'xwallpaper --zoom {shlex.quote(path)}')
        return

    raise RuntimeError("No supported wallpaper setter found on this system.")


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

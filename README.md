# AdminV

A console-based multi-user OS emulator written in Python.

## Features

- Multi-user system with login and session management
- Admin and non-admin privilege levels
- Fernet-encrypted passwords
- Per-user themes, disk, and settings
- Built-in apps: CLI file explorer, text editor
- Dynamic app system (`.eux` apps)
- Admin controls: user management, disk settings, factory reset

## Structure

```
main.py                 entry point and boot
login.py                authentication
home.py                 main shell
apps.py                 app loader
exp.py                  file explorer
text_editor.py          text editor
admin_settings.py
user_settings.py
theme_settings.py
disk_settings.py
```

## Run

```
python main.py
```
## Default Login

- **Username:** admin
- **Password:** admin

> ⚠️ The `disk/` directory is integrity-checked at boot. Modifying it manually will cause a fatal boot error.
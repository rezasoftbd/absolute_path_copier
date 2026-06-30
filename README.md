# Absolute Path Copier

A tiny macOS GUI app. Drag any file or folder onto it → it shows the absolute path and
copies it to your clipboard automatically.

## Install

The built app is at:

```
dist/Absolute Path Copier.app
```

Drag **`Absolute Path Copier.app`** into your `/Applications` folder. Done.

First launch: macOS may say it's from an unidentified developer (the app is unsigned).
Right-click the app → **Open** → **Open**, or go to
**System Settings → Privacy & Security** and click **Open Anyway**.

## Use

1. Open the app.
2. Drag a file or folder onto the drop area.
3. The absolute path appears in the box and is already on your clipboard — just paste.

Drop multiple items at once and you get all their paths, newline-separated, on the clipboard.

## Develop / run from source

Requires Python 3.12 with a modern Tk (Homebrew `python-tk@3.12`).

```bash
.venv/bin/python3 app.py        # run directly
```

## Rebuild the .app

```bash
.venv/bin/pyinstaller --name "Absolute Path Copier" --windowed --noconfirm \
  --osx-bundle-identifier com.reza.absolutepathcopier app.py
```

## Notes

- Built with PyInstaller on **Python 3.12 / Tk 9.0.3**. The system Python 3.9 (Tk 8.5)
  will *not* work on macOS 26 (Tahoe) — its Tk has a version-gate bug that aborts at launch
  with `macOS 26 (2601) or later required`.
- Drag-and-drop is provided by `tkinterdnd2` (native `tkdnd`), bundled into the .app.

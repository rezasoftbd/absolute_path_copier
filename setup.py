"""Build script: `python setup.py py2app` produces dist/Absolute Path Copier.app"""

from setuptools import setup

APP = ["app.py"]
OPTIONS = {
    "argv_emulation": False,
    "packages": ["tkinterdnd2"],
    "plist": {
        "CFBundleName": "Absolute Path Copier",
        "CFBundleDisplayName": "Absolute Path Copier",
        "CFBundleIdentifier": "com.reza.absolutepathcopier",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "10.13",
    },
}

setup(
    app=APP,
    name="Absolute Path Copier",
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)

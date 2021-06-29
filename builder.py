import PyInstaller.__main__
import platform

options = [
    './main.py',
    '--onefile',
    '--windowed',
    '--clean'
]

os = platform.system()

if os == "Windows":
    options.append('--icon=./assets/icon.ico')
elif os == "Darwin":
    options.append('--icon=./assets/icon.icns')

PyInstaller.__main__.run(options)

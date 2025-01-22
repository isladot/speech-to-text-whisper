import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--noconsole',
    '--noconfirm',
    '--name=S2T',
])
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['omai_main.py'],
    pathex=[],
    binaries=[],
    datas=[('config', 'config'), ('images', 'images')],
    hiddenimports=['neo_api_client', 'PIL', 'pandas', 'numpy', 'requests', 'pyotp', 'openpyxl', 'flask', 'telethon'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Jss_Wealthtech',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

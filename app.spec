# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app.py','a2.py','cities.py','extension.py','funcs.py','mymodels.py'],
    pathex=['D:\\workspace\\pycharm\\plate_locator'],
    binaries=[],
    datas=['D:\\workspace\\pycharm\\plate_locator\\templates\\static\\bg\\bg1.png','D:\\workspace\\pycharm\\plate_locator\\templates\\static\\bg\\bg2.png',
    'D:\\workspace\\pycharm\\plate_locator\\templates\\static\\bg\\bg3.png','D:\\workspace\\pycharm\\plate_locator\\templates\\static\\bg\\zcbotton.png'],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='lpdr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lpdr',
)

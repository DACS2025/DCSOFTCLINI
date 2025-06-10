# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['start.py'],
    pathex=['C:\\\\PYDjango_CLIVET\\DCSoftClini\\'],
    binaries=[],
    datas=[('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\db.sqlite3', '.'), ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\core\\\\templates', 'core/templates'), ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\core\\\\static', 'core/static'), ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\media\\\\projects', 'media/projects'),
    ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\DCSoftClini\\\\settings.py', 'DCSoftClini'),
    ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\DCSoftClini\\\\__init__.py', 'DCSoftClini'),
    ('C:\\\\PYDjango_CLIVET\\\\DCSoftClini\\\\DCSoftClini\\\\urls.py', 'DCSoftClini'),
    ('apply_migrations.py', '.'),],
    hiddenimports=[],
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
    name='start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

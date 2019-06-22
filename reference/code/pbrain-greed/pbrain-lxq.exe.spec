# -*- mode: python -*-

block_cipher = None


a = Analysis(['greed.py', 'pisqpipe.py'],
             pathex=['C:\\Users\\11029\\Documents\\GitHub\\FDU-Artificial-Intelligence\\Projects\\Gomoku Competition\\code\\pbrain-greed'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pbrain-lxq.exe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

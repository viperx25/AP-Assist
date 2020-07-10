from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('apassist.py', base=base)
]

setup(name='APAssist',
      version = '1.0',
      description = 'Quickly send your images from a mobile device to your computer to submit for AP testing!',
      options = dict(build_exe = buildOptions),
      executables = executables)

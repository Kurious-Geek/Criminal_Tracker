import cx_Freeze as cx
import os
import platform
import sys


if platform.system() == "Windows":
        PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))
        os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tcl8.6')
        os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tk8.6')
        
include_files = [('criminal_record/images', 'images')]

include_files += [(os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
                 (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), '')]

base = None
target_name = 'Criminal_Tracker'
if platform.system() == "Windows":
                 base = "Win32GUI"
                 target_name = 'Criminal_Tracker.exe'

shortcut_data = [
    ('DesktopShortcut', 'DesktopFolder', 'CRIMINAL_TRACKER', 'TARGETDIR',
     '[TARGETDIR]'+target_name, None,
     'proposed application for criminal data entry and monitoring', None,
     None, None, None, 'TARGETDIR'),
    ('MenuShortcut', 'ProgramMenuFolder', 'CRIMINAL_TRACKER', 'TARGETDIR',
     '[TARGETDIR]'+target_name, None,
     'proposed application for criminal data entry and monitoring', None,
     None, None, None, 'TARGETDIR')
    ]

cx.setup(
    name = 'Criminal_Tracker',
    version = '1.0',
    author = 'Kurious Geek',
    description = 'multifunctional data entry application',
    packages = ['criminal_record'],

    executables = [
        cx.Executable('criminal_record.py', base=base,
                      targetName=target_name, icon='ctracker.ico')],
    options = {
        'build_exe': {
            'packages': ['psycopg2', 'requests', 'matplotlib', 'numpy'],
            'includes': ['idna.idnadata', 'zlib'],
            'include_files': include_files,
            'excludes': ['PyQt4', 'PyQt5', 'PySide', 'Ipython', 'jupiter_client',
                         'jupiter_core', 'ipykernel', 'ipython_genutils'] 
        },
        'bdist_msi': {
            'upgrade_code': '{42B1AEB0-5109-48CD-A479-898C6D2CF510}',
            'data': {'Shortcut': shortcut_data}

        }
    }          
)            
            

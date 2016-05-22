#!/usr/bin/env python
import os
import shutil
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scanproj.settings")

    from django.core.management import execute_from_command_line

    PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
    if sys.argv[1] == 'configure':
        scancode_dir = os.path.join(PROJ_DIR, 'scancode-toolkit')
        if os.path.exists(scancode_dir):
            shutil.rmtree(scancode_dir)
        else:
            os.system('git clone https://github.com/nexB/scancode-toolkit.git ' + scancode_dir)
    else:
        execute_from_command_line(sys.argv)

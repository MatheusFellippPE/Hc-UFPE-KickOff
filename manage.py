#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as e:
        if "django" in str(e).lower():
            print("Django não instalado. Execute: pip install django")
            sys.exit(1)
        raise
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
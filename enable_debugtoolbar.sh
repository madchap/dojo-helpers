#!/usr/bin/env bash
set -xe

settings_file=dojo/settings/settings.py

[[ ! -f $settings_file ]] &&
    echo "File settings.py not found. Make sure to execute this from within your defectdojo root directory. Aborting." && exit 1

if ! grep -qE 'debug_toolbar', $settings_file ; then
    sed -i '/INSTALLED_APPS = (/a \    ''debug_toolbar'','  $settings_file
    sed -i '/DJANGO_MIDDLEWARE_CLASSES = \[/a \    ''debug_toolbar.middleware.DebugToolbarMiddleware'','  $settings_file

    TOOLFORCE="
## force toolbar to show no matter what
# def show_toolbar(request):
#     return True
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK' : show_toolbar,
# }
    "

    echo "INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()" >> $settings_file
    echo "$TOOLFORCE" >> $settings_file
else
    echo "Debug toolbar seems to be already enabled."
fi

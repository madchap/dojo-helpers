#!/usr/bin/env bash
set -e

settings_file=dojo/settings/settings.py

[[ ! -f $settings_file ]] &&
    echo "File settings.py not found. Make sure to execute this from within your defectdojo root directory. Aborting." && exit 1

if ! grep -q 'import debug_toolbar' $settings_file ; then
    # settings file
    sed -i '/import os/i import debug_toolbar' $settings_file
    sed -i '/INSTALLED_APPS = (/a \    '\'debug_toolbar\'','  $settings_file
    sed -i '/DJANGO_MIDDLEWARE_CLASSES = \[/a \    '\'debug_toolbar.middleware.DebugToolbarMiddleware\'','  $settings_file

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

    # requirements.txt
    echo "django-debug-toolbar" >> requirements.txt

    # urls.py
    sed -i '/if settings.DEBUG:/a \    import debug_toolbar \
    urlpatterns.insert(0, url(r"^__debug__/", include(debug_toolbar.urls)))' dojo/urls.py
    
    echo "Django debug toolbar enabled."
    echo "Please rebuild your docker images to enable the debug toolbar library."

else
    echo "Debug toolbar seems to be already enabled."
fi

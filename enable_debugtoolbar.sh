#!/usr/bin/env bash
set -e

# settings_file=dojo/settings/settings.py
settings_file=dojo/settings/settings.dist.py
urls_file=dojo/urls.py
reqs_files=requirements.txt

[[ ! -f $settings_file ]] &&
    echo "File settings.py not found. Make sure to execute this from within your defectdojo root directory. Aborting." && exit 1

INTERNAL_IPS="INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()"

usage () { 
    echo "Usage: $0 [-e] [-d] [-h]";
    echo "  -e: Enable"
    echo "  -d: Disable"    
}

disable_toolbar() {
    sed -i "/$INTERNAL_IPS\|debug_toolbar/d" $settings_file
    sed -i '/debug_toolbar.urls\|import debug_toolbar/d' $urls_file
    sed -i '/django-debug-toolbar/d' $reqs_files

    echo "Debug toolbar configuration removed."
}

enable_toolbar() {
    if ! grep -q 'import debug_toolbar' $settings_file ; then
        # settings file
        sed -i '/import os/i import debug_toolbar' $settings_file
        sed -i '/INSTALLED_APPS = (/a \    '\'debug_toolbar\'','  $settings_file
        sed -i '/DJANGO_MIDDLEWARE_CLASSES = \[/a \    '\'debug_toolbar.middleware.DebugToolbarMiddleware\'','  $settings_file

        echo "$INTERNAL_IPS" >> $settings_file

        # requirements.txt
        echo "django-debug-toolbar" >> $reqs_files

        # urls.py
        # odd indentation to keep urls.py indentation
        sed -i '/if settings.DEBUG:/a \    import debug_toolbar \
    urlpatterns.insert(0, url(r"^__debug__/", include(debug_toolbar.urls)))' $urls_file

        echo "Django debug toolbar enabled."
        echo "Copy the modified settings.dist.py over to your settings.py."
        echo "Please rebuild your docker images to enable the debug toolbar library."
    else
        echo "Debug toolbar seems to be already configured."
    fi
}

while getopts ":ed" opt; do
    case ${opt} in
        e)  enable_toolbar 
            ;;
        d)  disable_toolbar
            ;;
        *)  usage
            exit 1
            ;;    
    esac
done
shift $((OPTIND -1))

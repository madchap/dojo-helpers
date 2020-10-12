#!/usr/bin/env bash
set -e
# Notes
# 1. build-arg with UID of your local user
# 2. allows you to 'docker-compose exec uwsgi /bin/sh -c 'mkdir -p /app/components/node_modules' and make it work :thinking:


both_settings_file=( dojo/settings/settings.dist.py dojo/settings/settings.py )
urls_file=dojo/urls.py
reqs_files=requirements.txt

[[ ! -d dojo ]] &&
    echo "dojo directory not found. Make sure to execute this from within your defectdojo root directory. Aborting." && exit 1

usage () { 
    echo "Usage: $0 [-e] [-d] [-h]";
    echo "  -e: Enable"
    echo "  -d: Disable"    
}

disable_toolbar() {
    for settings_file in "${both_settings_file[@]}"; do
        sed -i "/INTERNAL_IPS\|debug_toolbar/d" "$settings_file"
    done
    sed -i '/debug_toolbar.urls\|import debug_toolbar/d' $urls_file
    sed -i '/django-debug-toolbar/d' $reqs_files

    echo "Debug toolbar configuration removed."
    }

enable_toolbar() {
    for settings_file in "${both_settings_file[@]}"; do
        if ! grep -q 'import debug_toolbar' "$settings_file" ; then
            # settings file
            sed -i '/import os/i import debug_toolbar' "$settings_file"
            sed -i '/INSTALLED_APPS = (/a \    '\'debug_toolbar\'','  "$settings_file"
            sed -i '/DJANGO_MIDDLEWARE_CLASSES = \[/a \    '\'debug_toolbar.middleware.DebugToolbarMiddleware\'','  "$settings_file"
            echo "INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()" >> "$settings_file"
        else
            echo "Debug toolbar seems to be already configured."
            exit 1
        fi
    done

    # requirements.txt
    echo "django-debug-toolbar" >> $reqs_files

    # urls.py
    # odd indentation to keep urls.py indentation
    sed -i '/if settings.DEBUG:/a \    import debug_toolbar\
    urlpatterns.insert(0, url(r"^__debug__/", include(debug_toolbar.urls)))' $urls_file

    echo "Django debug toolbar enabled."
    echo "Tip: Please rebuild your docker images with '--build-arg uid=xxx' to enable the debug toolbar library."
    echo "Tip: you may have to run docker-compose exec uwsgi /bin/sh -c 'mkdir -p /app/components/node_modules' too."
    }

while getopts ":ed" opt; do
    case ${opt} in
        e)  enable_toolbar 
            ;;
        d)  disable_toolbar
            ;;
        *)  usage
            exit 0
            ;;    
    esac
done
shift $((OPTIND -1))

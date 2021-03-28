#!/usr/bin/env bash
set -e
set -o pipefail

# DD or CB or ...
TARGET_ENV="$1"

function get_admin_token() {
    cd /home/fblaise/gitrepos/madchap_ddojo
    ADMINPASSWD=$(grep -m1 "Admin password:" <(docker-compose logs -f) |awk '{print $5}')
    ADMINTOKEN=$(curl -s -XPOST -H 'content-type: application/json' http://localhost:8080/api/v2/api-token-auth/ -d "{\"username\": \"admin\", \"password\": \"$ADMINPASSWD\"}" |jq -r .token)
    cd -
    sed -ri "s/dd_token=.*/dd_token=\"$ADMINTOKEN\"/" _config.py
}

function enable_google_login() {
    cd /home/fblaise/gitrepos/madchap_ddojo
    IFS=$'\n'; for line in $(cat ${OLDPWD}/_google_creds.txt); do
        sed -r -i "s/(.*)${line%=*}=.*/\1${line}/" dojo/settings/settings.dist.py;
    done
    cd -
}

case "$TARGET_ENV" in
    "DD")
        echo "Using local DD"
        ln -sf ./_config.py-DD ./_config.py
        ln -sf ./_jira_creds.py-DD ./_jira_creds.py
        ln -sf ./_slack_creds.py-DD ./_slack_creds.py
        get_admin_token
        enable_google_login
        ;;
    "CB")
        echo "Using CB prod"
        ln -sf ./_config.py-CB ./_config.py
        ln -sf ./_jira_creds.py-CB ./_jira_creds.py
        ln -sf ./_slack_creds.py-CB ./_slack_creds.py
        ;;
    "CBSTAGING")
        echo "Using CB staging"
        ln -sf ./_config.py-CBSTAGING ./_config.py
        ln -sf ./_jira_creds.py-CB ./_jira_creds.py
        ln -sf ./_slack_creds.py-CB ./_slack_creds.py
        ;;
    *)
        echo "Not a recognized target environment"
        exit 1
        ;;
esac


python ./settings_config.py
python ./jira_config.py
python ./import_initial_data.py

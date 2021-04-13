#!/usr/bin/env bash
set -e
set -o pipefail

# DD or CB or ...
TARGET_ENV="$1"
DEBUG_YES_NO="$2"
BASE_DIR="/home/fblaise/gitrepos/madchap_ddojo"

function get_admin_token() {
    echo "Waiting for admin credentials to grab"
    cd $BASE_DIR
    ADMINPASSWD=$(grep -m1 "Admin password:" <(docker-compose logs -f) |awk '{print $5}')
    sleep 1
    ADMINTOKEN=$(curl -s -XPOST -H 'content-type: application/json' http://localhost:8080/api/v2/api-token-auth/ -d "{\"username\": \"admin\", \"password\": \"$ADMINPASSWD\"}" |jq -r .token)
    JIRAWEBHOOK=$(grep -m1 "JIRA Webhook" <(docker-compose logs -f) |awk '{print $6}')
    echo "JIRA Webhook: /jira/webhook/$JIRAWEBHOOK"
    cd -
    sed -ri "s/dd_token=.*/dd_token=\"$ADMINTOKEN\"/" _config.py
}

function enable_google_login() {
    echo "Enabling google SSO"
    # and potentially change other vars in settings.dist.py, need to rename
    cd $BASE_DIR
    IFS=$'\n'; for line in $(cat ${OLDPWD}/_google_creds.txt); do
        sed -r -i "s/(.*)${line%=*}=.*/\1${line}/" dojo/settings/settings.dist.py;
    done
    cd -
}

function enable_toolbar() {
    local_settings_file=$BASE_DIR/dojo/settings/local_settings.py
    if [ "$DEBUG_YES_NO" == "debug" ]; then
        echo "Enabling toolbar and rebuilding images"
        cp /home/fblaise/templates/local_settings.py $local_settings_file
        # rebuild
        cd $BASE_DIR
        echo "Stopping stack"
        docker-compose stop >/dev/null 2>&1
        echo "Building images with arg $(id -u)"
        docker-compose build --build-arg uid=$(id -u) >/dev/null
        docker-compose up -d
        cd -
    else
        echo "Pass 'debug' as 2nd argument to rebuild with debug_toolbar."
    fi
}

function create_env_file() {
    cat > ${BASE_DIR}/.env <<EOF
DD_FEATURE_FINDING_GROUPS="True"
EOF
}

case "$TARGET_ENV" in
    "DD")
        echo "Using local DD"
        ln -sf ./_config.py-DD ./_config.py
        ln -sf ./_jira_creds.py-DD ./_jira_creds.py
        ln -sf ./_slack_creds.py-DD ./_slack_creds.py
        create_env_file
        enable_toolbar
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
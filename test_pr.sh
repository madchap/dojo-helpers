#!/bin/bash
set -ex
# quick script to initialize dojo to test PRs


function clean_current_env() {
    docker-compose stop
    docker-compose rm -vf
    docker volume rm -f madchap_ddojo_defectdojo_data
}

function new_pr_env() {
    # cp dojo/settings/settings.dist.py dojo/settings/settings.py
    docker-compose build
    docker-compose up -d
    echo "Waiting for admin password to show up..."
    # wait arbitrary time for containers to show up
    sleep 15
    ADMINPASSWD=$(grep -m1 "Admin password:" <(docker-compose logs -f) |awk '{print $5}')
    # FIXME: loop for API page to become available
    sleep 10

    # get token
    ADMINTOKEN=$(curl -s -XPOST -H 'content-type: application/json' http://localhost:8080/api/v2/api-token-auth/ -d "{\"username\": \"admin\", \"password\": \"$ADMINPASSWD\"}" |jq -r .token)

    echo "Replacing token in dojo-helpers _config file"
    sed -ri "s/dd_token=.*/dd_token=\"$ADMINTOKEN\"/" $HELPERSDIR/_config.py-DD

    echo "Importing test data and setting up configuration"
    cd "$HELPERSDIR"
    /usr/bin/pipenv run ./import_initial_data.py
    /usr/bin/pipenv run ./_jira_creds.py-DD
    # need to turn some flags in global settings
}

[[ -z "$1" ]] && echo "Please pass in an upstream PR number"

ROOTDIR=$HOME/gitrepos/madchap_ddojo
HELPERSDIR=$HOME/gitrepos/dojo-helpers
cd "$ROOTDIR"

clean_current_env
hub pr checkout "${1}" "test-${1}"
new_pr_env

# enable ngrok for webhook?

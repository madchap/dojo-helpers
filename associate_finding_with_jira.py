from jira import JIRA, exceptions
import _jira_creds
import _config
import dojo
import re
import argparse
import sys


def associate(action):
    link_dict = {
        "jira_id": issue.id,
        "jira_key": issue.key,
        "finding": finding_to_link,
    }

    if action == "patch":
        print("Looking if an association already exists, and patch.")
        return dojo_client.patch_data('jira_finding_mappings', finding_to_link, link_dict)
    elif action == "create":
        print("Creating new association.")
        return dojo_client.post_create_data('jira_finding_mappings', link_dict)

def delete(former_id):
    print(f"Deleting association for jira_id {former_id}")
    return dojo_client.delete_data('jira_finding_mappings', former_id)

def find_former_association():
    print("Identifying former association")
    json_results = dojo_client.get_all_data('jira_finding_mappings')

    for result in json_results:
        if result['finding'] == finding_to_link:
            print(f"Found {result}")
            return result['id']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create or associate a JIRA to an existing finding.')
    parser.add_argument('jirakey', type=str, help='Example: JIRA-1234')
    parser.add_argument('finding', type=int, help='DefectDojo finding ID')
    args = parser.parse_args()
    
    dojo_client = dojo.DojoClient(base_url=_config.dd_api_url, api_key=_config.dd_token)

    finding_to_link = args.finding
    issue_key = args.jirakey

    try:
        jira = JIRA(server=_jira_creds.url, basic_auth=(_jira_creds.username, _jira_creds.token))
        issue = jira.issue(issue_key)
    except exceptions.JIRAError as e:
        print(e)
        sys.exit(1)

    print(f"JIRA KEY: {issue.key}")
    print(f"JIRA ID: {issue.id}")

    if associate("patch") >= 400:
        # patching only works if the finding is not already associated with a jira key... :/
        if associate("create") >= 400:
            # create will fail if the finding is already associated to a different jira key...
            # in this case, delete to re-create
            # TODO: pending merge https://github.com/DefectDojo/django-DefectDojo/pull/2138
            if delete(find_former_association()) < 400:
                associate("create")

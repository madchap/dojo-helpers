import dojo
import _jira_creds


def create_jira_config():

    jira_url = "https://defectdojo.atlassian.net"
    config = {
        "configuration_name": "DefectDojo test site",
        "url": jira_url,
        "username": _jira_creds.username,
        "password": _jira_creds.password,
        "epic_name_id": "10011",
        "open_status_key": "11",
        "close_status_key": "41",
        "info_mapping_severity": "Info",
        "low_mapping_severity": "Low",
        "medium_mapping_severity": "Medium",
        "high_mapping_severity": "High",
        "critical_mapping_severity": "Critical",
    }

    if not dd_client.exists_jira_url(jira_url):
        dd_client.post_create_data('jira_configurations', config)


if __name__ == "__main__":
    dd_api_url = "http://localhost:8080/api/v2"
    dd_token = open('token', 'r').readline().strip()

    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    if dd_client.is_dojo_up():
        create_jira_config()
import dojo
import _jira_creds
import _config


def create_jira_config():

    jira_url = _config.jira_url
    config = {
        "configuration_name": "DefectDojo test site",
        "url": jira_url,
        "username": _jira_creds.username,
        "password": _jira_creds.token,
        "epic_name_id": "10011",
        "open_status_key": "11",
        "close_status_key": "41",
        "info_mapping_severity": "Lowest",
        "low_mapping_severity": "Low",
        "medium_mapping_severity": "Medium",
        "high_mapping_severity": "High",
        "critical_mapping_severity": "Highest",
    }

    if not dd_client.exists_jira_url(jira_url):
        dd_client.post_create_data('jira_configurations', config)


if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token

    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    if dd_client.check_valid_token() and dd_client.is_dojo_up():
        create_jira_config()

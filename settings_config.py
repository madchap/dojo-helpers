import dojo
import _config


def update_settings():

    config = {
        "enable_auditlog": "false",
        "enable_deduplication": "true",
        "enable_jira": "true",
    }
    dd_client.patch_data('system_settings', dd_entity_id=1, info_dict=config)


if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token

    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    if dd_client.check_valid_token() and dd_client.is_dojo_up():
        update_settings()

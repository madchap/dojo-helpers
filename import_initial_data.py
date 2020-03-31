import dojo
import _config
from datetime import date
from datetime import timedelta
import random
import string
import io
import os
from pathlib import Path
from distutils.util import strtobool


def create_test_product():

    product_config = {
        "name": "Auto {}".format(''.join(random.sample(string.ascii_lowercase, 10))),
        "description":  "Test created automatically",
        "prod_type": 1,
    }

    return dd_client.post_create_data('products', product_config)

def create_test_engagement(product_id):
    engagement_config = {
        "name": "Test engagement",
        "target_start": target_start,
        "target_end": target_end,
        "product": product_id,
        "active": True
    }

    return dd_client.post_create_data('engagements', engagement_config)

def create_test_test(engagement_id, test_type):
    test_config = {
        "name": "Test test",
        "target_start": test_target_start,
        "target_end": test_target_end,
        "engagement": engagement_id,
        "test_type": test_type,
    }

    return dd_client.post_create_data('tests', test_config)

def import_scan_in_test(engagement_id, scan_type, scan_report):
    with open(scan_report, "rb") as f:
        file_data = f.read()

    import_data = {
        "scan_type": scan_type,
        "engagement": engagement_id,
    }

    dd_client.import_report(file_data, import_data)

def enable_product_for_jira(product_id):
    product_jira_config = {
        "project_key": _config.jira_project,
        "push_all_issues": True,
        "enable_engagement_epic_mapping": False,
        "push_notes": True,
        "product": product_id,
        "conf": 1  # should only have 1 jira conf here
    }

    dd_client.post_create_data('jira_product_configurations', product_jira_config)


if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = open('token', 'r').readline().strip()
    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    start = date.today()
    end = start + timedelta(days=7)
    # used for engagement...
    target_start = start.isoformat()
    target_end = end.isoformat()
    # used for tests...
    test_target_start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    test_target_end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    if dd_client.is_dojo_up():
        # create a product
        product_id = create_test_product()

        # if config says so, enable jira, push all issues for product
        if strtobool(_config.enable_jira_for_product):
            enable_product_for_jira(product_id)
        
        # create an engagement
        engagement_id = create_test_engagement(product_id)

        # create a test
        # test_id = create_test_test(engagement_id, 101)  # anchore
         
        # import scans in test
        # Loop over each subdirectories, each having to be named per the scanner name in factory.py
        reports_directories = rf'{_config.reports_directory}'
        for scanner_directory in os.scandir(reports_directories):
            for filename in os.scandir(scanner_directory.path):
                if filename.is_file():
                    import_scan_in_test(engagement_id, scanner_directory.name, Path(filename).absolute())
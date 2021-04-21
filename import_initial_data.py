import dojo
import _config
from datetime import date
from datetime import timedelta
import random
import string
import os
from pathlib import Path
from distutils.util import strtobool
import re


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
        "active": True,
        "engagement_type": "CI/CD",

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
        tags_array = [scan_report.stem]

    import_data = {
        "scan_type": scan_type,
        "engagement": engagement_id,
        "tags": tags_array,
        "active": True,
        "verified": False
    }

    dd_client.import_report(file_data, import_data)

def enable_product_for_jira(product_id):
    product_jira_config = {
        "project_key": _config.jira_project,
        "push_all_issues": False,
        "enable_engagement_epic_mapping": False,
        "push_notes": False,
        "product": product_id,
        "jira_instance": 1,  # should only have 1 jira conf here
        "risk_acceptance_expiration_notification": True,
        "product_jira_sla_notification": True
    }

    dd_client.post_create_data('jira_product_configurations', product_jira_config)

def get_files_from_directory(directory):
    try:
        for element in os.scandir(directory):
            if element.is_dir():
                # skip directory starting with underscore
                if re.search("^_.*", directory.name):
                    return []
            get_files_from_directory(element)
            if element.is_file():
                filenames.append(element)
    except NotADirectoryError as e:
        pass

    return filenames


if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token
    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    start = date.today()
    end = start + timedelta(days=7)
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
        # increase the range to loop over many times..
        for x in range(0, 1):
            target_start = (start - timedelta(days=random.randint(20, 100))).isoformat()
            target_end = end.isoformat()
            engagement_id = create_test_engagement(product_id)

            # import scans in test
            # Loop over each subdirectories, each having to be named per the scanner name in factory.py
            # if directory starts with an underscore, skip it
            reports_directories = rf'{_config.reports_directory}'
            for scanner_directory in os.scandir(reports_directories):
                filenames = []
                files = get_files_from_directory(scanner_directory)
                for filename in sorted(files, key=lambda e: e.name):
                    import_scan_in_test(engagement_id, Path(filename).absolute().parent.name, Path(filename).absolute())

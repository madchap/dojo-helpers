import dojo
from datetime import date
from datetime import timedelta
import random
import string
import io

def create_test_product():

    product_config = {
        "name": "Auto {}".format(''.join(random.sample(string.ascii_lowercase, 10))),
        "description":  "Test created automatically",
    }

    return dd_client.post_create_data('products', product_config)

def create_test_engagement(product_id):
    engagement_config = {
        "name": "Test engagement",
        "target_start": target_start,
        "target_end": target_end,
        "product": product_id,
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


if __name__ == "__main__":
    dd_api_url = "http://localhost:8080/api/v2"
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

    scan_test_dict = {
        "101", "Anchore Engine Scan",
    }

    if dd_client.is_dojo_up():
        # create a product
        product_id = create_test_product()
        
        # create an engagement
        engagement_id = create_test_engagement(product_id)

        # create a test
        # test_id = create_test_test(engagement_id, 101)  # anchore
         
        # import scans in test
        import_scan_in_test(engagement_id, 'Anchore Engine Scan',
            ".json")

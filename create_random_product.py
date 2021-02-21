import dojo
import _config
import os
import random
import string


def create_random_product():
    product_config = {
        "name": "Auto {}".format(''.join(random.sample(string.ascii_lowercase, 10))),
        "description":  "Test created automatically",
        "prod_type": 1,
    }

    return dd_client.post_create_data('products', product_config)

if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token
    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    if dd_client.is_dojo_up():
        create_random_product()

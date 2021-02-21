import dojo
import _config


def patch_product(id):
    product_config = {
        "id": id,
        "enable_simple_risk_acceptance": False,
    }

    return dd_client.patch_data('products', id, product_config)


def patch_jira_config(id):
    jira_config = {
        "id": id,
        "risk_acceptance_expiration_notification": True,
    }

    return dd_client.patch_data('jira_product_configurations', id, jira_config)


def get_products():
    products = dd_client.get_all_data('products')
    product_ids = []
    for product in products:
        product_ids.append(product.get('id'))

    return product_ids


def get_jira_product_configs():
    results = dd_client.get_all_data('jira_product_configurations')
    results_ids = []
    for result in results:
        results_ids.append(result.get('id'))

    return results_ids


if __name__ == "__main__":
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token
    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    if dd_client.is_dojo_up():
        # for id in get_products():
        #    patch_product(id)
        for id in get_jira_product_configs():
            patch_jira_config(id)

import dojo
import _config
import os


def get_engagements(product_id):
    engagements = dd_client.get_all_data('engagements')
    for e in engagements:
        if e['product'] == product_id:
            print(e['name'])
            rename_engagement(e['id'], e['name'])

def rename_engagement(eng_id, former_name):
    data = {
        "name": f"whatever-man/{former_name}",
        "product": product_id
    }
    dd_client.patch_data('engagements', eng_id, data)


if __name__ == "__main__":
    """
    Rename all engagements within a product with a certain prefix
    or just change the data dict with what you want
    """
    dd_api_url = _config.dd_api_url
    dd_token = _config.dd_token
    dd_client = dojo.DojoClient(base_url=dd_api_url, api_key=dd_token)

    product_id = 40
    if dd_client.is_dojo_up():
        engagements_list = get_engagements(product_id)
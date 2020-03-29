import requests

class DojoClient:
    def __init__(self, base_url: str, api_key: str):
        self._headers = {'content-type': 'application/json', 'accept': 'application/json',
                         'authorization': 'token ' + api_key}
        self._base_url = base_url
        self._api_key = api_key

    def is_dojo_up(self):
        url = f'{self._base_url}'
        r = requests.get(url)
        if r.status_code > 400:
            print(r.status_code)
            print("The DefectDojo instance appears to be down.")
            return False
        else:
            return True

    def get_findings(self, engagement_id: int):
        findings = []
        url = f'{self._base_url}/findings/?test__engagement={engagement_id}'
        page = 1
        while url is not None:
            print(f"Page {page} for findings in engagement {engagement_id}")
            page += 1
            with requests.get(url, headers=self._headers) as r:
                body = r.json()
            findings.extend(body.get('results', []))
            url = body.get('next')
        return findings

    def patch_finding_status(self, finding_id, finding_status_info: dict):
        url = f'{self._base_url}/findings/{finding_id}/'
        r = requests.patch(url, json=finding_status_info, headers=self._headers)
        print(r.text)
        return r.status_code
    
    def exists_jira_url(self, jira_config_url):
        url = f'{self._base_url}/jira_configurations/'
        r = requests.get(url, json=jira_config_url, headers=self._headers)
        if r.json().get('count') == 0:
            return False
        else:
            print(f"JIRA configuration for url {jira_config_url} already exists.")
            return True

    def post_create_data(self, endpoint, data_dict: dict):
        """ returns the ID of the entity created """
        url = f'{self._base_url}/{endpoint}/'
        r = requests.post(url, json=data_dict, headers=self._headers)
        print(r.text)
        return r.json().get('id')

    def get_data(self, endpoint, entity_id: int) -> dict:
        """ returns a json """
        url = f'{self._base_url}/{endpoint}/{entity_id}'
        r = requests.get(url, headers=self._headers)
        return r.json()

    def delete_data(self, endpoint, entity_id: int) -> dict:
        """ returns a json """
        url = f'{self._base_url}/{endpoint}/{entity_id}'
        r = requests.delete(url, headers=self._headers)
        return r.json()
    
    def import_report(self, file_data, data_dict: dict):
        import_headers = {'authorization': 'token ' + self._api_key}
        url = f'{self._base_url}/import-scan/'
        r = requests.post(url, data=data_dict, files={"file": file_data}, headers=import_headers)
        print(r.text)
        return r.status_code
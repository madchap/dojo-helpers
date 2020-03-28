import requests

class DojoClient:
    def __init__(self, base_url: str, api_key: str):
        self._headers = {'content-type': 'application/json', 'accept': 'application/json',
                         'authorization': 'token ' + api_key}
        self._base_url = base_url

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

    def get_finding(self, finding_id: int):
        url = f'{self._base_url}/findings/{finding_id}/'
        with requests.get(url, headers=self._headers) as r:
            return r.json()

    def get_note(self, note_id):
        url = f'{self._base_url}/notes/{note_id}'
        r = requests.get(url, headers=self._headers)
        print(f"Note get result: {str(r.status_code)}")
        return r.json()

    def patch_finding_status(self, finding_id, finding_status_info: dict):
        url = f'{self._base_url}/findings/{finding_id}/'
        r = requests.patch(url, json=finding_status_info, headers=self._headers)
        print(r.text)
        return r.status_code
    
    def create_jira_config(self, jira_config: dict):
        url = f'{self._base_url}/jira_configurations/'
        r = requests.post(url, json=jira_config, headers=self._headers)
        print(r.text)
        return r.status_code

    def exists_jira_url(self, jira_config_url):
        url = f'{self._base_url}/jira_configurations/'
        r = requests.get(url, json=jira_config_url, headers=self._headers)
        if r.json().get('count') == 0:
            return False
        else:
            return True


    
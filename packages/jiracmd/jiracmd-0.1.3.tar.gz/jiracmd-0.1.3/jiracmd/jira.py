import os
import requests
import base64
from getpass import getpass
from urllib.parse import urlencode
from jiracmd.objects import Worklog


class JiraAPIClient():
    def __init__(self):
        server, username, token = self._authenticate()
        self.base_url = f"https://{server}/rest/api"
        self.api_version = 3
        self.headers = self._generate_header(username, token)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _authenticate(self):
        var_list = ['JIRA_SERVER', 'JIRA_USERNAME', 'JIRA_API_TOKEN']
        for env_var in var_list:
            if not os.getenv(env_var):
                print(f'Check your environment variables: {var_list}')
                exit(1)

        return (
            os.getenv('JIRA_SERVER'),
            os.getenv('JIRA_USERNAME'),
            os.getenv('JIRA_API_TOKEN')
        )

    def _generate_header(self, username, token):
        auth_bytes = f"{username}:{token}".encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        return {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }

    def _get_endpoint(self, suffix, api_version=3):
        endpoint = f"{self.base_url}/{api_version}/{suffix}"
        return endpoint

    def _get(self, call, api_version=3, **kwargs):
        endpoint = self._get_endpoint(call, api_version=api_version) 
        return self.session.get(endpoint)

    def _post(self, call, body, **kwargs):
        endpoint = self._get_endpoint(call)
        return self.session.post(endpoint, data=body)

    def _delete(self, call, **kwargs):
        endpoint = self._get_endpoint(call) 
        return self.session.delete(endpoint)

    def get_issue(self, issue, params=[], api_version=2):
        call = f"issue/{issue}"
        if params:
            encoded_params = "?" + "&".join([urlencode(p) for p in params])
            call += encoded_params
        return self._get(call, api_version=api_version).json()
    
    def get_issue_worklogs(self, issue):
        response = self._get(f'issue/{issue}/worklog').json()['worklogs']
        worklog_list = [Worklog(issue_key=issue, **w) for w in response]
        return worklog_list
         
    def validate_worklog(self, issue, start):
        worklogs = self.get_issue_worklogs(issue)
        for w in worklogs:
            started = w.started
            if started == start:
                return f"duplicated_start_time {w}"
                # if w.timeSpentSeconds == seconds:
        return "ok"



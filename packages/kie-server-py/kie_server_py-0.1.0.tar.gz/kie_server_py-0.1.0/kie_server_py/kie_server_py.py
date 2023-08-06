import requests
import json

from requests import Response
from requests.auth import HTTPBasicAuth


class KIEServerBaseAdapter:
    def __init__(
        self,
        host: str,
        port: str,
        auth_username: str,
        auth_password: str,
        headers: dict = None
    ):
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        self.host = host
        self.port = port
        self.auth_username = auth_username
        self.auth_password = auth_password
        self.base_url = self.host + ":" + self.port
        self.headers = headers

    def execute_dmn(
        self,
        container_name: str,
        model_namespace: str,
        model_name: str,
        dmn_context: dict,
        timeout: float = 1,
    ) -> Response:
        url = (
            self.base_url
            + "/kie-server/services/rest/server/containers/"
            + container_name
            + "/dmn"
        )
        payload = json.dumps(
            {
                "model-namespace": model_namespace,
                "model-name": model_name,
                "dmn-context": dmn_context,
            }
        )
        response: Response = requests.post(
            url=url,
            headers=self.headers,
            data=payload,
            auth=HTTPBasicAuth(self.auth_username, self.auth_password),
            timeout=timeout,
        )
        return response

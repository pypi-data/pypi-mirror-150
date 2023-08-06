import logging.config
import requests
from infoworks.core.iw_authentication import is_token_valid, get_bearer_token
from infoworks.sdk import local_configurations
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = local_configurations.REQUEST_TIMEOUT_IN_SEC
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def initialise_http_client():
    retries = Retry(total=local_configurations.MAX_RETRIES, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    http = requests.Session()
    adapter = TimeoutHTTPAdapter(max_retries=retries)
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


class BaseClient(object):
    client_config = {
        'protocol': None,
        'ip': None,
        'port': None,
        'refresh_token': None,
        'bearer_token': None
    }

    def __init__(self):
        self.http = initialise_http_client()
        logging.basicConfig(filename=local_configurations.LOG_LOCATION, filemode='w',
                            format='%(asctime)s - %(module)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s',
                            level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('infoworks_sdk_logs')

    def initialize_client(self, protocol=None, ip=None, port=None, ):
        """
        initialize the client
        :param protocol: protocol to be used for server call
        :type protocol: String
        :param ip: Client IP
        :type ip: String
        :param port: Client Port
        :type port: String
        """

        if all(v is not None for v in [protocol, ip, port]):
            self.client_config['protocol'] = protocol
            self.client_config['ip'] = ip
            self.client_config['port'] = port
        else:
            logging.error(ValueError("Pass valid values"))
            raise ValueError("Pass valid values")

    def initialize_client_with_user(self, protocol, ip, port, refresh_token):
        """
        initializes the client and a user with given configuration
        :param protocol: protocol to be used for server call
        :type protocol: String
        :param ip: ip address of the server
        :type ip: String
        :param port: port on which the rest service resides
        :type port: String
        :param refresh_token: refresh_token of the user
        :type refresh_token: String
        """
        self.client_config['refresh_token'] = refresh_token
        self.client_config['bearer_token'] = get_bearer_token(protocol, ip, port, refresh_token)
        self.initialize_client(protocol, ip, port)

    def get_configurations(self):
        """
        returns client configurations
        :return: configuration dictionary
        """
        return self.client_config

    def regenerate_bearer_token_if_needed(self):
        if not is_token_valid(self.client_config, self.http):
            self.client_config['bearer_token'] = get_bearer_token(protocol=self.client_config["protocol"],
                                                                  ip=self.client_config["ip"],
                                                                  port=self.client_config["port"],
                                                                  refresh_token=self.client_config["refresh_token"])

    def call_api(self, method, url, headers, data=None):
        self.regenerate_bearer_token_if_needed()
        if method.upper() == "GET":
            self.logger.info(f"Calling {url}")
            response = self.http.get(url, headers=headers, timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                     verify=False)
            if response.status_code == "406":
                self.regenerate_bearer_token_if_needed()
                return self.http.get(url, headers=headers, timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                     verify=False)
            else:
                return response
        elif method.upper() == "POST":
            self.logger.info(f"Calling {url}")
            response = self.http.post(url, headers=headers, json=data,
                                      timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            if response.status_code == "406":
                self.regenerate_bearer_token_if_needed()
                return self.http.post(url, headers=headers, json=data,
                                      timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            else:
                return response
        elif method.upper() == "PUT":
            self.logger.info(f"Calling {url}")
            response = self.http.put(url, headers=headers, json=data,
                                     timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            if response.status_code == "406":
                self.regenerate_bearer_token_if_needed()
                return self.http.put(url, headers=headers, json=data,
                                     timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            else:
                return response
        elif method.upper() == "PATCH":
            self.logger.info(f"Calling {url}")
            response = self.http.patch(url, headers=headers, json=data,
                                       timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            if response.status_code == "406":
                self.regenerate_bearer_token_if_needed()
                return self.http.put(url, headers=headers, json=data,
                                     timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
            else:
                return response
        elif method.upper() == "DELETE":
            self.logger.info(f"Calling {url}")
            response = self.http.delete(url, headers=headers, timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                        verify=False)
            if response.status_code == "406":
                self.regenerate_bearer_token_if_needed()
                return self.http.delete(url, headers=headers, timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                        verify=False)
            else:
                return response

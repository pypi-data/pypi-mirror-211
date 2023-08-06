import base64
import ipaddress
import json
import re
import socket
import time
from datetime import datetime, date
from http import HTTPStatus
from json import JSONDecodeError
from typing import Union
from urllib.parse import urljoin, urlencode

import requests
from plogger import logger
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)


class RESTAssertion:
    """Parse requests response to get status code."""

    @staticmethod
    def is_success(response) -> bool:
        """200 <= status_code < 400"""
        return response.ok

    @staticmethod
    def is_ok(response) -> bool:
        """OK, 200. Request fulfilled, document follows"""
        return response.status_code == HTTPStatus.OK

    @staticmethod
    def is_not_found(response) -> bool:
        """Nothing matches the given URI. 404"""

        return response.status_code == HTTPStatus.NOT_FOUND

    @staticmethod
    def is_bad_request(response) -> bool:
        """Bad request syntax or unsupported method. 400"""
        return response.status_code == HTTPStatus.BAD_REQUEST

    @staticmethod
    def is_unauthorized(response) -> bool:
        """Bad request syntax or unsupported method. 401"""
        return response.status_code == HTTPStatus.UNAUTHORIZED


# noinspection PyPep8Naming
class RESTClient(RESTAssertion):
    """ Main class for RestAPI """

    def __init__(self,
                 protocol: str = 'https',
                 host: str = None,
                 port: int = 0,
                 username: str = None,
                 password: str = None,
                 header: dict = None,
                 auth_basic: bool = False,
                 auth_uri: str = '',
                 auth_key: str = 'token',
                 auth_payload: dict = None,
                 connect_timeout: int = 5,
                 read_timeout: int = 60,
                 log_enabled: bool = True,
                 log_level: str = 'INFO'):

        # Enable/disable logger
        self.logger = logger('RESTClient', enabled=log_enabled, level=log_level)

        # Credentials and settings for api url
        self.username = username
        self.password = password
        self.protocol = protocol  # HTTP or HTTPS
        self.host = host if host is not None else '127.0.0.1'
        self.port = port
        self.auth_uri = auth_uri
        self.auth_key = auth_key
        self.auth_payload = auth_payload
        self.auth_basic = auth_basic
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.header = header or get_header_default()  # Default header

    def __str__(self):
        msg_print = (f'Username: {self.username}\n'
                     f'Password: {self.password}\n'
                     f'Base URL: {self.base_url}\n')

        return msg_print

    @property
    def base_url(self):
        """Create tested URL. Add port if it provided"""

        base_url = f'{self.protocol}://{self.host}:{self.port}' if self.port else f'{self.protocol}://{self.host}'

        return base_url

    def requested_url(self, url) -> str:
        """Return full URL if link specified starts with <http>"""

        try:
            requested_url = url if url.startswith('http') else urljoin(self.base_url, url)
        except Exception as err:
            self.logger.exception(f'URL does not specified. Used: "{url}" only. Specify full URL or use constructor')
            raise err

        return requested_url

    @property
    def auth_url(self):
        """Get full authorization URL"""

        return urljoin(self.base_url, self.auth_uri)

    @staticmethod
    def _validate_url(url):
        return re.match(r'https?://[\w/.]+', url)

    def encode_to_base64(self, string: str) -> str:
        """Encode string to base64. Do not use it during creating class instance (logger won't work)

        Args:
            string: Some text to encode.

        Returns:
            Base64 encoded string.
        """

        try:
            str_text = string.encode()
            base64_encoded = base64.b64encode(str_text)
        except AttributeError as err:
            self.logger.error(f'Cannot encode specific data ({string}, {type(string)})')
            raise err

        result = base64_encoded.decode()
        return result

    def get_token(self):
        """Get token.

        - Send request to auth URL
        - Get dict
        - Get specific key

        :return:
        """

        self.logger.debug(f'-> Get auth token by "{self.auth_key}"')

        response_json = None
        payload = self.auth_payload
        timeout = (self.connect_timeout, self.read_timeout)
        params = {
            'url': self.auth_url,
            'json': payload,
            'verify': False,
            'timeout': timeout,
        }

        self.logger.debug(f'Body: {dict_to_log(params)}')

        try:
            response = requests.post(**params)

            resp_to_log = f'{response.status_code}: {dict_to_log(response.json())}'
            self.logger.debug(resp_to_log)

            response_json = response.json()
            return response_json[self.auth_key]
        except KeyError as err:
            self.logger.exception(f'Cannot get key (token) from json data:{dict_to_log(response_json)}')
            raise err
        except json.decoder.JSONDecodeError as err:
            msg = f'Cannot get token property. URL: {self.auth_url} ({self.auth_payload})'
            self.logger.exception(msg)
            raise err
        except TypeError as err:
            self.logger.exception('Endpoint is available but "token" key cannot be retrieved.')
            raise err
        except requests.exceptions.ConnectTimeout as err:
            self.logger.exception(f'Perhaps, URI ({self.auth_url}) or service is unreachable:\n\t{err}')
            raise err

    def get_auth_header(self, header: dict = '') -> dict:
        """Get auth header with a token

        :param header: custom header is needed
        :return:
        """

        self.logger.debug('Get auth header with a token')

        try:
            self.header = header.copy()
        except AttributeError:
            self.header = get_header_default()

        # if 'Authorization' in self.header:
        #     self.logger.debug('Header already contains "Authorization"')
        #     return self.header
        # else:
        #     self.logger.debug('Try to get token to header')

        try:
            # noinspection PyAttributeOutsideInit
            self.token = self.get_token()
            self.header['Authorization'] = self.token

            self.logger.debug(self.header)

            return self.header
        except KeyError as err:
            self.logger.error(f'Cannot get token: {err}')
            raise err

    def _auth_basic(self):
        """Enable basic auth if provided"""

        self.header = {}
        return self.username, self.password

    def send_request(self,
                     method: str,
                     url: str,
                     data: dict = None,
                     files=None,
                     query_params: dict = None,
                     verify: bool = False,
                     custom_header: dict = None,
                     cookies=None,
                     read_timeout: int = None):
        """Send common REST request

        To upload file use:

        with open(files, 'rb') as f:
             files = {'licenseFile': (License.name, f)}

        Args:
            method: GET, POST, DELETE
            url: unified identifier, self.url (BASE) + url
            data: json data
            files: "files: {'licenseFile': (License.name, f)}"
            query_params: Query parameters in the url
            cookies:
            verify: Ignore SSL verification?
            custom_header: Use specified header
            read_timeout: Read timeout in sec.

        Returns:
            requests.request('POST', url=url, headers=HEADER, files=files, verify=False)
        """

        # Get timeouts
        read_timeout_ = self.read_timeout if read_timeout is None else read_timeout
        common_timeout = self.read_timeout, read_timeout_

        # Set auth method
        if self.auth_payload is not None:
            self.header = self.get_auth_header(header=custom_header)
        elif self.auth_basic:
            self.auth_basic = self._auth_basic()

        if custom_header:
            self.header = custom_header

        # Make full url to use in request
        link = self.requested_url(url)

        # Add params to requested link
        if query_params:
            link += '?' + urlencode(query_params)

        method = method.upper()
        methods_available = 'GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS'
        assert method in methods_available, 'Specified methods is not compatible.'

        if data and files:
            self.logger.error('Data parameter cannot be used with files parameter simultaneously.')
            raise ValueError('Data parameter cannot be used with files parameter simultaneously.')

        # Extend header
        if 'Content-Type' not in self.header:
            self.header['Content-Type'] = 'application/json'

        response = 'Invalid requests. Check parameters'

        self.logger.info(f'[{method}] {link}')

        try:
            # For 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if data and not files:

                    self.logger.debug(f'Parameters:\n\t{self.header = }\n\t{cookies = }\n\t{common_timeout = }')
                    self.logger.info('PAYLOAD:\n' + json.dumps(data, indent=4))

                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=self.header,
                                                json=data,
                                                cookies=cookies,
                                                verify=verify,
                                                timeout=common_timeout)

                elif files:
                    files_header = self.header.copy()
                    del files_header['Content-Type']

                    self.logger.debug(f'{files_header = }, {cookies = }, {common_timeout = }')
                    self.logger.info('PAYLOAD:\n' + json.dumps(data, indent=4))

                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=files_header,
                                                cookies=cookies,
                                                files=files,
                                                verify=verify,
                                                timeout=common_timeout)

                elif not files and not data:
                    self.logger.debug(f'Parameters:\n\t{self.header = }\n\t{cookies = }\n\t{common_timeout = }')

                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=self.header,
                                                cookies=cookies,
                                                verify=verify,
                                                timeout=common_timeout)

            # For 'GET', 'HEAD' request
            else:
                # For usual 'GET' without query params
                self.logger.debug(f'Parameters:\n\t{self.header = }\n\t{cookies = }\n\t{common_timeout = }')

                response = requests.request(method=method,
                                            url=link,
                                            auth=self.auth_basic,
                                            cookies=cookies,
                                            headers=self.header,
                                            verify=verify,
                                            timeout=common_timeout)
        except requests.exceptions.ReadTimeout as err:
            self.logger.exception(f'The request took too long. Read timed out. (read timeout={common_timeout[1]})')
            raise err
        except BaseException as err:
            self.logger.exception('Something went wrong.')
            raise err

        self.logger.info(f'{response.status_code}: "{response.text}"')

        return response

    @property
    def is_service_available(self):
        """Check base url availability within 10 sec."""

        try:
            response = requests.get(self.base_url, timeout=10, verify=False)
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.ConnectionError:
            return False

    def download(self, url: str, dst: str):
        """Download file.

        :param url: Full url to file
        :param dst: path to store
        :return:
        """

        response = self.GET(url)
        try:
            if response.ok:
                with open(dst, 'wb') as f:
                    f.write(response.content)
                    return True
            else:
                return False
        except (ConnectionError, ConnectionRefusedError) as err:
            self.logger.exception('Download failed')
            return err

    # noinspection PyPep8Naming
    def GET(self,
            url: str = '',
            query_params: dict = None,
            cookies=None,
            read_timeout: int = None,
            header: dict = None):

        return self.send_request(method='GET',
                                 url=url,
                                 query_params=query_params,
                                 cookies=cookies,
                                 read_timeout=read_timeout,
                                 custom_header=header)

    # noinspection PyPep8Naming
    def POST(self,
             url: str = '',
             data: dict = None,
             file=None,
             query_params: dict = None,
             cookies=None,
             read_timeout: int = None,
             header: dict = None):

        return self.send_request(method='POST',
                                 url=url,
                                 query_params=query_params,
                                 data=data,
                                 files=file,
                                 cookies=cookies,
                                 read_timeout=read_timeout,
                                 custom_header=header)

    # noinspection PyPep8Naming
    def PUT(self,
            url: str = '',
            data: dict = '',
            files='',
            query_params: dict = None,
            cookies=None,
            read_timeout: int = None,
            header: dict = None):

        header_original = self.header.copy()

        if files:  # FIXME
            del header_original['Content-Type']

        return self.send_request(method='PUT',
                                 url=url,
                                 data=data,
                                 files=files,
                                 query_params=query_params,
                                 cookies=cookies,
                                 read_timeout=read_timeout,
                                 custom_header=header)

    def DELETE(self,
               url: str = '',
               data: dict = '',
               query_params: dict = None,
               cookies=None,
               read_timeout: int = None,
               header: dict = None):

        return self.send_request(method='DELETE',
                                 url=url,
                                 query_params=query_params,
                                 data=data,
                                 cookies=cookies,
                                 read_timeout=read_timeout,
                                 custom_header=header)

    def is_host_available(self, port: int = 0, timeout: int = 5) -> bool:
        """Check remote host availability using socket and specified port"""

        port_ = port or self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((self.host, port_))
            return False if result else True

    def is_service_initialized(self, timeout: Union[int, float] = 20) -> bool:
        """Send GET to base URL https://{IP}:{PORT}

        :param timeout:
        :return:
        """

        try:
            response = requests.get(self.base_url, verify=False, timeout=timeout)
            return response.ok
        except requests.exceptions.ConnectionError:
            return False

    def wait_service_start(self, timeout: int = 30, interval: int = 3) -> bool:
        """Waiting for the service start.

        :param timeout: in sec.
        :param interval: in sec.
        :return:
        """

        timer = 0
        status = self.is_service_initialized(1)

        while not status:
            status = self.is_service_initialized(1)
            timer += interval

            if timer > timeout - 2:
                raise TimeoutError(f'The service was not started within {timeout} seconds.')
            time.sleep(interval)
        return status


def get_header_default(user_agent='ide', content_type='application/json-patch+json', accept='application/json'):
    return {
        'User-Agent': user_agent,
        'Content-Type': content_type,
        'Accept': accept,
        # 'UserAgentInternal': 'webfrontend/1.0'
    }


def dict_to_log(data: dict | list, sort: bool = False, ensure_ascii: bool = False) -> str:
    """Pretty dict data to log"""

    def convert_data_to_log(obj):
        """Convert datetime, IPv4Address, requests Response...

        :param obj: Object to convert
        :return:
        """

        from requests.models import Response
        from io import BufferedReader

        match obj:
            # IP address object handler
            case ipaddress.IPv4Address() | set():
                return obj.__str__()
            # Datetime handler
            case datetime() | date():
                return obj.isoformat()
            # REST response handler
            case Response():
                try:
                    response_json_data = obj.json()
                except JSONDecodeError:
                    response_json_data = None

                msg = {
                    'ok': obj.ok,
                    'response_code': obj.status_code,
                    'text': obj.text,
                    'json': response_json_data,
                    'reason': obj.reason,
                    'url': obj.url,
                }
                return msg
            # Stream object handler
            case BufferedReader():
                return f'[BufferedReader] {obj.name}'
            # case _:
            # logger.debug('No data types detected to convert. Pass data directly.')
            # return obj

    json_data = json.dumps(obj=data, sort_keys=sort, ensure_ascii=ensure_ascii, indent=4, default=convert_data_to_log)

    return f'\n{json_data}'

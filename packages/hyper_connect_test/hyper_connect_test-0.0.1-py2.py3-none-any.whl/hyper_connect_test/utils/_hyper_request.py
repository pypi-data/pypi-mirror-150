from typing import Any, Dict, Optional
from urllib.parse import urlencode, urlparse

from ramda import is_empty

from hyper_connect_test.types import (
    Action,
    HyperRequest,
    HyperRequestParams,
    Method,
    RequestOptions,
    ServiceType,
)

from ._generate_token import decode_token, generate_token
from ._get_host import get_host
from ._get_key import get_key
from ._get_secret import get_secret

# from datetime import datetime, timezone

# from promisio import promisify

# TODO: DELETE THIS FN
# Python program to illustrate functions
# Functions can return another function

# def create_adder(x):
#     def adder(y):
#         return x + y
#     return adder


def hyper(connection_string: str, domain: str):
    async def create_hyper_request(req_params: HyperRequest) -> HyperRequestParams:
        parsed_url = urlparse(connection_string)
        is_cloud: bool
        protocol: str
        public_key: Optional[str]
        secret: Optional[str]
        token: str
        host: Optional[str]
        pathname: str
        service: str
        appdomain: str
        params: Optional[str]
        url: str
        resource: Optional[str]
        action: Optional[Action]

        if parsed_url.scheme == "cloud":
            is_cloud = True
            protocol = "https:"
        else:
            is_cloud = False
            protocol = f"{parsed_url.scheme}:"

        # print("is_cloud {0:} protocol {1:}".format(is_cloud, protocol))

        # If you’d like to add HTTP headers to a request, simply pass in a dict to the headers parameter.
        # For example, we didn’t specify our user-agent in the previous example:

        # url = 'https://api.github.com/some/endpoint'
        # headers = {'user-agent': 'my-app/0.0.1'}
        # r = requests.get(url, headers=headers)
        headers: Dict[str, str] = {"Content-Type": "application/json"}

        # Get key and secret from connection_string

        # print(f"netloc: {parsed_url.netloc}")

        # print(f"netloc2: {urlparse('https://api.github.com/some/endpoint').netloc}")

        public_key = get_key(parsed_url.netloc)
        secret = get_secret(parsed_url.netloc)

        if public_key is not None and secret is not None:
            # print('I am the key master')

            token = generate_token(public_key, secret)
            # print('minty fresh token: ' + token)

            # decoded_token: Dict[str, Any] = decode_token(token, secret)
            # print('decoded_token below')
            # print(decoded_token)
            # print('exp: ', decoded_token["exp"])
            # print(datetime.fromtimestamp(decoded_token["exp"], timezone.utc))

            headers["Authorization"] = f"Bearer {token}"

            # print(headers)

        host = get_host(parsed_url.netloc)

        if is_cloud == True:
            pathname = parsed_url.path
            appdomain = f"/{domain}"
        else:
            pathname = ""
            appdomain = parsed_url.path

        service = req_params["service"]

        if req_params["service"] == "info":
            url = f"{protocol}//{host}"
        else:
            url = f"{protocol}//{host}{pathname}/{service}{appdomain}"

        resource = req_params["resource"]
        action = req_params["action"]
        if resource is not None:
            url = f"{url}/{resource}"
        elif action is not None:

            url = f"{url}/{action}"

        if req_params["params"] is not None:
            # Convert a mapping object or a sequence of two-element tuples,
            # which may contain str or bytes objects, to a percent-encoded ASCII text string.
            params = urlencode(req_params["params"])
            url = f"{url}?{params}"

        requestOptions = RequestOptions(
            {
                "headers": headers,
                "method": req_params["method"],
                "body": req_params["body"],
            }
        )

        hyperRequestParams = HyperRequestParams({"url": url, "options": requestOptions})

        return hyperRequestParams

    return create_hyper_request

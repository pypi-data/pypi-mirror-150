from typing import Any, Dict, Optional, TypedDict

import requests
from promisio import promisify

from hyper_connect_test.types import HyperRequest, HyperRequestParams
from hyper_connect_test.utils import create_hyper_request_params


@promisify
def addData(body: Any, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "POST",
        "body": body,
        "resource": None,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    # Example HyperRequestParams
    # {
    #     'url': 'https://cloud.hyper.io/express-quickstart/data/default',
    #     'options': {
    #         'headers': {
    #             'Content-Type': 'application/json',
    #             'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bWd0YTBudW02ajduNnVuN2FhNm91Z2EyNnZxbjc4NCIsImV4cCI6MTY1MTc2NTAwMX0.ChZqjXFOJDYFgsHMFHLTk_iIRR-qW1BfRutJxMObvqE'
    #             },
    #         'method': 'GET',
    #         'body': 'foo bar'
    #     }
    # }
    # print('inside _data.py addData() hyperRequestParams dict')

    # for k, v in hyperRequestParams.items():
    #     print(k, v)

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.post(url, headers=headers, data=body)


@promisify
def getData(id: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "GET",
        "body": None,
        "resource": id,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    # Example HyperRequestParams
    # {
    #     'url': 'https://cloud.hyper.io/express-quickstart/data/default',
    #     'options': {
    #         'headers': {
    #             'Content-Type': 'application/json',
    #             'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bWd0YTBudW02ajduNnVuN2FhNm91Z2EyNnZxbjc4NCIsImV4cCI6MTY1MTc2NTAwMX0.ChZqjXFOJDYFgsHMFHLTk_iIRR-qW1BfRutJxMObvqE'
    #             },
    #         'method': 'GET',
    #         'body': 'foo bar'
    #     }
    # }
    # print('inside _data.py addData() hyperRequestParams dict')

    # for k, v in hyperRequestParams.items():
    #     print(k, v)

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)

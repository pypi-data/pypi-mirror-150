from typing import Any

# from ._cache import addCacheDoc
from hyper_connect_test.services import addData, getData
from hyper_connect_test.types import Hyper, HyperData
from hyper_connect_test.utils import handle_response

# cache = {"add": addCacheDoc}

# >>> from hyper_connect import connect
# >>> hyper = connect('cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart','default')
# >>> result = await hyper.data.add(doc)


def connect_test(CONNECTION_STRING: str, domain: str = "default") -> Hyper:
    def printIdentity(prefix):
        def print_this(x):
            print(f"{prefix} -> {x}")

        return print_this

    def addDataDoc(body: Any):
        return addData(body, CONNECTION_STRING, domain).then(handle_response)

    def getDataDoc(id: str):
        return getData(id, CONNECTION_STRING, domain).then(handle_response)

    hyperData: HyperData = HyperData(addDataDocFn=addDataDoc, getDataDocFn=getDataDoc)

    hyper: Hyper = Hyper(data=hyperData)

    # hyper = {
    #     "data": {
    #         "add": lambda body: addData(body, CONNECTION_STRING, domain).then(
    #             handle_response
    #         )
    #     }
    # }
    return hyper

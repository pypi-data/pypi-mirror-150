from hyper_connect_test import connect_test
from hyper_connect_test.types import Hyper

# >>> from sandbox import data_add, data_get
# >>> import asyncio
# >>> asyncio.run(data_add('{ "_id":"book-102","type":"book", "name":"Horton hears a who 2","author":"Dr. Suess","published":"1953" }'))

hyper: Hyper = connect_test(
    "cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart"
)


async def data_add(doc: str):

    result = await hyper.data.add(doc)

    return result


async def data_get(id: str):

    result = await hyper.data.get(id)

    return result

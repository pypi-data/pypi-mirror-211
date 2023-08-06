import requests

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_coastlines(age, model="MULLER2022"):
    """Get paleo-coastlines

    :param age: the input paleo age
    :returns: paleo-coastlines
    :rtype: geojson

    """
    headers = {
        "Accept": "application/json",
    }
    params = {"time": age, "model": model}

    ret = requests.get(
        a.server_url + "/reconstruct/coastlines/",
        params == params,
        verify=True,
        headers=headers,
        proxies={"http": a.proxy},
    )
    return ret.json()

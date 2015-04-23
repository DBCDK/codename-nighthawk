import requests


def get_fabrics(config, query_params):
    path = config["console"] + "/rest/v1/-"
    r = requests.get(path, auth=(config["username"], config["password"]))
    response = r.json() if r.ok else dict(error=r.reason)

    return r.status_code, response


def get_fabric(config, query_params, fabric=None):
    path = config["console"] + "/rest/v1/" + fabric
    r = requests.get(path, auth=(config["username"], config["password"]))
    response = r.json() if r.ok else dict(error=r.reason)

    return r.status_code, response


def glu_request(config, query_params, path=None):
    path = config["console"] + "/rest/v1/" + path
    r = requests.get(path, auth=(config["username"], config["password"]))
    response = r.json() if r.ok else dict(error=r.reason)

    return r.status_code, response


paths = {"/": get_fabrics,
         "/<path:path>": glu_request}
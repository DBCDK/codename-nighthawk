#!/usr/bin/env python3

import os
import sys
import argparse
import importlib

import yaml
from flask import Flask, request, Response, jsonify, json

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(script_dir, "modules"))


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", required=True,
                    help="configuration-file")
parser.add_argument("-d", "--debug",
                    action="store_true",
                    help="Enable debug-mode for Flask. Do not do this in production. Seriously.")
args = parser.parse_args()

with open(args.config) as f:
    config = yaml.load(f)

print(config)

modules = config.get("modules")
if modules is None:
    modules = []

loaded_modules = {}


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

endpoints = []


def forward_request(callee, mod_config):
    def wrapped_fn(**kwargs):
        status_code, result = callee(mod_config, request.args.to_dict(), **kwargs)

        transformers = {dict: jsonify,
                        list: lambda r: Response(response=json.dumps(r)),
                        str: lambda r: Response(response=r)}

        if type(result) in transformers:
            response = transformers.get(type(result))(result)
        else:
            response = Response(response=result)

        response.status_code = status_code
        return response

    return wrapped_fn


for i, mod in enumerate(modules):
    for field in ["module"]:
        if field not in mod:
            print("Error in configuration. Missing property '%s' in module number '%s'" % (field, i+1))
            exit(1)


    mod_name = mod["module"]
    mod_config = mod["config"] if "config" in mod else dict()

    if mod_name not in loaded_modules:
        print("loading %s" % mod_name)
        loaded_modules[mod_name] = importlib.import_module(mod_name)

    mod_paths = mod["paths"] if "paths" in mod else dict()

    if mod.get("mountpoint"):
        for path, fn_name in getattr(loaded_modules[mod_name], "paths").items():
            if path not in mod_paths:
                mod_paths[mod["mountpoint"] + path] = fn_name

    for path, fn_name in mod_paths.items():
        endpoints.append(path)
        try:
            if isinstance(fn_name, str):
                fn = getattr(loaded_modules[mod_name], fn_name)
            else:
                fn = fn_name
        except AttributeError:
            print("Error in configuration. Missing function '%s' in module '%s'" % (fn_name, mod["module"]))
            exit(1)
        app.add_url_rule(path, path, forward_request(fn, mod_config))


def to_link(route):
    return """<a href="%(route)s">%(route)s</a>""" % {"route": route}


@app.route("/")
def index():
    return "<br>\n".join(map(to_link, endpoints))


if __name__ == "__main__":
    app.run(debug=args.debug)
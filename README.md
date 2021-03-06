# codename-nighthawk

Running it:
* clone it
* create a virual env
* ``pip install -r requirements.txt``
* ``python3 nighthawk.py -c config.yaml``


## module requirements

Codename-Nighthawk maps URLs to functions specified in modules.
The most basic module looks like this:
```python
def dump_request(config, query_params, **kwargs):
    return 200, dict(config=config, query_params=query_params, **kwargs)

paths = {
    "/dump-request": dump_request
}
```

This function can now be mapped to an URL in two ways:
* implicit mapping, utilizing the paths-attribute of a module (see mountpoint config-option)
* explicit mapping (see paths config-option)

arguments:
* config: the config-part of a module-configuration is passed as first argument
* query_params: contains query parameters. Multiple arguments with same name is unsupported (e.g. ?foo=1&foo=2).
* **kwargs: placeholders from paths will appear here.


## configuration format
```yaml
modules:
- module: debug
  paths:
    "/debug": dump_request
    "/debug/<foo>": dump_request
  mountpoint: /debug/2
  config:
    hello: world
    alist:
      - 1
      - 2
      - 3
```

Implicing mapping with the mountpoint option will prefix the paths specified in the module with the mountpoint.

*Note that it's not required for a module to specify default paths.*

Explicing mapping of paths will simply map a given path to a function in the module.

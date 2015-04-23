def dump_request(config, query_params, **kwargs):
    return 200, dict(config=config, query_params=query_params, **kwargs)

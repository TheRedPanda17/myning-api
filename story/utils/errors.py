from aiohttp import web


def wrap_errors(errs: str | list[str], status=400):
    if isinstance(errs, str):
        errs = [errs]

    return web.json_response(status=status, data={"errors": errs})

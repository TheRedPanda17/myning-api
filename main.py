from aiohttp import web

import myning.app

app = myning.app.get_app()
web.run_app(app)

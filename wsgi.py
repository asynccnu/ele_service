from service import app, web, loop
from service.database import setup_db
from service.api import api

dordb = loop.run_until_complete(setup_db())
api['dordb'] = dordb

if __name__ == '__main__':
    web.run_app(app)

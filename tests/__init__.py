from service import app
from service.api import api
from service.database import setup_db
from .test_ele_api import test_ele_search_api

if __name__ == '__main__':
    test_ele_search_api(api)

import pytest
import configparser

from specmatic.core.specmatic import Specmatic
from specmatic.utils import get_project_root

PROJECT_ROOT = get_project_root()

app_host = "127.0.0.1"
app_port = 8000
stub_host = "127.0.0.1"
stub_port = 8080

expectation_json_file = PROJECT_ROOT + '/test/data/expectation.json'
app_contract_file = PROJECT_ROOT + '/test/spec/product-search-bff-api.yaml'
stub_contract_file = PROJECT_ROOT + '/test/spec/api_order_v1.yaml'
app_module = PROJECT_ROOT + '/test/sanic_app'


class TestContract:
    pass


def update_app_config_with_stub_info(host: str, port: int):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['dev']['ORDER_API_HOST'] = host
    config['dev']['ORDER_API_PORT'] = str(port)
    with open('./../config.ini', 'w') as configfile:
        config.write(configfile)


def reset_app_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['dev']['ORDER_API_HOST'] = '127.0.0.1'
    config['dev']['ORDER_API_PORT'] = '8080'
    with open('./../config.ini', 'w') as configfile:
        config.write(configfile)


Specmatic.test_asgi_app('test.sanic_app:app',
                        TestContract,
                        project_root=PROJECT_ROOT,
                        expectation_files=[expectation_json_file],
                        app_config_update_func=update_app_config_with_stub_info)

reset_app_config()

if __name__ == '__main__':
    pytest.main()

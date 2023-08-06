# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvola_api']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'mvola-api',
    'version': '1.0.2',
    'description': 'Python package for MVola API',
    'long_description': '## Python package for MVOLA API\n\n###Installation\n```cmd\n    python -m pip install mvola_api\n```\n###Exemple\n\n```python\n\nimport os\nimport uuid\nfrom datetime import datetime as dt\nfrom pathlib import Path\nfrom mvola_api import MVolaMerchantPayAPI, AUthResult, Config, MvolaTransactionData, HashedMap,PRODUCTION_URL\nfrom dotenv import dotenv_values\n#load .env\nconfig = dotenv_values(Path(os.getcwd(), \'.env\'))\n\n# for sandbox\napi: MVolaMerchantPayAPI = MVolaMerchantPayAPI()\n\n# for production \napi: MVolaMerchantPayAPI = MVolaMerchantPayAPI(PRODUCTION_URL)\n\n# revoke token\n\napi.revoke_token(config.get(\'CONSUMER_KEY\'), config.get(\'CONSUMER_SECRET\'), True)\n\n# The third parameter fro revoke_token is to auto update Bearer token for the API, So, no need to call set_access_token \n# If you want to load access token\n\nauth_data = api.revoke_token(config.get(\'CONSUMER_KEY\'), config.get(\'CONSUMER_SECRET\'), True)\n\nprint(auth_data.access_token)\n\n#Transaction\n#create transaction config\n\ntransaction_config: Config = Config(**{\n    \'version\': "1.0",\n    \'xCorrelationID\': f\'{uuid.uuid4()}\',\n    \'userLanguage\': "MG",\n    \'userAccountIdentifier\': "msisdn;034350003",\n    \'partnerName\': "Mvola API"\n})\n#  init transaction  config\napi.init_config(transaction_config)\n\ntransaction: MvolaTransactionData = MvolaTransactionData(**{\n    \'amount\': 500,\n    \'currency\': "Ar",\n    \'descriptionText\': "Description",\n    \'requestDate\': dt.now().isoformat(),\n    \'debitParty\': [\n        HashedMap(**{\n            \'key\': "msisdn",\n            \'value\': "034350003",\n        })\n    ],\n    \'creditParty\': [\n        HashedMap(**{\n            \'key\': "msisdn",\n            \'value\': "034350003",\n        }),\n    ],\n    \'metadata\': [\n        HashedMap(**{\n            \'key\': "partnerName",\n            \'value\': "Mvola API",\n        }),\n        HashedMap(**{\n            \'key\': "fc",\n            \'value\': "USD",\n        }),\n        HashedMap(**{\n            \'key\': "amountFc",\n            \'value\': "1",\n        }),\n    ],\n    \'requestingOrganisationTransactionReference\': f\'{uuid.uuid4()}\',\n    \'originalTransactionReference\': f\'{uuid.uuid4()}\',\n})\n# start transaction\ntransaction_response = api.initiate_transaction(transaction)\nprint(transaction_response)\n\n# get details\n\ntransaction_details = api.get_details(transactionId)\n\n#get status\ntransaction_status = api.get_status(serverCorrelationId)\n```',
    'author': 'tsiresymila',
    'author_email': 'tsiresymila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

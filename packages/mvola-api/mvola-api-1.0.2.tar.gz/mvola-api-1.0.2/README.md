## Python package for MVOLA API

###Installation
```cmd
    python -m pip install mvola_api
```
###Exemple

```python

import os
import uuid
from datetime import datetime as dt
from pathlib import Path
from mvola_api import MVolaMerchantPayAPI, AUthResult, Config, MvolaTransactionData, HashedMap,PRODUCTION_URL
from dotenv import dotenv_values
#load .env
config = dotenv_values(Path(os.getcwd(), '.env'))

# for sandbox
api: MVolaMerchantPayAPI = MVolaMerchantPayAPI()

# for production 
api: MVolaMerchantPayAPI = MVolaMerchantPayAPI(PRODUCTION_URL)

# revoke token

api.revoke_token(config.get('CONSUMER_KEY'), config.get('CONSUMER_SECRET'), True)

# The third parameter fro revoke_token is to auto update Bearer token for the API, So, no need to call set_access_token 
# If you want to load access token

auth_data = api.revoke_token(config.get('CONSUMER_KEY'), config.get('CONSUMER_SECRET'), True)

print(auth_data.access_token)

#Transaction
#create transaction config

transaction_config: Config = Config(**{
    'version': "1.0",
    'xCorrelationID': f'{uuid.uuid4()}',
    'userLanguage': "MG",
    'userAccountIdentifier': "msisdn;034350003",
    'partnerName': "Mvola API"
})
#  init transaction  config
api.init_config(transaction_config)

transaction: MvolaTransactionData = MvolaTransactionData(**{
    'amount': 500,
    'currency': "Ar",
    'descriptionText': "Description",
    'requestDate': dt.now().isoformat(),
    'debitParty': [
        HashedMap(**{
            'key': "msisdn",
            'value': "034350003",
        })
    ],
    'creditParty': [
        HashedMap(**{
            'key': "msisdn",
            'value': "034350003",
        }),
    ],
    'metadata': [
        HashedMap(**{
            'key': "partnerName",
            'value': "Mvola API",
        }),
        HashedMap(**{
            'key': "fc",
            'value': "USD",
        }),
        HashedMap(**{
            'key': "amountFc",
            'value': "1",
        }),
    ],
    'requestingOrganisationTransactionReference': f'{uuid.uuid4()}',
    'originalTransactionReference': f'{uuid.uuid4()}',
})
# start transaction
transaction_response = api.initiate_transaction(transaction)
print(transaction_response)

# get details

transaction_details = api.get_details(transactionId)

#get status
transaction_status = api.get_status(serverCorrelationId)
```
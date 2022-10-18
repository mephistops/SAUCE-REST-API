import json
import requests
from requests.auth import HTTPBasicAuth

psa_url = 'https://api2.sauce.online/api/Paises'
psa_username = 'Consultastamaria'
psa_password = '123456789'

url = psa_url
username = psa_username
password = psa_password

response = requests.get(url,
                         auth=(username, password),
                         headers={'Content-Type': 'application/json'},
                        )

print(json.loads(response.text))

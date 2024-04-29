#%%
#pip install requests
#pip isntall pandas
#install openpyxl

import requests
import pandas as pd
import json
from ares_util.ares import call_ares
#našel jsem když jsem si vygooglil "ares api python"


import requests
from urllib.parse import urljoin



df = pd.read_excel("ico.xlsx")

#get 1st column:
data = df.iloc[:,0]
#add leading 0s as in 00005886 etc......
data = data.dropna().astype(int).astype(str).str.zfill(8)

#drop NaN

#drop NaN
#%%
import datetime

df_ico = pd.DataFrame(columns=['company_name', 'company_id', 'company_vat_id', 'legal_form', 'region', 'city', 'city_part', 'street', 'zip_code'])

requests_sent = 0
for ICO in data:
    current_hour = datetime.datetime.now().hour
    if (8 <= current_hour < 18 and requests_sent >= 1000) or (18 <= current_hour < 8 and requests_sent >= 5000):
        print("Request limit reached, waiting until next time window.")
        break
    try:
        company_info = call_ares(ICO)
        if company_info:
            merged_info = {**company_info['legal'], **company_info['address']}
            df_ico = pd.concat([df_ico, pd.DataFrame([merged_info])], ignore_index=True)
            requests_sent += 1
    except Exception as e:
        print(f"Error occurred: {e}")
        error_row = {key: 'XXX' for key in df_ico.columns}
        df_ico = pd.concat([df_ico, pd.DataFrame([error_row])], ignore_index=True)
# %%
#%%


df_ico.to_excel("ares_output.xlsx", index=False)
















#Moje verze  aby jsi viděl i pod pokličku
# def call_ares(company_id):
#     """
#     Fetch data from ARES.

#     :param company_id: 8-digit number
#     :type company_id: unicode|int
#     """
#     ARES_API_URL = "https://ares.gov.cz/"
#     url = urljoin(ARES_API_URL, f'ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{company_id}')
#     response = requests.get(url)

#     if response.status_code != 200:
#         return False

#     response_json = response.json()

#     address = response_json["sidlo"]

#     result_company_info = {
#         'legal': {
#             'company_name': response_json.get("obchodniJmeno"),
#             'company_id': response_json.get("ico"),
#             'company_vat_id': response_json.get("dic"),
#             'legal_form': response_json.get("pravniForma"),
#         },
#         'address': {
#             'region': address.get('nazevOkresu'),
#             'city': address.get('nazevObce'),
#             'city_part': address.get('nazevCastiObce'),
#             'street': address.get('nazevUlice'),
#             'zip_code': address.get('psc')
#         }
#     }
#     return result_company_info
# %%

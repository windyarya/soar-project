import requests
import json

true = True
null = None
false = False

def get_iris_iocs(case_id, api_key):
    url = "https://10.15.42.248/case/ioc/list"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "cid": case_id
    }

    try:
        # Melakukan permintaan GET ke Iris DFIR API menggunakan requests
        response = requests.get(url, headers=headers, data=json.dumps(body), verify=False)

        # Mengecek apakah permintaan berhasil (kode status 200 OK)
        if response.status_code == 200:
            ioc_data = response.json()
            return ioc_data
        else:
            print(f"Permintaan tidak berhasil. Kode status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
    
def get_iris_assets(case_id, api_key):
    url = "https://10.15.42.248/case/assets/list"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "cid": case_id
    }

    try:
        # Melakukan permintaan GET ke Iris DFIR API menggunakan requests
        response = requests.get(url, headers=headers, data=json.dumps(body), verify=False)

        # Mengecek apakah permintaan berhasil (kode status 200 OK)
        if response.status_code == 200:
            ioc_data = response.json()
            return ioc_data
        else:
            print(f"Permintaan tidak berhasil. Kode status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

json_alert = $add_new_alert.body.data
# Ganti dengan case_id dan api_key yang sesuai
case_ids = $check_case_present.message.case_ids
api_key = "YOUR_API_KEY"

result_json = {}

# Mendapatkan data IOC
for case_id in case_ids:
    # Mendapatkan data IOC untuk setiap case_id
    result_ioc = get_iris_iocs(case_id, api_key)
    result_asset = get_iris_assets(case_id, api_key)

    exist_data_ioc = result_ioc.get("data", {}).get("ioc", [])
    new_ioc = json_alert.get("iocs", [])  # Mendapatkan data IOC dari JSON alert
    exist_data_values = {ioc.get("ioc_value") for ioc in exist_data_ioc if "ioc_value" in ioc}
    #print(exist_data_values)
    missing_ioc_uuids = [ioc.get("ioc_value") for ioc in new_ioc if ioc.get("ioc_value") not in exist_data_values]
    #print(missing_ioc_uuids)


    exist_data_asset = result_asset.get("data", {}).get("assets", [])
    new_asset = json_alert.get("assets", [])
    exist_data_values = {asset.get("asset_ip") for asset in exist_data_asset if "asset_ip" in asset}
    missing_asset_uuids = [asset.get("asset_ip") for asset in new_asset if asset.get("asset_ip") not in exist_data_values]

    check_ioc = missing_ioc_uuids
    check_asset = missing_asset_uuids
    if not check_ioc and not check_asset:
        result_json[case_id] = {
            "result": 0,
            "case_id": case_id,
        }
    else:
        iocs = [ioc["ioc_uuid"] for ioc in json_alert.get("iocs", []) if "ioc_uuid" in ioc]
        output_string_iocs = '["' + '", "'.join(iocs) + '"]'

        assets = [asset["asset_uuid"] for asset in json_alert.get("assets", []) if "asset_uuid" in asset]
        output_string_assets = '["' + '", "'.join(assets) + '"]'

        result_json[case_id] = {
            "result": 1,
            "case_id": case_id,
            "output_string_iocs": output_string_iocs,
            "output_string_assets": output_string_assets
        }

data_result = result_json

result = {}

for ioc_id, ioc_data in data_result.items():
    if ioc_data.get("result") == 0:
        case_id = ioc_data.get("case_id")
        result = result_json[case_id]
        break
    elif ioc_data.get("result") == 1:
        case_id = ioc_data.get("case_id")
        result = result_json[case_id]

print(json.dumps(result, indent=2))
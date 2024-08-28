import json

true = True
null = None
false = False

json_alert_1 = $add_new_alert.body.data
    
json_alert_str = json.dumps(json_alert_1)
json_alert = json.loads(json_alert_str)

# Mendapatkan UUID dari IoC
iocs = [ioc["ioc_uuid"] for ioc in json_alert.get("iocs", [])]
output_iocs = '["' + '", "'.join(iocs) + '"]'

# Mendapatkan UUID dari asset
assets = [asset["asset_uuid"] for asset in json_alert.get("assets", [])]
output_assets = '["' + '", "'.join(assets) + '"]'

result_json = {
    "iocs": output_iocs,
    "assets": output_assets
}

print(json.dumps(result_json, indent=2))
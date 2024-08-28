import json

true = True
null = None
false = False

iocs = $parse_ioc_asset.message.iocs
case_id = $repeat_case_id.message

ip_iocs = []
hash_iocs = []

for ioc in iocs:
    if 76 <= ioc["ioc_type_id"] <= 80:  # Assuming 79 represents the IOC type for IP addresses
        ip_iocs.append(ioc["ioc_value"])
    elif 90 <= ioc["ioc_type_id"] <= 119:
        hash_iocs.append(ioc["ioc_value"])

result_json = {
    "case_id": case_id,
    "ip_iocs": ip_iocs,
    "hash_iocs": hash_iocs
}

print(json.dumps(result_json, indent=2))
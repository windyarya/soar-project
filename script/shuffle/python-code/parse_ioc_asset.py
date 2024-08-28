import json

true = True
null = None
false = False

json_list = [
    {
        "asset_name": "Switch Ubiquiti US-8-150W",
        "asset_ip": "10.15.40.245",
        "asset_type_id": 9
    },
    {
        "asset_name": "Access Point IT-Lobby",
        "asset_ip": "10.15.40.247",
        "asset_type_id": 8
    },
    {
        "asset_name": "Access Point IT-Sekdep",
        "asset_ip": "10.15.40.243",
        "asset_type_id": 8
    },
    {
        "asset_name": "Access Point IT-SOC",
        "asset_ip": "10.15.40.246",
        "asset_type_id": 8
    },
    {
        "asset_name": "Access Point IT-608",
        "asset_ip": "10.15.40.242",
        "asset_type_id": 8
    },
    {
        "asset_name": "Access Point IT-KCKS",
        "asset_ip": "10.15.40.244",
        "asset_type_id": 8
    },
    {
        "asset_name": "nids-vm",
        "asset_ip": "10.15.42.248",
        "asset_type_id": 3
    },
    {
        "asset_name": "web-server-vm",
        "asset_ip": "10.15.42.116",
        "asset_type_id": 3
    },
    {
        "asset_name": "raspi-firewall",
        "asset_ip": "10.15.41.44",
        "asset_type_id": 3
    },
    {
        "asset_name": "Windows-10-1",
        "asset_ip": "10.15.42.175",
        "asset_type_id": 12
    }
]

def parse_ioc_hash(json_iocs):
    # Mappings untuk tipe hash ke ID dan TLP
    hash_type_mapping = {
        "md5": (90, 2),
        "sha1": (111, 2),
        "sha224": (112, 2),
        "sha256": (113, 2),
        "sha3-224": (114, 2),
        "sha3-256": (115, 2),
        "sha3-384": (116, 2),
        "sha3-512": (117, 2),
        "sha384": (118, 2),
        "sha512": (119, 2),
    }

    result = {"found_hash": 0, "hash_info": []}

    # Proses setiap IOC
    for ioc in json_iocs:
        data = ioc.get("data", "")
        data_type = ioc.get("data_type", "").lower()

        # Periksa apakah tipe hash yang valid
        if data_type in hash_type_mapping:
            if result["found_hash"] == 0:
                result["found_hash"] = 1

            ioc_id, tlp_id = hash_type_mapping[data_type]
            hash_info = {
                "ioc_value": data,
                "ioc_type_id": ioc_id,
                "ioc_tlp_id": tlp_id
            }
            result["hash_info"].append(hash_info)
    return result

def parse_ioc_ip(json_data):
    ip_list = [entry['asset_ip'] for entry in json_list]
    ip_2 = [entry['data'] for entry in json_data]

    ip_local_it = []
    ip_local_its = []
    ip_public = []
    ip_asset = []
    ioc_ip = []

    result = {"found_ip": 0, "ip_ioc":[]}

    # Parse alamat IP yang ditemukan
    for entry in json_data:
        if entry['data'] not in ["0.0.0.0", "255.255.255.255"]:
            # print(entry['is_private_ip'])
            if entry['data_type'] == 'ip' and entry['is_private_ip'] == True:  
                ip_entry = entry['data']
                if ip_entry in ip_list:
                    for asset_entry in json_list:
                        if asset_entry['asset_ip'] == ip_entry:
                            ip_asset.append(asset_entry)
                elif ip_entry.startswith("10.15"):
                    ip_local_it.append(ip_entry)
                else:
                    ip_local_its.append(ip_entry)
            elif entry['data_type'] == 'ip' and entry['is_private_ip'] == False:
                ip_public.append(entry['data'])
    ioc_ip.extend(ip_local_its)
    if ip_public:
        ioc_ip.extend(ip_public)

    if ioc_ip:
        result["found_ip"] = 1
    
    # Iterasi melalui setiap alamat IP
    for ip_address in ioc_ip:
        ioc_type_id = 79
        ioc_object = {"ioc_value": ip_address, "ioc_type_id": ioc_type_id, "ioc_tlp_id": 2}
        result["ip_ioc"].append(ioc_object)
    print
    return ip_asset, result

json_str = '$parse_ioc'
json_data = json.loads(json_str)

ip_parsed = parse_ioc_ip(json_data)

# Konversi list ke json
asset_info = ip_parsed[0]
#output_asset = {key: value for item in asset_info for key, value in item.items()}

ioc_info = ip_parsed[1]

ioc_objects = ioc_info["ip_ioc"]

hash_ioc = parse_ioc_hash(json_data)

if hash_ioc["found_hash"] == 1:
    ioc_objects.extend(hash_ioc["hash_info"])

result_json = {
    "assets": asset_info,
    "found_hash": hash_ioc["found_hash"],
    "found_ip": ioc_info["found_ip"],
    "iocs": ioc_objects
}

# Cetak hasil dalam format JSON
print(json.dumps(result_json, indent=2))
import json

# String JSON yang diberikan
json_string = '$get_alienvault_ip_list.body.data.affected_items.#'

# Mengonversi string JSON menjadi list Python
ip_dict = json.loads(json_string)

# Alamat IP yang akan diperiksa
target_ip = $validating_iocs.message.ip_iocs

# Memeriksa apakah alamat IP ada dalam list
found_ip_exists = any(ip in ip_dict for ip in target_ip)

# Persiapkan output dalam format JSON
output_json = {"target_ip": target_ip[0], "found_ip_exists": int(found_ip_exists)}

# Mengonversi hasil ke dalam format JSON dan mencetaknya
output_json_str = json.dumps(output_json, indent=2)
print(output_json_str)
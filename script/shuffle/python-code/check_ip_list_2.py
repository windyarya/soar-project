import json

true = True
null = None
false = False

# String JSON yang diberikan
json_string = '$get_custom_ip_list.body.data.affected_items.#'

# Mengonversi string JSON menjadi list Python
ip_dict = json.loads(json_string)

# Alamat IP yang akan diperiksa
target_ip = $check_ip_list_1

# Memeriksa keberadaan setiap alamat IP dalam list di dalam ip_list
found_ip_exists = {ip["message"]["target_ip"]: ip["message"]["target_ip"] in ip_dict for ip in target_ip}

# Persiapkan output dalam format JSON
output_json = [{"target_ip": ip, "found_ip_exists": int(found)} for ip, found in found_ip_exists.items()]

# Mengonversi hasil ke dalam format JSON dan mencetaknya
output_json_str = json.dumps(output_json, indent=2)
print(output_json_str)
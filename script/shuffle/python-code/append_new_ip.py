import json

true = True
null = None
false = False

# JSON yang sudah ada
existing_json = '$get_custom_ip_list.body.data.affected_items.#'
# Mengonversi JSON menjadi dictionary Python
existing_dict = json.loads(existing_json)

# Alamat IP yang akan ditambahkan
new_ips = $check_ip_list_2

# Memeriksa keberadaan setiap alamat IP baru dengan found_ip_exists == 0
new_ips_to_add = [ip["message"][0]["target_ip"] for ip in new_ips if ip["message"][0]["found_ip_exists"] == 0]

# Menambahkan alamat IP baru ke dalam dictionary jika ditemukan
existing_dict.update({ip: "" for ip in new_ips_to_add})

# Menentukan status berdasarkan apakah ada alamat IP baru yang ditambahkan atau tidak
status = 1 if new_ips_to_add else 0

# Menyiapkan output dalam format JSON
updated_json = {
    "status": status,
    "updated_list": existing_dict
}

# Mengonversi hasil ke dalam format JSON dan mencetaknya
updated_json_str = json.dumps(updated_json, indent=2)
print(updated_json_str)
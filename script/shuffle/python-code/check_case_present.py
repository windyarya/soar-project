import json

true = True
null = None
false = False

# JSON data contoh
json_data = $get_cases_list.body
alert_title = "$add_new_alert.body.data.alert_title"
# Membuat daftar untuk menyimpan case_id yang memiliki nama kasus yang sama
case_ids_list = []

# Loop melalui data JSON
for item in json_data["data"]:
    case_name = item.get("case_name", "")
    if alert_title in case_name:
        case_id = item.get("case_id")
        case_ids_list.append(case_id)

# Menentukan nilai found
found = 1 if case_ids_list else 0

# Menampilkan hasil dalam format JSON
output_json = json.dumps({"found": found, "case_ids": case_ids_list}, indent=2)
print(output_json)
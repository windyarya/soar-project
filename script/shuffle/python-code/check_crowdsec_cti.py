import requests
import json

def get_crowdsec_cti(ip_address, api_key):
    url = f"https://cti.api.crowdsec.net/v2/smoke/{ip_address}"
    headers = {
        "x-api-key": api_key
    }

    try:
        # Melakukan permintaan GET ke CrowdSec CTI API menggunakan requests
        response = requests.get(url, headers=headers)

        # Mengecek apakah permintaan berhasil (kode status 200 OK)
        if response.status_code == 200:
            cti_data = response.json()
            return cti_data
        else:
            return None
    except Exception as e:
        return None

def is_public_ip(ip_address):
    # Pemisahan bagian alamat IP
    ip_parts = list(map(int, ip_address.split('.')))

    # Penentuan alamat IP publik atau privat berdasarkan blok alamat IP
    if (
        (ip_parts[0] == 10) or
        (ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31) or
        (ip_parts[0] == 192 and ip_parts[1] == 168)
    ):
        return False  # IP privat
    else:
        return True  # IP publik

# Ganti dengan kunci API CrowdSec yang valid
api_key = "YOUR_API_KEY"

# Ganti dengan alamat IP yang ingin dicari informasi CTI-nya
ip_to_check = $validating_iocs.message.ip_iocs
public_ips_to_check = [ip for ip in ip_to_check if is_public_ip(ip)]

# Memanggil fungsi untuk mendapatkan informasi CTI hanya untuk alamat IP publik
cti_info = {}
for ip in public_ips_to_check:
    info = get_crowdsec_cti(ip, api_key)
    if info:
        cti_info[ip] = info

result = {}

# Menampilkan informasi CTI (jika ada)
if cti_info:
    ip_addresses = []
    for ip, details in cti_info.items():
        ip_addresses.append(details["ip"])
    result = {
        "status": 1,
        "ip_addresses": ip_addresses,
        "cti_info": cti_info
    }
else:
    result = {
        "status": 0
    }

print(json.dumps(result, indent=2))
import json

true = True
null = None
false = False

# Cek MITRE ID
def check_mitre_id(json_data):
    try:
        mitre_ids = json_data.get("all_fields", {}).get("rule", {}).get("mitre", {}).get("id", [])
        return mitre_ids if mitre_ids else []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Klasifikasi MITRE ID ke Klasifikasi IRIS
def find_classification_ids(mitre_ids, classification_data):
    classification_ids = set()
    for mitre_id in mitre_ids:
        mitre_id_without_suffix = mitre_id.split('.')[0]
        for classification in classification_data["classifications"]:
            classification_mitre_id = classification["mitre_id"].split('.')[0]
            if mitre_id_without_suffix == classification_mitre_id:
                classification_ids.add(classification["id"])
    
    return list(classification_ids)

# Alert JSON data
json_data = $exec

# Parse JSON data
json_data_str = json.dumps(json_data)
data = json.loads(json_data_str)

# Klasifikasi MITRE ID ke Klasifikasi IRIS
classification_id = 36
case_template_id = 4
mitre_ids_check_result = check_mitre_id(data)

if mitre_ids_check_result:
    classification_rules = {
        (4, 5, 6, 7, 8, 9, 10): 2,
        (11, 12): 6,
        (15,): 5,
        (21,): 3,
        (22, 23): 1
    }
    classification_data = {
        "classifications": [
            {"id": 1, "title": "Spam", "mitre_id": ""},
            {"id": 2, "title": "Harmful Speech", "mitre_id": ""},
            {"id": 3, "title": "Child/Sexual/Violence", "mitre_id": ""},
            {"id": 4, "title": "Virus", "mitre_id": ""},
            {"id": 5, "title": "Worm", "mitre_id": ""},
            {"id": 6, "title": "Ransomware", "mitre_id": "T1486"},
            {"id": 7, "title": "Trojan/Malware", "mitre_id": "T1032"},
            {"id": 8, "title": "Spyware/Rat", "mitre_id": ""},
            {"id": 9, "title": "Dialer", "mitre_id": ""},
            {"id": 10, "title": "Rootkit", "mitre_id": "T1060, T1036"},
            {"id": 11, "title": "Scanning", "mitre_id": "T1595"},
            {"id": 12, "title": "Sniffing", "mitre_id": "T1003"},
            {"id": 13, "title": "Social Engineering", "mitre_id": "T1566"},
            {"id": 14, "title": "Exploit Known Vulnerabilities", "mitre_id": "T1190"},
            {"id": 15, "title": "Login Attempts", "mitre_id": "T1110"},
            {"id": 16, "title": "New Attack Signature", "mitre_id": ""},
            {"id": 17, "title": "Privileged Account Compromise", "mitre_id": ""},
            {"id": 18, "title": "Unprivileged Account Compromise", "mitre_id": ""},
            {"id": 19, "title": "Botnet Member", "mitre_id": "T1056, T1489"},
            {"id": 20, "title": "Domain Compromise", "mitre_id": "T1482"},
            {"id": 21, "title": "Application Compromise", "mitre_id": "T1056"},
            {"id": 22, "title": "DoS", "mitre_id": "T1498"},
            {"id": 23, "title": "DDoS", "mitre_id": ""},
            {"id": 24, "title": "Sabotage", "mitre_id": "T1485"},
            {"id": 25, "title": "Outage", "mitre_id": "T1489"},
            {"id": 26, "title": "Unauthorized Access to Information", "mitre_id": "T1005"},
            {"id": 27, "title": "Unauthorized Modification to Information", "mitre_id": "T1565"},
            {"id": 28, "title": "Copyright", "mitre_id": ""},
            {"id": 29, "title": "Masquerade", "mitre_id": "T1036"},
            {"id": 30, "title": "Phishing", "mitre_id": "T1566"},
            {"id": 31, "title": "Open for Abuse", "mitre_id": ""},
            {"id": 32, "title": "Regulator", "mitre_id": ""},
            {"id": 33, "title": "Standard", "mitre_id": ""},
            {"id": 34, "title": "Security Policy", "mitre_id": "T1562"},
            {"id": 35, "title": "Conformity: Other", "mitre_id": ""},
            {"id": 36, "title": "Other: Other", "mitre_id": ""}
        ]
    }

    # Mencari ID klasifikasi dari MITRE IDs
    classification_ids = find_classification_ids(mitre_ids_check_result, classification_data)
    
    if classification_ids:
        for rule_set, template_id in classification_rules.items():
            if any(cid in rule_set for cid in classification_ids):
                classification_id = classification_ids[0]
                case_template_id = template_id
                break

# Mapping Rule Level Wazuh ke Severity IRIS
alert_level = int(data["all_fields"]["rule"]["level"])
severity = 1
if 0 < alert_level < 5:
    severity = 2
elif 5 <= alert_level < 7:
    severity = 3
elif 7 <= alert_level < 10:
    severity = 4
elif 10 <= alert_level < 13:
    severity = 5
elif alert_level >= 13:
    severity = 6

# Membuat json hasil parsing
alert_info = {
    "title": data["title"],
    "description": data["all_fields"]["rule"]["description"],
    "timestamp": data["timestamp"],
    "classification_id": classification_id,
    "case_template_id": case_template_id,
    "severity": severity,
}

print(json.dumps(alert_info, indent=2))
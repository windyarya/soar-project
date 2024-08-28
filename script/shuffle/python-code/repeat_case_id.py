import json

true = True
null = None
false = False

esc_1 = "$escalate_alert.body.data.case_id"
esc_2 = "$escalate_alert_2.body.data.case_id"
merge = "$merge_alert.body.data.case_id"

case_id = 0

for var_name in ["esc_1", "esc_2", "merge"]:
    var_value = locals()[var_name]
    if isinstance(var_value, str) and var_value.strip() and var_value[0].isdigit():
        case_id = int(var_value)

print(case_id)
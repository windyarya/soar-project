import json

true = True
null = None
false = False

# Given JSON alert
alert_json = $add_new_alert

# Parse JSON
json_data_str = json.dumps(alert_json)
alert_data = json.loads(json_data_str)

# Extract relevant information
alert_id = alert_data["body"]["data"]["alert_id"]
alert_title = alert_data["body"]["data"]["alert_title"]
timestamp = alert_data["body"]["data"]["alert_source_event_time"]

# Generate output message
output_message = f'New alert with ID {alert_id}, titled \'{alert_title}\', recorded on {timestamp}. For detailed alert information, go to https://10.15.42.248/alerts'

# Print the output message
print(output_message)
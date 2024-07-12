import pandas as pd
from sqlite_dbcon import db_connect


f_select = "device_id,devices_type,inspec_note"
t_select = "db_sde.devices_income"
this_mac_con = db_connect()
condition = "devices_type = 'Actuator Controller 3CH' LIMIT 500"
this_mac_con.connect_select(t_select,condition,f_select)
mac_id = []
device_type = []
status = []
for this_mac in this_mac_con :
    mac_id.append(this_mac[0])
    device_type.append(this_mac[1])
    status.append(this_mac[2])
print(mac_id)

# Sample data
data = {
    'Device ID': mac_id,
    'Device Type': device_type,
    'Status': status
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to an Excel file
df.to_excel('device_data.xlsx', index=False, engine='openpyxl')

print("Excel file created successfully.")


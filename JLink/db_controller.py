
from sqlite_dbcon import db_connect
from utils import *
from utils import *
dt_string = get_date_time()
import JLink.insign_db as insign_db

def device_update(ui,mac_id,controller_type,first_stack,second_stack): 
    # Check Duplicate Device ID ===================================
    f_select = "device_id"
    t_select = "db_sde.devices_income"
    box_lot_id = ui.boxlot_Box.currentText()
    print(box_lot_id)
    c_select = None
    port_array = []
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    #==============================================================
    this_mac_con = db_connect()
    condition = "device_id = '"+mac_id+"'"
    this_mac_con.connect_select(t_select,condition,f_select)
    this_mac_array = []
    for this_mac in this_mac_con :
        print("====================================================")
        print(this_mac)
        this_mac_array.append(this_mac)
    if len(this_mac_array) != 0:
         pass
    else :
        qty_status = 'good_product'
        insign_db.addDevice_action(ui,qty_status,controller_type)
    #=============================================================
    if controller_type.startswith('Sensor Controller') :
            data = [
                    ['pm_1',first_stack[0]],
                    ['pm_2_5',first_stack[1]],
                    ['pm_10',first_stack[2]],
                    ['scd_co2',second_stack[0]],
                    ['scd_temp',second_stack[1]],
                    ['scd_hum',second_stack[2]],
                    ['create_at',dt_string]
                    ]
            fill_db = ["GOOD","","0"]
            sensor_db_value = "('"+mac_id+"','"+fill_db[0]+"','"+controller_type+"','"+str(first_stack[0])+"','"+str(first_stack[1])+"','"+str(first_stack[2])+"','"+str(second_stack[0])+"','"+str(second_stack[1])+"','"+str(second_stack[2])+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+box_lot_id+"','"+fill_db[1]+"','"+fill_db[2]+"','"+dt_string+"')"
            device_db_table = "db_sde.devices_income"
            device_sensor = db_connect()
            device_sensor.connect_sql_insert(device_db_table,sensor_db_value)
    #===========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
    if controller_type.startswith('Actuator Controller') :
            level_all = []
            for level in first_stack :
                if level == '3' :
                    level_st = 'HIGH'
                elif level == '2' :
                    level_st = 'MID'
                elif level == '1' :
                    level_st = 'LOW'
                else :
                    level_st = 'OFF'
                level_all.append(level_st)
            data = [
                    ['sw_1st',level_all[0]],
                    ['current_1st',second_stack[1]],
                    ['sw_2nd',level_all[1]],
                    ['current_2nd',second_stack[2]],
                    ['sw_3rd',level_all[2]],
                    ['current_3rd',second_stack[3]],
                    ['sw_4th',level_all[3]],
                    ['current_4th',second_stack[4]],
                    ['create_at',dt_string]
                    ]
            fill_db = ["GOOD","","0"]
            actuator_db_value = "('"+mac_id+"','"+fill_db[0]+"','"+controller_type+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+fill_db[1]+"','"+first_stack[0]+"','"+second_stack[1]+"','"+first_stack[1]+"','"+second_stack[2]+"','"+first_stack[2]+"','"+second_stack[3]+"','"+first_stack[3]+"','"+second_stack[4]+"','"+box_lot_id+"','"+fill_db[1]+"','"+fill_db[2]+"','"+dt_string+"')"
            device_db_table = "db_sde.devices_income"
            device_actuator = db_connect()
            device_actuator.connect_sql_insert(device_db_table,actuator_db_value)
    # ====================================================================================
    #===========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
    # Store Device ID =====================
    for port_data in db_con :
        #==================================
        port_array.append(port_data[0])
    #============================================================
        if mac_id == port_data[0] :
                print("Duplicated Device")
                for update in data :
                    where = "device_id = '"+mac_id+"'"
                    set_to = ""+update[0]+" = '"+update[1]+"'"
                    print(set_to)
                    db_con_up = db_connect()
                    db_con_up.connect_update(t_select,set_to,where)
#==========================================================================================================================================================================================================================================================================================================================================================================================================================
def reject_device(ui,device_id,device_type,timestamp) :
    feild_select = 'qty_inspected'
    table_select = 'db_sde.devices_income_box'
    lot_id = ui.boxlot_Box.currentText()
    issue_name = ui.error_point_Box.currentText()
    condetion = "lot_box_id = '"+lot_id+"'"
    qty_con = db_connect()
    qty_con.connect_select(table_select,condetion,feild_select)
    reject_data = db_connect()
    null = ''
    table = "db_sde.devices_income"
    value = "('"+device_id+"','NG','"+device_type+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+null+"','"+lot_id+"','"+issue_name+"','0','"+timestamp+"')"
    reject_data.connect_sql_insert(table,value)
    pass
#==========================================================================================================================================================================================================================================================================================================================================================================================================================
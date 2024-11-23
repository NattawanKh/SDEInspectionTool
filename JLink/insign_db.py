from PyQt5.QtGui import QStandardItemModel, QStandardItem
from sqlite_dbcon import db_connect
from utils import *

#================================================================================================================================================================
def incoming_device(ui):
    lot_no = ui.incom_date.text()
    lot_id_box(ui)
    # device_qt  = ui.income_qt.text()
    lot_db_table = "db_sde.devices_income_lot"
    lot_condition = "lot_no = '"+lot_no+"'"
    lot_field = "lot_no"
    lot_invalid = []
    check_lot = db_connect()
    check_lot.connect_select(lot_db_table,lot_condition,lot_field)
    for lot_list in check_lot :
         print(lot_list[0])
         lot_invalid.append(lot_list[0])
    null_space = 0
    null_space = str(null_space)
    # duplicated lot name 
    if len(lot_no) >= 4  :
        # ADD Data ===========================================================================================================
        dt_string = get_date_time()
        income_db = "('"+lot_no+"','"+null_space+"','"+null_space+"','"+null_space+"','"+null_space+"','"+dt_string+"')"
        device_db_table = "db_sde.devices_income_lot"
        device_sensor = db_connect()
        device_sensor.connect_sql_insert(device_db_table,income_db)
        # SHOW STATUS ========================================================================================================
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p>   <span style=\"color:#4CAF50\">Update Incoming Lot </span></p>")
        # Clear Input ========================================================================================================
        #ui.income_qt.clear()
        ui.incom_date.clear()
    elif len(lot_no) == 0  :
        print("------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p><span style=\"color:RED\">Invalid Data</span></p>")
        #ui.income_qt.clear()
        ui.incom_date.clear()
    elif lot_invalid != 0  :
        print("------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p><span style=\"color:RED\">Error Duplicated Lot No.</span></p>")
        #ui.income_qt.clear()
        ui.incom_date.clear()
    incoming_list(ui,0)

def incoming_list(ui,status) :
    if status == 0 :
        ui.big_controller_btn.show()
        ui.big_insign_bt.hide()
        ui.big_db_btn.show()
    f_select = "lot_no,qty_inspected,good_product,ng_product"
    t_select = "db_sde.devices_income_lot"
    c_select = "status = '"+str(status)+"' AND lot_no like '%"+ui.lot_finder.text()+"%'"
    issue_array = []
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    columnHeaders = ["Lot No.","Quantity","Good","NG"]
    for issue in db_con :
        issue_array.append(issue)
    if status == 0 :
        TableData(ui.incomeTableView, columnHeaders, issue_array)
        TableData(ui.incomeTableView_2, columnHeaders, issue_array)
    if status == 1 : 
        TableData(ui.incomeTableView_4, columnHeaders, issue_array)

def lot_id_box(ui) :
    f_select = "lot_no"
    t_select = "db_sde.devices_income_lot"
    c_select = "status = '0'"
    lot_id_array = []
    ui.boxlot_Box.clear()
    ui.boxlot_finder.clear()
    #ui.set_stage_boxlot_Box.clear()
    ui.boxlot_finder.addItem("Lot No.")
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    for lot_id_list in db_con :
        lot_id_array.append(lot_id_list)
    for lot_id_fill in lot_id_array :
        ui.boxlot_Box.addItem(lot_id_fill[0])
        ui.boxlot_finder.addItem(lot_id_fill[0])
        #ui.set_stage_boxlot_Box.addItem(lot_id_fill[0])
    pass

def finish_lot() :
    table_select = 'db_sde.devices_income_lot'
    value  = "status = '1'"
    condition = "status = '0'"
    a_lot_con = db_connect()
    a_lot_con.connect_update(table_select,value,condition)
     
#================================================================================================================================================================

# def issue_update(ui):
#     issue_input = ui.issue_input.text()
#     #error_type_text = ui.error_type.currentText()
#     error_type_index = ui.error_type.currentIndex()
#     error_type_text = ["","All","Actuator Controller 3CH","Sensor Controller"]
#     print(len(issue_input))
#     if len(issue_input) > 0  and error_type_index > 0 :
#         # ADD Data ===========================================================================================================
#         dt_string = get_date_time()
#         income_db = "('"+issue_input+"','"+error_type_text[error_type_index]+"','0','"+dt_string+"')"
#         print(income_db)
#         device_db_table = "db_sde.devices_income_issue"
#         device_sensor = db_connect()
#         device_sensor.connect_sql_insert(device_db_table,income_db)
#         # SHOW STATUS ========================================================================================================
#         ui.insign_status.setText(
#             "<span style=\"color:WHITE\">Status : </span></p>   <span style=\"color:#4CAF50\">Update Issue Success</span></p>")
#         # Clear Input ========================================================================================================
#         ui.error_type.setCurrentIndex(0)
#         ui.issue_input.clear()
#     else :
#         ui.insign_status.setText(
#             "<span style=\"color:WHITE\">Status : </span></p><span style=\"color:RED\">Invalid Data</span></p>")
#         ui.error_type.setCurrentIndex(0)
#         ui.issue_input.clear()
#     issue_list(ui)

# def issue_list(ui) :
#     f_select = "issue_name,device_type,qty_ng_product"
#     t_select = "db_sde.devices_income_issue"
#     c_select = None
#     issue_array = []
#     db_con = db_connect()
#     db_con.connect_select(t_select,c_select,f_select)
#     columnHeaders = ["Issue Name","Device Type","Quantity"]
#     for issue in db_con :
#         issue_array.append(issue)
#     TableData(ui.issue_list_table, columnHeaders, issue_array)
#     pass

# def set_issue_reject_box(ui) :
#     f_select = "issue_name"
#     t_select = "db_sde.devices_income_issue"
#     c_select = [None,"device_type = 'Actuator Controller' or device_type = 'All' ","device_type = 'Sensor Controller' or device_type = 'All' "]
#     issue_array = []
#     #ui.error_point_Box.clear()
#     db_con = db_connect()
#     db_con.connect_select(t_select,c_select[ui.error_type_box.currentIndex()],f_select)
#     for issue in db_con :
#         issue_array.append(issue)
#     for issue_fill in issue_array :
#         ui.error_point_Box.addItem(issue_fill[0])

#================================================================================================================================================================
# Table View = ui.devicesTableData
def TableData(tableView, columnHeaders, data):
    # Create a model and set it for the table view
    model = QStandardItemModel()
    tableView.setModel(model)

    # Set column headers
    model.setHorizontalHeaderLabels(columnHeaders)

    # Populate the model with data
    for row in data:
        item_list = [QStandardItem(str(item)) for item in row]
        model.appendRow(item_list)

    tableView.resizeColumnsToContents()

#================================================================================================================================================================
def addDevice_action(ui,qty_status,device_type):
        print(qty_status)
        print("=====================================================================================")
        action_case = ""
        lot_reject = ui.boxlot_Box.currentText()
        feild_select = 'qty_inspected'
        table_select = 'db_sde.devices_income_lot'
        condetion = "lot_no = '"+lot_reject+"'"
        qty_con = db_connect()
        qty_num = []
        qty_con.connect_select(table_select,condetion,feild_select)
        for qty in qty_con :
            qty_num.append(qty)
            pass
        print(qty_num)   
        if device_type :
                    print("ADD BAD Device")
                    if qty_status == 'ng_product' :
                        f_select = ['qty_ng_product',qty_status,'qty_inspected']
                        t_select = ["db_sde.devices_income_issue","db_sde.devices_income_lot","db_sde.devices_income_lot"]
                        c_select = ["issue_name = '"+action_case+"' ","lot_no = '"+lot_reject+"'","lot_no = '"+lot_reject+"'"]
                        rounds = ['0','1','2']
                    else :
                        f_select = [qty_status,'qty_inspected']
                        t_select = ["db_sde.devices_income_lot","db_sde.devices_income_lot"]
                        c_select = ["lot_no = '"+lot_reject+"'","lot_no = '"+lot_reject+"'"]
                        rounds = ['0','1']
                    for round in rounds :
                        round = int(round)
                        db_con = db_connect()
                        db_con.connect_select(str(t_select[round]),str(c_select[round]),str(f_select[round]))
                        for data in db_con : 
                            count_1 = int(data[0]) + 1
                            feild_data_reject = ""+str(f_select[round])+" = '"+str(count_1)+"'"
                            update_onlot_reject = db_connect()
                            update_onlot_reject.connect_update(str(t_select[round]),str(feild_data_reject),str(c_select[round]))
        else :
                    ui.flashStatusLabel.setText(
                        "Status : <span style=\"color:RED\">Select Device Type for Reject</span></p>")
                    pass 
#================================================================================================================================================================
def lot4export(ui) :
    table_select = 'db_sde.devices_income_lot'
    condetion = "status = '1' AND lot_no like '%"+ui.lot_finder.text()+"%'"
    feild_select = 'lot_no'
    a_lot_con = db_connect()
    ui.alive_lot_box.clear()
    a_lot_con.connect_select(table_select,condetion,feild_select)
    lot_list = []
    for lots in a_lot_con :
            ui.alive_lot_box.addItem(lots[0])
            lot_list.append(lots[0])
    ui.lot_finder.clear()  
       
def lot4display(ui) :
     print("checked")

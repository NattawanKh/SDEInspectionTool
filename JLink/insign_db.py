from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIntValidator,QStandardItemModel, QStandardItem
from sqlite_dbcon import db_connect
import JLink.ui_funciton as uif
from utils import *

def set_lineedit_int_only(line_edit):
    validator = QIntValidator()
    line_edit.setValidator(validator)
#================================================================================================================================================================
def incoming_device(ui):
    set_lineedit_int_only(ui.income_qt) 
    lot_no = ui.incom_date.text()
    device_qt  = ui.income_qt.text()
    null_space = 0
    null_space = str(null_space)
    if len(lot_no) >= 4 and device_qt != '' :
        # ADD Data ===========================================================================================================
        dt_string = get_date_time()
        income_db = "('"+lot_no+"','"+device_qt+"','"+null_space+"','"+null_space+"','"+null_space+"','"+null_space+"','"+dt_string+"')"
        device_db_table = "db_sde.devices_income_lot"
        device_sensor = db_connect()
        device_sensor.connect_sql_insert(device_db_table,income_db)
        # SHOW STATUS ========================================================================================================
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p>   <span style=\"color:#4CAF50\">Update Incoming Lot </span></p>")
        # Clear Input ========================================================================================================
        ui.income_qt.clear()
        ui.incom_date.clear()
    else :
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p><span style=\"color:RED\">Invalid Data</span></p>")
        ui.income_qt.clear()
        ui.incom_date.clear()
    incoming_list(ui)

def incoming_list(ui) :
    f_select = "lot_no,qty_product,qty_inspected,good_product,ng_product"
    t_select = "db_sde.devices_income_lot"
    c_select = "status = '0'"
    issue_array = []
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    columnHeaders = ["Lot No.","Quantity"," Inspected QTY","Good","NG"]
    for issue in db_con :
        issue_array.append(issue)
    TableData(ui.incomeTableView, columnHeaders, issue_array)

def lot_id_box(ui) :
    f_select = "lot_no"
    t_select = "db_sde.devices_income_lot"
    c_select = "status = '0'"
    lot_id_array = []
    ui.boxlot_Box.clear()
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    for lot_id_list in db_con :
        lot_id_array.append(lot_id_list)
    for lot_id_fill in lot_id_array :
        ui.boxlot_Box.addItem(lot_id_fill[0])
    pass

#================================================================================================================================================================

def issue_update(ui):
    issue_input = ui.issue_input.text()
    error_type_text = ui.error_type.currentText()
    error_type_index = ui.error_type.currentIndex()
    print(len(issue_input))
    if len(issue_input) > 0  and error_type_index > 0 :
        # ADD Data ===========================================================================================================
        print(issue_input)
        print(error_type_text)
        dt_string = get_date_time()
        income_db = "('"+issue_input+"','"+error_type_text+"','0','"+dt_string+"')"
        device_db_table = "db_sde.devices_income_issue"
        device_sensor = db_connect()
        device_sensor.connect_sql_insert(device_db_table,income_db)
        # SHOW STATUS ========================================================================================================
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p>   <span style=\"color:#4CAF50\">Update Issue Success</span></p>")
        # Clear Input ========================================================================================================
        ui.error_type.setCurrentIndex(0)
        ui.issue_input.clear()
    else :
        ui.insign_status.setText(
            "<span style=\"color:WHITE\">Status : </span></p><span style=\"color:RED\">Invalid Data</span></p>")
        ui.error_type.setCurrentIndex(0)
        ui.issue_input.clear()
    issue_list(ui)

def issue_list(ui) :
    f_select = "issue_name,device_type,qty_ng_product"
    t_select = "db_sde.devices_income_issue"
    c_select = None
    issue_array = []
    db_con = db_connect()
    db_con.connect_select(t_select,c_select,f_select)
    columnHeaders = ["Issue Name","Device Type","Quantity"]
    for issue in db_con :
        issue_array.append(issue)
    TableData(ui.issue_list_table, columnHeaders, issue_array)
    pass

def set_issue_reject_box(ui) :
    f_select = "issue_name"
    t_select = "db_sde.devices_income_issue"
    c_select = [None,"device_type = 'Actuator Controller' or device_type = 'All' ","device_type = 'Sensor Controller' or device_type = 'All' "]
    issue_array = []
    ui.error_point_Box.clear()
    db_con = db_connect()
    db_con.connect_select(t_select,c_select[ui.error_type_box.currentIndex()],f_select)
    for issue in db_con :
        issue_array.append(issue)
    for issue_fill in issue_array :
        ui.error_point_Box.addItem(issue_fill[0])

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
        action_case = ui.error_point_Box.currentText()
        lot_reject = ui.boxlot_Box.currentText()
        feild_select = 'qty_product,qty_inspected'
        table_select = 'db_sde.devices_income_lot'
        condetion = "lot_no = '"+lot_reject+"'"
        qty_con = db_connect()
        qty_con.connect_select(table_select,condetion,feild_select)
        for qty in qty_con :
            pass
        inspected_qty = str(qty[1]+1)
        if qty_status == 'ng_product' :
            device_type = ui.error_type_box.currentIndex() > 0
        else :
            device_type != ''   
        if device_type :
                    if qty_status == 'ng_product' :
                        uif.add_bad_device_event(ui,inspected_qty)
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
                            if round == 1 or round == 2 :
                                if int(qty[0]) == count_1 :
                                    qty_status_up = db_connect()
                                    status_up = "status = '1'"
                                    qty_status_up.connect_update(table_select,status_up,condetion)
                                    lot_id_box(ui)
                    if qty_status == 'ng_product' :
                        ui.flashStatusLabel.setText(
                            "Device Status : <span style=\"color:RED\">Rejected Case -  "+action_case+" </span></p>")      
                        pass
        else :
                    ui.flashStatusLabel.setText(
                        "Device Status : <span style=\"color:RED\">Select Device Type for Reject</span></p>")
                    pass
#================================================================================================================================================================

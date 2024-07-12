import os
import threading
import JLink.jlink as jlink
import JLink.log as log
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from utils import *
import JLink.serialReader as srr
import JLink.db_controller as db_controller
from sqlite_dbcon import db_connect

mac_id_list = []
mcu_data_list = []
header = ['Device ID', 'Note','Data']


def power_on_event(ui):
    ui.powerOnButton.setChecked(False) 
    ui.powerOffButton.setChecked(True) 
    jlink.power_on()


def power_off_event(ui):
    ui.powerOnButton.setChecked(True) 
    ui.powerOffButton.setChecked(False)
    jlink.power_off()

def flash_config(ui) :
    if ui.ap_enable.isChecked() and not ui.inspec_enable.isChecked():
        ap_flash_event(ui)
    else :
        flash_event(ui)
def erase_event(ui):
    recover = jlink.recover()
    erase = jlink.eraseall()
    if recover and erase :
        ui.flashStatusLabel.setText(
            "Erase Status : <span style=\"color:Green\">Erase Success</span></p>")
    else :
        ui.flashStatusLabel.setText(
            "Erase Status : <span style=\"color:RED\">Erase FAIL</span></p>")
    pass


def flash_event(ui):
    thr = threading.Thread(target=flashing_thread_callback, args=[ui])
    thr.start()
    ui.flashStatusLabel.setText(
        "Programming Status : <span style=\"color:orange\">In Progress</span></p>")


def flashing_thread_callback(ui):
    jlink.power_on()
    result = jlink.flash_program(os.path.join(
        "JLink/program_files", ui.programFileComboBox.currentText()))
    if result:
        ui.flashStatusLabel.setText(
            "Programming Status : <span style=\"color:green\">Success</span></p>")
        jlink.reset()
    else:
        ui.flashStatusLabel.setText(
            "Programming Status : <span style=\"color:red\">Fail</span></p>")

def ap_flash_event(ui):
    thr = threading.Thread(target=ap_flashing_thread_callback, args=[ui])
    thr.start()
    ui.flashStatusLabel.setText(
        "Programming Status : <span style=\"color:orange\">In Progress</span></p>")


def ap_flashing_thread_callback(ui):
    jlink.power_on()
    result = jlink.flash_program(os.path.join(
        "JLink/program_files", ui.programFileComboBox.currentText()))
    if result:
        ui.flashStatusLabel.setText(
            "Programming Status : <span style=\"color:green\">AP Programming Success</span></p>")
        jlink.protection()
    else:
        ui.flashStatusLabel.setText(
            "Programming Status : <span style=\"color:red\">AP Programming Fail</span></p>")


def program_combobox_click_event(ui):
    program_files_folder = "JLink/program_files"

    # Clear the current items in the combobox
    currentText = ui.programFileComboBox.currentText()
    ui.programFileComboBox.clear()

    # Check if the folder exists
    if os.path.exists(program_files_folder) and os.path.isdir(program_files_folder):
        # Get a list of file names in the folder
        file_names = os.listdir(program_files_folder)

        # Filter out only the files (not directories) and add them to the combobox
        for file_name in file_names:
            file_path = os.path.join(program_files_folder, file_name)
            if os.path.isfile(file_path):
                ui.programFileComboBox.addItem(file_name)
                ui.programFileComboBox.setCurrentText(currentText)

def add_good_device_event(ui):
    global mac_id_list
    jlink.power_on()
    mac_id = jlink.mac_id_check()
    if not mac_id:
        ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:red\">Read Device ID Fail</span></p>")
        return

    is_mac_id_duplicated = check_value_in_lists(mac_id_list, mac_id)

    if is_mac_id_duplicated:
        ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:red\">Device ID are Duplicated</span></p>")
        return
    else:
            srr.testing_event(ui)
    
    mac_id_list.append([mac_id, 'note'])
    if len(mac_id_list) == 3:
        log.write_csv(['macID', 'note'], mac_id_list, "JLink/database/devices.csv")
        for device in mac_id_list:
            log.update_print_label_by_mac_id(device[0])
        mac_id_list = []


    
def add_bad_device_event(ui):  #### UPDATE
    jlink.power_on()
    global mac_id_list
    global mcu_data_list
    global header
    device_id = jlink.mac_id_check()
    timestamp = get_date_time()
    if not device_id:
        ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:red\">Read Device ID Fail</span></p>")
        return
    is_mac_id_duplicated = check_value_in_lists(mac_id_list, device_id)
    if is_mac_id_duplicated:
        ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:red\">Device ID are Duplicated</span></p>")
        return
    else:
        device_type = ui.error_type_box.currentIndex()
        device_type_real = ["All","Actuator Controller 3CH","Sensor Controller"]
        db_controller.reject_device(ui,device_id,device_type_real[device_type],timestamp)
        note = ui.error_point_Box.currentText()
        mac_id_list.append([device_id, 'NG',note])
        if len(mac_id_list) == 3:
            mcu_data_list = []
        mcu_data_list.append([device_id, 'NG',note])
        if len(mac_id_list) == 3:
            log.write_csv(['macID', 'note'], mac_id_list, "JLink/database/devices.csv")
            for device in mac_id_list:
                print(device)
                log.update_print_label_by_mac_id(device[0])
            mac_id_list = []
            mcu_data_list = []
        populate_table_view(ui.devicesTableView, header, mcu_data_list)


def clear_list_event(ui):
    global mac_id_list
    global mcu_data_list
    mac_id_list = []
    mcu_data_list = []

    ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:green\">Clear Table</span></p>")
    populate_table_view(ui.devicesTableView, header, mac_id_list)


def print_now_event(ui):
    global mac_id_list
    global mcu_data_list
    log.write_csv(['macID', 'note'], mac_id_list, "JLink/database/devices.csv")
    for device in mac_id_list:
        log.update_print_label_by_mac_id(device[0])  # device 0 equal macId
    mac_id_list = []
    mcu_data_list = []

    populate_table_view(ui.devicesTableView, header, mac_id_list)
    ui.flashStatusLabel.setText(
            "Device Status : <span style=\"color:green\">Create Device Barcode</span></p>")

def onboard_data_ui(ui,type,data1,data2) :
    global mcu_data_list
    jlink.power_on()
    mac_id = jlink.mac_id_check()
    note = 'Good'
    pm_all = []
    scd_all = []
    level_all = []
    current_all = []
    if type == 'Sensor Controller' :
        if len(mcu_data_list) == 3:
            mcu_data_list = []
        header = ['Device ID', 'Note',' PM2.5(ug/m3) ',' CO2(ppm) ',' Temp(*C) ',' Humid(%) ']
        for pm in data1 :
            pm_all.append(pm)
        for scd in data2 :
            scd_all.append(scd)
        mcu_data_list.append([mac_id,note,pm_all[1],scd_all[0],scd_all[1],scd_all[2]])
        #populate_table_view(ui.devicesTableView, header, mcu_data_list)
        pass
    elif type == 'Actuator Controller 3CH' :
        if len(mcu_data_list) == 3:
            mcu_data_list = []
        for level in data1 :
            if level == '3' :
                level = 'HIGH'
            elif level == '2' :
                level = 'MID'
            elif level == '1' :
                level = 'LOW'
            else :
                level = 'OFF'
            level_all.append(level)
        for current in data2 :
             current_all.append(current)
        current_all = current_all[1:]
        print(current_all)
        header = [' Device ID ', 'Note',level_all[0],level_all[1], level_all[2], level_all[3]]
        mcu_data_list.append([mac_id,note,current_all[0],current_all[1],current_all[2],current_all[3]])
        pass
    # if len(mcu_data_list) == 3:
    #     mcu_data_list = []
    print(mcu_data_list)
    populate_table_view(ui.devicesTableView, header, mcu_data_list)

def populate_table_view(tableView, columnHeaders, data):
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

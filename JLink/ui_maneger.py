from JLink.ui_funciton import *
import serial.tools.list_ports
import JLink.serialReader as srr
import JLink.insign_db as insign_db 
from JLink.controller_data import *


def button_interface(ui):
    # Helper Functions
    def connect_buttons(buttons, function):
        for button in buttons:
            button.clicked.connect(function)
    def connect_pages(buttons, page):
        for button in buttons:
            button.clicked.connect(lambda: change_page(ui, page))
    # MENU BAR ===========================================================================
    populate_table_view(ui.devicesTableView, header, mac_id_list)
    onboard_show(ui)
    check_com_ports(ui)
    insign_db.set_issue_reject_box(ui)
    insign_db.lot_id_box(ui)
    #=====================================================================================
    ui.mini_menu.hide()
    connect_buttons([ui.big_menu_btn, ui.mini_menu_btn], lambda: check_com_ports(ui))
    connect_buttons([ui.big_controller_btn, ui.big_controller_btn], lambda: insign_db.lot_id_box(ui))
    connect_buttons([ui.big_db_btn, ui.mini_db_btn], lambda: onboard_show(ui))
    connect_pages([ui.big_controller_btn, ui.mini_controller_btn], 0)
    connect_pages([ui.big_db_btn, ui.mini_db_btn], 1)
    connect_pages([ui.big_insign_bt, ui.mini_insign_bt], 2)
    connect_buttons([ui.big_insign_bt], lambda: insign_db.incoming_list(ui))
    connect_buttons([ui.big_insign_bt], lambda: insign_db.issue_list(ui))
    connect_buttons([ui.mini_insign_bt], lambda: insign_db.incoming_list(ui))
    connect_buttons([ui.mini_insign_bt], lambda: insign_db.issue_list(ui))
    # Device Config Bar ==================================================================
    ui.powerOffButton.clicked.connect(lambda: power_on_event(ui))
    ui.powerOnButton.clicked.connect(lambda: power_off_event(ui))
    ui.inspec_enable.setChecked(True)
    ui.ap_enable.setChecked(True)
    # Serial Monitor Bar =================================================================
    connect_buttons([ui.serial_r], lambda: serial_switching_readMode(ui))
    connect_buttons([ui.serial_s], lambda: serial_switching_stopMode(ui))
    ui.error_type_box.currentIndexChanged.connect(lambda: insign_db.set_issue_reject_box(ui))
    ui.RejectButton.clicked.connect(lambda: reject_action(ui))
    # Controller Page ====================================================================
    connect_buttons([ui.flashButton], lambda: flash_config(ui))
    connect_buttons([ui.eraseButton], lambda: erase_event(ui))
    connect_buttons([ui.addGoodDeviceButton], lambda: addGood_action(ui))
    connect_buttons([ui.clearListButton], lambda: clear_list_event(ui))
    connect_buttons([ui.printNowButton], lambda: print_now_event(ui))
    # Insign Page ========================================================================
    connect_buttons([ui.income_submit], lambda: insign_db.incoming_device(ui))
    connect_buttons([ui.update_issue_bt], lambda: insign_db.issue_update(ui))
    # Controller Data ====================================================================
    connect_buttons([ui.controller_finder], lambda: onboard_show(ui))

def addGood_action(ui) :
    print(ui.boxlot_Box.count())
    if ui.boxlot_Box.count() :
        add_good_device_event(ui)
    else :
        ui.flashStatusLabel.setText(
        "Device Status : <span style=\"color:RED\">Not Found Lot No.</span></p>")


def reject_action(ui) :
    print(ui.boxlot_Box.count())
    if ui.boxlot_Box.count() > 0 :
        qty_status = 'ng_product'
        controller_type  = ui.error_type_box.count()
        insign_db.addDevice_action(ui,qty_status,controller_type)
    else :
        ui.flashStatusLabel.setText(
        "Device Status : <span style=\"color:RED\">Not Found Lot No.</span></p>")

def check_com_ports(ui):
    com_ports = serial.tools.list_ports.comports()
    ui.uart_portBox.clear()
    if com_ports:
        #print("Available COM Ports:")
        for port in com_ports:
            #print(port.device)
            ui.uart_portBox.addItem(port.device)
    else:
        ui.label_28.setText(
            "Serial Monitor Status : <span style=\"color:RED\">No COM Ports available.</span></p>")
        print("No COM Ports available.")

def ComboBoxInitialize(ui):
    program_combobox_click_event(ui)

def change_page(ui, index):
    ui.main_page.setCurrentIndex(index)
    page_color(ui)
    check_com_ports(ui)
        

def page_color(ui):
    index = ui.main_page.currentIndex()
    highlight = "text-align:left;color:white;background-color:#222222;border-radius: 0px;padding: 5px 10px;background-color: #f44336;"
    un_highlight = "text-align:left;color:white;background-color:#222222;border-radius: 0px;padding: 5px 10px;"

    buttons = [(ui.big_controller_btn, ui.mini_controller_btn),
               (ui.big_db_btn, ui.mini_db_btn),
               (ui.big_insign_bt, ui.mini_insign_bt)]

    for i, (big_btn, mini_btn) in enumerate(buttons):
        style = highlight if index == i else un_highlight
        big_btn.setStyleSheet(style)
        mini_btn.setStyleSheet(style)

def serial_switching_readMode(ui) :
    srr.start_reading(ui)
    ui.serial_r.setChecked(True)
    ui.serial_s.setChecked(False)
    pass

def serial_switching_stopMode(ui) :
    srr.stop_reading(ui)
    ui.serial_s.setChecked(True)
    ui.serial_r.setChecked(False)
    pass
'''
 Read Serial Port For Inspection Data From All Controller Board
 (c) All Right Reserved SDE Inspection Software 2024
'''

import serial
import struct
import JLink.jlink as jlink
from utils import *
import threading
import JLink.ui_funciton as uif
import JLink.db_controller as db_mcu
from PyQt5 import QtGui
import time
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtGui import QTextCursor

# Define the serial port and baudrate
baud_rate = 115200
# All-Porpose Variable =================================
dt_string = get_date_time()

def testing_event(ui):
    thr = threading.Thread(target=ReadSerial_Controller, args=[ui])
    thr.start() 
    ui.flashStatusLabel.setText(
            "<span style=\"color:orange\">Inspection In Progress </span></p>")

# Read Serial Port =====================================
def ReadSerial_Controller(ui):
    # Actuator Variable ====================================
    act_stack = []
    curr_stack = []
    # Actuator Variable ====================================
    scd_stack = []
    pm_stack = []
    start = True
    device_type = 'Incomming Controlller Board'
    serial_port = ui.uart_portBox.currentText()
    print(serial_port)
    try:
        # Create a serial object
        jlink.reset()
        ser = serial.Serial(serial_port, baud_rate)
        print("Status : Serial port opened successfully.")
        while start:
            # Read a line from the serial port
            #line = ser.readline().decode('utf-8').strip()
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
# the received Sensor Data ==========================================================================================
            if line.startswith('<info> app: sensor type co2,temp,humid:'):
                device_type = 'Sensor Controller'
                sensor_data = line.strip()
                raw_data = sensor_data[40:]
                if raw_data.startswith("2") :
                    pm_array = raw_data.split(',')
                    pm_array = pm_array[1:]
                    for pm in pm_array :  
                        pm_pack = struct.pack('I', int(pm))
                        pm_float = struct.unpack('f', pm_pack)[0]
                        pm_float = int(pm_float)
                        pm_stack.append(pm_float)
                    #print(pm_stack)
                if raw_data.startswith("3") :
                    scd_array = raw_data.split(',')
                    scd_array = scd_array[1:]
                    #print(scd_array)
                    for scd in scd_array :  
                        scd_pack = struct.pack('I', int(scd))
                        scd_float = struct.unpack('f', scd_pack)[0]
                        scd_float = int(scd_float)
                        scd_stack.append(scd_float)
                    #print(scd_stack)
                    end_process_(ui,device_type,pm_stack,scd_stack)
                    break
# the received Actuator Data ================================================================================================
            # Level Switch ================================
            elif line.startswith('<info> app: Relay output'):
                device_type = 'Actuator Controller 3CH'
                act_data = line.strip()
                act_stat = act_data[25:]
                act_cn_lv = len(act_stack)
                if act_cn_lv < 5 :
                 act_stack.append(act_stat)
            # Current ======================================= 
            elif line.startswith('<info> app: Current output'):
                device_type = 'Actuator Controller 3CH'
                act_curr = line.strip()
                act_amp = act_curr[27:]
                act_cn = len(curr_stack)
                if act_cn < 5 :
                 curr_stack.append(act_amp)
        #====================================================
            end_process_act = len(curr_stack)
        # Actuator Controller End Message ================================
            #if device_type.startswith('Actuator Controller 3CH') :
            if end_process_act == 5 :
                print("End Level")
                end_process_(ui,device_type,act_stack,curr_stack)
                break
    except serial.SerialException as e:
        print("Error opening or reading serial port:", e)

    finally:
        # Close the serial port
        if ser.is_open:
            ser.close()
            print("Status : Serial port are closed.")
def end_process_(ui,controller_type,first_stack,second_stack):
        mac_id = jlink.mac_id_check()
        uif.onboard_data_ui(ui,controller_type,first_stack,second_stack)
        db_mcu.device_update(ui,mac_id,controller_type,first_stack,second_stack)
        if ui.ap_enable.isChecked()  :
            jlink.protection()
            ui.flashStatusLabel.setText(
                "<span style=\"color:green\">Inspection Complete | Protection : On</span></p>")
        else :
            ui.flashStatusLabel.setText(
                "<span style=\"color:green\">Inspection Complete | </span></p>""<span style=\"color:RED\"> Protection : Off</span></p>")
#==================================================================================================================================================================================
# Flag to control the reading process
reading = False
# Create a QObject class to handle signals
class SerialReader(QObject):
    new_data = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, port, baud_rate):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.reading = False

    def start_reading(self):
        self.reading = True
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.read_from_port)
        self.thread.start()

    def stop_reading(self):
        self.reading = False
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

    def read_from_port(self):
        try:
            ser = serial.Serial(self.port, self.baud_rate)
        except Exception as e:
            self.error_occurred.emit(f"Error opening serial port: {e}")
            return
        
        while self.reading:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    self.new_data.emit(line)
                    time.sleep(0.005)  # Sleep for 5 milliseconds
            except Exception as e:
                self.error_occurred.emit(f"Error reading from serial port: {e}")
                break

        ser.close()

# Function to start reading
def start_reading(ui):
    global serial_reader
    serial_port = ui.uart_portBox.currentText()
    serial_reader = SerialReader(serial_port, baud_rate)
    serial_reader.new_data.connect(lambda line: update_ui(ui, line))
    serial_reader.error_occurred.connect(lambda error: ui.serial_monitor.append(error))
    serial_reader.start_reading()
    ui.serial_monitor.append("Started reading from the serial port.")

# Function to stop reading
def stop_reading(ui):
    global serial_reader
    if serial_reader.reading:
        serial_reader.stop_reading()
        ui.serial_monitor.append("Stopped reading from the serial port.")

# Function to update the UI
def update_ui(ui, line):
    ui.serial_monitor.append(line)
    ui.serial_monitor.moveCursor(QTextCursor.End)
    ui.serial_monitor.ensureCursorVisible()
#=============================================================================================================================================================================================================================================================================================================================================================================================
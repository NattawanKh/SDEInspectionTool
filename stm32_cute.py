from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer
import os

firmware_path_list = []

def flash_firmware(file_path, target_type='STM32G070KBTx'):
    try:
        # Attempt to connect with the specified target type
        with ConnectHelper.session_with_chosen_probe(target_override=target_type) as session:
            programmer = FileProgrammer(session)
            
            if file_path.endswith('.bin'):
                programmer.program(file_path, file_format='bin')
                print(f"Binary firmware {file_path} flashed successfully.")
            elif file_path.endswith('.hex'):
                programmer.program(file_path, file_format='hex')
                print(f"Hex firmware {file_path} flashed successfully.")
            else:
                print(f"Unsupported file type: {file_path}")
                
    except Exception as e:
        print(f"An error occurred while flashing firmware: {e}")

def firmware_combobox__event():
    processor_firmware = "processor_firmware"
    firmware_list = []

    if os.path.exists(processor_firmware) and os.path.isdir(processor_firmware):
        file_names = os.listdir(processor_firmware)

        for file_name in file_names:
            file_path = os.path.join(processor_firmware, file_name)
            if os.path.isfile(file_path):
                firmware_path_list.append(file_path)
                firmware_list.append(file_name)

    #print(firmware_list)
    return firmware_path_list

# Fetch firmware paths
firmware_combobox__event()
fw_paths = firmware_combobox__event()

# Flash firmware files
#for fw_path in fw_paths:
flash_firmware(fw_paths[0], target_type='STM32G070KBTx')

from pyocd.core.helpers import ConnectHelper

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

def detect_target():
    try:
        # Connect to the first available probe
        session = ConnectHelper.session_with_chosen_probe(blocking=False, target_override='stm32g070rbtx')
        if session is None:
            print("Failed to open session with the probe.")
            return

        try:
            session.open()
            target_type = session.board.target_type
            unique_id = session.board.unique_id
            print(f"Detected target: {target_type}")
            print(f"Unique ID: {unique_id}")

        finally:
            # Close the session
            session.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    detect_target()
    # Fetch firmware paths
    firmware_combobox__event()
    fw_paths = firmware_combobox__event()
    # Flash firmware files
    #for fw_path in fw_paths:
    flash_firmware(fw_paths[0], target_type='STM32G070KBTx')

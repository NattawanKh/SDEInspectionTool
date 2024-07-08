import pylink

def detect_stm32g070_with_pylink():
    # Initialize a JLink object
    jlink = pylink.JLink()

    # Get connected devices
    devices = jlink.connected_emulators()

    # Print all connected devices for debugging
    print("Connected devices:")
    for device in devices:
        print(device)

    # Look for STLink V2 (JTAG/SWD) connected to an STM32G070 MCU
    for device in devices:
        if device[0] == pylink.enums.JLinkInterfaces.SWD and device[1] == pylink.enums.JLinkDeviceFamilies.STM32 and "STM32G070" in device[2]:
            print(f"Found STM32G070KBTx MCU connected via STLink V2 ({device[2]})")
            return True

    print("No STM32G070KBTx MCU detected with STLink V2 using pylink")
    return False

# Detect and connect to STM32G070KBTx with STLink V2 using pylink
detect_stm32g070_with_pylink()

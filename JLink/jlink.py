'''
 JLink Function Command 
 (c) All Right Reserved SDE Inspection Software 2024
'''

import subprocess

def recover() :
    recover = "nrfjprog --recover --family NRF52  \n"
    try:
    # Execute the command
        subprocess.run(recover, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)

def reset() :
    reset = "nrfjprog --reset --family NRF52  \n"
    try:
    # Execute the command
        subprocess.run(reset, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)

def eraseall() :
    eraseall = "nrfjprog -f NRF52 --eraseall \n"
    try:
    # Execute the command
        subprocess.run(eraseall, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        pass


def protection() :
    protection = "nrfjprog -f NRF52 --rbp ALL  \n"
    try:
    # Execute the command
        subprocess.run(protection, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
    pass

def mac_id_check():
    # Define the nrfjprog command you want to run
    #recover()
    command = "nrfjprog --memrd 0x10000060 --n 8 --family nrf52 "
    mac_id = ""

    # Run the command and capture the return code
    try:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result)
        mac_id = "F4CE36" + \
            result.stdout.split(" ")[1][6:] + result.stdout.split(" ")[2]
        print(mac_id)
    except Exception as e:
        print("Cant Read macID with jprog")
        print("An error occurred:", e)
    return mac_id


def power_on():
    jlink_process = subprocess.Popen("jlink", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Send the "power on" command
    command = "power on\n"  # Add '\n' to simulate pressing Enter
    jlink_process.stdin.write(command)
    jlink_process.stdin.flush()

    # Read the response from J-Link (if needed)
    output, error = jlink_process.communicate()

    # Close the subprocess
    jlink_process.stdin.close()
    jlink_process.stdout.close()
    jlink_process.stderr.close()
    jlink_process.wait()


def power_off():
    jlink_process = subprocess.Popen(
        "jlink", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Send the "power on" command
    command = "power off\n"  # Add '\n' to simulate pressing Enter
    jlink_process.stdin.write(command)
    jlink_process.stdin.flush()

    # Read the response from J-Link (if needed)
    output, error = jlink_process.communicate()

    # Close the subprocess
    jlink_process.stdin.close()
    jlink_process.stdout.close()
    jlink_process.stderr.close()
    jlink_process.wait()


def flash_program(hex_name):
    recover()
    eraseall()
    erase_command = 'nrfjprog -e'
    result = subprocess.run(
        erase_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result)
    # Define the nrfjprog command you want to run
    command = f"nrfjprog -f nrf52 --program ./{hex_name} --verify --reset"
    #command = f"nrfjprog -f nrf52 --program ./{hex_name} --sectorerase"
    print(command)

    is_ok = 0

    # Run the command and capture the return code
    try:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if "Verify file - Done verifying" in result.stdout:
            is_ok = 1
        else:
            is_ok = 0

    except Exception as e:
        print("Cant Read macID with jprog")
        print("An error occurred:", e)
    return is_ok


if __name__ == "__main__":
    # JLink_Power_On()
    pass
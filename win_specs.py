""" Python script to gather data about device's (on which it is run) specifications """
import wmi
import re

c = wmi.WMI()

def get_list_serial():
    """ WMI call to gather identifying number """
    serial = []
    serial.append(c.Win32_ComputerSystemProduct()[0].IdentifyingNumber)
    for i in serial.copy():
        if i == "System Serial Number":
            serial.remove(i)
    return serial

def get_list_cpu():
    """ WMI call to gather CPU info """
    cpu = None
    for i in c.Win32_Processor():
        if cpu is None:
            cpu = []
        cpu.append(i.Name)
    return cpu

def get_list_gpu():
    """ WMI call to gather GPU info """
    gpu = None
    for i in c.Win32_VideoController():
        if i.name[len(i.name)-2:] == "GB" or i.name[len(i.name)-2:] == "MB":
            if gpu is None:
                gpu = []
            gpu.append(i.name)
            continue
        video_adapter_str = i.name + " "
        if int(i.AdapterRam)/1024/1024 > 2047:
            video_adapter_str +=  str(round(int(i.AdapterRam)/1024/1024/1024)) + " GB"
        else:
            video_adapter_str +=  str(round(int(i.AdapterRam)/1024/1024)) + " MB"
        gpu.append(video_adapter_str)
    return gpu

def get_list_ram():
    """ WMI call to gather RAM info """
    map_memory_type = {
        "0": "Unknown",
        "1": "Other",
        "2": "DRAM",
        "3": "Synchronous DRAM",
        "4": "Cache DRAM",
        "5": "EDO",
        "6": "EDRAM",
        "7": "VRAM",
        "8": "SRAM",
        "9": "RAM",
        "10": "ROM",
        "11": "Flash",
        "12": "EEPROM",
        "13": "FEPROM",
        "14": "EPROM",
        "15": "CDRAM",
        "16": "3DRAM",
        "17": "SDRAM",
        "18": "SGRAM",
        "19": "RDRAM",
        "20": "DDR",
        "21": "DDR2",
        "22": "DDR2 FB-DIMM",
        # 23 not present
        "24": "DDR3",
        "25": "FBD2",
        "26": "DDR4"
    }
    ram = None
    for i in c.Win32_PhysicalMemory():
        memory_string = ""
        memory_string += str(round(int(i.Capacity)/1024/1024/1024)) + " GB " + str(i.Speed) + " MHz " + map_memory_type[str(i.SMBIOSMemoryType)]

        memory_string = re.sub(' +', ' ', memory_string)
        memory_string = "".join(memory_string.rstrip().lstrip())
        if ram is None:
            ram = []
        ram.append(memory_string)
    return ram

def get_list_storage():
    """ WMI call to gather Storage device(s) info """
    storage = None
    for i in c.Win32_DiskDrive():
        if i.InterfaceType in ("IDE", "SCSI"):
            if storage is None:
                storage = []
            storage.append(i.Model)
    return storage

def get_list_os_attributes_system_name():
    """ WMI call to gather OS info (system_name) """
    system_name = None
    for i in c.Win32_OperatingSystem():
        if system_name is None:
            system_name = []
        system_name.append(i.CSName)
    return system_name

def get_list_os_attributes_os_version():
    """ WMI call to gather OS info (os_version) """
    os_version= None
    for i in c.Win32_OperatingSystem():
        if os_version is None:
            os_version= []
        os_version.append(i.Name.split("|")[0])
    return os_version

def get_list_system_accounts():
    """ WMI call to gather OS Users info """
    system_accounts = None
    for i in c.Win32_UserAccount():
        if system_accounts is None:
            system_accounts = []
        system_accounts.append(i.Name)
    return system_accounts

def main():
    """ the function which will make calls to other functions to gather specs """
    payload = {
        "SERIAL": get_list_serial(),
        "OS": get_list_os_attributes_os_version(),
        "SYSTEM_NAME": get_list_os_attributes_system_name(),
        "USERS": get_list_system_accounts(),
        "CPU": get_list_cpu(),
        "GPU": get_list_gpu(),
        "RAM": get_list_ram(),
        "STORAGE": get_list_storage()
    }

    # Beautiful print
    for part, values in payload.items():
        print(part)
        for value in values:
            print("    " + value)

if __name__ == "__main__":
    main()

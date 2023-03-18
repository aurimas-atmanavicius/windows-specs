import wmi
import re

c = wmi.WMI()

def get_list_cpu():
    cpu = None
    for iter in c.Win32_Processor():
        if cpu == None:
            cpu = []
        cpu.append(iter.Name)
    return cpu

def get_list_gpu():
    gpu = None
    for iter in c.Win32_VideoController():
        if iter.name[len(iter.name)-2:] == "GB" or iter.name[len(iter.name)-2:] == "MB":
            if gpu == None:
                gpu = []
            gpu.append(iter.name)
            continue
        videoAdapterString = iter.name + " "
        if int(iter.AdapterRam)/1024/1024 > 2047:
            videoAdapterString +=  str(round(int(iter.AdapterRam)/1024/1024/1024)) + " GB"
        else:  
            videoAdapterString +=  str(round(int(iter.AdapterRam)/1024/1024)) + " MB"
        gpu.append(videoAdapterString)
    return gpu

def get_list_ram():
    memoryFormFactorMAP = {
        "0": "Unknown",
        "1": "Other",
        "2": "SIP",
        "3": "DIP",
        "4": "ZIP",
        "5": "SOJ",
        "6": "Proprietary",
        "7": "SIMM",
        "8": "DIMM",
        "9": "TSOP",
        "10": "PGA",
        "11": "RIMM",
        "12": "SODIMM",
        "13": "SRIMM",
        "14": "SMD",
        "15": "SSMP",
        "16": "QFP",
        "17": "TQFP",
        "18": "SOIC",
        "19": "LCC",
        "20": "PLCC",
        "21": "BGA",
        "22": "FPBGA",
        "23": "LGA"
    }
    memoryTypeMAP = {
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
    for iter in c.Win32_PhysicalMemory():
        memoryString = ""
        memoryString += str(round(int(iter.Capacity)/1024/1024/1024)) + " GB " + str(iter.Speed) + " MHz " + memoryTypeMAP[str(iter.SMBIOSMemoryType)]

        memoryString = re.sub(' +', ' ', memoryString)
        memoryString = "".join(memoryString.rstrip().lstrip())
        if ram == None:
            ram = []
        ram.append(memoryString)
    return ram

def get_list_storage():
    storage = None
    for iter in c.Win32_DiskDrive():
        if iter.InterfaceType == "IDE" or iter.InterfaceType == "SCSI":
            if storage == None:
                storage = []
            storage.append(iter.Model)
    return storage

def get_list_OS_attributes():
    systemName = None
    os = None
    for iter in c.Win32_OperatingSystem():
        if systemName == None:
            systemName = []
        if os == None:
            os = []

        systemName.append(iter.CSName)
        os.append(iter.Name.split("|")[0])
    return os, systemName

def get_list_systemAccounts():
    systemAccounts = None
    for iter in c.Win32_UserAccount():
        if systemAccounts == None:
            systemAccounts = []
        systemAccounts.append(iter.Name)
    return systemAccounts

def main():
    payload = {
        "SERIAL": None,
        "OS": None,
        "SYSTEM_NAME": None,
        "USERS": None,
        "CPU": None,
        "GPU": None,
        "RAM": None,
        "STORAGE": None
    }
    payload["SERIAL"] = c.Win32_ComputerSystemProduct()[0].IdentifyingNumber
    if payload["SERIAL"] == "System Serial Number":
        del payload["SERIAL"]

    payload["OS"], payload["SYSTEM_NAME"] = get_list_OS_attributes()
    payload["USERS"] = get_list_systemAccounts()

    payload["CPU"] = get_list_cpu()
    payload["GPU"] = get_list_gpu()
    payload["RAM"] = get_list_ram()
    payload["STORAGE"] = get_list_storage()
    
    # Beautiful print
    for part in payload:
        print(part)
        for identifier in payload[part]:
            print("    " + identifier)

if __name__ == "__main__":
    main()

import wmi
import re

c = wmi.WMI()

payload = {
    "SERIAL": None,
    "CPU": None,
    "GPU": None,
    "RAM": None,
    "STORAGE": None
}
payload["SERIAL"] = c.Win32_ComputerSystemProduct()[0].IdentifyingNumber

if payload["SERIAL"] == "System Serial Number":
    del payload["SERIAL"]

for iter in c.Win32_Processor():
    if payload["CPU"] == None:
        payload["CPU"] = []
    payload["CPU"].append(iter.Name)

for iter in c.Win32_VideoController():
    if iter.name[len(iter.name)-2:] == "GB" or iter.name[len(iter.name)-2:] == "MB":
        if payload["GPU"] == None:
            payload["GPU"] = []
        payload["GPU"].append(iter.name)
        continue
    videoAdapterString = iter.name + " "
    if int(iter.AdapterRam)/1024/1024 > 2047:
        videoAdapterString +=  str(round(int(iter.AdapterRam)/1024/1024/1024)) + " GB"
    else:  
        videoAdapterString +=  str(round(int(iter.AdapterRam)/1024/1024)) + " MB"
    payload["GPU"].append(videoAdapterString)

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

for iter in c.Win32_PhysicalMemory():
    memoryString = ""
    memoryString += str(round(int(iter.Capacity)/1024/1024/1024)) + " GB " + str(iter.Speed) + " MHz " + memoryTypeMAP[str(iter.SMBIOSMemoryType)]

    memoryString = re.sub(' +', ' ', memoryString)
    memoryString = "".join(memoryString.rstrip().lstrip())
    if payload["RAM"] == None:
        payload["RAM"] = []
    payload["RAM"].append(memoryString)

for iter in c.Win32_DiskDrive():
    if iter.InterfaceType == "IDE" or iter.InterfaceType == "SCSI":
        if payload["STORAGE"] == None:
            payload["STORAGE"] = []
        
        payload["STORAGE"].append(iter.Model)


# Beautiful print
for part in payload:
    print(part)
    for identifier in payload[part]:
        print("    " + identifier)


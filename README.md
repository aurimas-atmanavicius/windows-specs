# windows-specs
## Description
This code retrieves computer's, running Windows OS, hardware specifications via Windows Management Instrumentation (WMI). You can read more WMI [here](https://learn.microsoft.com/en-us/windows/win32/wmisdk/about-wmi).

The information printed out via the code is:
* Serial number (if exists)
* Operating system
* Device name (as SYSTEM_NAME)
* Computer user(s)
* CPU model(s)
* GPU model(s)
* RAM information
* Storage device(s)

## Prerequisites
* **Python 3**
* **wmi** (Python package)

To get WMI, use this command:
```
pip3 install wim
```

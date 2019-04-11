# NIR Scan Nano Python Driver
This is a logging system designed to support taking and logging scans captured using the NIR Nano spectrometer by TI.  It also includes support for logging from the Bosch CISS, and the warp platform.

## Usage
### Requirements
In order to use these scripts, it is reccomended to run the scripts using a venv, where all the requirements from the `requirements.txt` can be installed independently of other Python installations on the machine.  The 'main' logging script is sesame_log.py

In order to support logging from the NIRScan Nano, the DLPSpectrumLibrary will need to be installed, and compiled on the computer.  These python scripts require a dynamic library to be compiled, which is then wrapped using the python ctypes library. 
This dynamic library can be compiled using the following steps on MacOS.  Instructions for linux and windows can be found online.
```
gcc -c -DTPL_NOLIB -Wall dlpspec.c dlpspec_scan.c dlpspec_calib.c dlpspec_util.c tpl.c dlpspec_scan_col.c dlpspec_scan_had.c dlpspec_helper.c
clang -dynamiclib -o libtest.dylib dlpspec.o dlpspec_scan.o dlpspec_calib.o dlpspec_util.o tpl.o dlpspec_scan_had.o dlpspec_scan_col.o dlpspec_helper.o
rm *.o
```
Currently, the full path of the c library is referred to in test_dll.py, and should be updated to reflect the installation.

### File Breakdown
#### sesame_log.py
This program uses a complete CLI to make directories in the sesame-0000000000000xxx format,
create a matching repo on the physcomplab git organisation, and facilitate the logging of data 
from: Spectrometers, CISSs, and (In Progress, warp via the jlink library).

Example command:
```
python sesame_log.py --create_repo --logging_level deBug --directory_index 17 log --ciss /dev/tty.usbmodem144210 --ciss /dev/tty.usbmodem144211 --spectrometer 0 --timeout_mins 1
``` 
The first three parameters are used to setup the repo.  This currently creates the folder within the current directory, 
in this case, it will create a repote repo on github, and commit the readme as the first commit.
The directory index created the folder name in the designated format, and the logging level is set.

The `log` command starts the log part of the program, now the settings for a repo have been defined.
Here, two CISS devices are initalised (With the relevant com port passed as a parameter for each), 
and the spectrometer initialised, with the s/n set to zero.  This will work for one spectrometer, and a serial number
can be passed if working with more than one device (untested).  

Note: This has currently not been tested on a fresh install.  I forsee some errors with:
git not being installed on the system / setup with a default user
multiple devices

#### Data manipulation scripts 
export_json_csv.py - take the .JSON files produced for each scan, and aggregate them into a .csv file

plot_3d_json.py - plots of the amplitude - wavelength diagrams

others - not too sure, there may be something usefull here

#### Behind the scenes
start_print.py - old logging script - more barebones, may be broken due to changes in start functions.

usb.py - Handles read and writes to the spectrometer using the NIRscan USB protocol

scan.py - Completes a scan on the spectrometer

test_dll.py - converts the .dat from scan.py into a json object.

CissUsbConnectord.py - CISS logging stuff.

## Issues
- Refactor the logging functions out to individual folders for each of CISS / Spectrometer / Warp (Files are a mess, and what does what is complicated!  -  This was a result of a constant evolution, i'm sorry) 
- location of DLPSpectrumLibrary should be a enviroment variable, or something more sensible
- Warp logger doesn't support hotplug disconnect / reconnect
- Add an option to the log function to commit every 'n' minutes (should probably make commit* a function of fileStructure class)
- Spectrometer logger currently uses the last set scan profile.  This could be changed, but need to remember to keep this consistent.


## Notes and References
#### Spectrometer reading
For information on the scan workflow; look at section 5.2.1 of the DLP® NIRscan™ Nano EVM User's Guide.

For information on the USB commands; refer to section H.1 of the DLP® NIRscan™ Nano EVM User's Guide.

Details on `ctrl_transfer` in the `PyUSB` library: https://www.beyondlogic.org/usbnutshell/usb6.shtml#SetupPacket

Details on writing / reading: https://stackoverflow.com/questions/29345325/raspberry-pyusb-gets-resource-busy

USB communication example for another product using python/PyUSB: https://github.com/respeaker/respeaker_python_library/blob/master/respeaker/usb_hid/pyusb_backend.py 

Cython HIDAPI:
https://github.com/trezor/cython-hidapi
After much experimentation, this has been used instead of PyUSB.  This library works on MacOS, and provides a more simple interface with the HID device type.

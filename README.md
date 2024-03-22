# CANedge MF4 to XLSX converter
A quick MF4 to Excel converter using a DBC file for the University of Nottingham Racing Team.

## Usage
```
usage: CANedge2xlsx.py [-h] [mdf_filename] [xlsx_filename] [dbc_filename]

Convert MF4 files from datalogger to Excel spreadsheets

positional arguments:
  mdf_filename   MF4 file to be converted to XLSX. Default: data.mf4
  xlsx_filename  XLSX file to be generated. Default: data
  dbc_filename   CAN database file. Default: 2023.dbc

options:
  -h, --help     show this help message and exit
```
Example - 
```shell
$ CANedge2xlsx.py 00000002.MF4 data 2023.dbc
```

## Requirements 
```
# pip
pandas
canmatrix
can_decoder
mdf_iter
openpyxl
cython # Optional - required to make compiled executable
```

## Executable binares
The instructions below are for compiling the Python code to a executable binares on Linux. 
This is not for performance, but for ease of use.
It is worth exploring how to do this on/for Windows
### Compilation (for Linux)
Convert .py to .c using cython
```shell
$ cython CANedge2xlsx.py --embed
```
Create python library version variable (for linker)
```shell
$ PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)
```
Compile binary
```shell
$ gcc -O $(python3-config --includes) CANedge2xlsx.c -o CANedge2xlsx $(python3-config --ldflags) -l$PYTHONLIBVER
```

## Performance notes

Linux (Python)   - ~30 seconds
Linux (Compiled) - ~36 seconds
Windows (Python) - ~65 seconds

### Test systems - Linux 
```
                            ....               user@host
              .',:clooo:  .:looooo:.           ----------------
           .;looooooooc  .oooooooooo'          OS: Ubuntu jammy 22.04 x86_64
        .;looooool:,''.  :ooooooooooc          Host: Windows Subsystem for Linux - Ubuntu (2.0.14.0)
       ;looool;.         'oooooooooo,          Kernel: 5.15.133.1-microsoft-standard-WSL2
      ;clool'             .cooooooc.  ,,       Uptime: 18 hours, 29 mins
         ...                ......  .:oo,      Packages: 1447 (dpkg), 5 (snap)
  .;clol:,.                        .loooo'     Shell: zsh 5.8.1
 :ooooooooo,                        'ooool     Display (westonrdp): 2560x1600 @ 60Hz
'ooooooooooo.                        loooo.    WM: WSLg (Wayland)
'ooooooooool                         coooo.    Theme: Yaru [GTK3]
 ,loooooooc.                        .loooo.    Icons: Yaru [GTK3]
   .,;;;'.                          ;ooooc     Terminal: Windows Terminal
       ...                         ,ooool.     Terminal Font: MesloLGS NF (12pt)
    .cooooc.              ..',,'.  .cooo.      CPU: 13th Gen Intel(R) Core(TM) i7-13700HX (24) @ 2.30 GHz
      ;ooooo:.           ;oooooooc.  :l.       GPU: llvmpipe (LLVM 15.0.7, 256 bits)
       .coooooc,..      coooooooooo.           Memory: 2.05 GiB / 15.49 GiB (13%)
         .:ooooooolc:. .ooooooooooo'           Swap: 0 B / 4.00 GiB (0%)
           .':loooooo;  ,oooooooooc            Disk (/): 58.69 GiB / 1006.85 GiB (6%) - ext4
               ..';::c'  .;loooo:'             Disk (/mnt/c): 836.79 GiB / 952.59 GiB (88%) - 9p
                             .                 Local IP (eth0): x.x.x.x/x *
                                               Battery: 79% [Charging]
                                               Locale: C.UTF-8
```

### Test systems - Windows 
```
/////////////////  /////////////////    user@host
/////////////////  /////////////////    ----------------
/////////////////  /////////////////    OS: Windows 11 (Home) x86_64
/////////////////  /////////////////    Host: Predator PH16-71 (V1.16)
/////////////////  /////////////////    Kernel: 10.0.22621.3296 (22H2)
/////////////////  /////////////////    Uptime: 19 hours, 40 mins
/////////////////  /////////////////    Packages: 1 (choco)
/////////////////  /////////////////    Shell: Windows PowerShell 5.1.22621.2506
                                        Display (xxxxxxx): 2560x1600 @ 83Hz (as 1707x1067) [Built-in]
/////////////////  /////////////////    DE: Fluent
/////////////////  /////////////////    WM: Desktop Window Manager
/////////////////  /////////////////    WM Theme: Custom - #68580D (System: Dark, Apps: Dark)
/////////////////  /////////////////    Icons:
/////////////////  /////////////////    Font: Segoe UI (12pt) [Caption / Menu / Message / Status]
/////////////////  /////////////////    Cursor: Windows Default (32px)
/////////////////  /////////////////    Terminal: Windows Terminal 1.19.10573.0
/////////////////  /////////////////    Terminal Font: MesloLGS NF (12pt)
                                        CPU: 13th Gen Intel(R) Core(TM) i7-13700HX (24) @ 8.50 GHz
                                        GPU 1: Intel(R) UHD Graphics (128.00 MiB) [Integrated]
                                        GPU 2: NVIDIA GeForce RTX 4060 Laptop GPU (7.77 GiB) [Discrete]
                                        Memory: 24.16 GiB / 31.74 GiB (76%)
                                        Swap: 141.17 MiB / 24.00 GiB (1%)
                                        Disk (C:\): 836.81 GiB / 952.59 GiB (88%) - NTFS
                                        Local IP (Ethernet): x.x.x.x/x *
                                        Battery: 80% [AC Connected, Charging]
                                        Locale: en-GB
```
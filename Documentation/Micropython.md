# Setting Up the ESP32

## Flash Micropython

    sudo esptool.py --port /dev/ttyUSB0 erase_flash
    sudo esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 Firmware/esp32-20210902-v1.17.bin
    

 or sudo screen /dev/ttyUSB0
 sudo picocom -b 115200 /dev/ttyUSB0
 and then if you need to:
    CTRL+d	preforms soft reboot
    CTRL+a x	exits picocom
    CTRL+a \	exits screen


## RShell

    rshell --buffer-size=30 -p /dev/ttyUSB0 -a

Sync with the device filesystem:

    rsync ./src /pyboard

Go into repl:

    repl 

ctrl-x to exit

and then "import foo" to run foo.py



## Check Memory

import micropython
micropython.mem_info()

## Check Flash

In repl:

    uos.statvfs("/")

Returns a tuple with the filesystem information in the following order:

    f_bsize – file system block size
    f_frsize – fragment size
    f_blocks – size of fs in f_frsize units
    f_bfree – number of free blocks
    f_bavail – number of free blocks for unprivileged users
    f_files – number of inodes
    f_ffree – number of free inodes
    f_favail – number of free inodes for unprivileged users
    f_flag – mount flags
    f_namemax – maximum filename length
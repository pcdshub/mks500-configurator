import io
import os
import sys
import json
import time

from serial.tools import list_ports
import serial

serialNumberCommand = 'SN'

timestamp = time.strftime("%Y%m%d-%H%M%S")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        print(sys._MEIPASS)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def rw(sio, command, argument=''):
    if argument == '' or argument == 'NA':
        writeLine = command
    else:
        writeLine = command + ' ' + argument

    sio.write(writeLine+'\r')
    sio.flush()
    resp = sio.readline()
    return resp.strip("*\r")


def runCommands(sio, executeDict, writeSettings=0):
    whichFile = {0: '-save-', 1: '-resp-', 2: '-check-'}
    currentConfig = {}
    for command in executeDict.keys():
        if writeSettings == 1:
            value = rw(sio, command, executeDict[command]['argument'])
        else:
            value = rw(sio, command, '')
        currentConfig[command] = {'helptext':executeDict[command]['helptext'],'value':value}

    # Record current settings
    filename = currentConfig[serialNumberCommand]['value'].strip('* \r')+whichFile[writeSettings]+timestamp
    with open(filename, 'w') as currentFile:
        json.dump(currentConfig, currentFile, indent=1)


if __name__ == "__main__":
    # Open serial interface
    valid_ports = list_ports.grep("SER=500")
    try:
        port = next(valid_ports)
    except StopIteration:
        print('No device found')
        print('Enter to close')
        input()
        exit()

    ser = serial.Serial(port.device, timeout=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline='\r')
    try:
        print('Import config settings')
        f = open(resource_path("settings.cfg"))
        executeDict = {}
        for line in f:
            if line[0] == '#':
                continue
            comarg = line.split(' ',maxsplit=2)
            print(comarg)

            executeDict[comarg[0]] = {'argument':comarg[1], 'helptext':comarg[2]}

        print('Retrieve all current settings')
        runCommands(sio, executeDict, 0)

        print('Apply new config settings')
        runCommands(sio, executeDict, 1)

        print('Record new settings')
        runCommands(sio, executeDict, 2)
    finally:
        ser.close()
        print('Enter to close')
        input()

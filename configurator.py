import serial
import io
import json
import time

serialNumberCommand = 'SN'



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
    filename = currentConfig[serialNumberCommand]['value'].strip('* \r')+whichFile[writeSettings]+time.strftime("%Y%m%d-%H%M%S")
    with open(filename, 'w') as currentFile:
        json.dump(currentConfig, currentFile, indent=1)


if __name__ == "__main__":
    # Open serial interface
    ser = serial.Serial("COM4", timeout=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline='\r')
    try:
        

        # Import config settings
        f = open("settings")
        executeDict = {}
        for line in f:
            if line[0] == '#':
                continue
            comarg = line.split(' ',maxsplit=2)
            print(comarg)

            executeDict[comarg[0]] = {'argument':comarg[1], 'helptext':comarg[2]}

        
        # Retrieve all current settings
        runCommands(sio, executeDict, 0)

        # Apply new config settings
        runCommands(sio, executeDict, 1)

        # Record new settings   
        runCommands(sio, executeDict, 2)
    finally:
        ser.close()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tango import AttrWriteType, DevState, DispLevel, DevFloat, Except, DevError
from tango.server import Device, attribute, command, device_property
from time import sleep
import serial


class NewportSMC100(Device):

    Address = device_property(
        dtype='str',
    )

    Port = device_property(
        dtype='str',
    )

# Errors from page 64 of the manual
    __ERROR_NEG_END_OF_RUN = 1
    __ERROR_POS_END_OF_RUN = 2
    __ERROR_OUT_OF_RANGE   = 'C'

# States from page 65 of the manual
    __STATE_NOT_REFERENCED = ('3C', '0A', '0B', '0c' ,'0D', '0E', '0F', '10')
    __STATE_READY = ('32', '33', '34', '35')

    __STATE_MOVING = '28'

    position = attribute(
        label='Position',
        dtype='float',
        access=AttrWriteType.READ_WRITE,
        unit="mm",
        format="%8.4f",
    )

    referenced = attribute(
        dtype='bool',
    )
    
    velocity = attribute(
        label='Velocity',
        dtype='float',
        access=AttrWriteType.READ_WRITE,
        unit="mm/s",
        format="%8.4f",
    )
    
    acceleration = attribute(
        label='Acceleration',
        dtype='float',
        access=AttrWriteType.READ_WRITE,
        unit="mm/s^2",
        format="%8.4f",
    )

    def init_device(self):
        Device.init_device(self)
        
        self.set_state(DevState.INIT)
        try:
            self.info_stream("Connecting to NewportSMC on port: {:s} ...".format(self.Port))
            self.serial = serial.Serial(
                port = self.Port,
                baudrate = 57600,
                bytesize = 8,
                stopbits = 1,
                parity = 'N',
                xonxoff = True,
                timeout = 0.050)
            if self.serial.isOpen():
                self.serial.close()
            self.serial.open()
            self.info_stream("Success!")
            self.info_stream('Connection established:\n{:s}\n{:s}'.format(self.query('VE?'), self.query('ID?')))
        except:
            self.error_stream("Cannot connect!")
            self.set_state(DevState.OFF)

        self.set_state(DevState.ON)

    def always_executed_hook(self):
        res = self.query('TS?')
        if (res != ''):
            err = int(res[:4],16)
            state = res[4:].strip()
            if (state in self.__STATE_MOVING):
                self.set_status('Device is MOVING')
                self.set_state(DevState.MOVING)
            elif (state in self.__STATE_READY):
                self.set_status('Device is ON')
                self.set_state(DevState.ON)
            else:
                self.set_status('Device is UNKOWN')
                self.set_state(DevState.UNKNOWN)

            if (state in self.__STATE_NOT_REFERENCED):
                self.__Referenced  = False
            else:
                self.__Referenced  = True

    def delete_device(self):
        if self.serial.isOpen():
            self.serial.close()
            self.info_stream('Connection closed for port {:s}'.format(self.Port))

    def read_position(self):
        return float(self.query('TP?'))

    def write_position(self, value):
        self.query('PA' + str(value))
        err = self.get_cmd_error_string()
        if err in self.__ERROR_OUT_OF_RANGE:
            Except.throw_exception('position out of range',
                'position out of range',
                'write_position')
        else:
            self.set_state(DevState.MOVING)

    def read_referenced(self):
        return self.__Referenced

    def read_velocity(self):
        return float(self.query('VA?'))

    def write_velocity(self, value):
        # enter config mode
        self.query('PW1')
        self.query('VA' + str(value))
        # exit configuration mode
        # store new acceleration in nvram
        self.query('PW0')

    def read_acceleration(self):
        return float(self.query('AC?'))

    def write_acceleration(self, value):
        # enter config mode
        self.query('PW1')
        self.query('AC' + str(value))
        # exit configuration mode
        # store new acceleration in nvram
        self.query('PW0')

    @command
    def Stop(self):
        self.query('ST')

    @command
    def Homing(self):
        self.query('OR')
        self.set_state(DevState.MOVING)
    
    @command
    def Reset(self):
        self.query('RS')

    def query(self, cmd):
        prefix = self.Address + cmd[:-1]
        self.send_cmd(self.Address + cmd)
        answer = self.serial.readline().decode('utf-8')
        self.debug_stream(answer)
        if answer.startswith(prefix):
           answer = answer[len(prefix):].strip()
        else:
           answer = ''
        return answer

    def send_cmd(self, cmd):
        snd_str = cmd + '\r\n'       
        self.debug_stream(snd_str) 
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.write(snd_str.encode('utf-8'))
        self.serial.flush()  
        
    def get_cmd_error_string(self):
        error = self.query('TE?')
        return error.strip()


# start the server
if __name__ == '__main__':
    NewportSMC100.run_server()

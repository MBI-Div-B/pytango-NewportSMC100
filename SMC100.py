# -*- coding: utf-8 -*-
#
# This file is part of the SMC100 project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" Tangodevice SMC100

"""

__all__ = ["SMC100", "main"]

# PyTango imports
import PyTango
from PyTango import DebugIt, DeviceProxy
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command, pipe
from PyTango.server import class_property, device_property
from PyTango import AttrQuality,DispLevel, DevState
from PyTango import AttrWriteType, PipeWriteType
# Additional import
# PROTECTED REGION ID(SMC100.additionnal_import) ENABLED START #
from time import sleep
import serial
# PROTECTED REGION END #    //  SMC100.additionnal_import

flagDebugIO = 1


class SMC100(Device):
    """
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(SMC100.class_variable) ENABLED START #
    # PROTECTED REGION END #    //  SMC100.class_variable
    # ----------------
    # Class Properties

    # ----------------

    # read name of serial port ('com1' .. (Windows) or '/dev/ttyUSB0' .. (Linux)) 
    # read the address of the device (1..31)

# -----------------
    # Device Properties
    # -----------------

    Address = device_property(
        dtype='int16',
    )
    Port = device_property(
        dtype='str',
    )


    # some Constants
    __EOL = '\r\n'


# time to wait after sending a command.
    COMMAND_WAIT_TIME_SEC = 0.06

# Errors from page 64 of the manual
    __ERROR_NEG_END_OF_RUN = 1
    __ERROR_POS_END_OF_RUN = 2


# States from page 65 of the manual
    __STATE_NOT_REFERENCED = ('0A', '0B', '0c' ,'0D', '0E', '0F', '10')
    __STATE_READY = ('32', '33', '34', '35')

    __STATE_MOVING = '28'

# some private variables
    __ser_port = None
    __smcID    = ''
    __port     = ''
    
    __smc_state    = ''
    __error        = ''
    
# private status variables, are are updated by "get_smc__state()"
    __Limit_Minus = False
    __Limit_Plus  = False
    __Motor_Run   = False
    __Referenced  = False
    __Homing      = False
    __Pos         = 0.0
    __acceleration= 0.0
    __velocity    = 0.0



    
    # ----------
    # Attributes
    # ----------

    limit_minus = attribute(
        dtype='bool',)
    
    limit_plus = attribute(
        dtype='bool',
    )
    moving = attribute(
        dtype='bool',
    )
    position = attribute(
        dtype='float',
        access=AttrWriteType.READ_WRITE,
        label="mm",
        unit="mm",
        display_unit="mm",
        format="%8.3",
    )
    ready = attribute(
        dtype='bool',
    )
    homing = attribute(
        dtype='bool',
    )
    referenced = attribute(
        dtype='bool',
    )
    
    
    # -----
    # Pipes
    # -----

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(SMC100.init_device) ENABLED START #
        
        self.proxy = DeviceProxy(self.get_name())
        
        self.__smcID = str(self.Address)
        self.__port  = self.Port
        
        if flagDebugIO:
            print("Get_name: %s" % (self.get_name()))
            print 'Connecting to SMC100 on %s'%(port)
            
        self.__ser_port = serial.Serial(
            port = self.__port,
            baudrate = 57600,
            bytesize = 8,
            stopbits = 1,
            parity = 'N',
            xonxoff = True,
            timeout = 0.050)    
        
        if ("SMC_CC" in self.read_controller_info()):
            self.get_smc_state()
            self.read_position()
            self.set_state(PyTango.DevState.ON)  
        else:
            self.set_state(PyTango.DevState.OFF)
        
        if flagDebugIO:
            print "Limit-: ",self.__Limit_Minus
            print "Limit+: ",self.__Limit_Plus
            print "Run: ",self.__Motor_Run
            print "Postion: ", self.__Pos    
            
        # PROTECTED REGION END #    //  SMC100.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(SMC100.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(SMC100.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.delete_device
    
    
    def read_controller_info(self):
        return (self.write_read('VE?'))
    
    def send_cmd(self, cmd):
        # PROTECTED REGION ID(SMC100.send_cmd) ENABLED START #
        snd_str = cmd + self.__EOL
        self.__ser_port.flushOutput()
        self.__ser_port.write(snd_str)
        self.__ser_port.flush()
        # PROTECTED REGION END #    //  SMC100.send_cmd    

    def get_position(self):
        pos = self.write_read('PA?')
        if pos != '':
            self.__Pos = float(pos)
        
        
    # ------------------
    # Attributes methods
    # ------------------

    def read_limit_minus(self):
        # PROTECTED REGION ID(SMC100.limit_minus_read) ENABLED START #
        return self.__Limit_Minus
        # PROTECTED REGION END #    //  SMC100.limit_minus_read

    def read_limit_plus(self):
        # PROTECTED REGION ID(SMC100.limit_plus_read) ENABLED START #
        return self.__Limit_Plus
        # PROTECTED REGION END #    //  SMC100.limit_plus_read

    def read_moving(self):
        # PROTECTED REGION ID(SMC100.moving_read) ENABLED START #
        return self.__Motor_Run
        # PROTECTED REGION END #    //  SMC100.moving_read

    def read_position(self):
        # PROTECTED REGION ID(SMC100.position_read) ENABLED START #
        return self.__Pos
        # PROTECTED REGION END #    //  SMC100.position_read

    def write_position(self, value):
        # PROTECTED REGION ID(SMC100.position_write) ENABLED START #
        self.write_read('PA' + str(value))
        # PROTECTED REGION END #    //  SMC100.position_write

    def read_ready(self):
        # PROTECTED REGION ID(SMC100.ready_read) ENABLED START #
        return self.__Ready
        # PROTECTED REGION END #    //  SMC100.ready_read

    def read_homing(self):
        # PROTECTED REGION ID(SMC100.homing_read) ENABLED START #
        return self.__Homing
        # PROTECTED REGION END #    //  SMC100.homing_read

    def read_referenced(self):
        # PROTECTED REGION ID(SMC100.homing_read) ENABLED START #
        return self.__Referenced
        # PROTECTED REGION END #    //  SMC100.homing_read
    # -------------
    # Pipes methods
    # -------------

    # --------
    # Commands
    # --------
    @command(dtype_in=str, 
    dtype_out=str, 
    )
    @DebugIt()
    def write_read(self, argin):
        # PROTECTED REGION ID(SMC100.write_read) ENABLED START #
        # if argin ended with "?", then we expected an answer
        response = (argin[-1] == '?')
        if response:
            # cut the "?"
            prefix = self.__smcID + argin[:-1]
            send_str = argin
            self.__ser_port.flushInput()
            self.send_cmd(send_str)
            tmp_answer = self.__ser_port.readline()
            if tmp_answer.startswith(prefix):
                answer = tmp_answer[len(prefix):]
            else:
                answer = ''    
        else:    
            send_str = self.__smcID + argin[:-1]
            self.send_cmd(send_str)
            answer = ''
        return answer
        # PROTECTED REGION END #    //  SMC100.write_read
        

    @command(
    dtype_out=float, 
    )
    @DebugIt()
    def get_velocity(self):
        # PROTECTED REGION ID(SMC100.get_velocity) ENABLED START #
        v= self.write_read('VA?')
        if '' == v:
            return self.__velocity
        else:
            self.__velocity = float(v)
            return self.__velocity
        # PROTECTED REGION END #    //  SMC100.get_velocity

    @command(dtype_in=float, 
    )
    @DebugIt()
    def set_velocity(self, argin):
        # PROTECTED REGION ID(SMC100.set_velocity) ENABLED START #
        # enter config mode
        self.write_read('PW1')
        self.write_read('VA' + str(argin))
        # exit configuration mode
        # store new acceleration in nvram
        self.write_read('PW0')
        # PROTECTED REGION END #    //  SMC100.set_velocity

    @command(
    dtype_out=float, 
    )
    @DebugIt()
    def get_acceleration(self):
        # PROTECTED REGION ID(SMC100.get_acceleration) ENABLED START #
        acc = self.write_read('AC?')
        if '' == acc:
            return self.__acceleration
        else:
            self.__acceleration = float(acc)
            return self.__acceleration
        # PROTECTED REGION END #    //  SMC100.get_acceleration

    @command(dtype_in=float, 
    )
    @DebugIt()
    def set_acceleration(self, argin):
        # PROTECTED REGION ID(SMC100.set_acceleration) ENABLED START #
        # enter config mode
        self.write_read('PW1')
        self.write_read('AC' + str(argin))
        # exit configuration mode
        # store new acceleration in nvram
        self.write_read('PW0')
        # PROTECTED REGION END #    //  SMC100.set_acceleration

    @command
    @DebugIt()
    def stop_motion(self):
        # PROTECTED REGION ID(SMC100.stop_motion) ENABLED START #
        self.write_read('ST')
        # PROTECTED REGION END #    //  SMC100.stop_motion
    
    
    @command ()#(polling_period=200, doc_out='state of SMC100' ) 
    @DebugIt()
    def get_smc_state(self):
        # PROTECTED REGION ID(SMC100.get_smc_state) ENABLED START #
        self.read_position()
        resp = self.write_read('TS?')
        if (resp != ''):
            #self.__error = resp[:4]
            self.__smc_state = resp[4:]
            self.__Limit_Minus = self.__ERROR_NEG_END_OF_RUN & error
            self.__Limit_Plus  = self.__ERROR_POS_END_OF_RUN & error
            self.__Motor_Run   = self.__smc_state = self.__STATE_MOVING
            self.__Referenced  = self.__smc_state not in self.__STATE_NOT_REFERENCED
            self.__Ready       = self.__smc_state in self.__STATE_READY
        # PROTECTED REGION END #    //  SMC100.get_smc_state

    

    @command
    @DebugIt()
    def homing(self):
        # PROTECTED REGION ID(SMC100.homing) ENABLED START #
        self.write_read('OR')
        # PROTECTED REGION END #    //  SMC100.homing

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    # PROTECTED REGION ID(SMC100.main) ENABLED START #
    from PyTango.server import run
    return run((SMC100,), args=args, **kwargs)
    # PROTECTED REGION END #    //  SMC100.main

if __name__ == '__main__':
    main()

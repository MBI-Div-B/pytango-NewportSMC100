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
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command, pipe
from PyTango.server import class_property, device_property
from PyTango import AttrQuality,DispLevel, DevState
from PyTango import AttrWriteType, PipeWriteType
# Additional import
# PROTECTED REGION ID(SMC100.additionnal_import) ENABLED START #
# PROTECTED REGION END #    //  SMC100.additionnal_import


class SMC100(Device):
    """
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(SMC100.class_variable) ENABLED START #
    # PROTECTED REGION END #    //  SMC100.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    Address = device_property(
        dtype='int16',
    )
    Port = device_property(
        dtype='str',
    )
    # ----------
    # Attributes
    # ----------

    limit_minus = attribute(
        dtype='bool',
    )
    limit_plus = attribute(
        dtype='bool',
    )
    run = attribute(
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
    # -----
    # Pipes
    # -----

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(SMC100.init_device) ENABLED START #
        # PROTECTED REGION END #    //  SMC100.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(SMC100.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(SMC100.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_limit_minus(self):
        # PROTECTED REGION ID(SMC100.limit_minus_read) ENABLED START #
        return False
        # PROTECTED REGION END #    //  SMC100.limit_minus_read

    def read_limit_plus(self):
        # PROTECTED REGION ID(SMC100.limit_plus_read) ENABLED START #
        return False
        # PROTECTED REGION END #    //  SMC100.limit_plus_read

    def read_run(self):
        # PROTECTED REGION ID(SMC100.run_read) ENABLED START #
        return False
        # PROTECTED REGION END #    //  SMC100.run_read

    def read_position(self):
        # PROTECTED REGION ID(SMC100.position_read) ENABLED START #
        return 0.0
        # PROTECTED REGION END #    //  SMC100.position_read

    def write_position(self, value):
        # PROTECTED REGION ID(SMC100.position_write) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.position_write

    # -------------
    # Pipes methods
    # -------------

    # --------
    # Commands
    # --------

    @command(
    dtype_out='float', 
    )
    @DebugIt()
    def get_velocity(self):
        # PROTECTED REGION ID(SMC100.get_velocity) ENABLED START #
        return 0.0
        # PROTECTED REGION END #    //  SMC100.get_velocity

    @command(dtype_in='float', 
    )
    @DebugIt()
    def set_velocity(self, argin):
        # PROTECTED REGION ID(SMC100.set_velocity) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.set_velocity

    @command(
    dtype_out='float', 
    )
    @DebugIt()
    def get_acceleration(self):
        # PROTECTED REGION ID(SMC100.get_acceleration) ENABLED START #
        return 0.0
        # PROTECTED REGION END #    //  SMC100.get_acceleration

    @command(dtype_in='float', 
    )
    @DebugIt()
    def set_acceleration(self, argin):
        # PROTECTED REGION ID(SMC100.set_acceleration) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.set_acceleration

    @command
    @DebugIt()
    def stop_motion(self):
        # PROTECTED REGION ID(SMC100.stop_motion) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SMC100.stop_motion

    @command(dtype_in='str', 
    dtype_out='str', 
    )
    @DebugIt()
    def send_cmd(self, argin):
        # PROTECTED REGION ID(SMC100.send_cmd) ENABLED START #
        return ""
        # PROTECTED REGION END #    //  SMC100.send_cmd

    @command
    @DebugIt()
    def homing(self):
        # PROTECTED REGION ID(SMC100.homing) ENABLED START #
        pass
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

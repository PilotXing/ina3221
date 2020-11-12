from machine import I2C, Pin, Timer
from micropython import const

INA3221_I2C_ADDR = const(64)
INA3221_REG_MASK = const(0x0f)
INA3221_REG_ID = const(0xff)
R_SHUNT = [50, 100, 100]

class Ina3221:
    def __init__(self, addr = INA3221_I2C_ADDR):
        self.addr = addr
        self.i2c = I2C(scl = Pin(14), sda = Pin(2), freq = 100000)

    
    def getVShuntRaw(self, chl_num = 0):
        """获取分压电阻原始数据"""
        reg = 1 + chl_num * 2
        v_shunt_raw = self.i2c.readfrom_mem(self.addr, reg, 2)
        return v_shunt_raw

    def getVBusRaw(self, chl_num = 0):
        """获取输入电压原始数据"""
        reg = (chl_num + 1)* 2
        v_bus_raw = self.i2c.readfrom_mem(self.addr, reg, 2)
        return v_bus_raw
	
    def getVBus(self, chl_num = 0):
        """获取输入电压"""
        v_bus_raw = self.getVBusRaw(chl_num)
        v_bus = v_bus_raw[0]  * 256 + v_bus_raw[1]
        return v_bus

    
    def getIShunt(self, chl_num = 0):
        """获取chl_num电流"""
        v_shunt_raw = self.getVShuntRaw(chl_num)
        v_shunt = v_shunt_raw[1] * 5 + v_shunt_raw[0] * 1280
        i_shunt = v_shunt / R_SHUNT[chl_num]
        return i_shunt



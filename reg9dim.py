#!/usr/bin/python3
# -*- coding: utf-8 -*-
from smbus import SMBus
from time import sleep
from datetime import datetime
import sqlite3

# I2C address
ADDRESS_SNSR_ACC = 0x6a # Accelerometer
ADDRESS_SNSR_GYR = 0x6a # Gyroscope
ADDRESS_SNSR_MAG = 0x1c # Magnetometer

# Accelerometer register address map
CTRL_REG5_XL = 0x1F 
# Gyroscope register address map
CTRL_REG1_G_ = 0x10
CTRL_REG4___ = 0x1E
# Magnetometer register address map
CTRL_REG3_M_ = 0x22

# Accelerometer register address map
ACC_OUT_X_XL = 0x28 # x (2Bytes)
ACC_OUT_Y_XL = 0x2a # y (2Bytes)
ACC_OUT_Z_XL = 0x2c # z (2Bytes)
# Gyroscope register address map
GYR_OUT_X_G_ = 0x18 # x (2Bytes)
GYR_OUT_Y_G_ = 0x1a # y (2Bytes)
GYR_OUT_Z_G_ = 0x1c # z (2Bytes)
# Magnetometer register address map
MAG_OUT_X_L_M = 0x28
MAG_OUT_X_H_M = 0x29 # x
MAG_OUT_Y_L_M = 0x2a
MAG_OUT_Y_H_M = 0x2b # y
MAG_OUT_Z_L_M = 0x2c
MAG_OUT_Z_H_M = 0x2d # z

def InitAE_LSM9DS1_I2C(bus):
    # Initialize Accelerometer and gyroscope
    bus.write_byte_data(ADDRESS_SNSR_ACC, CTRL_REG5_XL, 0b00111000)  # enable accelerometer
    bus.write_byte_data(ADDRESS_SNSR_GYR, CTRL_REG1_G_, 0b00100000)  # gyro/accel odr and bw
    bus.write_byte_data(ADDRESS_SNSR_GYR, CTRL_REG4___, 0b00111000)  # enable gyro axis
    bus.write_byte_data(ADDRESS_SNSR_MAG, CTRL_REG3_M_, 0b00000000)  # enable mag continuous

def ConvertTwosComplement(value):
    return value if value < 32768 else value - 65536

def GetAcceleration(bus):
    data = bus.read_i2c_block_data(ADDRESS_SNSR_ACC, ACC_OUT_X_XL, 6)
    x = ConvertTwosComplement(data[0] | (data[1] << 8))
    y = ConvertTwosComplement(data[2] | (data[3] << 8))
    z = ConvertTwosComplement(data[4] | (data[5] << 8))
    return (x, y, z)
    
def GetAngularRate(bus):
    data = bus.read_i2c_block_data(ADDRESS_SNSR_GYR, GYR_OUT_X_G_, 6)
    x = ConvertTwosComplement(data[0] | (data[1] << 8))
    y = ConvertTwosComplement(data[2] | (data[3] << 8))
    z = ConvertTwosComplement(data[4] | (data[5] << 8))
    return (x, y, z)

def GetMagneticField(bus):
    data = bus.read_i2c_block_data(ADDRESS_SNSR_MAG, MAG_OUT_X_H_M, 6)
    x = ConvertTwosComplement(data[0] | (data[1] << 8))
    y = ConvertTwosComplement(data[2] | (data[3] << 8))
    z = ConvertTwosComplement(data[4] | (data[5] << 8))
    return (x, y, z)

bus = SMBus(1)
InitAE_LSM9DS1_I2C(bus)
for i in range(600):
    dt = datetime.now()
    (ax, ay, az) = GetAcceleration(bus)
    (gx, gy, gz) = GetAngularRate(bus)
    (mx, my, mz) = GetMagneticField(bus)
    #print(datetime.now())
    #print(ax, ay, az)
    #print(gx, gy, gz)
    #print(mx, my, mz)
    connection = sqlite3.connect("/home/pi/kweb/db/main.sqlite3")
    cursor = connection.cursor()
    cursor.execute("insert into T_9DIM values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (dt, ax, ay, az, gx, gy, gz, mx, my, mz))
    connection.commit()
    sleep(1)
bus.close()


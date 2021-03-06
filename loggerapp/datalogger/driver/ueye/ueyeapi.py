# -*- coding: utf-8 -*-

# Created on 20.08.2014

# @author: K. Viebahn

# This file used to be the uEye.h header file for cpp code and it has been translated to python. All necessary files and libraries (for Win 64bit and 32bit) can be found in this directory (and \drivers).
# Otherwise find them in \IDS\uEye\Develop\include (h file) and \IDS\uEye\USB_driver_package (dll) upon installing the uEye Software from www.ueyesetup.com (for that you need to register with your email address).
# Linux should also be supported.

# Find the Manual for detailed information on uEye functions in '\IDS\uEye\Help\uEye_Manual\Start_uEye_Manual.html' or upon installing uEye software.


# This file is part of beam-cam, a camera project to monitor and characterise laser beams.
# Copyright (C) 2015 Christian Gross <christian.gross@mpq.mpg.de>, Timon Hilker <timon.hilker@mpq.mpg.de>, Michael Hoese <michael.hoese@physik.lmu.de> and Konrad Viebahn <kv291@cam.ac.uk> 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Please see the README.md file for a copy of the GNU General Public License, or otherwise find it on <http://www.gnu.org/licenses/>.


import ctypes as ct
import os, sys
import numpy as np
import time
import platform
import matplotlib.pyplot as plt
from scipy.ndimage import zoom





# ----------------------------------------------------------------------------
# Error codes
# ----------------------------------------------------------------------------
    
def flipDict(dictionary):
    flippedDict = {}
    for k, v in dictionary.items():
        flippedDict[v] = k
    return flippedDict

ErrorCodes={
    'IS_NO_SUCCESS'                  :      -1,   # function call failed
    'IS_SUCCESS'                     :       0,   # function call succeeded
    'IS_INVALID_CAMERA_HANDLE'       :       1,   # camera handle is not valid or zero
    'IS_INVALID_HANDLE'              :       1,   # a handle other than the camera handle is invalid

    'IS_IO_REQUEST_FAILED              ':    2,   # an io request to the driver failed
    'IS_CANT_OPEN_DEVICE               ':    3,   # returned by is_InitCamera
    'IS_CANT_CLOSE_DEVICE              ':    4,
    'IS_CANT_SETUP_MEMORY              ':    5,
    'IS_NO_HWND_FOR_ERROR_REPORT       ':    6,
    'IS_ERROR_MESSAGE_NOT_CREATED      ':    7,
    'IS_ERROR_STRING_NOT_FOUND         ':    8,
    'IS_HOOK_NOT_CREATED               ':    9,
    'IS_TIMER_NOT_CREATED              ':   10,
    'IS_CANT_OPEN_REGISTRY             ':   11,
    'IS_CANT_READ_REGISTRY             ':   12,
    'IS_CANT_VALIDATE_BOARD            ':   13,
    'IS_CANT_GIVE_BOARD_ACCESS         ':   14,
    'IS_NO_IMAGE_MEM_ALLOCATED         ':   15,
    'IS_CANT_CLEANUP_MEMORY            ':   16,
    'IS_CANT_COMMUNICATE_WITH_DRIVER   ':   17,
    'IS_FUNCTION_NOT_SUPPORTED_YET     ':   18,
    'IS_OPERATING_SYSTEM_NOT_SUPPORTED ':   19,

    'IS_INVALID_VIDEO_IN               ':   20,
    'IS_INVALID_IMG_SIZE               ':   21,
    'IS_INVALID_ADDRESS                ':   22,
    'IS_INVALID_VIDEO_MODE             ':   23,
    'IS_INVALID_AGC_MODE               ':   24,
    'IS_INVALID_GAMMA_MODE             ':   25,
    'IS_INVALID_SYNC_LEVEL             ':   26,
    'IS_INVALID_CBARS_MODE             ':   27,
    'IS_INVALID_COLOR_MODE             ':   28,
    'IS_INVALID_SCALE_FACTOR           ':   29,
    'IS_INVALID_IMAGE_SIZE             ':   30,
    'IS_INVALID_IMAGE_POS              ':   31,
    'IS_INVALID_CAPTURE_MODE           ':   32,
    'IS_INVALID_RISC_PROGRAM           ':   33,
    'IS_INVALID_BRIGHTNESS             ':   34,
    'IS_INVALID_CONTRAST               ':   35,
    'IS_INVALID_SATURATION_U           ':   36,
    'IS_INVALID_SATURATION_V           ':   37,
    'IS_INVALID_HUE                    ':   38,
    'IS_INVALID_HOR_FILTER_STEP        ':   39,
    'IS_INVALID_VERT_FILTER_STEP       ':   40,
    'IS_INVALID_EEPROM_READ_ADDRESS    ':   41,
    'IS_INVALID_EEPROM_WRITE_ADDRESS   ':   42,
    'IS_INVALID_EEPROM_READ_LENGTH     ':   43,
    'IS_INVALID_EEPROM_WRITE_LENGTH    ':   44,
    'IS_INVALID_BOARD_INFO_POINTER     ':   45,
    'IS_INVALID_DISPLAY_MODE           ':   46,
    'IS_INVALID_ERR_REP_MODE           ':   47,
    'IS_INVALID_BITS_PIXEL             ':   48,
    'IS_INVALID_MEMORY_POINTER         ':   49,

    'IS_FILE_WRITE_OPEN_ERROR          ':   50,
    'IS_FILE_READ_OPEN_ERROR           ':   51,
    'IS_FILE_READ_INVALID_BMP_ID       ':   52,
    'IS_FILE_READ_INVALID_BMP_SIZE     ':   53,
    'IS_FILE_READ_INVALID_BIT_COUNT    ':   54,
    'IS_WRONG_KERNEL_VERSION           ':   55,

    'IS_RISC_INVALID_XLENGTH           ':   60,
    'IS_RISC_INVALID_YLENGTH           ':   61,
    'IS_RISC_EXCEED_IMG_SIZE           ':   62,

    'IS_DD_MAIN_FAILED                 ':   70, # DirectDraw Mode errors
    'IS_DD_PRIMSURFACE_FAILED          ':   71,
    'IS_DD_SCRN_SIZE_NOT_SUPPORTED     ':   72,
    'IS_DD_CLIPPER_FAILED              ':   73,
    'IS_DD_CLIPPER_HWND_FAILED         ':   74,
    'IS_DD_CLIPPER_CONNECT_FAILED      ':   75,
    'IS_DD_BACKSURFACE_FAILED          ':   76,
    'IS_DD_BACKSURFACE_IN_SYSMEM       ':   77,
    'IS_DD_MDL_MALLOC_ERR              ':   78,
    'IS_DD_MDL_SIZE_ERR                ':   79,
    'IS_DD_CLIP_NO_CHANGE              ':   80,
    'IS_DD_PRIMMEM_NULL                ':   81,
    'IS_DD_BACKMEM_NULL                ':   82,
    'IS_DD_BACKOVLMEM_NULL             ':   83,
    'IS_DD_OVERLAYSURFACE_FAILED       ':   84,
    'IS_DD_OVERLAYSURFACE_IN_SYSMEM    ':   85,
    'IS_DD_OVERLAY_NOT_ALLOWED         ':   86,
    'IS_DD_OVERLAY_COLKEY_ERR          ':   87,
    'IS_DD_OVERLAY_NOT_ENABLED         ':   88,
    'IS_DD_GET_DC_ERROR                ':   89,
    'IS_DD_DDRAW_DLL_NOT_LOADED        ':   90,
    'IS_DD_THREAD_NOT_CREATED          ':   91,
    'IS_DD_CANT_GET_CAPS               ':   92,
    'IS_DD_NO_OVERLAYSURFACE           ':   93,
    'IS_DD_NO_OVERLAYSTRETCH           ':   94,
    'IS_DD_CANT_CREATE_OVERLAYSURFACE  ':   95,
    'IS_DD_CANT_UPDATE_OVERLAYSURFACE  ':   96,
    'IS_DD_INVALID_STRETCH             ':   97,

    'IS_EV_INVALID_EVENT_NUMBER        ':  100,
    'IS_INVALID_MODE                   ':  101,
    'IS_CANT_FIND_FALCHOOK             ':  102,
    'IS_CANT_FIND_HOOK                 ':  102,
    'IS_CANT_GET_HOOK_PROC_ADDR        ':  103,
    'IS_CANT_CHAIN_HOOK_PROC           ':  104,
    'IS_CANT_SETUP_WND_PROC            ':  105,
    'IS_HWND_NULL                      ':  106,
    'IS_INVALID_UPDATE_MODE            ':  107,
    'IS_NO_ACTIVE_IMG_MEM              ':  108,
    'IS_CANT_INIT_EVENT                ':  109,
    'IS_FUNC_NOT_AVAIL_IN_OS           ':  110,
    'IS_CAMERA_NOT_CONNECTED           ':  111,
    'IS_SEQUENCE_LIST_EMPTY            ':  112,
    'IS_CANT_ADD_TO_SEQUENCE           ':  113,
    'IS_LOW_OF_SEQUENCE_RISC_MEM       ':  114,
    'IS_IMGMEM2FREE_USED_IN_SEQ        ':  115,
    'IS_IMGMEM_NOT_IN_SEQUENCE_LIST    ':  116,
    'IS_SEQUENCE_BUF_ALREADY_LOCKED    ':  117,
    'IS_INVALID_DEVICE_ID              ':  118,
    'IS_INVALID_BOARD_ID               ':  119,
    'IS_ALL_DEVICES_BUSY               ':  120,
    'IS_HOOK_BUSY                      ':  121,
    'IS_TIMED_OUT                      ':  122,
    'IS_NULL_POINTER                   ':  123,
    'IS_WRONG_HOOK_VERSION             ':  124,
    'IS_INVALID_PARAMETER              ':  125,  # a parameter specified was invalid
    'IS_NOT_ALLOWED                    ':  126,
    'IS_OUT_OF_MEMORY                  ':  127,
    'IS_INVALID_WHILE_LIVE             ':  128,
    'IS_ACCESS_VIOLATION               ':  129,  # an internal exception occurred
    'IS_UNKNOWN_ROP_EFFECT             ':  130,
    'IS_INVALID_RENDER_MODE            ':  131,
    'IS_INVALID_THREAD_CONTEXT         ':  132,
    'IS_NO_HARDWARE_INSTALLED          ':  133,
    'IS_INVALID_WATCHDOG_TIME          ':  134,
    'IS_INVALID_WATCHDOG_MODE          ':  135,
    'IS_INVALID_PASSTHROUGH_IN         ':  136,
    'IS_ERROR_SETTING_PASSTHROUGH_IN   ':  137,
    'IS_FAILURE_ON_SETTING_WATCHDOG    ':  138,
    'IS_NO_USB20                       ':  139,  # the usb port doesnt support usb 2.0
    'IS_CAPTURE_RUNNING                ':  140,  # there is already a capture running

    'IS_MEMORY_BOARD_ACTIVATED         ':  141,   # operation could not execute while mboard is enabled
    'IS_MEMORY_BOARD_DEACTIVATED       ':  142,  # operation could not execute while mboard is disabled
    'IS_NO_MEMORY_BOARD_CONNECTED      ':  143,   # no memory board connected
    'IS_TOO_LESS_MEMORY                ':  144,   # image size is above memory capacity
    'IS_IMAGE_NOT_PRESENT              ':  145,   # requested image is no longer present in the camera
    'IS_MEMORY_MODE_RUNNING            ':  146,
    'IS_MEMORYBOARD_DISABLED           ':  147,

    'IS_TRIGGER_ACTIVATED              ':  148,   # operation could not execute while trigger is enabled
    'IS_WRONG_KEY                      ':  150,
    'IS_CRC_ERROR                      ':  151,
    'IS_NOT_YET_RELEASED               ':  152,   # this feature is not available yet
    'IS_NOT_CALIBRATED                 ':  153,   # the camera is not calibrated
    'IS_WAITING_FOR_KERNEL             ':  154,   # a request to the kernel exceeded
    'IS_NOT_SUPPORTED                  ':  155,   # operation mode is not supported
    'IS_TRIGGER_NOT_ACTIVATED          ':  156,   # operation could not execute while trigger is disabled
    'IS_OPERATION_ABORTED              ':  157,
    'IS_BAD_STRUCTURE_SIZE             ':  158,
    'IS_INVALID_BUFFER_SIZE            ':  159,
    'IS_INVALID_PIXEL_CLOCK            ':  160,
    'IS_INVALID_EXPOSURE_TIME          ':  161,
    'IS_AUTO_EXPOSURE_RUNNING          ':  162,
    'IS_CANNOT_CREATE_BB_SURF          ':  163,   # error creating backbuffer surface  
    'IS_CANNOT_CREATE_BB_MIX           ':  164,   # backbuffer mixer surfaces can not be created
    'IS_BB_OVLMEM_NULL                 ':  165,   # backbuffer overlay mem could not be locked  
    'IS_CANNOT_CREATE_BB_OVL           ':  166,   # backbuffer overlay mem could not be created  
    'IS_NOT_SUPP_IN_OVL_SURF_MODE      ':  167,   # function not supported in overlay surface mode  
    'IS_INVALID_SURFACE                ':  168,   # surface invalid
    'IS_SURFACE_LOST                   ':  169,   # surface has been lost  
    'IS_RELEASE_BB_OVL_DC              ':  170,   # error releasing backbuffer overlay DC  
    'IS_BB_TIMER_NOT_CREATED           ':  171,   # backbuffer timer could not be created  
    'IS_BB_OVL_NOT_EN                  ':  172,   # backbuffer overlay has not been enabled  
    'IS_ONLY_IN_BB_MODE                ':  173,   # only possible in backbuffer mode 
    'IS_INVALID_COLOR_FORMAT           ':  174,   # invalid color format
    'IS_INVALID_WB_BINNING_MODE        ':  175,   # invalid binning mode for AWB 
    'IS_INVALID_I2C_DEVICE_ADDRESS     ':  176,   # invalid I2C device address
    'IS_COULD_NOT_CONVERT              ':  177,   # current image couldn't be converted
    'IS_TRANSFER_ERROR                 ':  178,   # transfer failed
    'IS_PARAMETER_SET_NOT_PRESENT      ':  179,   # the parameter set is not present
    'IS_INVALID_CAMERA_TYPE            ':  180,   # the camera type in the ini file doesn't match
    'IS_INVALID_HOST_IP_HIBYTE         ':  181,   # HIBYTE of host address is invalid
    'IS_CM_NOT_SUPP_IN_CURR_DISPLAYMODE':  182,   # color mode is not supported in the current display mode
    'IS_NO_IR_FILTER                   ':  183,
    'IS_STARTER_FW_UPLOAD_NEEDED       ':  184,   # device starter firmware is not compatible    

    'IS_DR_LIBRARY_NOT_FOUND                 ':    185,   # the DirectRender library could not be found
    'IS_DR_DEVICE_OUT_OF_MEMORY              ':    186,   # insufficient graphics adapter video memory
    'IS_DR_CANNOT_CREATE_SURFACE             ':    187,   # the image or overlay surface could not be created
    'IS_DR_CANNOT_CREATE_VERTEX_BUFFER       ':    188,   # the vertex buffer could not be created
    'IS_DR_CANNOT_CREATE_TEXTURE             ':    189,   # the texture could not be created  
    'IS_DR_CANNOT_LOCK_OVERLAY_SURFACE       ':    190,   # the overlay surface could not be locked
    'IS_DR_CANNOT_UNLOCK_OVERLAY_SURFACE     ':    191,   # the overlay surface could not be unlocked
    'IS_DR_CANNOT_GET_OVERLAY_DC             ':    192,   # cannot get the overlay surface DC 
    'IS_DR_CANNOT_RELEASE_OVERLAY_DC         ':    193,   # cannot release the overlay surface DC
    'IS_DR_DEVICE_CAPS_INSUFFICIENT          ':    194,   # insufficient graphics adapter capabilities
    'IS_INCOMPATIBLE_SETTING                 ':    195,   # Operation is not possible because of another incompatible setting
    'IS_DR_NOT_ALLOWED_WHILE_DC_IS_ACTIVE    ':    196,   # user App still has DC handle.
    'IS_DEVICE_ALREADY_PAIRED                ':    197,   # The device is already paired
    'IS_SUBNETMASK_MISMATCH                  ':    198,   # The subnetmasks of the device and the adapter differ
    'IS_SUBNET_MISMATCH                      ':    199,   # The subnets of the device and the adapter differ
    'IS_INVALID_IP_CONFIGURATION             ':    200,   # The IP configuation of the device is invalid
    'IS_DEVICE_NOT_COMPATIBLE                ':    201,   # The device is incompatible to the driver
    'IS_NETWORK_FRAME_SIZE_INCOMPATIBLE      ':    202,   # The frame size settings of the device and the network adapter are incompatible
    'IS_NETWORK_CONFIGURATION_INVALID        ':    203,   # The network adapter configuration is invalid
    'IS_ERROR_CPU_IDLE_STATES_CONFIGURATION  ':    204,   # The setting of the CPU idle state configuration failed
    'IS_DEVICE_BUSY                          ':    205,   # The device is busy. The operation must be executed again later.
    'IS_SENSOR_INITIALIZATION_FAILED         ':    206   # The sensor initialization failed
}

# The flipped dictionary for error decoding
EC = flipDict(ErrorCodes)


DeviceEnumerationDict = {
    'IS_USE_DEVICE_ID':0x8000,                 # Use Device ID for camera handle
    'IS_ALLOW_STARTER_FW_UPLOAD':0x10000      # Update Firmware if necessary
}



## ----------------------------------------------------------------------------
##  Sensor Types
## ----------------------------------------------------------------------------
SensorTypeDict = {
    0x0000:'IS_SENSOR_INVALID',           
    
    ## CMOS Sensors
    0x0001:'IS_SENSOR_UI141X_M      ',      # VGA rolling shutter, monochrome
    0x0002:'IS_SENSOR_UI141X_C      ',      # VGA rolling shutter, color
    0x0003:'IS_SENSOR_UI144X_M      ',      # SXGA rolling shutter, monochrome
    0x0004:'IS_SENSOR_UI144X_C      ',      # SXGA rolling shutter, SXGA color
    0x0030:'IS_SENSOR_UI154X_M      ',      # SXGA rolling shutter, monochrome
    0x0031:'IS_SENSOR_UI154X_C      ',      # SXGA rolling shutter, color
    0x0008:'IS_SENSOR_UI145X_C      ',      # UXGA rolling shutter, color
    0x000a:'IS_SENSOR_UI146X_C      ',      # QXGA rolling shutter, color
    0x000b:'IS_SENSOR_UI148X_M      ',      # 5MP rolling shutter, monochrome
    0x000c:'IS_SENSOR_UI148X_C      ',      # 5MP rolling shutter, color
    0x0010:'IS_SENSOR_UI121X_M      ',      # VGA global shutter, monochrome
    0x0011:'IS_SENSOR_UI121X_C      ',      # VGA global shutter, VGA color
    0x0012:'IS_SENSOR_UI122X_M      ',      # WVGA global shutter, monochrome
    0x0013:'IS_SENSOR_UI122X_C      ',      # WVGA global shutter, color
    0x0015:'IS_SENSOR_UI164X_C      ',      # SXGA rolling shutter, color
    0x0017:'IS_SENSOR_UI155X_C      ',      # UXGA rolling shutter, color
    0x0018:'IS_SENSOR_UI1223_M      ',      # WVGA global shutter, monochrome
    0x0019:'IS_SENSOR_UI1223_C      ',      # WVGA global shutter, color
    0x003E:'IS_SENSOR_UI149X_M      ',      # 10MP rolling shutter, monochrome
    0x003F:'IS_SENSOR_UI149X_C      ',      # 10MP rolling shutter, color
    0x0022:'IS_SENSOR_UI1225_M      ',      # WVGA global shutter, monochrome, LE model
    0x0023:'IS_SENSOR_UI1225_C      ',      # WVGA global shutter, color, LE model
    0x0025:'IS_SENSOR_UI1645_C      ',      # SXGA rolling shutter, color, LE model
    0x0027:'IS_SENSOR_UI1555_C      ',      # UXGA rolling shutter, color, LE model
    0x0028:'IS_SENSOR_UI1545_M      ',      # SXGA rolling shutter, monochrome, LE model
    0x0029:'IS_SENSOR_UI1545_C      ',      # SXGA rolling shutter, color, LE model
    0x002B:'IS_SENSOR_UI1455_C      ',      # UXGA rolling shutter, color, LE model
    0x002D:'IS_SENSOR_UI1465_C      ',      # QXGA rolling shutter, color, LE model
    0x002E:'IS_SENSOR_UI1485_M      ',      # 5MP rolling shutter, monochrome, LE model
    0x002F:'IS_SENSOR_UI1485_C      ',      # 5MP rolling shutter, color, LE model
    0x0040:'IS_SENSOR_UI1495_M      ',      # 10MP rolling shutter, monochrome, LE model
    0x0041:'IS_SENSOR_UI1495_C      ',      # 10MP rolling shutter, color, LE model
    0x004A:'IS_SENSOR_UI112X_M      ',      # 0768x576, HDR sensor, monochrome
    0x004B:'IS_SENSOR_UI112X_C      ',      # 0768x576, HDR sensor, color
    0x004C:'IS_SENSOR_UI1008_M      ',
    0x004D:'IS_SENSOR_UI1008_C      ',
    0x0076:'IS_SENSOR_UIF005_M      ', 
    0x0077:'IS_SENSOR_UIF005_C      ', 
    0x020A:'IS_SENSOR_UI1005_M      ', 
    0x020B:'IS_SENSOR_UI1005_C      ',
    0x0050:'IS_SENSOR_UI1240_M      ',      # SXGA global shutter, monochrome
    0x0051:'IS_SENSOR_UI1240_C      ',      # SXGA global shutter, color
    0x0062:'IS_SENSOR_UI1240_NIR    ',      # SXGA global shutter, NIR
    0x0054:'IS_SENSOR_UI1240LE_M    ',      # SXGA global shutter, monochrome, single board
    0x0055:'IS_SENSOR_UI1240LE_C    ',      # SXGA global shutter, color, single board
    0x0064:'IS_SENSOR_UI1240LE_NIR  ',      # SXGA global shutter, NIR, single board
    0x0066:'IS_SENSOR_UI1240ML_M    ',      # SXGA global shutter, monochrome, single board
    0x0067:'IS_SENSOR_UI1240ML_C    ',      # SXGA global shutter, color, single board
    0x0200:'IS_SENSOR_UI1240ML_NIR  ',      # SXGA global shutter, NIR, single board
    0x0078:'IS_SENSOR_UI1243_M_SMI  ',
    0x0079:'IS_SENSOR_UI1243_C_SMI  ',
    0x0032:'IS_SENSOR_UI1543_M      ',      # SXGA rolling shutter, monochrome, single board
    0x0033:'IS_SENSOR_UI1543_C      ',      # SXGA rolling shutter, color, single board
    0x003A:'IS_SENSOR_UI1544_M      ',      # SXGA rolling shutter, monochrome, single board
    0x003B:'IS_SENSOR_UI1544_C      ',      # SXGA rolling shutter, color, single board
    0x003C:'IS_SENSOR_UI1543_M_WO   ',      # SXGA rolling shutter, monochrome, single board
    0x003D:'IS_SENSOR_UI1543_C_WO   ',      # SXGA rolling shutter, color, single board
    0x0035:'IS_SENSOR_UI1453_C      ',      # UXGA rolling shutter, color, single board
    0x0037:'IS_SENSOR_UI1463_C      ',      # QXGA rolling shutter, color, single board
    0x0038:'IS_SENSOR_UI1483_M      ',      # QSXG rolling shutter, monochrome, single board
    0x0039:'IS_SENSOR_UI1483_C      ',      # QSXG rolling shutter, color, single board
    0x004E:'IS_SENSOR_UI1493_M      ',      # 10Mp rolling shutter, monochrome, single board
    0x004F:'IS_SENSOR_UI1493_C      ',      # 10MP rolling shutter, color, single board
    0x0044:'IS_SENSOR_UI1463_M_WO   ',      # QXGA rolling shutter, monochrome, single board
    0x0045:'IS_SENSOR_UI1463_C_WO   ',      # QXGA rolling shutter, color, single board
    0x0047:'IS_SENSOR_UI1553_C_WN   ',      # UXGA rolling shutter, color, single board
    0x0048:'IS_SENSOR_UI1483_M_WO   ',      # QSXGA rolling shutter, monochrome, single board
    0x0049:'IS_SENSOR_UI1483_C_WO   ',      # QSXGA rolling shutter, color, single board
    0x005A:'IS_SENSOR_UI1580_M      ',      # 5MP rolling shutter, monochrome
    0x005B:'IS_SENSOR_UI1580_C      ',      # 5MP rolling shutter, color
    0x0060:'IS_SENSOR_UI1580LE_M    ',      # 5MP rolling shutter, monochrome, single board
    0x0061:'IS_SENSOR_UI1580LE_C    ',      # 5MP rolling shutter, color, single board
    0x0068:'IS_SENSOR_UI1360M       ',      # 2.2MP global shutter, monochrome
    0x0069:'IS_SENSOR_UI1360C       ',      # 2.2MP global shutter, color
    0x0212:'IS_SENSOR_UI1360NIR     ',      # 2.2MP global shutter, NIR
    0x006A:'IS_SENSOR_UI1370M       ',      # 4.2MP global shutter, monochrome
    0x006B:'IS_SENSOR_UI1370C       ',      # 4.2MP global shutter, color
    0x0214:'IS_SENSOR_UI1370NIR     ',      # 4.2MP global shutter, NIR
    0x006C:'IS_SENSOR_UI1250_M      ',      # 2MP global shutter, monochrome
    0x006D:'IS_SENSOR_UI1250_C      ',      # 2MP global shutter, color
    0x006E:'IS_SENSOR_UI1250_NIR    ',      # 2MP global shutter, NIR
    0x0070:'IS_SENSOR_UI1250LE_M    ',      # 2MP global shutter, monochrome, single board
    0x0071:'IS_SENSOR_UI1250LE_C    ',      # 2MP global shutter, color, single board
    0x0072:'IS_SENSOR_UI1250LE_NIR  ',      # 2MP global shutter, NIR, single board
    0x0074:'IS_SENSOR_UI1250ML_M    ',      # 2MP global shutter, monochrome, single board
    0x0075:'IS_SENSOR_UI1250ML_C    ',      # 2MP global shutter, color, single board
    0x0202:'IS_SENSOR_UI1250ML_NIR  ',      # 2MP global shutter, NIR, single board
    0x020B:'IS_SENSOR_XS            ',      # 5MP rolling shutter, color
    0x0204:'IS_SENSOR_UI1493_M_AR   ',
    0x0205:'IS_SENSOR_UI1493_C_AR   ',
    #
    #
    ## CCD Sensors
    0x0080:'IS_SENSOR_UI223X_M   ',      # Sony CCD sensor - XGA monochrome
    0x0081:'IS_SENSOR_UI223X_C   ',      # Sony CCD sensor - XGA color
    0x0082:'IS_SENSOR_UI241X_M   ',      # Sony CCD sensor - VGA monochrome
    0x0083:'IS_SENSOR_UI241X_C   ',      # Sony CCD sensor - VGA color
    0x0084:'IS_SENSOR_UI234X_M   ',      # Sony CCD sensor - SXGA monochrome
    0x0085:'IS_SENSOR_UI234X_C   ',      # Sony CCD sensor - SXGA color
    0x0088:'IS_SENSOR_UI221X_M   ',      # Sony CCD sensor - VGA monochrome
    0x0089:'IS_SENSOR_UI221X_C   ',      # Sony CCD sensor - VGA color
    0x0090:'IS_SENSOR_UI231X_M   ',      # Sony CCD sensor - VGA monochrome
    0x0091:'IS_SENSOR_UI231X_C   ',      # Sony CCD sensor - VGA color
    0x0092:'IS_SENSOR_UI222X_M   ',      # Sony CCD sensor - CCIR / PAL monochrome
    0x0093:'IS_SENSOR_UI222X_C   ',      # Sony CCD sensor - CCIR / PAL color
    0x0096:'IS_SENSOR_UI224X_M   ',      # Sony CCD sensor - SXGA monochrome
    0x0097:'IS_SENSOR_UI224X_C   ',      # Sony CCD sensor - SXGA color
    0x0098:'IS_SENSOR_UI225X_M   ',      # Sony CCD sensor - UXGA monochrome
    0x0099:'IS_SENSOR_UI225X_C   ',      # Sony CCD sensor - UXGA color
    0x009A:'IS_SENSOR_UI214X_M   ',      # Sony CCD sensor - SXGA monochrome
    0x009B:'IS_SENSOR_UI214X_C   ',      # Sony CCD sensor - SXGA color
    0x009C:'IS_SENSOR_UI228X_M   ',      # Sony CCD sensor - QXGA monochrome
    0x009D:'IS_SENSOR_UI228X_C   ',      # Sony CCD sensor - QXGA color
    0x0182:'IS_SENSOR_UI241X_M_R2',      # Sony CCD sensor - VGA monochrome
    0x0182:'IS_SENSOR_UI251X_M   ',      # Sony CCD sensor - VGA monochrome
    0x0183:'IS_SENSOR_UI241X_C_R2',      # Sony CCD sensor - VGA color
    0x0183:'IS_SENSOR_UI251X_C   ',      # Sony CCD sensor - VGA color
    0x019E:'IS_SENSOR_UI2130_M   ',      # Sony CCD sensor - WXGA monochrome
    0x019F:'IS_SENSOR_UI2130_C   '     # Sony CCD sensor - WXGA color
}



#// ----------------------------------------------------------------------------
#// Gain definitions
#// ----------------------------------------------------------------------------
GainDict = {
    0x8000:'IS_GET_MASTER_GAIN        ',
    0x8001:'IS_GET_RED_GAIN           ',
    0x8002:'IS_GET_GREEN_GAIN         ',
    0x8003:'IS_GET_BLUE_GAIN          ',
    0x8004:'IS_GET_DEFAULT_MASTER     ',
    0x8005:'IS_GET_DEFAULT_RED        ',
    0x8006:'IS_GET_DEFAULT_GREEN      ',
    0x8007:'IS_GET_DEFAULT_BLUE       ',
    0x8008:'IS_GET_GAINBOOST          ',
    0x0001:'IS_SET_GAINBOOST_ON       ',
    0x0000:'IS_SET_GAINBOOST_OFF      ',
    0x0002:'IS_GET_SUPPORTED_GAINBOOST',
    0     :'IS_MIN_GAIN               ',
    100   :'IS_MAX_GAIN               '
}

#// ----------------------------------------------------------------------------
#// Gain factor definitions (not implemented yet)
#// ----------------------------------------------------------------------------
GainFactorDict = {
    0x8000:'IS_GET_MASTER_GAIN_FACTOR        ',
    0x8001:'IS_GET_RED_GAIN_FACTOR           ',
    0x8002:'IS_GET_GREEN_GAIN_FACTOR         ',
    0x8003:'IS_GET_BLUE_GAIN_FACTOR          ',
    0x8004:'IS_SET_MASTER_GAIN_FACTOR        ',
    0x8005:'IS_SET_RED_GAIN_FACTOR           ',
    0x8006:'IS_SET_GREEN_GAIN_FACTOR         ',
    0x8007:'IS_SET_BLUE_GAIN_FACTOR          ',
    0x8008:'IS_GET_DEFAULT_MASTER_GAIN_FACTOR',
    0x8009:'IS_GET_DEFAULT_RED_GAIN_FACTOR   ',
    0x800a:'IS_GET_DEFAULT_GREEN_GAIN_FACTOR ',
    0x800b:'IS_GET_DEFAULT_BLUE_GAIN_FACTOR  ',
    0x800c:'IS_INQUIRE_MASTER_GAIN_FACTOR    ',
    0x800d:'IS_INQUIRE_RED_GAIN_FACTOR       ',
    0x800e:'IS_INQUIRE_GREEN_GAIN_FACTOR     ',
    0x800f:'IS_INQUIRE_BLUE_GAIN_FACTOR      '
}



#// ----------------------------------------------------------------------------
#// Camera info constants
#// ----------------------------------------------------------------------------
CameraInfoDictFlip = {
    'IS_GET_STATUS           ':           0x8000,
    'IS_EXT_TRIGGER_EVENT_CNT':           0,
    'IS_FIFO_OVR_CNT         ':           1,
    'IS_SEQUENCE_CNT         ':           2,
    'IS_LAST_FRAME_FIFO_OVR  ':           3,
    'IS_SEQUENCE_SIZE        ':           4,
    'IS_VIDEO_PRESENT        ':           5,
    'IS_STEAL_FINISHED       ':           6,
    'IS_STORE_FILE_PATH      ':           7,
    'IS_LUMA_BANDWIDTH_FILTER':           8,
    'IS_BOARD_REVISION       ':           9,
    'IS_MIRROR_BITMAP_UPDOWN ':           10,
    'IS_BUS_OVR_CNT          ':           11,
    'IS_STEAL_ERROR_CNT      ':           12,
    'IS_LOW_COLOR_REMOVAL    ':           13,
    'IS_CHROMA_COMB_FILTER   ':           14,
    'IS_CHROMA_AGC           ':           15,
    'IS_WATCHDOG_ON_BOARD    ':           16,
    'IS_PASSTHROUGH_ON_BOARD ':           17,
    'IS_EXTERNAL_VREF_MODE   ':           18,
    'IS_WAIT_TIMEOUT         ':           19,
    'IS_TRIGGER_MISSED       ':           20,
    'IS_LAST_CAPTURE_ERROR   ':           21,
    'IS_PARAMETER_SET_1      ':           22,
    'IS_PARAMETER_SET_2      ':           23,
    'IS_STANDBY              ':           24,
    'IS_STANDBY_SUPPORTED    ':           25,
    'IS_QUEUED_IMAGE_EVENT_CN':           26,
    'IS_PARAMETER_EXT        ':           27
}
CameraInfoDict = flipDict(CameraInfoDictFlip)


#// ----------------------------------------------------------------------------
#// Board type defines
#// ----------------------------------------------------------------------------
BoardTypeDictFlip={
    'IS_BOARD_TYPE_UEYE_USB     ':         0x40, #(IS_INTERFACE_TYPE_USB + 0)     //  
    'IS_BOARD_TYPE_UEYE_USB_SE  ':         0x40, #IS_BOARD_TYPE_UEYE_USB          //  
    'IS_BOARD_TYPE_UEYE_USB_RE  ':         0x40, #IS_BOARD_TYPE_UEYE_USB          //  
    'IS_BOARD_TYPE_UEYE_USB_ME  ':         0x41, #(IS_INTERFACE_TYPE_USB + 0x01)  //  
    'IS_BOARD_TYPE_UEYE_USB_LE  ':         0x42, #(IS_INTERFACE_TYPE_USB + 0x02)  //  
    'IS_BOARD_TYPE_UEYE_USB_XS  ':         0x43, #(IS_INTERFACE_TYPE_USB + 0x03)  //  
    'IS_BOARD_TYPE_UEYE_USB_ML  ':         0x45, #(IS_INTERFACE_TYPE_USB + 0x05)  //  
    'IS_BOARD_TYPE_UEYE_USB3_LE ':         0x62, #(IS_INTERFACE_TYPE_USB3 + 0x02) //  
    'IS_BOARD_TYPE_UEYE_USB3_CP ':         0x64, #(IS_INTERFACE_TYPE_USB3 + 0x04) //  
    'IS_BOARD_TYPE_UEYE_USB3_ML ':         0x65, #(IS_INTERFACE_TYPE_USB3 + 0x05) //  
    'IS_BOARD_TYPE_UEYE_ETH     ':         0x80, #IS_INTERFACE_TYPE_ETH           //  
    'IS_BOARD_TYPE_UEYE_ETH_HE  ':         0x80, #IS_BOARD_TYPE_UEYE_ETH          //  
    'IS_BOARD_TYPE_UEYE_ETH_SE  ':         0x81, #(IS_INTERFACE_TYPE_ETH + 0x01)  //  
    'IS_BOARD_TYPE_UEYE_ETH_RE  ':         0x81, #IS_BOARD_TYPE_UEYE_ETH_SE       //  
    'IS_BOARD_TYPE_UEYE_ETH_LE  ':         0x82, #(IS_INTERFACE_TYPE_ETH + 0x02)  //  
    'IS_BOARD_TYPE_UEYE_ETH_CP  ':         0x84, #(IS_INTERFACE_TYPE_ETH + 0x04)  //  
    'IS_BOARD_TYPE_UEYE_ETH_SEP ':         0x86, #(IS_INTERFACE_TYPE_ETH + 0x06)  //  
    'IS_BOARD_TYPE_UEYE_ETH_REP ':         0x86, #IS_BOARD_TYPE_UEYE_ETH_SEP      //  
    'IS_BOARD_TYPE_UEYE_ETH_LEET':         0x87, #(IS_INTERFACE_TYPE_ETH + 0x07)  //  
    'IS_BOARD_TYPE_UEYE_ETH_TE  ':         0x88 #(IS_INTERFACE_TYPE_ETH + 0x08)  //  
}
BoardTypeDict = flipDict(BoardTypeDictFlip)

#// ----------------------------------------------------------------------------
#// Camera type defines
#// ----------------------------------------------------------------------------
CameraTypeDictFlip = {
    'IS_CAMERA_TYPE_UEYE_USB     ':     0x40, #IS_BOARD_TYPE_UEYE_USB_SE
    'IS_CAMERA_TYPE_UEYE_USB_SE  ':     0x40, #IS_BOARD_TYPE_UEYE_USB_SE
    'IS_CAMERA_TYPE_UEYE_USB_RE  ':     0x40, #IS_BOARD_TYPE_UEYE_USB_RE
    'IS_CAMERA_TYPE_UEYE_USB_ME  ':     0x41, #IS_BOARD_TYPE_UEYE_USB_ME
    'IS_CAMERA_TYPE_UEYE_USB_LE  ':     0x42, #IS_BOARD_TYPE_UEYE_USB_LE
    'IS_CAMERA_TYPE_UEYE_USB_ML  ':     0x45, #IS_BOARD_TYPE_UEYE_USB_ML
    'IS_CAMERA_TYPE_UEYE_USB3_LE ':     0x62, #IS_BOARD_TYPE_UEYE_USB3_LE
    'IS_CAMERA_TYPE_UEYE_USB3_CP ':     0x64, #IS_BOARD_TYPE_UEYE_USB3_CP
    'IS_CAMERA_TYPE_UEYE_USB3_ML ':     0x65, #IS_BOARD_TYPE_UEYE_USB3_ML
    'IS_CAMERA_TYPE_UEYE_ETH     ':     0x80, #IS_BOARD_TYPE_UEYE_ETH_HE
    'IS_CAMERA_TYPE_UEYE_ETH_HE  ':     0x80, #IS_BOARD_TYPE_UEYE_ETH_HE
    'IS_CAMERA_TYPE_UEYE_ETH_SE  ':     0x81, #IS_BOARD_TYPE_UEYE_ETH_SE
    'IS_CAMERA_TYPE_UEYE_ETH_RE  ':     0x81, #IS_BOARD_TYPE_UEYE_ETH_RE
    'IS_CAMERA_TYPE_UEYE_ETH_LE  ':     0x82, #IS_BOARD_TYPE_UEYE_ETH_LE
    'IS_CAMERA_TYPE_UEYE_ETH_CP  ':     0x84, #IS_BOARD_TYPE_UEYE_ETH_CP
    'IS_CAMERA_TYPE_UEYE_ETH_SEP ':     0x86, #IS_BOARD_TYPE_UEYE_ETH_SEP
    'IS_CAMERA_TYPE_UEYE_ETH_REP ':     0x86, #IS_BOARD_TYPE_UEYE_ETH_REP
    'IS_CAMERA_TYPE_UEYE_ETH_LEET':     0x87, #IS_BOARD_TYPE_UEYE_ETH_LEET
    'IS_CAMERA_TYPE_UEYE_ETH_TE  ':     0x88  #IS_BOARD_TYPE_UEYE_ETH_TE
}
CameraTypeDict = flipDict(CameraTypeDictFlip)



#typedef enum E_EXPOSURE_CMD
ExposureDictFlip = {
    'IS_EXPOSURE_CMD_GET_CAPS                       ':1,
    'IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT           ':2,
    'IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN         ':3,
    'IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX         ':4,
    'IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_INC         ':5,
    'IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE             ':6,
    'IS_EXPOSURE_CMD_GET_EXPOSURE':7,
    'IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MIN   ':8,
    'IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MAX   ':9,
    'IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_INC   ':10,
    'IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE       ':11,
    'IS_EXPOSURE_CMD_SET_EXPOSURE':12,
    'IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MIN    ':13,
    'IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MAX    ':14,
    'IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_INC    ':15,
    'IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE        ':16,
    'IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_ENABLE       ':17,
    'IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE       ':18,
    'IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_DEFAULT':19, 
    'IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_RANGE  ':20, 
    'IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO        ':21,
    'IS_EXPOSURE_CMD_SET_DUAL_EXPOSURE_RATIO        ':22
}
ExposureDict = flipDict(ExposureDictFlip)

#typedef enum E_EXPOSURE_CAPS
ExposureCapsDict = {
    0x00000001:'IS_EXPOSURE_CAP_EXPOSURE                   ' ,
    0x00000002:'IS_EXPOSURE_CAP_FINE_INCREMENT             ' ,
    0x00000004:'IS_EXPOSURE_CAP_LONG_EXPOSURE              ' ,
    0x00000008:'IS_EXPOSURE_CAP_DUAL_EXPOSURE              ' 
}




# Up to here dictionaries of parameters for IS functions





# // ----------------------------------------------------------------------------
# // Typedefs
# // ----------------------------------------------------------------------------

#aliases for common Win32 types
BOOLEAN = ct.c_int32
BOOL = ct.c_int32
INT = ct.c_int32
UINT = ct.c_uint32
LONG = ct.c_int32
VOID = ct.c_void_p # typedef void (no pointer?)
LPVOID = ct.c_void_p # typedet void*
ULONG = ct.c_uint32

UINT64 = ct.c_uint64
__int64 = ct.c_int64
LONGLONG = ct.c_int64
DWORD = ct.c_uint32
WORD = ct.c_uint16

BYTE = ct.c_ubyte
CHAR = ct.c_byte
TCHAR = ct.c_byte
UCHAR = ct.c_ubyte

LPTSTR = ct.pointer(ct.c_int8()) #typedef int8_t* (why ?)
LPCTSTR = ct.pointer(ct.c_int8()) #typedef const int8_t* (?)
LPCSTR = ct.pointer(ct.c_int8()) #typedef const int8_t* (?)
WPARAM = ct.c_uint32
LPARAM = ct.c_uint32
LRESULT = ct.c_uint32
HRESULT = ct.c_uint32

HWND = ct.c_void_p
HGLOBAL = ct.c_void_p
HINSTANCE = ct.c_void_p
HDC = ct.c_void_p
HMODULE = ct.c_void_p
HKEY = ct.c_void_p
HANDLE = ct.c_void_p

LPBYTE = ct.pointer(BYTE())
PDWORD = ct.pointer(DWORD()) # typedef DWORD*
PVOID = ct.pointer(VOID())
PCHAR = ct.pointer(CHAR())
    
# // ----------------------------------------------------------------------------
# // Info struct
# // See example (struct_BOARDINFO) to learn how to convert c structures to an instance of a ct.Structure class
# // ----------------------------------------------------------------------------

# typedef struct
# {
#  char          SerNo[12];          // e.g. "1234512345"  (11 char)
#  char          ID[20];             // e.g. "IDS GmbH"
#  char          Version[10];        // e.g. "V2.10"  (9 char)
#  char          Date[12];           // e.g. "24.01.2006" (11 char)
#  unsigned char Select;             // contains board select number for multi board support
#  unsigned char Type;               // e.g. IS_BOARD_TYPE_UEYE_USB
#  char          Reserved[8];        // (7 char)
# } BOARDINFO, *PBOARDINFO;

class struct_CAMERAINFO(ct.Structure):
    _fields_ = [
        ('dwCameraID', ct.c_uint32),    #DWORD      #brief this is the user definable camera ID
        ('dwDeviceID', ct.c_uint32),    #DWORD      #brief this is the systems enumeration ID
        ('dwSensorID', ct.c_uint32),    #DWORD      #brief this is the sensor ID e.g. IS_SENSOR_UI141X_M
        ('dwInUse', ct.c_uint32),       #DWORD      #brief flag, indicates whether the camera is in use or not
        ('SerNo[16]', 16*ct.c_char),    #IS_CHAR    #brief zero terminated serial number string
        ('Model[16]', 16*ct.c_char),    #IS_CHAR    #brief zero terminated short model name string
        ('dwStatus', ct.c_uint32),      #DWORD      #brief various flags with camera status
        ('dwReserved[2]', 2*ct.c_uint32), #DWORD    #brief reserved
        ('FullModelName[32]', 32*ct.c_char), #IS_CHAR #brief zero terminated full model name string,note Use this string for display purpose only!,Do not depend on the contents of this string!
        ('dwReserved2[5]', 5*ct.c_uint32), #DWORD    #brief reserved
        ]

##################################################################
# The following structure is not optimal,
# as it occupies much unused storage to ensure compatability with multiple cameras.
class struct_CAMERALIST(ct.Structure):
    _fields_ = [
    ('dwCount', ct.c_uint32),   #ULONG
    ('uci[1]', struct_CAMERAINFO * 50) #struct_CAMERAINFO * maximal number of connected cams, change to higher value if necessary! 
    ]
##################################################################

class struct_BOARDINFO(ct.Structure):
    _fields_ = [
        ('SerNo[12]', 12*ct.c_char),
        ('ID[20]', 20*ct.c_char),
        ('Version[10]', 10*ct.c_char),
        ('Date[12]', 12*ct.c_char),
        ('Select', ct.c_ubyte),
        ('Type', ct.c_ubyte),
        ('Reserved[8]', 8*ct.c_char)
        ]


class struct_SENSORINFO(ct.Structure):
    _fields_ = [
        ('SensorID', ct.c_uint16),           #WORD          # e.g. IS_SENSOR_UI224X_C
        ('strSensorName[32]', 32*ct.c_char), #IS_CHAR       # e.g. "UI-224X-C"
        ('nColorMode', ct.c_char),           #char       # e.g. IS_COLORMODE_BAYER
        ('nMaxWidth', ct.c_uint32),          #DWORD        # e.g. 1280
        ('nMaxHeight', ct.c_uint32),         #DWORD        # e.g. 1024
        ('bMasterGain', ct.c_int32),         #BOOL        # e.g. TRUE
        ('bRGain', ct.c_int32),              #BOOL        # e.g. TRUE
        ('bGGain', ct.c_int32),              #BOOL        # e.g. TRUE
        ('bBGain', ct.c_int32),              #BOOL        # e.g. TRUE
        ('bGlobShutter', ct.c_int32),        #BOOL        # e.g. TRUE
        ('wPixelSize', ct.c_uint16),         #WORD         # e.g. 465 = 4.65 um
        ('nUpperLeftBayerPixel', ct.c_char),  #char      # e.g. BAYER_PIXEL_RED (value = 0)  
        ('Reserved[13]', 13*ct.c_char)       #char         # not used
        ]



class struct_IMAGE_FILE_PARAMS(ct.Structure):
    _fields_ = [
    ('pwchFileName', ct.c_char),    
    ('nFileType', UINT),    
    ('nQuality', UINT),
    ('ppcImageMem', ct.c_char),    
    ('pnImageID', UINT),
    ('reserved[32]', 32*ct.c_char)
    ]


IMAGE_FILE_CMD = UINT
IS_IMAGE_FILE_CMD_LOAD = IMAGE_FILE_CMD(1) # not zero
IS_IMAGE_FILE_CMD_SAVE = IMAGE_FILE_CMD(2)




#// ----------------------------------------------------------------------------
#// Capture status
#// ----------------------------------------------------------------------------
UEYE_CAPTURE_STATUS = {
    0xa2:'IS_CAP_STATUS_API_NO_DEST_MEM      ',
    0xa3:'IS_CAP_STATUS_API_CONVERSION_FAILED',
    0xa5:'IS_CAP_STATUS_API_IMAGE_LOCKED     ',
    0xb2:'IS_CAP_STATUS_DRV_OUT_OF_BUFFERS   ',
    0xb4:'IS_CAP_STATUS_DRV_DEVICE_NOT_READY ',
    0xc7:'IS_CAP_STATUS_USB_TRANSFER_FAILED  ',
    0xd6:'IS_CAP_STATUS_DEV_TIMEOUT          ',
    0xe4:'IS_CAP_STATUS_ETH_BUFFER_OVERRUN   ',
    0xe5:'IS_CAP_STATUS_ETH_MISSED_IMAGES    '
}

class struct_UEYE_CAPTURE_STATUS_INFO(ct.Structure):
    _fields_ = [
    ('dwCapStatusCnt_Total', ct.c_uint32), # DWORD
    ('reserved[60]', 60*ct.c_ubyte), # BYTE
    ('adwCapStatusCnt_Detail[256]', 256*ct.c_uint32) #// access via UEYE_CAPTURE_STATUS # DWORD
    ]

#this was a c 'enum' which I translate to a python dict  
E_CAPTURE_STATUS_CMD = {
    1:'IS_CAPTURE_STATUS_INFO_CMD_RESET',
    2:'IS_CAPTURE_STATUS_INFO_CMD_GET'
}



#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
#
# Here the class with the functions starts.
#
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################

class UEyeAPI(object):
    """Provides basic programming functionality for a uEye camera."""

    def __init__(self):
        
        print("Initialising uEye library") 
        # self.dllFolder = os.getcwd()
        # self.dllFolder = os.path.join(self.dllFolder,'beamprofiler/driver/ueye')
        # print(self.dllFolder)
        if platform.architecture()[1] == 'ELF':
            self.dllPath = 'libueye_api.so'
        elif platform.architecture()[0] == '64bit':
            self.dllPath = 'ueye_api_64.dll'
            print(self.dllPath)
        elif platform.architecture()[0] == '32bit':
            self.dllPath = 'uEye_api.dll'

        else:
            print("ERROR - loading .dll according to platform architecture failed!")
        # print(self.dllPath)
        self.dll = ct.cdll.LoadLibrary(self.dllPath) 
        # self.dll = ct.cdll.LoadLibrary('ueye_api_64.dll')   #For testing 
        
        self.nHeight = 1200 # height of display in px (our uEye has 1200 px)
        self.nWidth = 1600 # width of display in px (our uEye has 1600 px)

        # This is the camera handle: (default is 1)
        self.hCam = 1

        #zooming issue (see is_RescaleImage)
        self.zoomfactor = 2./3.
        
        # The array where the image is going to stored in. These are just default values,
        # the size of the actual image will be changed if necessary.
        self.imagearrayraw = np.zeros((self.nHeight, self.nWidth), dtype = np.uint16)
        
        #the mein (scaled) image array
        self.imagearray = self.is_RescaleImage(self.imagearrayraw)
        
        # exposure time kept as class variable to check whether update is necessary
        self.exposuretime = 0.0

    def __del__(self):
        '''Shut down camera in any case'''
        try:
            print("Closing camera")
            self.dll.is_ExitCamera(UINT(self.hCam))
        except:
            pass

    def is_CreateHandle(self, deviceid=1):
        print("Opening uEye camera")
        print(DeviceEnumerationDict['IS_USE_DEVICE_ID'])
        CameraHandle = deviceid | DeviceEnumerationDict['IS_USE_DEVICE_ID']
        phCam = ct.pointer(ct.c_uint32(CameraHandle))
        err = self.dll.is_InitCamera(phCam, None)
        if int(err) == 3:
            raise Exception('Error: No camera detected or camera already in use')
        self.hCam = phCam.contents.value
        return err, phCam.contents.value

    def is_RescaleImage(self, imagearray):
        '''we manually fix a bug where the long axis of the image is scaled by 2/3.'''
        return zoom(imagearray, [1.0, self.zoomfactor])

#==============================================================================
# Some general camera information
#==============================================================================
    
    def is_GetNumberOfCameras(self):
        stat = ct.c_int32()
        p_stat = ct.pointer(stat)
        err = self.dll.is_GetNumberOfCameras(p_stat)
        # print('is_GetNumberOfCameras %s' % (EC[err]))
        print('Number of cameras = %i' % (p_stat.contents.value))
        return err, int(p_stat.contents.value)

    def is_GetCameraList(self,camnum=0):

        # err0, camnum = self.is_GetNumberOfCameras()
        camlist = struct_CAMERALIST()
        camlist.dwCount = ct.c_uint32(camnum)
        # camlist = ct.c_uint32() + (struct_CAMERAINFO * camnum)()
        
        # camnum = int(camnum)
        pcamlist = ct.pointer(camlist)
        err1 = self.dll.is_GetCameraList(pcamlist)
        
        return err1, pcamlist.contents
        
        

    def is_PrintCameraList(self,camnum=0):

        err, camlist = self.is_GetCameraList(camnum)
        camnumu = getattr(camlist, 'dwCount')
        print('We have %i cameras' % (int(camnumu)))
        caminfo = getattr(camlist, 'uci[1]')
        print(caminfo)
        for i in range(camnumu):
            print('Specs of camera #%i' % i)
            for field_name, field_type in caminfo[i]._fields_:
                print(field_name, getattr(caminfo[i], field_name))


    def is_GetCameraInfo(self):
        '''Returns an abstract struct with some camera information'''
        pInfo = ct.pointer(struct_BOARDINFO())
        err = self.dll.is_GetCameraInfo(UINT(self.hCam), pInfo)
        return err, pInfo.contents
    
    def is_PrintCameraInfo(self):
        '''Prints some camera information, incl. model'''
        pInfo = ct.pointer(struct_BOARDINFO())
        err = self.dll.is_GetCameraInfo(UINT(self.hCam), pInfo)
        for field_name, field_type in pInfo.contents._fields_:
            if field_name == 'Select':
                print(field_name, getattr(pInfo.contents, field_name))
            elif field_name == 'Type':
                print(field_name, CameraTypeDict[getattr(pInfo.contents, field_name)])
            else:
                print(field_name, getattr(pInfo.contents, field_name))
        return err, pInfo.contents
    
    def is_GetSerialNumber(self):
        '''returns and prints the serial number of the camera'''
        err, structInfo = self.is_GetCameraInfo()
        if int(err) != 0:
            raise Exception('Error loading Serial number')
        my_serial = getattr(structInfo, 'SerNo[12]')
        print('Serial number: {0}'.format(my_serial))
        return my_serial
    
    def is_GetModel(self):
        '''returns and prints the camera model'''
        err, structInfo = self.is_GetCameraInfo()
        if int(err) != 0:
            raise Exception('Error loading Serial number')
        my_model = CameraTypeDict[getattr(structInfo, 'Type')]
        print('Camera model: {0}'.format(my_model))
        return my_model

    def is_GetSensorInfo(self):
        '''Returns an abstract struct with some sensor information'''
        pInfo = ct.pointer(struct_SENSORINFO())
        err = self.dll.is_GetSensorInfo(UINT(self.hCam), pInfo)
        return err, pInfo.contents

    def is_GetSensorType(self):
        '''Returns and prints the sensor type.'''
        err, structSensor = self.is_GetSensorInfo()
        sensor = getattr(structSensor, 'strSensorName[32]')
        print('Sensor type: {0}'.format(sensor))
        return sensor
    
    def is_PrintSensorInfo(self):
        '''Prints some sensor information, incl. pixel pitch and dimensions'''
        pInfo = ct.pointer(struct_SENSORINFO())
        err = self.dll.is_GetSensorInfo(UINT(self.hCam), pInfo)
        for field_name, field_type in pInfo.contents._fields_:
            print(field_name, getattr(pInfo.contents, field_name))

    def is_GetPixelPitch(self):
        '''Returns pixel size in um'''
        err, structSensor = self.is_GetSensorInfo()
        pitch = getattr(structSensor, 'wPixelSize')/100.
        print('Pixel pitch = {:1.2f} um'.format(pitch))
        return pitch

    def is_GetSensorHeightWidth(self):
        '''returns the sensor dimensions as (height, width) pixels'''
        err, structSensor = self.is_GetSensorInfo()
        nWidth = int(getattr(structSensor, 'nMaxWidth'))
        nHeight = int(getattr(structSensor, 'nMaxHeight'))
        print('Sensor height/width = {0}/{1} px'.format(nHeight, nWidth))
        self.nHeight = nHeight
        self.nWidth = nWidth
        return (nHeight, nWidth)

#==============================================================================
# Pixel clock
#
# We've had USB transmission errors in the past. Reducing the pixel clock to
# values below 12 MHz helped (if the camera was conencted via USB hub and
# 10 meters' worth of cables.)
#==============================================================================

    def is_GetPixelClock(self):
        '''Returns the current value of pixel clock (in MHz)'''
        pParam = ct.c_void_p()
        err = self.dll.is_PixelClock(UINT(self.hCam), UINT(5), ct.byref(pParam), UINT(ct.sizeof(pParam)))
        if int(err) != 0:
            raise Exception('Error getting pixelclock value: {0}'.format(EC[err]))
        value = pParam.value
        print('Pixel clock is at {0} MHz').format(value)
        return value

    def is_SetPixelClock(self, value = 11):
        '''Set the current value of pixel clock (in MHz)'''
        pParam = UINT(value) #20 MHz
        err = self.dll.is_PixelClock(UINT(self.hCam), UINT(6), ct.byref(pParam), UINT(ct.sizeof(pParam)))
        if int(err) != 0:
            raise Exception('Error setting pixelclock value: {0}'.format(EC[err]))
        value = pParam.value
        print('Pixel clock set to {0} MHz'.format(value))
        return value

#==============================================================================
# Memory management
#==============================================================================

    def is_AllocateImageMemory(self):
        '''Allocates the right amount of memory on the camera RAM for one image.
        height and width of array has to be given first by calling is_GetSensorHeightWidth.
        Returns memory address (ctypes pointer) and image id (int).'''
        
        self.imagearrayraw = np.zeros((self.nHeight, self.nWidth), dtype = np.uint16)
        numpyArray = self.imagearrayraw
        pcMem = numpyArray.ctypes.data_as(ct.POINTER(ct.c_uint16))
        pid = ct.pointer(ct.c_int())
        err = self.dll.is_SetAllocatedImageMem(
            UINT(self.hCam), ct.c_int(self.nWidth), ct.c_int(self.nHeight), ct.c_int(16), pcMem, pid)
        #print 'is_SetAllocatedImageMem: pcMem = %s' %(pcMem)
        #print 'is_SetAllocatedImageMem: pid = %s' %(pid.contents)        
        #print 'is_SetAllocatedImageMem: %s' % (EC[err])
        return err, pcMem, pid.contents.value

    def is_ActivateImageMemory(self, pcMem, idMem):
        '''This method makes the allocated memory active.'''
        err = self.dll.is_SetImageMem(UINT(self.hCam), pcMem, ct.c_int(idMem))
        #print 'is_SetImageMem: %s' % (EC[err])
        return err
        
    def is_InitialiseMemory(self):
        '''Combines a couple of memory routines to provide the correct memory on the camera RAM for one image.'''
        self.is_GetSensorHeightWidth()
        err1, my_address, my_id = self.is_AllocateImageMemory()
        err2 = self.is_ActivateImageMemory(my_address, my_id)
        if (int(err1) != 0)|(int(err2) != 0):
            raise Exception('Error during image memory allocation: {0}, {1}'.format(EC[err1], EC[err2]))
        else:
            print('Image memory successfully allocated')

#==============================================================================
# Trigger settings   
#==============================================================================

    def is_SetTriggerHardware(self):
        '''Sets the trigger to hardware (5V TTL on falling edge).'''
        err = self.dll.is_SetExternalTrigger(UINT(self.hCam), INT(0x0001))
        if int(err) == 0:
            print('Trigger set to external TTL')
            return 0
        else:
            raise Exception('Error during trigger setting: {0}'.format(EC[err]))
            
    def is_SetTriggerInternal(self):
        '''No external trigger needs to be given to take picture.'''
        err = self.dll.is_SetExternalTrigger(UINT(self.hCam), INT(0x0000))
        if int(err) == 0:
            print('Trigger set to automatic (no trigger)')
            return 0
        else:
            raise Exception('Error during trigger setting: {0}'.format(EC[err]))

    def is_GetSupportedTrigger(self):
        '''Returns supported trigger modes.
        
        From IDS documentation:
        If called with IS_GET_SUPPORTED_TRIGGER_MODE = 0x8004, then it returns supported mode,
        seperated by logical ORs.
        Hence 0x1009 means modes 0x1000, 0x0001, and 0x1008'''
        err = self.dll.is_SetExternalTrigger(UINT(self.hCam), INT(0x8004))
        print('Supported trigger modes: {0}.'.format(hex(err)))
        return err

#==============================================================================
# Acquisition settings
#==============================================================================

    def is_GetExposureTime(self):
        '''Returns the exposure time in ms'''
        Param = ct.c_double()
        pParam = ct.pointer(Param)
        nSizeOfParam = 8 
        err = self.dll.is_Exposure(UINT(self.hCam), UINT(7), pParam, UINT(nSizeOfParam))
        if int(err) != 0:
            raise Exception('Error during exposure time enquiry: {0}'.format(EC[err]))
        print('Exposure time is {:1.3f} ms'.format(pParam.contents.value))
        self.exposuretime = pParam.contents.value
        return pParam
        
    def is_SetExposureTime(self, exposure = 10.):
        '''Sets the exposure time in ms'''
        Param = ct.c_double(exposure)
        pParam = ct.pointer(Param)
        nSizeOfParam = 8 
        err = self.dll.is_Exposure(UINT(self.hCam), UINT(12), pParam, UINT(nSizeOfParam))
        if int(err) != 0:
            raise Exception('Error while setting exposure time: {0}'.format(EC[err]))
        print('Exposure time set to {:1.3f} ms'.format(pParam.contents.value))
        self.exposuretime = pParam.contents.value
        return pParam

    def is_GetGainValue(self):
        '''Returns the current gain value'''
        err = self.dll.is_SetHardwareGain(UINT(self.hCam), INT(0x8000), INT(-1), INT(-1), INT(-1))
        print('Gain is currently {0}'.format(err))
        return err

    def is_SetGainValue(self, gain = 10):
        '''Set the gain to this value. Min = 0, max = 100.
        
        From IDS documentation:
        if nMaster in [0,100] the gain level is set to this value
        if nMaster == 0x8000 the current gain value is returned
        if nMaster == 0x8004 the default gain value is returned
        '''
        if int(gain) in np.arange(101):
            nMaster = gain
        else:
            print('WARNING: Gain out of range. Setting to default')
            nMaster = 10
        err = self.dll.is_SetHardwareGain(UINT(self.hCam), INT(nMaster), INT(-1), INT(-1), INT(-1))
        print('Gain set to {0}'.format(nMaster))
        return err

    def is_Blacklevel(self):
        '''Disable auto blacklevel correction'''
        Param = UINT(0)
        pParam = ct.pointer(Param)
        nSizeOfParam = 8
        err = self.dll.is_Exposure(UINT(self.hCam), UINT(4), pParam, UINT(nSizeOfParam))
        if int(err) != 0:
            raise Exception('Error while disabling automatic blacklevel correction: {0}'\
            .format(EC[err]))
        else:
            print('automatic blacklevel correction disabled')
        return err

#==============================================================================
# Acquisition (single frame)
#==============================================================================

    def is_ArmCamera(self, timeout = 2):
        '''Puts the camera in a state of high readiness.
        It will wait for a trigger for timeout seconds.'''
        my_timeout = int(100.*timeout) # uEye expects value in 10ms
        err = self.dll.is_FreezeVideo(UINT(self.hCam), INT(my_timeout))
        if int(err) != 0:
            print(EC[err])
            raise Exception('Error during image acquisition or no trigger received')
        else:
            print('Frame returned')
            return err
    
    def is_GetRescaledArray(self):
        self.imagearray = self.is_RescaleImage(self.imagearrayraw)
        return self.imagearray

    def is_ClearFrame(self):
        '''Clear one frame before aquisition in order to avoid lines in the image.
        Changes back to hardware trigger mode afterwards!'''
        err1 = self.dll.is_SetExternalTrigger(UINT(self.hCam), INT(0x0000))
        err2 = self.dll.is_CaptureVideo(UINT(self.hCam), INT(5))
        err3 = self.dll.is_SetExternalTrigger(UINT(self.hCam), INT(0x0001))
        if int(err1) != 0 or int(err2) != 0 or int(err3) != 0:
            raise Exception('Error during frame clear: {0}, {1}, or {2}'.format(EC[err1],EC[err2],EC[err3]))
        else:
            print('Frame cleared')
            return err1, err2, err3

#==============================================================================
# Initialisation routine
#==============================================================================

    def is_Initialise(self):
        '''Some initialisation routines for standard operation in sequence.'''
        self.is_CreateHandle()
        self.is_GetModel()
        self.is_GetSensorType()
        self.is_GetSerialNumber()
        self.is_GetPixelPitch()
        self.is_GetPixelClock()
        self.is_Blacklevel()
        self.is_SetTriggerHardware()
        
        self.is_SetGainValue()
        self.is_GetExposureTime()
        
        self.is_InitialiseMemory()

if __name__ == '__main__':
    from time import sleep
    
    check = UEyeAPI()
    err, camnum = check.is_GetNumberOfCameras()
    check.is_GetCameraList(camnum)
    check.is_PrintCameraList(camnum)
    check.is_CreateHandle(deviceid=1)
    # check.is_GetModel()
    # check.is_GetSensorType()
    # check.is_GetSerialNumber()
    #check.is_GetSensorHeightWidth()
    # check.is_GetPixelPitch()
    # check.is_GetPixelClock()
    # check.is_Blacklevel()
    check.is_SetGainValue()
    check.is_SetExposureTime(3)
    #check.is_GetSupportedTrigger()
    #check.is_SetTriggerHardware()   
    
    check.is_InitialiseMemory()
    check.is_ClearFrame()
    check.is_SetTriggerInternal() 
    # print check.imagearrayraw
    sleep(1)
    
    check.is_ArmCamera(10)
    
    sleep(1)
    
    # print check.imagearrayraw
    
    check.__del__()

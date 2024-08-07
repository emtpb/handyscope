"""This module implements an interface to the TiePie device library.

Information on the specific functions can be found in the `library's api
documentation <http://api.tiepie.com/libtiepie/>`_

It is implemented as a module and not as a class, because modules are only
imported once in Python. This ensures that there is only one instance
(=> singleton). See also `the Python FAQ
<https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_.

Attributes:
    libtiepie (:py:class:`ctypes.CDLL`): instance of the library
"""

import platform
import warnings
from ctypes import *

from pkg_resources import resource_filename

# Type definitions for callback usage
Callback = CFUNCTYPE(None, c_void_p)
CallbackDeviceList = CFUNCTYPE(None, c_void_p, c_uint32, c_uint32)
CallbackObject = CFUNCTYPE(None, c_void_p, c_uint32, c_uint32)
CallbackHandle = CFUNCTYPE(None, c_void_p, c_uint32)


def _load_lib():
    """Load the library and define argument and return types as well as error
    check functions.

    Returns:
        libtiepie (:py:class:`ctypes.CDLL`): instance of the library
    """
    if platform.system() == 'Linux':
        # Use bundled amd64 library
        if platform.machine() in ('x86_64', 'x86-64', 'amd64', 'x64'):
            library_name = 'libtiepie.so'
            library_path = resource_filename(__name__, 'bin/{}'.format(library_name))
        # Other architectures are not included, requires installation of
        # https://www.tiepie.com/en/download/linux
        else:
            library_name = 'libtiepie.so.0'
            library_path = library_name

    # Use bundled libraries on Windows
    elif platform.system() == 'Windows':
        from ctypes.wintypes import HANDLE, HWND, LPARAM, WPARAM
        if sizeof(c_voidp) == 4:
            library_name = 'libtiepie32.dll'
        if sizeof(c_voidp) == 8:
            library_name = 'libtiepie64.dll'
        library_path = resource_filename(__name__, 'bin/{}'.format(library_name))
    else:
        raise Exception(
            'Can\'t determine library name, unknown platform.system(): ' + platform.system())

    libtiepie = CDLL(library_path)

    # define result and argument types
    libtiepie.LibInit.restype = None
    libtiepie.LibInit.argtypes = []
    libtiepie.LibInit.errcheck = _check_status
    libtiepie.LibIsInitialized.restype = c_uint8
    libtiepie.LibIsInitialized.argtypes = []
    libtiepie.LibIsInitialized.errcheck = _check_status
    libtiepie.LibExit.restype = None
    libtiepie.LibExit.argtypes = []
    libtiepie.LibExit.errcheck = _check_status
    libtiepie.LibGetVersion.restype = c_uint64
    libtiepie.LibGetVersion.argtypes = []
    libtiepie.LibGetVersion.errcheck = _check_status
    libtiepie.LibGetVersionExtra.restype = c_char_p
    libtiepie.LibGetVersionExtra.argtypes = []
    libtiepie.LibGetVersionExtra.errcheck = _check_status
    libtiepie.LibGetConfig.restype = c_uint32
    libtiepie.LibGetConfig.argtypes = [c_void_p, c_uint32]
    libtiepie.LibGetConfig.errcheck = _check_status
    # No error check function for LibGetLastStatus to avoid infinite recursion
    libtiepie.LibGetLastStatus.restype = c_int32
    libtiepie.LibGetLastStatus.argtypes = []
    # No error check function for LibGetLastStatusStr to avoid infinite recursion
    libtiepie.LibGetLastStatusStr.restype = c_char_p
    libtiepie.LibGetLastStatusStr.argtypes = []

    libtiepie.LstUpdate.restype = None
    libtiepie.LstUpdate.argtypes = []
    libtiepie.LstUpdate.errcheck = _check_status
    libtiepie.LstGetCount.restype = c_uint32
    libtiepie.LstGetCount.argtypes = []
    libtiepie.LstGetCount.errcheck = _check_status
    libtiepie.LstOpenDevice.restype = c_uint32
    libtiepie.LstOpenDevice.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstOpenDevice.errcheck = _check_status
    libtiepie.LstOpenOscilloscope.restype = c_uint32
    libtiepie.LstOpenOscilloscope.argtypes = [c_uint32, c_uint32]
    libtiepie.LstOpenOscilloscope.errcheck = _check_status
    libtiepie.LstOpenGenerator.restype = c_uint32
    libtiepie.LstOpenGenerator.argtypes = [c_uint32, c_uint32]
    libtiepie.LstOpenGenerator.errcheck = _check_status
    libtiepie.LstOpenI2CHost.restype = c_uint32
    libtiepie.LstOpenI2CHost.argtypes = [c_uint32, c_uint32]
    libtiepie.LstOpenI2CHost.errcheck = _check_status
    libtiepie.LstCreateCombinedDevice.restype = c_uint32
    libtiepie.LstCreateCombinedDevice.argtypes = [c_void_p, c_uint32]
    libtiepie.LstCreateCombinedDevice.errcheck = _check_status
    libtiepie.LstCreateAndOpenCombinedDevice.restype = c_uint32
    libtiepie.LstCreateAndOpenCombinedDevice.argtypes = [c_void_p, c_uint32]
    libtiepie.LstCreateAndOpenCombinedDevice.errcheck = _check_status
    libtiepie.LstRemoveDevice.restype = None
    libtiepie.LstRemoveDevice.argtypes = [c_uint32]
    libtiepie.LstRemoveDevice.errcheck = _check_status
    libtiepie.LstRemoveDeviceForce.restype = None
    libtiepie.LstRemoveDeviceForce.argtypes = [c_uint32]
    libtiepie.LstRemoveDeviceForce.errorcheck = _check_status
    libtiepie.LstDevCanOpen.restype = c_uint8
    libtiepie.LstDevCanOpen.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstDevCanOpen.errcheck = _check_status
    libtiepie.LstDevGetProductId.restype = c_uint32
    libtiepie.LstDevGetProductId.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetProductId.errcheck = _check_status
    libtiepie.LstDevGetVendorId.restype = c_uint32
    libtiepie.LstDevGetVendorId.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetVendorId.errcheck = _check_status
    libtiepie.LstDevGetName.restype = c_uint32
    libtiepie.LstDevGetName.argtypes = [c_uint32, c_uint32, c_char_p, c_uint32]
    libtiepie.LstDevGetName.errcheck = _check_status
    libtiepie.LstDevGetNameShort.restype = c_uint32
    libtiepie.LstDevGetNameShort.argtypes = [c_uint32, c_uint32, c_char_p,
                                             c_uint32]
    libtiepie.LstDevGetNameShort.errcheck = _check_status
    libtiepie.LstDevGetNameShortest.restype = c_uint32
    libtiepie.LstDevGetNameShortest.argtypes = [c_uint32, c_uint32, c_char_p,
                                                c_uint32]
    libtiepie.LstDevGetNameShortest.errcheck = _check_status
    libtiepie.LstDevGetDriverVersion.restype = c_uint64
    libtiepie.LstDevGetDriverVersion.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetDriverVersion.errcheck = _check_status
    libtiepie.LstDevGetRecommendedDriverVersion.restype = c_uint64
    libtiepie.LstDevGetRecommendedDriverVersion.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetRecommendedDriverVersion.errcheck = _check_status
    libtiepie.LstDevGetFirmwareVersion.restype = c_uint64
    libtiepie.LstDevGetFirmwareVersion.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetFirmwareVersion.errcheck = _check_status
    libtiepie.LstDevGetRecommendedFirmwareVersion.restype = c_uint64
    libtiepie.LstDevGetRecommendedFirmwareVersion.argtypes = [c_uint32,
                                                              c_uint32]
    libtiepie.LstDevGetRecommendedFirmwareVersion.errcheck = _check_status
    libtiepie.LstDevGetCalibrationDate.restype = c_uint32
    libtiepie.LstDevGetCalibrationDate.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetCalibrationDate.errcheck = _check_status
    libtiepie.LstDevGetSerialNumber.restype = c_uint32
    libtiepie.LstDevGetSerialNumber.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetSerialNumber.errcheck = _check_status

    libtiepie.LstDevGetIPv4Address.restype = c_uint32
    libtiepie.LstDevGetIPv4Address.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetIPPort.restype = c_uint16
    libtiepie.LstDevGetIPPort.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevHasServer.restype = c_uint8
    libtiepie.LstDevHasServer.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetServer.restype = c_uint32
    libtiepie.LstDevGetServer.argtypes = [c_uint32, c_uint32]

    libtiepie.LstDevGetTypes.restype = c_uint32
    libtiepie.LstDevGetTypes.argtypes = [c_uint32, c_uint32]
    libtiepie.LstDevGetTypes.errcheck = _check_status
    libtiepie.LstDevGetContainedSerialNumbers.restype = c_uint32
    libtiepie.LstDevGetContainedSerialNumbers.argtypes = [c_uint32, c_uint32,
                                                          c_void_p, c_uint32]
    libtiepie.LstDevGetContainedSerialNumbers.errcheck = _check_status
    libtiepie.LstCbDevGetProductId.restype = c_uint32
    libtiepie.LstCbDevGetProductId.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstCbDevGetProductId.errcheck = _check_status
    libtiepie.LstCbDevGetVendorId.restype = c_uint32
    libtiepie.LstCbDevGetVendorId.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstCbDevGetVendorId.errcheck = _check_status
    libtiepie.LstCbDevGetName.restype = c_uint32
    libtiepie.LstCbDevGetName.argtypes = [c_uint32, c_uint32, c_uint32,
                                          c_char_p, c_uint32]
    libtiepie.LstCbDevGetName.errcheck = _check_status
    libtiepie.LstCbDevGetNameShort.restype = c_uint32
    libtiepie.LstCbDevGetNameShort.argtypes = [c_uint32, c_uint32, c_uint32,
                                               c_char_p, c_uint32]
    libtiepie.LstCbDevGetNameShort.errcheck = _check_status
    libtiepie.LstCbDevGetNameShortest.restype = c_uint32
    libtiepie.LstCbDevGetNameShortest.argtypes = [c_uint32, c_uint32, c_uint32,
                                                  c_char_p, c_uint32]
    libtiepie.LstCbDevGetNameShortest.errcheck = _check_status
    libtiepie.LstCbDevGetDriverVersion.restype = c_uint64
    libtiepie.LstCbDevGetDriverVersion.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstCbDevGetDriverVersion.errcheck = _check_status
    libtiepie.LstCbDevGetFirmwareVersion.restype = c_uint64
    libtiepie.LstCbDevGetFirmwareVersion.argtypes = [c_uint32, c_uint32,
                                                     c_uint32]
    libtiepie.LstCbDevGetFirmwareVersion.errcheck = _check_status
    libtiepie.LstCbDevGetCalibrationDate.restype = c_uint32
    libtiepie.LstCbDevGetCalibrationDate.argtypes = [c_uint32, c_uint32,
                                                     c_uint32]
    libtiepie.LstCbDevGetCalibrationDate.errcheck = _check_status
    libtiepie.LstCbScpGetChannelCount.restype = c_uint16
    libtiepie.LstCbScpGetChannelCount.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.LstCbScpGetChannelCount.errcheck = _check_status
    libtiepie.LstSetCallbackDeviceAdded.restype = None
    libtiepie.LstSetCallbackDeviceAdded.argtypes = [CallbackDeviceList,
                                                    c_void_p]
    libtiepie.LstSetCallbackDeviceAdded.errcheck = _check_status
    libtiepie.LstSetCallbackDeviceRemoved.restype = None
    libtiepie.LstSetCallbackDeviceRemoved.argtypes = [CallbackDeviceList,
                                                      c_void_p]
    libtiepie.LstSetCallbackDeviceRemoved.errcheck = _check_status
    libtiepie.LstSetCallbackDeviceCanOpenChanged.restype = None
    libtiepie.LstSetCallbackDeviceCanOpenChanged.argtypes = [CallbackDeviceList,
                                                             c_void_p]
    libtiepie.LstSetCallbackDeviceCanOpenChanged.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.LstSetEventDeviceAdded.restype = None
        libtiepie.LstSetEventDeviceAdded.argtypes = [c_int]
        libtiepie.LstSetEventDeviceAdded.errcheck = _check_status
        libtiepie.LstSetEventDeviceRemoved.restype = None
        libtiepie.LstSetEventDeviceRemoved.argtypes = [c_int]
        libtiepie.LstSetEventDeviceRemoved.errcheck = _check_status
        libtiepie.LstSetEventDeviceCanOpenChanged.restype = None
        libtiepie.LstSetEventDeviceCanOpenChanged.argtypes = [c_int]
        libtiepie.LstSetEventDeviceCanOpenChanged.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.LstSetEventDeviceAdded.restype = None
        libtiepie.LstSetEventDeviceAdded.argtypes = [HANDLE]
        libtiepie.LstSetEventDeviceAdded.errcheck = _check_status
        libtiepie.LstSetEventDeviceRemoved.restype = None
        libtiepie.LstSetEventDeviceRemoved.argtypes = [HANDLE]
        libtiepie.LstSetEventDeviceRemoved.errcheck = _check_status
        libtiepie.LstSetMessageDeviceAdded.restype = None
        libtiepie.LstSetMessageDeviceAdded.argtypes = [HWND]
        libtiepie.LstSetMessageDeviceAdded.errcheck = _check_status
        libtiepie.LstSetMessageDeviceRemoved.restype = None
        libtiepie.LstSetMessageDeviceRemoved.argtypes = [HWND]
        libtiepie.LstSetMessageDeviceRemoved.errcheck = _check_status
        libtiepie.LstSetMessageDeviceCanOpenChanged.restype = None
        libtiepie.LstSetMessageDeviceCanOpenChanged.argtypes = [HWND]
        libtiepie.LstSetMessageDeviceCanOpenChanged.errcheck = _check_status
    libtiepie.NetGetAutoDetectEnabled.restype = c_uint8
    libtiepie.NetGetAutoDetectEnabled.argtypes = []
    libtiepie.NetGetAutoDetectEnabled.errcheck = _check_status
    libtiepie.NetSetAutoDetectEnabled.restype = c_uint8
    libtiepie.NetSetAutoDetectEnabled.argtypes = [c_uint8]
    libtiepie.NetSetAutoDetectEnabled.errcheck = _check_status
    libtiepie.NetSrvAdd.restype = c_uint8
    libtiepie.NetSrvAdd.argtypes = [c_char_p, c_uint32, c_void_p]
    libtiepie.NetSrvAdd.errcheck = _check_status
    libtiepie.NetSrvRemove.restype = c_uint8
    libtiepie.NetSrvRemove.argtypes = [c_char_p, c_uint32, c_uint8]
    libtiepie.NetSrvRemove.errcheck = _check_status
    libtiepie.NetSrvGetCount.restype = c_uint32
    libtiepie.NetSrvGetCount.argtypes = []
    libtiepie.NetSrvGetCount.errcheck = _check_status
    libtiepie.NetSrvGetByIndex.restype = c_uint32
    libtiepie.NetSrvGetByIndex.argtypes = [c_uint32]
    libtiepie.NetSrvGetByIndex.errcheck = _check_status
    libtiepie.NetSrvGetByURL.restype = c_uint32
    libtiepie.NetSrvGetByURL.argtypes = [c_char_p, c_uint32]
    libtiepie.NetSrvGetByURL.errcheck = _check_status
    libtiepie.NetSrvSetCallbackAdded.restype = None
    libtiepie.NetSrvSetCallbackAdded.argtypes = [CallbackHandle, c_void_p]
    libtiepie.NetSrvSetCallbackAdded.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.NetSrvSetEventAdded.restype = None
        libtiepie.NetSrvSetEventAdded.argtypes = [c_int]
        libtiepie.NetSrvSetEventAdded.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.NetSrvSetEventAdded.restype = None
        libtiepie.NetSrvSetEventAdded.argtypes = [HANDLE]
        libtiepie.NetSrvSetEventAdded.errcheck = _check_status
        libtiepie.NetSrvSetMessageAdded.restype = None
        libtiepie.NetSrvSetMessageAdded.argtypes = [HWND]
        libtiepie.NetSrvSetMessageAdded.errcheck = _check_status
    libtiepie.ObjClose.restype = None
    libtiepie.ObjClose.argtypes = [c_uint32]
    libtiepie.ObjClose.errcheck = _check_status
    libtiepie.ObjIsRemoved.restype = c_uint8
    libtiepie.ObjIsRemoved.argtypes = [c_uint32]
    libtiepie.ObjIsRemoved.errcheck = _check_status
    libtiepie.ObjGetInterfaces.restype = c_uint64
    libtiepie.ObjGetInterfaces.argtypes = [c_uint32]
    libtiepie.ObjGetInterfaces.errcheck = _check_status
    libtiepie.ObjSetEventCallback.restype = None
    libtiepie.ObjSetEventCallback.argtypes = [c_uint32, CallbackObject,
                                              c_void_p]
    libtiepie.ObjSetEventCallback.errcheck = _check_status
    libtiepie.ObjSetEventCallback.errcheck = _check_status
    libtiepie.ObjGetEvent.restype = c_uint8
    libtiepie.ObjGetEvent.argtypes = [c_uint32, c_void_p, c_void_p]
    libtiepie.ObjGetEvent.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.ObjSetEventEvent.restype = None
        libtiepie.ObjSetEventEvent.argtypes = [c_uint32, c_int]
        libtiepie.ObjSetEventEvent.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.ObjSetEventEvent.restype = None
        libtiepie.ObjSetEventEvent.argtypes = [c_uint32, HANDLE]
        libtiepie.ObjSetEventEvent.errcheck = _check_status
        libtiepie.ObjSetEventWindowHandle.restype = None
        libtiepie.ObjSetEventWindowHandle.argtypes = [c_uint32, HWND]
        libtiepie.ObjSetEventWindowHandle.errcheck = _check_status
    libtiepie.DevClose.restype = None
    libtiepie.DevClose.argtypes = [c_uint32]
    libtiepie.DevClose.errcheck = _check_status
    libtiepie.DevIsRemoved.restype = c_uint8
    libtiepie.DevIsRemoved.argtypes = [c_uint32]
    libtiepie.DevIsRemoved.errcheck = _check_status
    libtiepie.DevGetDriverVersion.restype = c_uint64
    libtiepie.DevGetDriverVersion.argtypes = [c_uint32]
    libtiepie.DevGetDriverVersion.errcheck = _check_status
    libtiepie.DevGetFirmwareVersion.restype = c_uint64
    libtiepie.DevGetFirmwareVersion.argtypes = [c_uint32]
    libtiepie.DevGetFirmwareVersion.errcheck = _check_status
    libtiepie.DevGetCalibrationDate.restype = c_uint32
    libtiepie.DevGetCalibrationDate.argtypes = [c_uint32]
    libtiepie.DevGetCalibrationDate.errcheck = _check_status
    libtiepie.DevGetCalibrationToken.restype = c_uint32
    libtiepie.DevGetCalibrationToken.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.DevGetCalibrationToken.errcheck = _check_status
    libtiepie.DevGetSerialNumber.restype = c_uint32
    libtiepie.DevGetSerialNumber.argtypes = [c_uint32]
    libtiepie.DevGetSerialNumber.errcheck = _check_status
    libtiepie.DevGetIPv4Address.restype = c_uint32
    libtiepie.DevGetIPv4Address.argtypes = [c_uint32]
    libtiepie.DevGetIPv4Address.errcheck = _check_status
    libtiepie.DevGetIPPort.restype = c_uint16
    libtiepie.DevGetIPPort.argtypes = [c_uint32]
    libtiepie.DevGetIPPort.errcheck = _check_status
    libtiepie.DevGetProductId.restype = c_uint32
    libtiepie.DevGetProductId.argtypes = [c_uint32]
    libtiepie.DevGetProductId.errcheck = _check_status
    libtiepie.DevGetVendorId.restype = c_uint32
    libtiepie.DevGetVendorId.argtypes = [c_uint32]
    libtiepie.DevGetVendorId.errcheck = _check_status
    libtiepie.DevGetType.restype = c_uint32
    libtiepie.DevGetType.argtypes = [c_uint32]
    libtiepie.DevGetType.errcheck = _check_status
    libtiepie.DevGetName.restype = c_uint32
    libtiepie.DevGetName.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.DevGetName.errcheck = _check_status
    libtiepie.DevGetNameShort.restype = c_uint32
    libtiepie.DevGetNameShort.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.DevGetNameShort.errcheck = _check_status
    libtiepie.DevGetNameShortest.restype = c_uint32
    libtiepie.DevGetNameShortest.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.DevGetNameShortest.errcheck = _check_status
    libtiepie.DevHasBattery.restype = c_uint8
    libtiepie.DevHasBattery.argtypes = [c_uint32]
    libtiepie.DevHasBattery.errcheck = _check_status
    libtiepie.DevGetBatteryCharge.restype = c_int8
    libtiepie.DevGetBatteryCharge.argtypes = [c_uint32]
    libtiepie.DevGetBatteryCharge.errcheck = _check_status
    libtiepie.DevGetBatteryTimeToEmpty.restype = c_int32
    libtiepie.DevGetBatteryTimeToEmpty.argtypes = [c_uint32]
    libtiepie.DevGetBatteryTimeToEmpty.errcheck = _check_status
    libtiepie.DevGetBatteryTimeToFull.restype = c_int32
    libtiepie.DevGetBatteryTimeToFull.argtypes = [c_uint32]
    libtiepie.DevGetBatteryTimeToFull.errcheck = _check_status
    libtiepie.DevIsBatteryChargerConnected.restype = c_uint8
    libtiepie.DevIsBatteryChargerConnected.argtypes = [c_uint32]
    libtiepie.DevIsBatteryChargerConnected.errcheck = _check_status
    libtiepie.DevIsBatteryCharging.restype = c_uint8
    libtiepie.DevIsBatteryCharging.argtypes = [c_uint32]
    libtiepie.DevIsBatteryCharging.errcheck = _check_status
    libtiepie.DevIsBatteryBroken.restype = c_uint8
    libtiepie.DevIsBatteryBroken.argtypes = [c_uint32]
    libtiepie.DevIsBatteryBroken.errcheck = _check_status
    libtiepie.DevSetCallbackRemoved.restype = None
    libtiepie.DevSetCallbackRemoved.argtypes = [c_uint32, Callback, c_void_p]
    libtiepie.DevSetCallbackRemoved.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.DevSetEventRemoved.restype = None
        libtiepie.DevSetEventRemoved.argtypes = [c_uint32, c_int]
        libtiepie.DevSetEventRemoved.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.DevSetEventRemoved.restype = None
        libtiepie.DevSetEventRemoved.argtypes = [c_uint32, HANDLE]
        libtiepie.DevSetEventRemoved.errcheck = _check_status
        libtiepie.DevSetMessageRemoved.restype = None
        libtiepie.DevSetMessageRemoved.argtypes = [c_uint32, HWND, WPARAM,
                                                   LPARAM]
        libtiepie.DevSetMessageRemoved.errcheck = _check_status
    libtiepie.DevTrGetInputCount.restype = c_uint16
    libtiepie.DevTrGetInputCount.argtypes = [c_uint32]
    libtiepie.DevTrGetInputCount.errcheck = _check_status
    libtiepie.DevTrGetInputIndexById.restype = c_uint16
    libtiepie.DevTrGetInputIndexById.argtypes = [c_uint32, c_uint32]
    libtiepie.DevTrGetInputIndexById.errcheck = _check_status
    libtiepie.ScpTrInIsTriggered.restype = c_uint8
    libtiepie.ScpTrInIsTriggered.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpTrInIsTriggered.errcheck = _check_status
    libtiepie.DevTrInGetEnabled.restype = c_uint8
    libtiepie.DevTrInGetEnabled.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrInGetEnabled.errcheck = _check_status
    libtiepie.DevTrInSetEnabled.restype = c_uint8
    libtiepie.DevTrInSetEnabled.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.DevTrInSetEnabled.errcheck = _check_status
    libtiepie.DevTrInGetKinds.restype = c_uint64
    libtiepie.DevTrInGetKinds.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrInGetKinds.errcheck = _check_status
    libtiepie.ScpTrInGetKindsEx.restype = c_uint64
    libtiepie.ScpTrInGetKindsEx.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpTrInGetKindsEx.errcheck = _check_status
    libtiepie.DevTrInGetKind.restype = c_uint64
    libtiepie.DevTrInGetKind.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrInGetKind.errcheck = _check_status
    libtiepie.DevTrInSetKind.restype = c_uint64
    libtiepie.DevTrInSetKind.argtypes = [c_uint32, c_uint16, c_uint64]
    libtiepie.DevTrInSetKind.errcheck = _check_status
    libtiepie.DevTrInIsAvailable.restype = c_uint8
    libtiepie.DevTrInIsAvailable.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrInIsAvailable.errcheck = _check_status
    libtiepie.ScpTrInIsAvailableEx.restype = c_uint8
    libtiepie.ScpTrInIsAvailableEx.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpTrInIsAvailableEx.errcheck = _check_status
    libtiepie.DevTrInGetId.restype = c_uint32
    libtiepie.DevTrInGetId.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrInGetId.errcheck = _check_status
    libtiepie.DevTrInGetName.restype = c_uint32
    libtiepie.DevTrInGetName.argtypes = [c_uint32, c_uint16, c_char_p, c_uint32]
    libtiepie.DevTrInGetName.errcheck = _check_status
    libtiepie.DevTrGetOutputCount.restype = c_uint16
    libtiepie.DevTrGetOutputCount.argtypes = [c_uint32]
    libtiepie.DevTrGetOutputCount.errcheck = _check_status
    libtiepie.DevTrGetOutputIndexById.restype = c_uint16
    libtiepie.DevTrGetOutputIndexById.argtypes = [c_uint32, c_uint32]
    libtiepie.DevTrGetOutputIndexById.errcheck = _check_status
    libtiepie.DevTrOutGetEnabled.restype = c_uint8
    libtiepie.DevTrOutGetEnabled.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrOutGetEnabled.errcheck = _check_status
    libtiepie.DevTrOutSetEnabled.restype = c_uint8
    libtiepie.DevTrOutSetEnabled.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.DevTrOutSetEnabled.errcheck = _check_status
    libtiepie.DevTrOutGetEvents.restype = c_uint64
    libtiepie.DevTrOutGetEvents.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrOutGetEvents.errcheck = _check_status
    libtiepie.DevTrOutGetEvent.restype = c_uint64
    libtiepie.DevTrOutGetEvent.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrOutGetEvent.errcheck = _check_status
    libtiepie.DevTrOutSetEvent.restype = c_uint64
    libtiepie.DevTrOutSetEvent.argtypes = [c_uint32, c_uint16, c_uint64]
    libtiepie.DevTrOutSetEvent.errcheck = _check_status
    libtiepie.DevTrOutGetId.restype = c_uint32
    libtiepie.DevTrOutGetId.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrOutGetId.errcheck = _check_status
    libtiepie.DevTrOutGetName.restype = c_uint32
    libtiepie.DevTrOutGetName.argtypes = [c_uint32, c_uint16, c_char_p,
                                          c_uint32]
    libtiepie.DevTrOutGetName.errcheck = _check_status
    libtiepie.DevTrOutTrigger.restype = c_uint8
    libtiepie.DevTrOutTrigger.argtypes = [c_uint32, c_uint16]
    libtiepie.DevTrOutTrigger.errcheck = _check_status
    libtiepie.ScpGetChannelCount.restype = c_uint16
    libtiepie.ScpGetChannelCount.argtypes = [c_uint32]
    libtiepie.ScpGetChannelCount.errcheck = _check_status
    libtiepie.ScpChIsAvailable.restype = c_uint8
    libtiepie.ScpChIsAvailable.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChIsAvailable.errcheck = _check_status
    libtiepie.ScpChIsAvailableEx.restype = c_uint8
    libtiepie.ScpChIsAvailableEx.argtypes = [c_uint32, c_uint16, c_uint32,
                                             c_double, c_uint8, c_void_p,
                                             c_uint16]
    libtiepie.ScpChIsAvailableEx.errcheck = _check_status
    libtiepie.ScpChGetConnectorType.restype = c_uint32
    libtiepie.ScpChGetConnectorType.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetConnectorType.errcheck = _check_status
    libtiepie.ScpChIsDifferential.restype = c_uint8
    libtiepie.ScpChIsDifferential.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChIsDifferential.errcheck = _check_status
    libtiepie.ScpChGetImpedance.restype = c_double
    libtiepie.ScpChGetImpedance.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetImpedance.errcheck = _check_status
    libtiepie.ScpChGetBandwidths.restype = c_uint32
    libtiepie.ScpChGetBandwidths.argtypes = [c_uint32, c_uint16, c_void_p,
                                             c_uint32]
    libtiepie.ScpChGetBandwidths.errcheck = _check_status
    libtiepie.ScpChGetBandwidth.restype = c_double
    libtiepie.ScpChGetBandwidth.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetBandwidth.errcheck = _check_status
    libtiepie.ScpChSetBandwidth.restype = c_double
    libtiepie.ScpChSetBandwidth.argtypes = [c_uint32, c_uint16, c_double]
    libtiepie.ScpChSetBandwidth.errcheck = _check_status
    libtiepie.ScpChGetCouplings.restype = c_uint64
    libtiepie.ScpChGetCouplings.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetCouplings.errcheck = _check_status
    libtiepie.ScpChGetCoupling.restype = c_uint64
    libtiepie.ScpChGetCoupling.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetCoupling.errcheck = _check_status
    libtiepie.ScpChSetCoupling.restype = c_uint64
    libtiepie.ScpChSetCoupling.argtypes = [c_uint32, c_uint16, c_uint64]
    libtiepie.ScpChSetCoupling.errcheck = _check_status
    libtiepie.ScpChGetEnabled.restype = c_uint8
    libtiepie.ScpChGetEnabled.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetEnabled.errcheck = _check_status
    libtiepie.ScpChSetEnabled.restype = c_uint8
    libtiepie.ScpChSetEnabled.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.ScpChSetEnabled.errcheck = _check_status
    libtiepie.ScpChGetProbeGain.restype = c_double
    libtiepie.ScpChGetProbeGain.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetProbeGain.errcheck = _check_status
    libtiepie.ScpChSetProbeGain.restype = c_double
    libtiepie.ScpChSetProbeGain.argtypes = [c_uint32, c_uint16, c_double]
    libtiepie.ScpChSetProbeGain.errcheck = _check_status
    libtiepie.ScpChGetProbeOffset.restype = c_double
    libtiepie.ScpChGetProbeOffset.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetProbeOffset.errcheck = _check_status
    libtiepie.ScpChSetProbeOffset.restype = c_double
    libtiepie.ScpChSetProbeOffset.argtypes = [c_uint32, c_uint16, c_double]
    libtiepie.ScpChSetProbeOffset.errcheck = _check_status
    libtiepie.ScpChGetAutoRanging.restype = c_uint8
    libtiepie.ScpChGetAutoRanging.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetAutoRanging.errcheck = _check_status
    libtiepie.ScpChSetAutoRanging.restype = c_uint8
    libtiepie.ScpChSetAutoRanging.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.ScpChSetAutoRanging.errcheck = _check_status
    libtiepie.ScpChGetRanges.restype = c_uint32
    libtiepie.ScpChGetRanges.argtypes = [c_uint32, c_uint16, c_void_p, c_uint32]
    libtiepie.ScpChGetRanges.errcheck = _check_status
    libtiepie.ScpChGetRangesEx.restype = c_uint32
    libtiepie.ScpChGetRangesEx.argtypes = [c_uint32, c_uint16, c_uint64,
                                           c_void_p, c_uint32]
    libtiepie.ScpChGetRangesEx.errcheck = _check_status
    libtiepie.ScpChGetRange.restype = c_double
    libtiepie.ScpChGetRange.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetRange.errcheck = _check_status
    libtiepie.ScpChSetRange.restype = c_double
    libtiepie.ScpChSetRange.argtypes = [c_uint32, c_uint16, c_double]
    libtiepie.ScpChSetRange.errcheck = _check_status
    libtiepie.ScpChHasSafeGround.restype = c_uint8
    libtiepie.ScpChHasSafeGround.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChHasSafeGround.errcheck = _check_status
    libtiepie.ScpChGetSafeGroundEnabled.restype = c_uint8
    libtiepie.ScpChGetSafeGroundEnabled.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetSafeGroundEnabled.errcheck = _check_status
    libtiepie.ScpChSetSafeGroundEnabled.restype = c_uint8
    libtiepie.ScpChSetSafeGroundEnabled.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.ScpChSetSafeGroundEnabled.errcheck = _check_status
    libtiepie.ScpChGetSafeGroundThresholdMin.restype = c_double
    libtiepie.ScpChGetSafeGroundThresholdMin.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetSafeGroundThresholdMin.errcheck = _check_status
    libtiepie.ScpChGetSafeGroundThresholdMax.restype = c_double
    libtiepie.ScpChGetSafeGroundThresholdMax.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetSafeGroundThresholdMax.errcheck = _check_status
    libtiepie.ScpChGetSafeGroundThreshold.restype = c_double
    libtiepie.ScpChGetSafeGroundThreshold.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetSafeGroundThreshold.errcheck = _check_status
    libtiepie.ScpChSetSafeGroundThreshold.restype = c_double
    libtiepie.ScpChSetSafeGroundThreshold.argtypes = [c_uint32, c_uint16,
                                                      c_double]
    libtiepie.ScpChSetSafeGroundThreshold.errcheck = _check_status
    libtiepie.ScpChVerifySafeGroundThreshold.restype = c_double
    libtiepie.ScpChVerifySafeGroundThreshold.argtypes = [c_uint32, c_uint16,
                                                         c_double]
    libtiepie.ScpChVerifySafeGroundThreshold.errcheck = _check_status
    libtiepie.ScpChHasTrigger.restype = c_uint8
    libtiepie.ScpChHasTrigger.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChHasTrigger.errcheck = _check_status
    libtiepie.ScpChHasTriggerEx.restype = c_uint8
    libtiepie.ScpChHasTriggerEx.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChHasTriggerEx.errcheck = _check_status
    libtiepie.ScpChTrIsAvailable.restype = c_uint8
    libtiepie.ScpChTrIsAvailable.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrIsAvailable.errcheck = _check_status
    libtiepie.ScpChTrIsAvailableEx.restype = c_uint8
    libtiepie.ScpChTrIsAvailableEx.argtypes = [c_uint32, c_uint16, c_uint32,
                                               c_double, c_uint8, c_void_p,
                                               c_void_p, c_uint16]
    libtiepie.ScpChTrIsAvailableEx.errcheck = _check_status
    libtiepie.ScpChTrIsTriggered.restype = c_uint8
    libtiepie.ScpChTrIsTriggered.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrIsTriggered.errcheck = _check_status
    libtiepie.ScpChTrGetEnabled.restype = c_uint8
    libtiepie.ScpChTrGetEnabled.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetEnabled.errcheck = _check_status
    libtiepie.ScpChTrSetEnabled.restype = c_uint8
    libtiepie.ScpChTrSetEnabled.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.ScpChTrSetEnabled.errcheck = _check_status
    libtiepie.ScpChTrGetKinds.restype = c_uint64
    libtiepie.ScpChTrGetKinds.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetKinds.errcheck = _check_status
    libtiepie.ScpChTrGetKindsEx.restype = c_uint64
    libtiepie.ScpChTrGetKindsEx.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrGetKindsEx.errcheck = _check_status
    libtiepie.ScpChTrGetKind.restype = c_uint64
    libtiepie.ScpChTrGetKind.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetKind.errcheck = _check_status
    libtiepie.ScpChTrSetKind.restype = c_uint64
    libtiepie.ScpChTrSetKind.argtypes = [c_uint32, c_uint16, c_uint64]
    libtiepie.ScpChTrSetKind.errcheck = _check_status
    libtiepie.ScpChTrGetLevelModes.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetLevelModes.restype = c_uint32
    libtiepie.ScpChTrGetLevelModes.errcheck = _check_status
    libtiepie.ScpChTrGetLevelMode.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetLevelMode.restype = c_uint32
    libtiepie.ScpChTrGetLevelMode.errcheck = _check_status
    libtiepie.ScpChTrSetLevelMode.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrSetLevelMode.restype = c_uint32
    libtiepie.ScpChTrSetLevelMode.errcheck = _check_status
    libtiepie.ScpChTrGetLevelCount.restype = c_uint32
    libtiepie.ScpChTrGetLevelCount.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetLevelCount.errcheck = _check_status
    libtiepie.ScpChTrGetLevel.restype = c_double
    libtiepie.ScpChTrGetLevel.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrGetLevel.errcheck = _check_status
    libtiepie.ScpChTrSetLevel.restype = c_double
    libtiepie.ScpChTrSetLevel.argtypes = [c_uint32, c_uint16, c_uint32,
                                          c_double]
    libtiepie.ScpChTrSetLevel.errcheck = _check_status
    libtiepie.ScpChTrGetHysteresisCount.restype = c_uint32
    libtiepie.ScpChTrGetHysteresisCount.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetHysteresisCount.errcheck = _check_status
    libtiepie.ScpChTrGetHysteresis.restype = c_double
    libtiepie.ScpChTrGetHysteresis.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrGetHysteresis.errcheck = _check_status
    libtiepie.ScpChTrSetHysteresis.restype = c_double
    libtiepie.ScpChTrSetHysteresis.argtypes = [c_uint32, c_uint16, c_uint32,
                                               c_double]
    libtiepie.ScpChTrSetHysteresis.errcheck = _check_status
    libtiepie.ScpChTrGetConditions.restype = c_uint32
    libtiepie.ScpChTrGetConditions.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetConditions.errcheck = _check_status
    libtiepie.ScpChTrGetConditionsEx.restype = c_uint32
    libtiepie.ScpChTrGetConditionsEx.argtypes = [c_uint32, c_uint16, c_uint32,
                                                 c_uint64]
    libtiepie.ScpChTrGetConditionsEx.errcheck = _check_status
    libtiepie.ScpChTrGetCondition.restype = c_uint32
    libtiepie.ScpChTrGetCondition.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetCondition.errcheck = _check_status
    libtiepie.ScpChTrSetCondition.restype = c_uint32
    libtiepie.ScpChTrSetCondition.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrSetCondition.errcheck = _check_status
    libtiepie.ScpChTrGetTimeCount.restype = c_uint32
    libtiepie.ScpChTrGetTimeCount.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChTrGetTimeCount.errcheck = _check_status
    libtiepie.ScpChTrGetTime.restype = c_double
    libtiepie.ScpChTrGetTime.argtypes = [c_uint32, c_uint16, c_uint32]
    libtiepie.ScpChTrGetTime.errcheck = _check_status
    libtiepie.ScpChTrSetTime.restype = c_double
    libtiepie.ScpChTrSetTime.argtypes = [c_uint32, c_uint16, c_uint32, c_double]
    libtiepie.ScpChTrSetTime.errcheck = _check_status
    libtiepie.ScpChTrVerifyTime.restype = c_double
    libtiepie.ScpChTrVerifyTime.argtypes = [c_uint32, c_uint16, c_uint32,
                                            c_double]
    libtiepie.ScpChTrVerifyTime.errcheck = _check_status
    libtiepie.ScpChTrVerifyTimeEx2.restype = c_double
    libtiepie.ScpChTrVerifyTimeEx2.argtypes = [c_uint32, c_uint16, c_uint32,
                                               c_double, c_uint32, c_double,
                                               c_uint64, c_uint32]
    libtiepie.ScpChTrVerifyTimeEx2.errcheck = _check_status
    libtiepie.ScpGetData.restype = c_uint64
    libtiepie.ScpGetData.argtypes = [c_uint32, c_void_p, c_uint16, c_uint64,
                                     c_uint64]
    libtiepie.ScpGetData.errcheck = _check_status
    libtiepie.ScpGetData1Ch.restype = c_uint64
    libtiepie.ScpGetData1Ch.argtypes = [c_uint32, c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetData1Ch.errcheck = _check_status
    libtiepie.ScpGetData2Ch.restype = c_uint64
    libtiepie.ScpGetData2Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_uint64,
                                        c_uint64]
    libtiepie.ScpGetData2Ch.errcheck = _check_status
    libtiepie.ScpGetData3Ch.restype = c_uint64
    libtiepie.ScpGetData3Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_uint64, c_uint64]
    libtiepie.ScpGetData3Ch.errcheck = _check_status
    libtiepie.ScpGetData4Ch.restype = c_uint64
    libtiepie.ScpGetData4Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetData4Ch.errcheck = _check_status
    libtiepie.ScpGetData5Ch.restype = c_uint64
    libtiepie.ScpGetData5Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetData5Ch.errcheck = _check_status
    libtiepie.ScpGetData6Ch.restype = c_uint64
    libtiepie.ScpGetData6Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_void_p, c_void_p, c_uint64,
                                        c_uint64]
    libtiepie.ScpGetData6Ch.errcheck = _check_status
    libtiepie.ScpGetData7Ch.restype = c_uint64
    libtiepie.ScpGetData7Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_void_p, c_void_p, c_void_p,
                                        c_uint64, c_uint64]
    libtiepie.ScpGetData7Ch.errcheck = _check_status
    libtiepie.ScpGetData8Ch.restype = c_uint64
    libtiepie.ScpGetData8Ch.argtypes = [c_uint32, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_void_p, c_void_p, c_void_p,
                                        c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetData8Ch.errcheck = _check_status
    libtiepie.ScpGetValidPreSampleCount.restype = c_uint64
    libtiepie.ScpGetValidPreSampleCount.argtypes = [c_uint32]
    libtiepie.ScpGetValidPreSampleCount.errcheck = _check_status
    libtiepie.ScpChGetDataValueRange.restype = None
    libtiepie.ScpChGetDataValueRange.argtypes = [c_uint32, c_uint16, c_void_p,
                                                 c_void_p]
    libtiepie.ScpChGetDataValueRange.errcheck = _check_status
    libtiepie.ScpChGetDataValueMin.restype = c_double
    libtiepie.ScpChGetDataValueMin.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataValueMin.errcheck = _check_status
    libtiepie.ScpChGetDataValueMax.restype = c_double
    libtiepie.ScpChGetDataValueMax.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataValueMax.errcheck = _check_status
    libtiepie.ScpGetDataRaw.restype = c_uint64
    libtiepie.ScpGetDataRaw.argtypes = [c_uint32, c_void_p, c_uint16, c_uint64,
                                        c_uint64]
    libtiepie.ScpGetDataRaw.errcheck = _check_status
    libtiepie.ScpGetDataRaw1Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw1Ch.argtypes = [c_uint32, c_void_p, c_uint64,
                                           c_uint64]
    libtiepie.ScpGetDataRaw1Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw2Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw2Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_uint64, c_uint64]
    libtiepie.ScpGetDataRaw2Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw3Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw3Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetDataRaw3Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw4Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw4Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_uint64,
                                           c_uint64]
    libtiepie.ScpGetDataRaw4Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw5Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw5Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_void_p,
                                           c_uint64, c_uint64]
    libtiepie.ScpGetDataRaw5Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw6Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw6Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_void_p,
                                           c_void_p, c_uint64, c_uint64]
    libtiepie.ScpGetDataRaw6Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw7Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw7Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_uint64,
                                           c_uint64]
    libtiepie.ScpGetDataRaw7Ch.errcheck = _check_status
    libtiepie.ScpGetDataRaw8Ch.restype = c_uint64
    libtiepie.ScpGetDataRaw8Ch.argtypes = [c_uint32, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_void_p,
                                           c_void_p, c_void_p, c_void_p,
                                           c_uint64, c_uint64]
    libtiepie.ScpGetDataRaw8Ch.errcheck = _check_status
    libtiepie.ScpChGetDataRawType.restype = c_uint32
    libtiepie.ScpChGetDataRawType.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataRawType.errcheck = _check_status
    libtiepie.ScpChGetDataRawValueRange.restype = None
    libtiepie.ScpChGetDataRawValueRange.argtypes = [c_uint32, c_uint16,
                                                    c_void_p, c_void_p,
                                                    c_void_p]
    libtiepie.ScpChGetDataRawValueRange.errcheck = _check_status
    libtiepie.ScpChGetDataRawValueMin.restype = c_int64
    libtiepie.ScpChGetDataRawValueMin.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataRawValueMin.errcheck = _check_status
    libtiepie.ScpChGetDataRawValueZero.restype = c_int64
    libtiepie.ScpChGetDataRawValueZero.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataRawValueZero.errcheck = _check_status
    libtiepie.ScpChGetDataRawValueMax.restype = c_int64
    libtiepie.ScpChGetDataRawValueMax.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChGetDataRawValueMax.errcheck = _check_status
    libtiepie.ScpChIsRangeMaxReachable.restype = c_uint8
    libtiepie.ScpChIsRangeMaxReachable.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChIsRangeMaxReachable.errcheck = _check_status
    libtiepie.ScpIsGetDataAsyncCompleted.restype = c_uint8
    libtiepie.ScpIsGetDataAsyncCompleted.argtypes = [c_uint32]
    libtiepie.ScpIsGetDataAsyncCompleted.errcheck = _check_status
    libtiepie.ScpStartGetDataAsync.restype = c_uint8
    libtiepie.ScpStartGetDataAsync.argtypes = [c_uint32, c_void_p, c_uint16,
                                               c_uint64, c_uint64]
    libtiepie.ScpStartGetDataAsync.errcheck = _check_status
    libtiepie.ScpStartGetDataAsyncRaw.restype = c_uint8
    libtiepie.ScpStartGetDataAsyncRaw.argtypes = [c_uint32, c_void_p, c_uint16,
                                                  c_uint64, c_uint64]
    libtiepie.ScpStartGetDataAsyncRaw.errcheck = _check_status
    libtiepie.ScpCancelGetDataAsync.restype = c_uint8
    libtiepie.ScpCancelGetDataAsync.argtypes = [c_uint32]
    libtiepie.ScpCancelGetDataAsync.errcheck = _check_status
    libtiepie.ScpSetCallbackDataReady.restype = None
    libtiepie.ScpSetCallbackDataReady.argtypes = [c_uint32, Callback, c_void_p]
    libtiepie.ScpSetCallbackDataReady.errcheck = _check_status
    libtiepie.ScpSetCallbackDataOverflow.restype = None
    libtiepie.ScpSetCallbackDataOverflow.argtypes = [c_uint32, Callback,
                                                     c_void_p]
    libtiepie.ScpSetCallbackDataOverflow.errcheck = _check_status
    libtiepie.ScpSetCallbackConnectionTestCompleted.restype = None
    libtiepie.ScpSetCallbackConnectionTestCompleted.argtypes = [c_uint32,
                                                                Callback,
                                                                c_void_p]
    libtiepie.ScpSetCallbackConnectionTestCompleted.errcheck = _check_status
    libtiepie.ScpSetCallbackTriggered.restype = None
    libtiepie.ScpSetCallbackTriggered.argtypes = [c_uint32, Callback, c_void_p]
    libtiepie.ScpSetCallbackTriggered.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.ScpSetEventDataReady.restype = None
        libtiepie.ScpSetEventDataReady.argtypes = [c_uint32, c_int]
        libtiepie.ScpSetEventDataReady.errcheck = _check_status
        libtiepie.ScpSetEventDataOverflow.restype = None
        libtiepie.ScpSetEventDataOverflow.argtypes = [c_uint32, c_int]
        libtiepie.ScpSetEventDataOverflow.errcheck = _check_status
        libtiepie.ScpSetEventConnectionTestCompleted.restype = None
        libtiepie.ScpSetEventConnectionTestCompleted.argtypes = [c_uint32,
                                                                 c_int]
        libtiepie.ScpSetEventConnectionTestCompleted.errcheck = _check_status
        libtiepie.ScpSetEventTriggered.restype = None
        libtiepie.ScpSetEventTriggered.argtypes = [c_uint32, c_int]
        libtiepie.ScpSetEventTriggered.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.ScpSetEventDataReady.restype = None
        libtiepie.ScpSetEventDataReady.argtypes = [c_uint32, HANDLE]
        libtiepie.ScpSetEventDataReady.errcheck = _check_status
        libtiepie.ScpSetEventDataOverflow.restype = None
        libtiepie.ScpSetEventDataOverflow.argtypes = [c_uint32, HANDLE]
        libtiepie.ScpSetEventDataOverflow.errcheck = _check_status
        libtiepie.ScpSetEventConnectionTestCompleted.restype = None
        libtiepie.ScpSetEventConnectionTestCompleted.argtypes = [c_uint32,
                                                                 HANDLE]
        libtiepie.ScpSetEventConnectionTestCompleted.errcheck = _check_status
        libtiepie.ScpSetEventTriggered.restype = None
        libtiepie.ScpSetEventTriggered.argtypes = [c_uint32, HANDLE]
        libtiepie.ScpSetEventTriggered.errcheck = _check_status
        libtiepie.ScpSetMessageDataReady.restype = None
        libtiepie.ScpSetMessageDataReady.argtypes = [c_uint32, HWND, WPARAM,
                                                     LPARAM]
        libtiepie.ScpSetMessageDataReady.errcheck = _check_status
        libtiepie.ScpSetMessageDataOverflow.restype = None
        libtiepie.ScpSetMessageDataOverflow.argtypes = [c_uint32, HWND, WPARAM,
                                                        LPARAM]
        libtiepie.ScpSetMessageDataOverflow.errcheck = _check_status
        libtiepie.ScpSetMessageConnectionTestCompleted.restype = None
        libtiepie.ScpSetMessageConnectionTestCompleted.argtypes = [c_uint32,
                                                                   HWND, WPARAM,
                                                                   LPARAM]
        libtiepie.ScpSetMessageConnectionTestCompleted.errcheck = _check_status
        libtiepie.ScpSetMessageTriggered.restype = None
        libtiepie.ScpSetMessageTriggered.argtypes = [c_uint32, HWND, WPARAM,
                                                     LPARAM]
        libtiepie.ScpSetMessageTriggered.errcheck = _check_status
    libtiepie.ScpStart.restype = c_uint8
    libtiepie.ScpStart.argtypes = [c_uint32]
    libtiepie.ScpStart.errcheck = _check_status
    libtiepie.ScpStop.restype = c_uint8
    libtiepie.ScpStop.argtypes = [c_uint32]
    libtiepie.ScpStop.errcheck = _check_status
    libtiepie.ScpForceTrigger.restype = c_uint8
    libtiepie.ScpForceTrigger.argtypes = [c_uint32]
    libtiepie.ScpForceTrigger.errcheck = _check_status
    libtiepie.ScpGetMeasureModes.restype = c_uint32
    libtiepie.ScpGetMeasureModes.argtypes = [c_uint32]
    libtiepie.ScpGetMeasureModes.errcheck = _check_status
    libtiepie.ScpGetMeasureMode.restype = c_uint32
    libtiepie.ScpGetMeasureMode.argtypes = [c_uint32]
    libtiepie.ScpGetMeasureMode.errcheck = _check_status
    libtiepie.ScpSetMeasureMode.restype = c_uint32
    libtiepie.ScpSetMeasureMode.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpSetMeasureMode.errcheck = _check_status
    libtiepie.ScpIsRunning.restype = c_uint8
    libtiepie.ScpIsRunning.argtypes = [c_uint32]
    libtiepie.ScpIsRunning.errcheck = _check_status
    libtiepie.ScpIsTriggered.restype = c_uint8
    libtiepie.ScpIsTriggered.argtypes = [c_uint32]
    libtiepie.ScpIsTriggered.errcheck = _check_status
    libtiepie.ScpIsTimeOutTriggered.restype = c_uint8
    libtiepie.ScpIsTimeOutTriggered.argtypes = [c_uint32]
    libtiepie.ScpIsTimeOutTriggered.errcheck = _check_status
    libtiepie.ScpIsForceTriggered.restype = c_uint8
    libtiepie.ScpIsForceTriggered.argtypes = [c_uint32]
    libtiepie.ScpIsForceTriggered.errcheck = _check_status
    libtiepie.ScpIsDataReady.restype = c_uint8
    libtiepie.ScpIsDataReady.argtypes = [c_uint32]
    libtiepie.ScpIsDataReady.errcheck = _check_status
    libtiepie.ScpIsDataOverflow.restype = c_uint8
    libtiepie.ScpIsDataOverflow.argtypes = [c_uint32]
    libtiepie.ScpIsDataOverflow.errcheck = _check_status
    libtiepie.ScpGetAutoResolutionModes.restype = c_uint32
    libtiepie.ScpGetAutoResolutionModes.argtypes = [c_uint32]
    libtiepie.ScpGetAutoResolutionModes.errcheck = _check_status
    libtiepie.ScpGetAutoResolutionMode.restype = c_uint32
    libtiepie.ScpGetAutoResolutionMode.argtypes = [c_uint32]
    libtiepie.ScpGetAutoResolutionMode.errcheck = _check_status
    libtiepie.ScpSetAutoResolutionMode.restype = c_uint32
    libtiepie.ScpSetAutoResolutionMode.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpSetAutoResolutionMode.errcheck = _check_status
    libtiepie.ScpGetResolutions.restype = c_uint32
    libtiepie.ScpGetResolutions.argtypes = [c_uint32, c_void_p, c_uint32]
    libtiepie.ScpGetResolutions.errcheck = _check_status
    libtiepie.ScpGetResolution.restype = c_uint8
    libtiepie.ScpGetResolution.argtypes = [c_uint32]
    libtiepie.ScpGetResolution.errcheck = _check_status
    libtiepie.ScpSetResolution.restype = c_uint8
    libtiepie.ScpSetResolution.argtypes = [c_uint32, c_uint8]
    libtiepie.ScpSetResolution.errcheck = _check_status
    libtiepie.ScpIsResolutionEnhanced.restype = c_uint8
    libtiepie.ScpIsResolutionEnhanced.argtypes = [c_uint32]
    libtiepie.ScpIsResolutionEnhanced.errcheck = _check_status
    libtiepie.ScpIsResolutionEnhancedEx.restype = c_uint8
    libtiepie.ScpIsResolutionEnhancedEx.argtypes = [c_uint32, c_uint8]
    libtiepie.ScpIsResolutionEnhancedEx.errcheck = _check_status
    libtiepie.ScpGetClockSources.restype = c_uint32
    libtiepie.ScpGetClockSources.argtypes = [c_uint32]
    libtiepie.ScpGetClockSources.errcheck = _check_status
    libtiepie.ScpGetClockSource.restype = c_uint32
    libtiepie.ScpGetClockSource.argtypes = [c_uint32]
    libtiepie.ScpGetClockSource.errcheck = _check_status
    libtiepie.ScpSetClockSource.restype = c_uint32
    libtiepie.ScpSetClockSource.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpSetClockSource.errcheck = _check_status
    libtiepie.ScpGetClockSourceFrequencies.restype = c_uint32
    libtiepie.ScpGetClockSourceFrequencies.argtypes = [c_uint32, c_void_p,
                                                       c_uint32]
    libtiepie.ScpGetClockSourceFrequencies.errcheck = _check_status
    libtiepie.ScpGetClockSourceFrequenciesEx.restype = c_uint32
    libtiepie.ScpGetClockSourceFrequenciesEx.argtypes = [c_uint32, c_uint32,
                                                         c_void_p, c_uint32]
    libtiepie.ScpGetClockSourceFrequenciesEx.errcheck = _check_status
    libtiepie.ScpGetClockSourceFrequency.restype = c_double
    libtiepie.ScpGetClockSourceFrequency.argtypes = [c_uint32]
    libtiepie.ScpGetClockSourceFrequency.errcheck = _check_status
    libtiepie.ScpSetClockSourceFrequency.restype = c_double
    libtiepie.ScpSetClockSourceFrequency.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetClockSourceFrequency.errcheck = _check_status
    libtiepie.ScpGetClockOutputs.restype = c_uint32
    libtiepie.ScpGetClockOutputs.argtypes = [c_uint32]
    libtiepie.ScpGetClockOutputs.errcheck = _check_status
    libtiepie.ScpGetClockOutput.restype = c_uint32
    libtiepie.ScpGetClockOutput.argtypes = [c_uint32]
    libtiepie.ScpGetClockOutput.errcheck = _check_status
    libtiepie.ScpSetClockOutput.restype = c_uint32
    libtiepie.ScpSetClockOutput.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpSetClockOutput.errcheck = _check_status
    libtiepie.ScpGetClockOutputFrequencies.restype = c_uint32
    libtiepie.ScpGetClockOutputFrequencies.argtypes = [c_uint32, c_void_p,
                                                       c_uint32]
    libtiepie.ScpGetClockOutputFrequencies.errcheck = _check_status
    libtiepie.ScpGetClockOutputFrequenciesEx.restype = c_uint32
    libtiepie.ScpGetClockOutputFrequenciesEx.argtypes = [c_uint32, c_uint32,
                                                         c_void_p, c_uint32]
    libtiepie.ScpGetClockOutputFrequenciesEx.errcheck = _check_status
    libtiepie.ScpGetClockOutputFrequency.restype = c_double
    libtiepie.ScpGetClockOutputFrequency.argtypes = [c_uint32]
    libtiepie.ScpGetClockOutputFrequency.errcheck = _check_status
    libtiepie.ScpSetClockOutputFrequency.restype = c_double
    libtiepie.ScpSetClockOutputFrequency.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetClockOutputFrequency.errcheck = _check_status
    libtiepie.ScpGetSampleFrequencyMax.restype = c_double
    libtiepie.ScpGetSampleFrequencyMax.argtypes = [c_uint32]
    libtiepie.ScpGetSampleFrequencyMax.errcheck = _check_status
    libtiepie.ScpGetSampleFrequency.restype = c_double
    libtiepie.ScpGetSampleFrequency.argtypes = [c_uint32]
    libtiepie.ScpGetSampleFrequency.errcheck = _check_status
    libtiepie.ScpSetSampleFrequency.restype = c_double
    libtiepie.ScpSetSampleFrequency.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetSampleFrequency.errcheck = _check_status
    libtiepie.ScpVerifySampleFrequency.restype = c_double
    libtiepie.ScpVerifySampleFrequency.argtypes = [c_uint32, c_double]
    libtiepie.ScpVerifySampleFrequency.errcheck = _check_status
    libtiepie.ScpVerifySampleFrequencyEx.restype = c_double
    libtiepie.ScpVerifySampleFrequencyEx.argtypes = [c_uint32, c_double,
                                                     c_uint32, c_uint8,
                                                     c_void_p, c_uint16]
    libtiepie.ScpVerifySampleFrequencyEx.errcheck = _check_status
    libtiepie.ScpVerifySampleFrequenciesEx.restype = None
    libtiepie.ScpVerifySampleFrequenciesEx.argtypes = [c_uint32, c_void_p,
                                                       c_uint32, c_uint32,
                                                       c_uint32,
                                                       c_uint8, c_void_p,
                                                       c_uint16]
    libtiepie.ScpVerifySampleFrequenciesEx.errcheck = _check_status
    libtiepie.ScpGetRecordLengthMax.restype = c_uint64
    libtiepie.ScpGetRecordLengthMax.argtypes = [c_uint32]
    libtiepie.ScpGetRecordLengthMax.errcheck = _check_status
    libtiepie.ScpGetRecordLengthMaxEx.restype = c_uint64
    libtiepie.ScpGetRecordLengthMaxEx.argtypes = [c_uint32, c_uint32, c_uint8]
    libtiepie.ScpGetRecordLengthMaxEx.errcheck = _check_status
    libtiepie.ScpGetRecordLength.restype = c_uint64
    libtiepie.ScpGetRecordLength.argtypes = [c_uint32]
    libtiepie.ScpGetRecordLength.errcheck = _check_status
    libtiepie.ScpSetRecordLength.restype = c_uint64
    libtiepie.ScpSetRecordLength.argtypes = [c_uint32, c_uint64]
    libtiepie.ScpSetRecordLength.errcheck = _check_status
    libtiepie.ScpVerifyRecordLength.restype = c_uint64
    libtiepie.ScpVerifyRecordLength.argtypes = [c_uint32, c_uint64]
    libtiepie.ScpVerifyRecordLength.errcheck = _check_status
    libtiepie.ScpVerifyRecordLengthEx.restype = c_uint64
    libtiepie.ScpVerifyRecordLengthEx.argtypes = [c_uint32, c_uint64, c_uint32,
                                                  c_uint8, c_void_p, c_uint16]
    libtiepie.ScpVerifyRecordLengthEx.errcheck = _check_status
    libtiepie.ScpGetPreSampleRatio.restype = c_double
    libtiepie.ScpGetPreSampleRatio.argtypes = [c_uint32]
    libtiepie.ScpGetPreSampleRatio.errcheck = _check_status
    libtiepie.ScpSetPreSampleRatio.restype = c_double
    libtiepie.ScpSetPreSampleRatio.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetPreSampleRatio.errcheck = _check_status
    libtiepie.ScpGetSegmentCountMax.restype = c_uint32
    libtiepie.ScpGetSegmentCountMax.argtypes = [c_uint32]
    libtiepie.ScpGetSegmentCountMax.errcheck = _check_status
    libtiepie.ScpGetSegmentCountMaxEx.restype = c_uint32
    libtiepie.ScpGetSegmentCountMaxEx.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpGetSegmentCountMaxEx.errcheck = _check_status
    libtiepie.ScpGetSegmentCount.restype = c_uint32
    libtiepie.ScpGetSegmentCount.argtypes = [c_uint32]
    libtiepie.ScpGetSegmentCount.errcheck = _check_status
    libtiepie.ScpSetSegmentCount.restype = c_uint32
    libtiepie.ScpSetSegmentCount.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpSetSegmentCount.errcheck = _check_status
    libtiepie.ScpVerifySegmentCount.restype = c_uint32
    libtiepie.ScpVerifySegmentCount.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpVerifySegmentCount.errcheck = _check_status
    libtiepie.ScpVerifySegmentCountEx2.restype = c_uint32
    libtiepie.ScpVerifySegmentCountEx2.argtypes = [c_uint32, c_uint32, c_uint32,
                                                   c_uint64, c_void_p, c_uint16]
    libtiepie.ScpVerifySegmentCountEx2.errcheck = _check_status
    libtiepie.ScpHasTrigger.restype = c_uint8
    libtiepie.ScpHasTrigger.argtypes = [c_uint32]
    libtiepie.ScpHasTrigger.errcheck = _check_status
    libtiepie.ScpHasTriggerEx.restype = c_uint8
    libtiepie.ScpHasTriggerEx.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpHasTriggerEx.errcheck = _check_status
    libtiepie.ScpGetTriggerTimeOut.restype = c_double
    libtiepie.ScpGetTriggerTimeOut.argtypes = [c_uint32]
    libtiepie.ScpGetTriggerTimeOut.errcheck = _check_status
    libtiepie.ScpSetTriggerTimeOut.restype = c_double
    libtiepie.ScpSetTriggerTimeOut.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetTriggerTimeOut.errcheck = _check_status
    libtiepie.ScpVerifyTriggerTimeOut.restype = c_double
    libtiepie.ScpVerifyTriggerTimeOut.argtypes = [c_uint32, c_double]
    libtiepie.ScpVerifyTriggerTimeOut.errcheck = _check_status
    libtiepie.ScpVerifyTriggerTimeOutEx.restype = c_double
    libtiepie.ScpVerifyTriggerTimeOutEx.argtypes = [c_uint32, c_double,
                                                    c_uint32, c_double]
    libtiepie.ScpVerifyTriggerTimeOutEx.errcheck = _check_status
    libtiepie.ScpHasTriggerDelay.restype = c_uint8
    libtiepie.ScpHasTriggerDelay.argtypes = [c_uint32]
    libtiepie.ScpHasTriggerDelay.errcheck = _check_status
    libtiepie.ScpHasTriggerDelayEx.restype = c_uint8
    libtiepie.ScpHasTriggerDelayEx.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpHasTriggerDelayEx.errcheck = _check_status
    libtiepie.ScpGetTriggerDelayMax.restype = c_double
    libtiepie.ScpGetTriggerDelayMax.argtypes = [c_uint32]
    libtiepie.ScpGetTriggerDelayMax.errcheck = _check_status
    libtiepie.ScpGetTriggerDelayMaxEx.restype = c_double
    libtiepie.ScpGetTriggerDelayMaxEx.argtypes = [c_uint32, c_uint32, c_double]
    libtiepie.ScpGetTriggerDelayMaxEx.errcheck = _check_status
    libtiepie.ScpGetTriggerDelay.restype = c_double
    libtiepie.ScpGetTriggerDelay.argtypes = [c_uint32]
    libtiepie.ScpGetTriggerDelay.errcheck = _check_status
    libtiepie.ScpSetTriggerDelay.restype = c_double
    libtiepie.ScpSetTriggerDelay.argtypes = [c_uint32, c_double]
    libtiepie.ScpSetTriggerDelay.errcheck = _check_status
    libtiepie.ScpVerifyTriggerDelay.restype = c_double
    libtiepie.ScpVerifyTriggerDelay.argtypes = [c_uint32, c_double]
    libtiepie.ScpVerifyTriggerDelay.errcheck = _check_status
    libtiepie.ScpVerifyTriggerDelayEx.restype = c_double
    libtiepie.ScpVerifyTriggerDelayEx.argtypes = [c_uint32, c_double, c_uint32,
                                                  c_double]
    libtiepie.ScpVerifyTriggerDelayEx.errcheck = _check_status
    libtiepie.ScpHasTriggerHoldOff.restype = c_uint8
    libtiepie.ScpHasTriggerHoldOff.argtypes = [c_uint32]
    libtiepie.ScpHasTriggerHoldOff.errcheck = _check_status
    libtiepie.ScpHasTriggerHoldOffEx.restype = c_uint8
    libtiepie.ScpHasTriggerHoldOffEx.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpHasTriggerHoldOffEx.errcheck = _check_status
    libtiepie.ScpGetTriggerHoldOffCountMax.restype = c_uint64
    libtiepie.ScpGetTriggerHoldOffCountMax.argtypes = [c_uint32]
    libtiepie.ScpGetTriggerHoldOffCountMax.errcheck = _check_status
    libtiepie.ScpGetTriggerHoldOffCountMaxEx.restype = c_uint64
    libtiepie.ScpGetTriggerHoldOffCountMaxEx.argtypes = [c_uint32, c_uint32]
    libtiepie.ScpGetTriggerHoldOffCountMaxEx.errcheck = _check_status
    libtiepie.ScpGetTriggerHoldOffCount.restype = c_uint64
    libtiepie.ScpGetTriggerHoldOffCount.argtypes = [c_uint32]
    libtiepie.ScpGetTriggerHoldOffCount.errcheck = _check_status
    libtiepie.ScpSetTriggerHoldOffCount.restype = c_uint64
    libtiepie.ScpSetTriggerHoldOffCount.argtypes = [c_uint32, c_uint64]
    libtiepie.ScpSetTriggerHoldOffCount.errcheck = _check_status
    libtiepie.ScpHasConnectionTest.restype = c_uint8
    libtiepie.ScpHasConnectionTest.argtypes = [c_uint32]
    libtiepie.ScpHasConnectionTest.errcheck = _check_status
    libtiepie.ScpChHasConnectionTest.restype = c_uint8
    libtiepie.ScpChHasConnectionTest.argtypes = [c_uint32, c_uint16]
    libtiepie.ScpChHasConnectionTest.errcheck = _check_status
    libtiepie.ScpStartConnectionTest.restype = c_uint8
    libtiepie.ScpStartConnectionTest.argtypes = [c_uint32]
    libtiepie.ScpStartConnectionTest.errcheck = _check_status
    libtiepie.ScpStartConnectionTestEx.restype = c_uint8
    libtiepie.ScpStartConnectionTestEx.argtypes = [c_uint32, c_void_p, c_uint16]
    libtiepie.ScpStartConnectionTestEx.errcheck = _check_status
    libtiepie.ScpIsConnectionTestCompleted.restype = c_uint8
    libtiepie.ScpIsConnectionTestCompleted.argtypes = [c_uint32]
    libtiepie.ScpIsConnectionTestCompleted.errcheck = _check_status
    libtiepie.ScpGetConnectionTestData.restype = c_uint16
    libtiepie.ScpGetConnectionTestData.argtypes = [c_uint32, c_void_p, c_uint16]
    libtiepie.ScpGetConnectionTestData.errcheck = _check_status
    libtiepie.GenGetConnectorType.restype = c_uint32
    libtiepie.GenGetConnectorType.argtypes = [c_uint32]
    libtiepie.GenGetConnectorType.errcheck = _check_status
    libtiepie.GenIsDifferential.restype = c_uint8
    libtiepie.GenIsDifferential.argtypes = [c_uint32]
    libtiepie.GenIsDifferential.errcheck = _check_status
    libtiepie.GenGetImpedance.restype = c_double
    libtiepie.GenGetImpedance.argtypes = [c_uint32]
    libtiepie.GenGetImpedance.errcheck = _check_status
    libtiepie.GenGetResolution.restype = c_uint8
    libtiepie.GenGetResolution.argtypes = [c_uint32]
    libtiepie.GenGetResolution.errcheck = _check_status
    libtiepie.GenGetOutputValueMin.restype = c_double
    libtiepie.GenGetOutputValueMin.argtypes = [c_uint32]
    libtiepie.GenGetOutputValueMin.errcheck = _check_status
    libtiepie.GenGetOutputValueMax.restype = c_double
    libtiepie.GenGetOutputValueMax.argtypes = [c_uint32]
    libtiepie.GenGetOutputValueMax.errcheck = _check_status
    libtiepie.GenGetOutputValueMinMax.restype = None
    libtiepie.GenGetOutputValueMinMax.argtypes = [c_uint32, c_void_p, c_void_p]
    libtiepie.GenGetOutputValueMinMax.errcheck = _check_status
    libtiepie.GenIsControllable.restype = c_uint8
    libtiepie.GenIsControllable.argtypes = [c_uint32]
    libtiepie.GenIsControllable.errcheck = _check_status
    libtiepie.GenIsRunning.restype = c_uint8
    libtiepie.GenIsRunning.argtypes = [c_uint32]
    libtiepie.GenIsRunning.errcheck = _check_status
    libtiepie.GenGetStatus.restype = c_uint32
    libtiepie.GenGetStatus.argtypes = [c_uint32]
    libtiepie.GenGetStatus.errcheck = _check_status
    libtiepie.GenGetOutputOn.restype = c_uint8
    libtiepie.GenGetOutputOn.argtypes = [c_uint32]
    libtiepie.GenGetOutputOn.errcheck = _check_status
    libtiepie.GenSetOutputOn.restype = c_uint8
    libtiepie.GenSetOutputOn.argtypes = [c_uint32, c_uint8]
    libtiepie.GenSetOutputOn.errcheck = _check_status
    libtiepie.GenHasOutputInvert.restype = c_uint8
    libtiepie.GenHasOutputInvert.argtypes = [c_uint32]
    libtiepie.GenHasOutputInvert.errcheck = _check_status
    libtiepie.GenGetOutputInvert.restype = c_uint8
    libtiepie.GenGetOutputInvert.argtypes = [c_uint32]
    libtiepie.GenGetOutputInvert.errcheck = _check_status
    libtiepie.GenSetOutputInvert.restype = c_uint8
    libtiepie.GenSetOutputInvert.argtypes = [c_uint32, c_uint8]
    libtiepie.GenSetOutputInvert.errcheck = _check_status
    libtiepie.GenStart.restype = c_uint8
    libtiepie.GenStart.argtypes = [c_uint32]
    libtiepie.GenStart.errcheck = _check_status
    libtiepie.GenStop.restype = c_uint8
    libtiepie.GenStop.argtypes = [c_uint32]
    libtiepie.GenStop.errcheck = _check_status
    libtiepie.GenGetSignalTypes.restype = c_uint32
    libtiepie.GenGetSignalTypes.argtypes = [c_uint32]
    libtiepie.GenGetSignalTypes.errcheck = _check_status
    libtiepie.GenGetSignalType.restype = c_uint32
    libtiepie.GenGetSignalType.argtypes = [c_uint32]
    libtiepie.GenGetSignalType.errcheck = _check_status
    libtiepie.GenSetSignalType.restype = c_uint32
    libtiepie.GenSetSignalType.argtypes = [c_uint32, c_uint32]
    libtiepie.GenSetSignalType.errcheck = _check_status
    libtiepie.GenHasAmplitude.restype = c_uint8
    libtiepie.GenHasAmplitude.argtypes = [c_uint32]
    libtiepie.GenHasAmplitude.errcheck = _check_status
    libtiepie.GenHasAmplitudeEx.restype = c_uint8
    libtiepie.GenHasAmplitudeEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasAmplitudeEx.errcheck = _check_status
    libtiepie.GenGetAmplitudeMin.restype = c_double
    libtiepie.GenGetAmplitudeMin.argtypes = [c_uint32]
    libtiepie.GenGetAmplitudeMin.errcheck = _check_status
    libtiepie.GenGetAmplitudeMax.restype = c_double
    libtiepie.GenGetAmplitudeMax.argtypes = [c_uint32]
    libtiepie.GenGetAmplitudeMax.errcheck = _check_status
    libtiepie.GenGetAmplitudeMinMaxEx.restype = None
    libtiepie.GenGetAmplitudeMinMaxEx.argtypes = [c_uint32, c_uint32, c_void_p,
                                                  c_void_p]
    libtiepie.GenGetAmplitudeMinMaxEx.errcheck = _check_status
    libtiepie.GenGetAmplitude.restype = c_double
    libtiepie.GenGetAmplitude.argtypes = [c_uint32]
    libtiepie.GenGetAmplitude.errcheck = _check_status
    libtiepie.GenSetAmplitude.restype = c_double
    libtiepie.GenSetAmplitude.argtypes = [c_uint32, c_double]
    libtiepie.GenSetAmplitude.errcheck = _check_status
    libtiepie.GenVerifyAmplitude.restype = c_double
    libtiepie.GenVerifyAmplitude.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyAmplitude.errcheck = _check_status
    libtiepie.GenVerifyAmplitudeEx.restype = c_double
    libtiepie.GenVerifyAmplitudeEx.argtypes = [c_uint32, c_double, c_uint32,
                                               c_uint32, c_double]
    libtiepie.GenVerifyAmplitudeEx.errcheck = _check_status
    libtiepie.GenGetAmplitudeRanges.restype = c_uint32
    libtiepie.GenGetAmplitudeRanges.argtypes = [c_uint32, c_void_p, c_uint32]
    libtiepie.GenGetAmplitudeRanges.errcheck = _check_status
    libtiepie.GenGetAmplitudeRange.restype = c_double
    libtiepie.GenGetAmplitudeRange.argtypes = [c_uint32]
    libtiepie.GenGetAmplitudeRange.errcheck = _check_status
    libtiepie.GenSetAmplitudeRange.restype = c_double
    libtiepie.GenSetAmplitudeRange.argtypes = [c_uint32, c_double]
    libtiepie.GenSetAmplitudeRange.errcheck = _check_status
    libtiepie.GenGetAmplitudeAutoRanging.restype = c_uint8
    libtiepie.GenGetAmplitudeAutoRanging.argtypes = [c_uint32]
    libtiepie.GenGetAmplitudeAutoRanging.errcheck = _check_status
    libtiepie.GenSetAmplitudeAutoRanging.restype = c_uint8
    libtiepie.GenSetAmplitudeAutoRanging.argtypes = [c_uint32, c_uint8]
    libtiepie.GenSetAmplitudeAutoRanging.errcheck = _check_status
    libtiepie.GenHasOffset.restype = c_uint8
    libtiepie.GenHasOffset.argtypes = [c_uint32]
    libtiepie.GenHasOffset.errcheck = _check_status
    libtiepie.GenHasOffsetEx.restype = c_uint8
    libtiepie.GenHasOffsetEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasOffsetEx.errcheck = _check_status
    libtiepie.GenGetOffsetMin.restype = c_double
    libtiepie.GenGetOffsetMin.argtypes = [c_uint32]
    libtiepie.GenGetOffsetMin.errcheck = _check_status
    libtiepie.GenGetOffsetMax.restype = c_double
    libtiepie.GenGetOffsetMax.argtypes = [c_uint32]
    libtiepie.GenGetOffsetMax.errcheck = _check_status
    libtiepie.GenGetOffsetMinMaxEx.restype = None
    libtiepie.GenGetOffsetMinMaxEx.argtypes = [c_uint32, c_uint32, c_void_p,
                                               c_void_p]
    libtiepie.GenGetOffsetMinMaxEx.errcheck = _check_status
    libtiepie.GenGetOffset.restype = c_double
    libtiepie.GenGetOffset.argtypes = [c_uint32]
    libtiepie.GenGetOffset.errcheck = _check_status
    libtiepie.GenSetOffset.restype = c_double
    libtiepie.GenSetOffset.argtypes = [c_uint32, c_double]
    libtiepie.GenSetOffset.errcheck = _check_status
    libtiepie.GenVerifyOffset.restype = c_double
    libtiepie.GenVerifyOffset.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyOffset.errcheck = _check_status
    libtiepie.GenVerifyOffsetEx.restype = c_double
    libtiepie.GenVerifyOffsetEx.argtypes = [c_uint32, c_double, c_uint32,
                                            c_double]
    libtiepie.GenVerifyOffsetEx.errcheck = _check_status
    libtiepie.GenGetFrequencyModes.restype = c_uint32
    libtiepie.GenGetFrequencyModes.argtypes = [c_uint32]
    libtiepie.GenGetFrequencyModes.errcheck = _check_status
    libtiepie.GenGetFrequencyModesEx.restype = c_uint32
    libtiepie.GenGetFrequencyModesEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenGetFrequencyModesEx.errcheck = _check_status
    libtiepie.GenGetFrequencyMode.restype = c_uint32
    libtiepie.GenGetFrequencyMode.argtypes = [c_uint32]
    libtiepie.GenGetFrequencyMode.errcheck = _check_status
    libtiepie.GenSetFrequencyMode.restype = c_uint32
    libtiepie.GenSetFrequencyMode.argtypes = [c_uint32, c_uint32]
    libtiepie.GenSetFrequencyMode.errcheck = _check_status
    libtiepie.GenHasFrequency.restype = c_uint8
    libtiepie.GenHasFrequency.argtypes = [c_uint32]
    libtiepie.GenHasFrequency.errcheck = _check_status
    libtiepie.GenHasFrequencyEx.restype = c_uint8
    libtiepie.GenHasFrequencyEx.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.GenHasFrequencyEx.errcheck = _check_status
    libtiepie.GenGetFrequencyMin.restype = c_double
    libtiepie.GenGetFrequencyMin.argtypes = [c_uint32]
    libtiepie.GenGetFrequencyMin.errcheck = _check_status
    libtiepie.GenGetFrequencyMax.restype = c_double
    libtiepie.GenGetFrequencyMax.argtypes = [c_uint32]
    libtiepie.GenGetFrequencyMax.errcheck = _check_status
    libtiepie.GenGetFrequencyMinMax.restype = None
    libtiepie.GenGetFrequencyMinMax.argtypes = [c_uint32, c_uint32, c_void_p,
                                                c_void_p]
    libtiepie.GenGetFrequencyMinMax.errcheck = _check_status
    libtiepie.GenGetFrequencyMinMaxEx.restype = None
    libtiepie.GenGetFrequencyMinMaxEx.argtypes = [c_uint32, c_uint32, c_uint32,
                                                  c_void_p, c_void_p]
    libtiepie.GenGetFrequencyMinMaxEx.errcheck = _check_status
    libtiepie.GenGetFrequency.restype = c_double
    libtiepie.GenGetFrequency.argtypes = [c_uint32]
    libtiepie.GenGetFrequency.errcheck = _check_status
    libtiepie.GenSetFrequency.restype = c_double
    libtiepie.GenSetFrequency.argtypes = [c_uint32, c_double]
    libtiepie.GenSetFrequency.errcheck = _check_status
    libtiepie.GenVerifyFrequency.restype = c_double
    libtiepie.GenVerifyFrequency.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyFrequency.errcheck = _check_status
    libtiepie.GenVerifyFrequencyEx2.restype = c_double
    libtiepie.GenVerifyFrequencyEx2.argtypes = [c_uint32, c_double, c_uint32,
                                                c_uint32, c_uint64, c_double]
    libtiepie.GenVerifyFrequencyEx2.errcheck = _check_status
    libtiepie.GenHasPhase.restype = c_uint8
    libtiepie.GenHasPhase.argtypes = [c_uint32]
    libtiepie.GenHasPhase.errcheck = _check_status
    libtiepie.GenHasPhaseEx.restype = c_uint8
    libtiepie.GenHasPhaseEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasPhaseEx.errcheck = _check_status
    libtiepie.GenGetPhaseMin.restype = c_double
    libtiepie.GenGetPhaseMin.argtypes = [c_uint32]
    libtiepie.GenGetPhaseMin.errcheck = _check_status
    libtiepie.GenGetPhaseMax.restype = c_double
    libtiepie.GenGetPhaseMax.argtypes = [c_uint32]
    libtiepie.GenGetPhaseMax.errcheck = _check_status
    libtiepie.GenGetPhaseMinMaxEx.restype = None
    libtiepie.GenGetPhaseMinMaxEx.argtypes = [c_uint32, c_uint32, c_void_p,
                                              c_void_p]
    libtiepie.GenGetPhaseMinMaxEx.errcheck = _check_status
    libtiepie.GenGetPhase.restype = c_double
    libtiepie.GenGetPhase.argtypes = [c_uint32]
    libtiepie.GenGetPhase.errcheck = _check_status
    libtiepie.GenSetPhase.restype = c_double
    libtiepie.GenSetPhase.argtypes = [c_uint32, c_double]
    libtiepie.GenSetPhase.errcheck = _check_status
    libtiepie.GenVerifyPhase.restype = c_double
    libtiepie.GenVerifyPhase.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyPhase.errcheck = _check_status
    libtiepie.GenVerifyPhaseEx.restype = c_double
    libtiepie.GenVerifyPhaseEx.argtypes = [c_uint32, c_double, c_uint32]
    libtiepie.GenVerifyPhaseEx.errcheck = _check_status
    libtiepie.GenHasSymmetry.restype = c_uint8
    libtiepie.GenHasSymmetry.argtypes = [c_uint32]
    libtiepie.GenHasSymmetry.errcheck = _check_status
    libtiepie.GenHasSymmetryEx.restype = c_uint8
    libtiepie.GenHasSymmetryEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasSymmetryEx.errcheck = _check_status
    libtiepie.GenGetSymmetryMin.restype = c_double
    libtiepie.GenGetSymmetryMin.argtypes = [c_uint32]
    libtiepie.GenGetSymmetryMin.errcheck = _check_status
    libtiepie.GenGetSymmetryMax.restype = c_double
    libtiepie.GenGetSymmetryMax.argtypes = [c_uint32]
    libtiepie.GenGetSymmetryMax.errcheck = _check_status
    libtiepie.GenGetSymmetryMinMaxEx.restype = None
    libtiepie.GenGetSymmetryMinMaxEx.argtypes = [c_uint32, c_uint32, c_void_p,
                                                 c_void_p]
    libtiepie.GenGetSymmetryMinMaxEx.errcheck = _check_status
    libtiepie.GenGetSymmetry.restype = c_double
    libtiepie.GenGetSymmetry.argtypes = [c_uint32]
    libtiepie.GenGetSymmetry.errcheck = _check_status
    libtiepie.GenSetSymmetry.restype = c_double
    libtiepie.GenSetSymmetry.argtypes = [c_uint32, c_double]
    libtiepie.GenSetSymmetry.errcheck = _check_status
    libtiepie.GenVerifySymmetry.restype = c_double
    libtiepie.GenVerifySymmetry.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifySymmetry.errcheck = _check_status
    libtiepie.GenVerifySymmetryEx.restype = c_double
    libtiepie.GenVerifySymmetryEx.argtypes = [c_uint32, c_double, c_uint32]
    libtiepie.GenVerifySymmetryEx.errcheck = _check_status
    libtiepie.GenHasWidth.restype = c_uint8
    libtiepie.GenHasWidth.argtypes = [c_uint32]
    libtiepie.GenHasWidth.errcheck = _check_status
    libtiepie.GenHasWidthEx.restype = c_uint8
    libtiepie.GenHasWidthEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasWidthEx.errcheck = _check_status
    libtiepie.GenGetWidthMin.restype = c_double
    libtiepie.GenGetWidthMin.argtypes = [c_uint32]
    libtiepie.GenGetWidthMin.errcheck = _check_status
    libtiepie.GenGetWidthMax.restype = c_double
    libtiepie.GenGetWidthMax.argtypes = [c_uint32]
    libtiepie.GenGetWidthMax.errcheck = _check_status
    libtiepie.GenGetWidthMinMaxEx.restype = None
    libtiepie.GenGetWidthMinMaxEx.argtypes = [c_uint32, c_uint32, c_double,
                                              c_void_p, c_void_p]
    libtiepie.GenGetWidthMinMaxEx.errcheck = _check_status
    libtiepie.GenGetWidth.restype = c_double
    libtiepie.GenGetWidth.argtypes = [c_uint32]
    libtiepie.GenGetWidth.errcheck = _check_status
    libtiepie.GenSetWidth.restype = c_double
    libtiepie.GenSetWidth.argtypes = [c_uint32, c_double]
    libtiepie.GenSetWidth.errcheck = _check_status
    libtiepie.GenVerifyWidth.restype = c_double
    libtiepie.GenVerifyWidth.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyWidth.errcheck = _check_status
    libtiepie.GenVerifyWidthEx.restype = c_double
    libtiepie.GenVerifyWidthEx.argtypes = [c_uint32, c_double, c_uint32,
                                           c_double]
    libtiepie.GenVerifyWidthEx.errcheck = _check_status
    libtiepie.GenGetLeadingEdgeTimeMin.restype = c_double
    libtiepie.GenGetLeadingEdgeTimeMin.argtypes = [c_uint32]
    libtiepie.GenGetLeadingEdgeTimeMin.errcheck = _check_status
    libtiepie.GenGetLeadingEdgeTimeMax.restype = c_double
    libtiepie.GenGetLeadingEdgeTimeMax.argtypes = [c_uint32]
    libtiepie.GenGetLeadingEdgeTimeMax.errcheck = _check_status
    libtiepie.GenGetLeadingEdgeTimeMinMaxEx.restype = None
    libtiepie.GenGetLeadingEdgeTimeMinMaxEx.argtypes = [c_uint32, c_uint32,
                                                        c_double, c_double,
                                                        c_double, c_double,
                                                        c_void_p, c_void_p]
    libtiepie.GenGetLeadingEdgeTimeMinMaxEx.errcheck = _check_status
    libtiepie.GenGetLeadingEdgeTime.restype = c_double
    libtiepie.GenGetLeadingEdgeTime.argtypes = [c_uint32]
    libtiepie.GenGetLeadingEdgeTime.errcheck = _check_status
    libtiepie.GenSetLeadingEdgeTime.restype = c_double
    libtiepie.GenSetLeadingEdgeTime.argtypes = [c_uint32, c_double]
    libtiepie.GenSetLeadingEdgeTime.errcheck = _check_status
    libtiepie.GenVerifyLeadingEdgeTime.restype = c_double
    libtiepie.GenVerifyLeadingEdgeTime.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyLeadingEdgeTime.errcheck = _check_status
    libtiepie.GenVerifyLeadingEdgeTimeEx.restype = c_double
    libtiepie.GenVerifyLeadingEdgeTimeEx.argtypes = [c_uint32, c_double,
                                                     c_uint32, c_double,
                                                     c_double, c_double,
                                                     c_double]
    libtiepie.GenVerifyLeadingEdgeTimeEx.errcheck = _check_status
    libtiepie.GenGetTrailingEdgeTimeMin.restype = c_double
    libtiepie.GenGetTrailingEdgeTimeMin.argtypes = [c_uint32]
    libtiepie.GenGetTrailingEdgeTimeMin.errcheck = _check_status
    libtiepie.GenGetTrailingEdgeTimeMax.restype = c_double
    libtiepie.GenGetTrailingEdgeTimeMax.argtypes = [c_uint32]
    libtiepie.GenGetTrailingEdgeTimeMax.errcheck = _check_status
    libtiepie.GenGetTrailingEdgeTimeMinMaxEx.restype = None
    libtiepie.GenGetTrailingEdgeTimeMinMaxEx.argtypes = [c_uint32, c_uint32,
                                                         c_double, c_double,
                                                         c_double, c_double,
                                                         c_void_p, c_void_p]
    libtiepie.GenGetTrailingEdgeTimeMinMaxEx.errcheck = _check_status
    libtiepie.GenGetTrailingEdgeTime.restype = c_double
    libtiepie.GenGetTrailingEdgeTime.argtypes = [c_uint32]
    libtiepie.GenGetTrailingEdgeTime.errcheck = _check_status
    libtiepie.GenSetTrailingEdgeTime.restype = c_double
    libtiepie.GenSetTrailingEdgeTime.argtypes = [c_uint32, c_double]
    libtiepie.GenSetTrailingEdgeTime.errcheck = _check_status
    libtiepie.GenVerifyTrailingEdgeTime.restype = c_double
    libtiepie.GenVerifyTrailingEdgeTime.argtypes = [c_uint32, c_double]
    libtiepie.GenVerifyTrailingEdgeTime.errcheck = _check_status
    libtiepie.GenVerifyTrailingEdgeTimeEx.restype = c_double
    libtiepie.GenVerifyTrailingEdgeTimeEx.argtypes = [c_uint32, c_double,
                                                      c_uint32, c_double,
                                                      c_double, c_double,
                                                      c_double]
    libtiepie.GenVerifyTrailingEdgeTimeEx.errcheck = _check_status
    libtiepie.GenHasData.restype = c_uint8
    libtiepie.GenHasData.argtypes = [c_uint32]
    libtiepie.GenHasData.errcheck = _check_status
    libtiepie.GenHasDataEx.restype = c_uint8
    libtiepie.GenHasDataEx.argtypes = [c_uint32, c_uint32]
    libtiepie.GenHasDataEx.errcheck = _check_status
    libtiepie.GenGetDataLengthMin.restype = c_uint64
    libtiepie.GenGetDataLengthMin.argtypes = [c_uint32]
    libtiepie.GenGetDataLengthMin.errcheck = _check_status
    libtiepie.GenGetDataLengthMax.restype = c_uint64
    libtiepie.GenGetDataLengthMax.argtypes = [c_uint32]
    libtiepie.GenGetDataLengthMax.errcheck = _check_status
    libtiepie.GenGetDataLengthMinMaxEx.restype = None
    libtiepie.GenGetDataLengthMinMaxEx.argtypes = [c_uint32, c_uint32, c_void_p,
                                                   c_void_p]
    libtiepie.GenGetDataLengthMinMaxEx.errcheck = _check_status
    libtiepie.GenGetDataLength.restype = c_uint64
    libtiepie.GenGetDataLength.argtypes = [c_uint32]
    libtiepie.GenGetDataLength.errcheck = _check_status
    libtiepie.GenVerifyDataLength.restype = c_uint64
    libtiepie.GenVerifyDataLength.argtypes = [c_uint32, c_uint64]
    libtiepie.GenVerifyDataLength.errcheck = _check_status
    libtiepie.GenVerifyDataLengthEx.restype = c_uint64
    libtiepie.GenVerifyDataLengthEx.argtypes = [c_uint32, c_uint64, c_uint32]
    libtiepie.GenVerifyDataLengthEx.errcheck = _check_status
    libtiepie.GenSetData.restype = None
    libtiepie.GenSetData.argtypes = [c_uint32, c_void_p, c_uint64]
    libtiepie.GenSetData.errcheck = _check_status
    libtiepie.GenSetDataEx.restype = None
    libtiepie.GenSetDataEx.argtypes = [c_uint32, c_void_p, c_uint64, c_uint32,
                                       c_uint32]
    libtiepie.GenSetDataEx.errcheck = _check_status
    libtiepie.GenGetDataRawType.restype = c_uint32
    libtiepie.GenGetDataRawType.argtypes = [c_uint32]
    libtiepie.GenGetDataRawType.errcheck = _check_status
    libtiepie.GenGetDataRawValueRange.restype = None
    libtiepie.GenGetDataRawValueRange.argtypes = [c_uint32, c_void_p, c_void_p,
                                                  c_void_p]
    libtiepie.GenGetDataRawValueRange.errcheck = _check_status
    libtiepie.GenGetDataRawValueMin.restype = c_int64
    libtiepie.GenGetDataRawValueMin.argtypes = [c_uint32]
    libtiepie.GenGetDataRawValueMin.errcheck = _check_status
    libtiepie.GenGetDataRawValueZero.restype = c_int64
    libtiepie.GenGetDataRawValueZero.argtypes = [c_uint32]
    libtiepie.GenGetDataRawValueZero.errcheck = _check_status
    libtiepie.GenGetDataRawValueMax.restype = c_int64
    libtiepie.GenGetDataRawValueMax.argtypes = [c_uint32]
    libtiepie.GenGetDataRawValueMax.errcheck = _check_status
    libtiepie.GenSetDataRaw.restype = None
    libtiepie.GenSetDataRaw.argtypes = [c_uint32, c_void_p, c_uint64]
    libtiepie.GenSetDataRaw.errcheck = _check_status
    libtiepie.GenSetDataRawEx.restype = None
    libtiepie.GenSetDataRawEx.argtypes = [c_uint32, c_void_p, c_uint64,
                                          c_uint32, c_uint32]
    libtiepie.GenSetDataRawEx.errcheck = _check_status
    libtiepie.GenGetModes.restype = c_uint64
    libtiepie.GenGetModes.argtypes = [c_uint32]
    libtiepie.GenGetModes.errcheck = _check_status
    libtiepie.GenGetModesEx.restype = c_uint64
    libtiepie.GenGetModesEx.argtypes = [c_uint32, c_uint32, c_uint32]
    libtiepie.GenGetModesEx.errcheck = _check_status
    libtiepie.GenGetModesNative.restype = c_uint64
    libtiepie.GenGetModesNative.argtypes = [c_uint32]
    libtiepie.GenGetModesNative.errcheck = _check_status
    libtiepie.GenGetMode.restype = c_uint64
    libtiepie.GenGetMode.argtypes = [c_uint32]
    libtiepie.GenGetMode.errcheck = _check_status
    libtiepie.GenSetMode.restype = c_uint64
    libtiepie.GenSetMode.argtypes = [c_uint32, c_uint64]
    libtiepie.GenSetMode.errcheck = _check_status
    libtiepie.GenIsBurstActive.restype = c_uint8
    libtiepie.GenIsBurstActive.argtypes = [c_uint32]
    libtiepie.GenIsBurstActive.errcheck = _check_status
    libtiepie.GenGetBurstCountMin.restype = c_uint64
    libtiepie.GenGetBurstCountMin.argtypes = [c_uint32]
    libtiepie.GenGetBurstCountMin.errcheck = _check_status
    libtiepie.GenGetBurstCountMax.restype = c_uint64
    libtiepie.GenGetBurstCountMax.argtypes = [c_uint32]
    libtiepie.GenGetBurstCountMax.errcheck = _check_status
    libtiepie.GenGetBurstCountMinMaxEx.restype = None
    libtiepie.GenGetBurstCountMinMaxEx.argtypes = [c_uint32, c_uint64, c_void_p,
                                                   c_void_p]
    libtiepie.GenGetBurstCountMinMaxEx.errcheck = _check_status
    libtiepie.GenGetBurstCount.restype = c_uint64
    libtiepie.GenGetBurstCount.argtypes = [c_uint32]
    libtiepie.GenGetBurstCount.errcheck = _check_status
    libtiepie.GenSetBurstCount.restype = c_uint64
    libtiepie.GenSetBurstCount.argtypes = [c_uint32, c_uint64]
    libtiepie.GenSetBurstCount.errcheck = _check_status
    libtiepie.GenGetBurstSampleCountMin.restype = c_uint64
    libtiepie.GenGetBurstSampleCountMin.argtypes = [c_uint32]
    libtiepie.GenGetBurstSampleCountMin.errcheck = _check_status
    libtiepie.GenGetBurstSampleCountMax.restype = c_uint64
    libtiepie.GenGetBurstSampleCountMax.argtypes = [c_uint32]
    libtiepie.GenGetBurstSampleCountMax.errcheck = _check_status
    libtiepie.GenGetBurstSampleCountMinMaxEx.restype = None
    libtiepie.GenGetBurstSampleCountMinMaxEx.argtypes = [c_uint32, c_uint64,
                                                         c_void_p, c_void_p]
    libtiepie.GenGetBurstSampleCountMinMaxEx.errcheck = _check_status
    libtiepie.GenGetBurstSampleCount.restype = c_uint64
    libtiepie.GenGetBurstSampleCount.argtypes = [c_uint32]
    libtiepie.GenGetBurstSampleCount.errcheck = _check_status
    libtiepie.GenSetBurstSampleCount.restype = c_uint64
    libtiepie.GenSetBurstSampleCount.argtypes = [c_uint32, c_uint64]
    libtiepie.GenSetBurstSampleCount.errcheck = _check_status
    libtiepie.GenGetBurstSegmentCountMin.restype = c_uint64
    libtiepie.GenGetBurstSegmentCountMin.argtypes = [c_uint32]
    libtiepie.GenGetBurstSegmentCountMin.errcheck = _check_status
    libtiepie.GenGetBurstSegmentCountMax.restype = c_uint64
    libtiepie.GenGetBurstSegmentCountMax.argtypes = [c_uint32]
    libtiepie.GenGetBurstSegmentCountMax.errcheck = _check_status
    libtiepie.GenGetBurstSegmentCountMinMaxEx.restype = None
    libtiepie.GenGetBurstSegmentCountMinMaxEx.argtypes = [c_uint32, c_uint64,
                                                          c_uint32, c_uint32,
                                                          c_double,
                                                          c_uint64, c_void_p,
                                                          c_void_p]
    libtiepie.GenGetBurstSegmentCountMinMaxEx.errcheck = _check_status
    libtiepie.GenGetBurstSegmentCount.restype = c_uint64
    libtiepie.GenGetBurstSegmentCount.argtypes = [c_uint32]
    libtiepie.GenGetBurstSegmentCount.errcheck = _check_status
    libtiepie.GenSetBurstSegmentCount.restype = c_uint64
    libtiepie.GenSetBurstSegmentCount.argtypes = [c_uint32, c_uint64]
    libtiepie.GenSetBurstSegmentCount.errcheck = _check_status
    libtiepie.GenVerifyBurstSegmentCount.restype = c_uint64
    libtiepie.GenVerifyBurstSegmentCount.argtypes = [c_uint32, c_uint64]
    libtiepie.GenVerifyBurstSegmentCount.errcheck = _check_status
    libtiepie.GenVerifyBurstSegmentCountEx.restype = c_uint64
    libtiepie.GenVerifyBurstSegmentCountEx.argtypes = [c_uint32, c_uint64,
                                                       c_uint64, c_uint32,
                                                       c_uint32,
                                                       c_double, c_uint64]
    libtiepie.GenVerifyBurstSegmentCountEx.errcheck = _check_status
    libtiepie.GenSetCallbackBurstCompleted.restype = None
    libtiepie.GenSetCallbackBurstCompleted.argtypes = [c_uint32, Callback,
                                                       c_void_p]
    libtiepie.GenSetCallbackBurstCompleted.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.GenSetEventBurstCompleted.restype = None
        libtiepie.GenSetEventBurstCompleted.argtypes = [c_uint32, c_int]
        libtiepie.GenSetEventBurstCompleted.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.GenSetEventBurstCompleted.restype = None
        libtiepie.GenSetEventBurstCompleted.argtypes = [c_uint32, HANDLE]
        libtiepie.GenSetEventBurstCompleted.errcheck = _check_status
        libtiepie.GenSetMessageBurstCompleted.restype = None
        libtiepie.GenSetMessageBurstCompleted.argtypes = [c_uint32, HWND,
                                                          WPARAM, LPARAM]
        libtiepie.GenSetMessageBurstCompleted.errcheck = _check_status
    libtiepie.GenSetCallbackControllableChanged.restype = None
    libtiepie.GenSetCallbackControllableChanged.argtypes = [c_uint32, Callback,
                                                            c_void_p]
    libtiepie.GenSetCallbackControllableChanged.errcheck = _check_status
    if platform.system() == 'Linux':
        libtiepie.GenSetEventControllableChanged.restype = None
        libtiepie.GenSetEventControllableChanged.argtypes = [c_uint32, c_int]
        libtiepie.GenSetEventControllableChanged.errcheck = _check_status
    if platform.system() == 'Windows':
        libtiepie.GenSetEventControllableChanged.restype = None
        libtiepie.GenSetEventControllableChanged.argtypes = [c_uint32, HANDLE]
        libtiepie.GenSetEventControllableChanged.errcheck = _check_status
        libtiepie.GenSetMessageControllableChanged.restype = None
        libtiepie.GenSetMessageControllableChanged.argtypes = [c_uint32, HWND,
                                                               WPARAM, LPARAM]
        libtiepie.GenSetMessageControllableChanged.errcheck = _check_status
    libtiepie.I2CIsInternalAddress.restype = c_uint8
    libtiepie.I2CIsInternalAddress.argtypes = [c_uint32, c_uint16]
    libtiepie.I2CIsInternalAddress.errcheck = _check_status
    libtiepie.I2CGetInternalAddresses.restype = c_uint32
    libtiepie.I2CGetInternalAddresses.argtypes = [c_uint32, c_void_p, c_uint32]
    libtiepie.I2CGetInternalAddresses.errcheck = _check_status
    libtiepie.I2CRead.restype = c_uint8
    libtiepie.I2CRead.argtypes = [c_uint32, c_uint16, c_void_p, c_uint32,
                                  c_uint8]
    libtiepie.I2CRead.errcheck = _check_status
    libtiepie.I2CReadByte.restype = c_uint8
    libtiepie.I2CReadByte.argtypes = [c_uint32, c_uint16, c_void_p]
    libtiepie.I2CReadByte.errcheck = _check_status
    libtiepie.I2CReadWord.restype = c_uint8
    libtiepie.I2CReadWord.argtypes = [c_uint32, c_uint16, c_void_p]
    libtiepie.I2CReadWord.errcheck = _check_status
    libtiepie.I2CWrite.restype = c_uint8
    libtiepie.I2CWrite.argtypes = [c_uint32, c_uint16, c_void_p, c_uint32,
                                   c_uint8]
    libtiepie.I2CWrite.errcheck = _check_status
    libtiepie.I2CWriteByte.restype = c_uint8
    libtiepie.I2CWriteByte.argtypes = [c_uint32, c_uint16, c_uint8]
    libtiepie.I2CWriteByte.errcheck = _check_status
    libtiepie.I2CWriteByteByte.restype = c_uint8
    libtiepie.I2CWriteByteByte.argtypes = [c_uint32, c_uint16, c_uint8, c_uint8]
    libtiepie.I2CWriteByteByte.errcheck = _check_status
    libtiepie.I2CWriteByteWord.restype = c_uint8
    libtiepie.I2CWriteByteWord.argtypes = [c_uint32, c_uint16, c_uint8,
                                           c_uint16]
    libtiepie.I2CWriteByteWord.errcheck = _check_status
    libtiepie.I2CWriteWord.restype = c_uint8
    libtiepie.I2CWriteWord.argtypes = [c_uint32, c_uint16, c_uint16]
    libtiepie.I2CWriteWord.errcheck = _check_status
    libtiepie.I2CWriteRead.restype = c_uint8
    libtiepie.I2CWriteRead.argtypes = [c_uint32, c_uint16, c_void_p, c_uint32,
                                       c_void_p, c_uint32]
    libtiepie.I2CWriteRead.errcheck = _check_status
    libtiepie.I2CGetSpeedMax.restype = c_double
    libtiepie.I2CGetSpeedMax.argtypes = [c_uint32]
    libtiepie.I2CGetSpeedMax.errcheck = _check_status
    libtiepie.I2CGetSpeed.restype = c_double
    libtiepie.I2CGetSpeed.argtypes = [c_uint32]
    libtiepie.I2CGetSpeed.errcheck = _check_status
    libtiepie.I2CSetSpeed.restype = c_double
    libtiepie.I2CSetSpeed.argtypes = [c_uint32, c_double]
    libtiepie.I2CSetSpeed.errcheck = _check_status
    libtiepie.I2CVerifySpeed.restype = c_double
    libtiepie.I2CVerifySpeed.argtypes = [c_uint32, c_double]
    libtiepie.I2CVerifySpeed.errcheck = _check_status
    libtiepie.SrvConnect.restype = c_uint8
    libtiepie.SrvConnect.argtypes = [c_uint32, c_uint8]
    libtiepie.SrvConnect.errcheck = _check_status
    libtiepie.SrvDisconnect.restype = c_uint8
    libtiepie.SrvDisconnect.argtypes = [c_uint32, c_uint8]
    libtiepie.SrvDisconnect.errcheck = _check_status
    libtiepie.SrvRemove.restype = c_uint8
    libtiepie.SrvRemove.argtypes = [c_uint32, c_uint8]
    libtiepie.SrvRemove.errcheck = _check_status
    libtiepie.SrvGetStatus.restype = c_uint32
    libtiepie.SrvGetStatus.argtypes = [c_uint32]
    libtiepie.SrvGetStatus.errcheck = _check_status
    libtiepie.SrvGetLastError.restype = c_uint32
    libtiepie.SrvGetLastError.argtypes = [c_uint32]
    libtiepie.SrvGetLastError.errcheck = _check_status
    libtiepie.SrvGetURL.restype = c_uint32
    libtiepie.SrvGetURL.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.SrvGetURL.errcheck = _check_status
    libtiepie.SrvGetID.restype = c_uint32
    libtiepie.SrvGetID.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.SrvGetID.errcheck = _check_status
    libtiepie.SrvGetIPv4Address.restype = c_uint32
    libtiepie.SrvGetIPv4Address.argtypes = [c_uint32]
    libtiepie.SrvGetIPv4Address.errcheck = _check_status
    libtiepie.SrvGetIPPort.restype = c_uint16
    libtiepie.SrvGetIPPort.argtypes = [c_uint32]
    libtiepie.SrvGetIPPort.errcheck = _check_status
    libtiepie.SrvGetName.restype = c_uint32
    libtiepie.SrvGetName.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.SrvGetName.errcheck = _check_status
    libtiepie.SrvGetDescription.restype = c_uint32
    libtiepie.SrvGetDescription.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.SrvGetDescription.errcheck = _check_status
    libtiepie.SrvGetVersion.restype = c_uint64
    libtiepie.SrvGetVersion.argtypes = [c_uint32]
    libtiepie.SrvGetVersion.errcheck = _check_status
    libtiepie.SrvGetVersionExtra.restype = c_uint32
    libtiepie.SrvGetVersionExtra.argtypes = [c_uint32, c_char_p, c_uint32]
    libtiepie.SrvGetVersionExtra.errcheck = _check_status
    libtiepie.HlpPointerArrayNew.restype = c_void_p
    libtiepie.HlpPointerArrayNew.argtypes = [c_uint32]
    libtiepie.HlpPointerArrayNew.errcheck = _check_status
    libtiepie.HlpPointerArraySet.restype = None
    libtiepie.HlpPointerArraySet.argtypes = [c_void_p, c_uint32, c_void_p]
    libtiepie.HlpPointerArraySet.errcheck = _check_status
    libtiepie.HlpPointerArrayDelete.restype = None
    libtiepie.HlpPointerArrayDelete.argtypes = [c_void_p]
    libtiepie.HlpPointerArrayDelete.errcheck = _check_status

    return libtiepie


def _check_status(result, func, args):
    """Checks the status after calling a library function.

    This function is not intended as standalone function. It is
    a callable to be assigned to the :py:attr:`ctypes._FuncPtr.errcheck`
    attribute of the foreign function definitions.

    Args:
        result: what the foreign function returns, as specified by the restype
                attribute
        func: the foreign function object itself
        args:  tuple containing the parameters originally passed to the
               function call

    Returns:
        The unaltered result returned by the foreign function.
    """
    status_code = libtiepie.LibGetLastStatus()

    # From API documentation:
    # 0 means ok
    # <0 means error
    # >0 means ok, but with a side effect
    if status_code != 0:
        status_str = '[' + str(
            status_code) + ']: ' + libtiepie.LibGetLastStatusStr().decode(
            'utf-8')
        if status_code > 0:
            warnings.warn(status_str)
        else:
            raise IOError(status_str)

    return result


def is_initialized():
    """Get library initialized flag.

    Returns:
        bool: True is library is initialized, False otherwise
    """
    return libtiepie.LibIsInitialized() != 0


def get_version():
    """Get library version.

    Returns:
        str: library version major.minor.release.build
    """
    raw_version = libtiepie.LibGetVersion()
    return f"{raw_version >> 48}.{(raw_version >> 32) & 0xffff}.{(raw_version >> 16) & 0xffff}.{raw_version & 0xffff}"


def get_version_postfix():
    """Get library version postfix.

    Returns:
        str: version postfix
    """
    return libtiepie.LibGetVersionExtra().decode('utf-8')


libtiepie = _load_lib()

# Init the library
libtiepie.LibInit()

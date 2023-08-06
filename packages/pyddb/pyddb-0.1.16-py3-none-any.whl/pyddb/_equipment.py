# -*- coding: utf-8 -*-
# @Time : 2022/4/6 0006 10:38 
# @Author : ruomubingfeng
# @File : _equipment.py
import json
import os
from pyddb._usbmux import Shell, ADB


class Device:
    @staticmethod
    def __android_device_list(remote_adb_host=None) -> list:
        android_devices_list = []
        android_dict = {}
        if remote_adb_host:
            shell_str = 'adb -H {} devices'.format(remote_adb_host)
        else:
            shell_str = 'adb devices'
        for device in Shell.invoke(shell_str).splitlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_dict["ident"] = device
                android_dict["deviceName"] = ADB(device).adb_android_model()
                android_dict["platform"] = ADB(device).adb_platform_name()
                android_devices_list.append(str(android_dict))
        return android_devices_list

    @staticmethod
    def __ios_device_list() -> list:
        ios_list = []
        ios_datas_list = []
        ios_dict = {}
        device_list = []
        result_str = os.popen("tidevice list")
        results = result_str.read().split("\n")
        [ios_datas_list.append(results[result].split(" " * 8)) for result in range(0, len(results))]
        [ios_list.append(ios_data[0].strip().split(" " * 2)) for ios_data in ios_datas_list]
        ios_list.pop()
        ios_list.pop(0)
        for ios_device in range(0, len(ios_list)):
            ios_dict["ident"] = ios_list[ios_device][0]
            ios_dict["deviceName"] = ios_list[ios_device][1]
            ios_dict["platform"] = "iOS"
            device_list.append(str(ios_dict))
        return device_list

    @staticmethod
    def device_info():
        device_info = []
        for device in Device.__android_device_list() + Device.__ios_device_list():
            device_info.append(eval(device))
        return json.dumps(device_info, indent=4, ensure_ascii=False)

    @staticmethod
    def is_platform(ident):
        devices = json.loads(Device.device_info())
        return ''.join([device["platform"] for device in devices if ident == device["ident"]])

    @staticmethod
    def device_ident():
        devices = json.loads(Device.device_info())
        return [device["ident"] for device in devices]

    @staticmethod
    def device_list():
        devices = json.loads(Device.device_info())
        return [device["deviceName"] for device in devices]

    @staticmethod
    def device_sysinfo():
        pass

    @staticmethod
    def device_install(file_path):
        pass

    @staticmethod
    def device_uninstall():
        pass

    @staticmethod
    def device_reboot():
        pass

    @staticmethod
    def device_shutdown():
        pass

    @staticmethod
    def device_xctest():
        pass

    @staticmethod
    def device_wdaproxy():
        pass

    @staticmethod
    def device_syslog():
        pass

    @staticmethod
    def device_crashreport():
        pass

    @staticmethod
    def device_perf():
        pass

    @staticmethod
    def device_anr():
        pass

    @staticmethod
    def device_file():
        pass


if __name__ == '__main__':
    print(Device.device_info())

#!/usr/bin/env python3


import sys
import socket
import struct
from enum import Enum
from scapy.layers.bluetooth import HCI_Cmd_LE_Create_Connection

from bluetooth._bluetooth import hci_filter_new
from bluetooth._bluetooth import hci_filter_clear
from bluetooth._bluetooth import hci_open_dev
from bluetooth._bluetooth import hci_close_dev
from bluetooth._bluetooth import hci_filter_set_ptype
from bluetooth._bluetooth import hci_filter_set_event
from bluetooth._bluetooth import hci_send_cmd
from bluetooth._bluetooth import SOL_HCI
from bluetooth._bluetooth import HCI_EVENT_PKT
from bluetooth._bluetooth import EVT_DISCONN_COMPLETE
from bluetooth._bluetooth import HCI_FILTER
from bluetooth._bluetooth import OGF_LINK_CTL
from bluetooth._bluetooth import OCF_DISCONNECT
from bluetooth._bluetooth import EVT_DISCONN_COMPLETE_SIZE
from bluetooth._bluetooth import EVT_REMOTE_NAME_REQ_COMPLETE
from bluetooth._bluetooth import EVT_REMOTE_NAME_REQ_COMPLETE_SIZE
from bluetooth._bluetooth import EVT_CMD_COMPLETE
from bluetooth._bluetooth import hci_filter_set_opcode
from bluetooth._bluetooth import cmd_opcode_pack

from bluetooth._bluetooth import OGF_INFO_PARAM
from bluetooth._bluetooth import OCF_READ_BD_ADDR
from bluetooth._bluetooth import HCI_MAX_EVENT_SIZE

OCF_REMOTE_NAME_REQUEST = 0x0019

HCI_PKT_TYPE_SIZE   = 1
EVT_CODE_SIZE       = 1
PARAM_TOTAL_LEN     = 1
NON_EVT_PARAMS_SIZE = HCI_PKT_TYPE_SIZE + EVT_CODE_SIZE + PARAM_TOTAL_LEN

sys.path.insert(0, "/home/x/OneDrive/Projects/bthci/src")
from bthci import HCI


def read_bdaddr() -> dict:
    """HCI_Read_BD_ADDR command
    
    The controller will response HCI_Command_Complete event.
    """
    # sock = hci_open_dev(0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8873))


    if sock.fileno() < 0:
        raise RuntimeError('Failed to create HCI socket. No Bluetooth adapter?')

    flt = hci_filter_new()
    hci_filter_set_ptype(flt, HCI_EVENT_PKT)
    hci_filter_set_event(flt, EVT_CMD_COMPLETE)
    hci_filter_set_opcode(
        flt, cmd_opcode_pack(OGF_INFO_PARAM, OCF_READ_BD_ADDR))
    # sock.setsockopt(SOL_HCI, HCI_FILTER, flt)


    sock.send(bytes.fromhex('f1091000'))

    # hci_send_cmd(sock, OGF_INFO_PARAM, OCF_READ_BD_ADDR)

    print('sent')
    event_params = sock.recv(HCI_MAX_EVENT_SIZE)[3:]
    num_hci_cmd_pkts, cmd_opcode, status, bd_addr = struct.unpack("<BHB6s", event_params)
    bd_addr = ["%02X"%b for b in bd_addr]
    bd_addr.reverse()
    event_params = {
        'Num_HCI_Command_Packets': num_hci_cmd_pkts,
        'Command_Opcode': cmd_opcode,
        'Status': status,
        'BD_ADDR': ':'.join(bd_addr)
    }
    
    hci_close_dev(sock.fileno())
    return event_params


def remote_name_request(self, cmd_params={'BD_ADDR': bytes(6),
    'Page_Scan_Repetition_Mode': 0x01, 'Reserved': 0x00, 'Clock_Offset': 0x0000}) -> dict:
    """HCI_Remote_Name_Request command

    The controller will response HCI_Remote_Name_Request_Complete event.

    在 inquiry 的过程中发送该命令，将导致 inquiry 被立即结束，即 controller 
    返回成功的 HCI_Inquiry_Complete event。不过此时，请求远端名字的流程不会被影响。

    BD_ADDR - Big-endian. It will be converted to little-endian internally.
    """
    # sock = hci_open_dev(self.devid)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8873))

    bin_cmd_params = struct.pack('<6sBBH', cmd_params['BD_ADDR'][::-1],
        cmd_params['Page_Scan_Repetition_Mode'], cmd_params['Reserved'],
        cmd_params['Clock_Offset'])

    flt = hci_filter_new()
    hci_filter_set_ptype(flt, HCI_EVENT_PKT)
    hci_filter_set_event(flt, EVT_REMOTE_NAME_REQ_COMPLETE)
    sock.setsockopt(SOL_HCI, HCI_FILTER, flt)

    hci_send_cmd(sock, OGF_LINK_CTL, OCF_REMOTE_NAME_REQUEST, 
        bin_cmd_params)

    event_params = sock.recv(NON_EVT_PARAMS_SIZE + \
        EVT_REMOTE_NAME_REQ_COMPLETE_SIZE)[3:]
    status, bd_addr, remote_name = struct.unpack('<B6s248s', event_params)
    event_params = {
        'Status': status,
        'BD_ADDR': bd_addr,
        'Remote_Name': remote_name
    }
    return event_params


def disconnect(cmd_params:dict) -> dict:
    """
    cmd_params -- {
        'Connection_Handle': int, 2 bytes,
        'Reason': int, 1 bytes
    }
    """
    
    # dd = hci_open_dev(self.devid)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8873))

    # send some data
    # sock.send(b"GET / HTTP/1.1\r\nHost: bing.com\r\n\r\n")
    # receive some data
    #response = sock.recv(4096)

    dd = sock

    flt = hci_filter_new()
    hci_filter_clear(flt)
    hci_filter_set_ptype(flt, HCI_EVENT_PKT)
    hci_filter_set_event(flt, EVT_DISCONN_COMPLETE)

    print(sock)
    print(repr(SOL_HCI))
    print(repr(HCI_FILTER))
    print(repr(flt))
    dd.setsockopt(SOL_HCI, HCI_FILTER, flt)

    bin_cmd_params = cmd_params['Connection_Handle'].to_bytes(2, 'little') + \
        cmd_params['Reason'].to_bytes(1, 'little')

    hci_send_cmd(dd, OGF_LINK_CTL, OCF_DISCONNECT, bin_cmd_params)

    # Receive and exclude HCI packet type (1 B)
    event_params = dd.recv(3+EVT_DISCONN_COMPLETE_SIZE)[3:] 
    status, conn_handle, reason, = struct.unpack(
        '<BHB', event_params)

    event_params = {
        'Status': status,
        'Connection_Handle': conn_handle,
        'Reason': reason
    }

    hci_close_dev(dd.fileno())
    return event_params


# class ControllerErrorCodes(Enum):
#     """
#     参考 Bluetooth Core Specification Version 5.2, Vol 1: Architecture, Mixing,
#     and Conventions, Part F: Controller Error Codes
#     """
#     SUCCESS = 0x00
#     UNKNOWN_HCI_COMMAND = 0x01
#     UNKNOWN_CONNECTION_IDENTIFIER = 0x02
#     HARDWARE_FAILURE = 0x03
#     PAGE_TIMEOUT = 0x04
#     AUTHENTICATION_FAILURE = 0x05
#     PIN_OR_KEY_MISSING = 0x06
#     MEMORY_CAPACITY_EXCEEDED = 0x07
#     CONNECTION_TIMEOUT = 0x08
#     CONNECTION_LIMIT_EXCEEDED = 0x09
#     SYNCHRONOUS_CONNECTION_LIMIT_TO_A_DEVICE_EXCEEDED = 0x0A
#     CONNECTION_ALREADY_EXISTS = 0x0B
#     COMMAND_DISALLOWED = 0x0C
#     CONNECTION_REJECTED_DUE_TO_LIMITED_RESOURCES = 0x0D
#     CONNECTION_REJECTED_DUE_TO_SECURITY_REASONS = 0x0E
#     CONNECTION_REJECTED_DUE_TO_UNACCEPTABLE_BD_ADDR = 0x0F
#     CONNECTION_ACCEPT_TIMEOUT_EXCEEDED = 0x10
#     UNSUPPORTED_FEATURE_OR_PARAMETER_VALUE = 0x11
#     INVALID_HCI_COMMAND_PARAMETERS = 0x12
#     REMOTE_USER_TERMINATED_CONNECTION = 0x13
#     REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_LOW_RESOURCES = 0x14
#     REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_POWER_OFF = 0x15
#     CONNECTION_TERMINATED_BY_LOCAL_HOST = 0x16
#     REPEATED_ATTEMPTS = 0x17
#     PAIRING_NOT_ALLOWED = 0x18
#     UNKNOWN_LMP_PDU = 0x19
#     UNSUPPORTED_REMOTE_FEATURE_UNSUPPORTED_LMP_FEATURE = 0x1A
#     SCO_OFFSET_REJECTED = 0x1B
#     SCO_INTERVAL_REJECTED = 0x1C
#     SCO_AIR_MODE_REJECTED = 0x1D
#     INVALID_LMP_PARAMETERS_INVALID_LL_PARAMETERS = 0x1E
#     UNSPECIFIED_ERROR = 0x1F
#     UNSUPPORTED_LMP_PARAMETER_VALUE_UNSUPPORTED_LL_PARAMETER_VALUE = 0x20
#     ROLE_CHANGE_NOT_ALLOWED = 0x21
#     LMP_RESPONSE_TIMEOUT_LL_RESPONSE_TIMEOUT = 0x22
#     LMP_ERROR_TRANSACTION_COLLISION_LL_PROCEDURE_COLLISION = 0x23
#     LMP_PDU_NOT_ALLOWED = 0x24
#     ENCRYPTION_MODE_NOT_ACCEPTABLE = 0x25
#     LINK_KEY_CANNOT_BE_CHANGED = 0x26
#     REQUESTED_QOS_NOT_SUPPORTED = 0x27
#     INSTANT_PASSED = 0x28
#     PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED = 0x29
#     DIFFERENT_TRANSACTION_COLLISION = 0x2A
#     RESERVED_FOR_FUTURE_USE = 0x2B
#     QOS_UNACCEPTABLE_PARAMETER = 0x2C
#     QOS_REJECTED = 0x2D
#     CHANNEL_CLASSIFICATION_NOT_SUPPORTED = 0x2E
#     INSUFFICIENT_SECURITY = 0x2F
#     PARAMETER_OUT_OF_MANDATORY_RANGE = 0x30
#     RESERVED_FOR_FUTURE_USE = 0x31
#     ROLE_SWITCH_PENDING = 0x32
#     RESERVED_FOR_FUTURE_USE = 0x33
#     RESERVED_SLOT_VIOLATION = 0x34
#     ROLE_SWITCH_FAILED = 0x35
#     EXTENDED_INQUIRY_RESPONSE_TOO_LARGE = 0x36
#     SECURE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST = 0x37
#     HOST_BUSY_PAIRING = 0x38
#     CONNECTION_REJECTED_DUE_TO_NO_SUITABLE_CHANNEL_FOUND = 0x39
#     CONTROLLER_BUSY = 0x3A
#     UNACCEPTABLE_CONNECTION_PARAMETERS = 0x3B
#     ADVERTISING_TIMEOUT = 0x3C
#     CONNECTION_TERMINATED_DUE_TO_MIC_FAILURE = 0x3D
#     CONNECTION_FAILED_TO_BE_ESTABLISHED_SYNCHRONIZATION_TIMEOUT = 0x3E
#     MAC_CONNECTION_FAILED = 0x3F
#     COARSE_CLOCK_ADJUSTMENT_REJECTED_BUT_WILL_TRY_TO_ADJUST_USING_CLOCK_DRAGGING = 0x40
#     TYPE0_SUBMAP_NOT_DEFINED = 0x41
#     UNKNOWN_ADVERTISING_IDENTIFIER = 0x42
#     LIMIT_REACHED = 0x43
#     OPERATION_CANCELLED_BY_HOST = 0x44
#     PACKET_TOO_LONG = 0x45


def main():
    # # print(BT_SECURITY_SDP, BT_SECURITY_LOW, BT_SECURITY_MEDIUM, BT_SECURITY_HIGH)
    # dd = hci_open_dev(0)
    # print(type(dd))
    # hci_close_dev(dd.fileno())
    
    hci = HCI()
    
    # print(hci)
    # paddr = bytes.fromhex("22:22:33:44:55:66".replace(":", "")[::-1])
    # hci.le_create_connection(HCI_Cmd_LE_Create_Connection(paddr=paddr))
    # # hci.le_create_connection_cancel()

    # disconnect(cmd_params={
    #     'Connection_Handle': 0x0001,
    #     'Reason': 0x01
    # })
    
    # result = hci.send_cmd(0x00, 0x102, b'\x00')
    # print(result)
    
    # print(hci.write_simple_pairing_mode(0x01))
    # print(hci.read_bdaddr())
    # print(hci.read_local_name())
    # print(hci.read_page_timeout())
    
    print(hci.read_authentication_enable())
    print(hci.write_simple_pairing_mode(0x01))
    print(hci.read_authentication_enable())
    # print(hci.write_authentication_enable())
    # print(hci.read_authentication_enable())
    
    # print(hci.read_secure_connections_host_support())
    # print(hci.write_secure_connections_host_support())
    # print(hci.read_secure_connections_host_support())
    


if __name__ == "__main__":
    main()

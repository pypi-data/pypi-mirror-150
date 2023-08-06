#!/usr/bin/env python3

import sys
sys.path.insert(0, "/home/x/OneDrive/Projects/bthci/src")

from bthci.hci import HCI, HciPacketType
from bthci.hci_cmd_pkts import cmd_opcode_pack
 
from bthci.bluez_hci import hci_filter, hci_filter_set_ptype, hci_filter_set_event, hci_filter_set_opcode, \
    EVT_LE_META_EVENT, EVT_CMD_STATUS, OGF_LE_CTL, OCF_LE_CREATE_CONN, EVT_DISCONN_COMPLETE

hci_str = HCI.get_default_hcistr()
print("hci_str:", hci_str)

hci = HCI(hci_str)
result = hci.read_bdaddr()
print(result)
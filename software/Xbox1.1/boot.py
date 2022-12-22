# SPDX-FileCopyrightText: 2021 Milador
#
# SPDX-License-Identifier: MIT

"""
`Gamepad`
====================================================

* Author(s): Milad Hajihassan
"""

import usb_hid
import usb_midi
import usb_cdc

# This is the HID gamepad descriptor compatible with XAC.
XAC_GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (GamePad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x05,  #   Report ID (5)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x35, 0x00,  #   Physical Minimum (0)
    0x45, 0x01,  #   Physical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x08,  #   Report Count (8)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (0x01)
    0x29, 0x08,  #   Usage Maximum (0x08)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x26, 0xFF, 0x00,  #   Logical Maximum (255)
    0x46, 0xFF, 0x00,  #   Physical Maximum (255)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x02,  #   Report Count (2)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))

xac_gamepad = usb_hid.Device(
    report_descriptor=XAC_GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(5,),           # Descriptor uses report ID 5.
    in_report_lengths=(3,),    # This gamepad sends 3 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

# Disable CDC if needed
#usb_cdc.disable()

# Disable midi if needed
usb_midi.disable()

usb_hid.enable((xac_gamepad,))


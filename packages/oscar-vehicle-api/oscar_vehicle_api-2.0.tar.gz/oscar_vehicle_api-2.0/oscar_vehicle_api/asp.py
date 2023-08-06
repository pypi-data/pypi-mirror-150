###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

SERIAL_PKG_LEN = 15
START_BYTE     = 0xAA
ASP_TIME       = bytearray.fromhex('0000')
CAN_CH         = bytearray.fromhex('02')
CAN_ID_L       = 4
CAN_ID_H       = 5
CAN_DATA       = 6
CAN_DATA_SIZE  = 8


def create_raw_serial_from_raw_oscar_data(raw_data):
    raw_asp_data = bytearray([START_BYTE]) + \
                   ASP_TIME + \
                   CAN_CH + \
                   bytearray([raw_data[1]]) + \
                   bytearray([raw_data[0]]) + \
                   raw_data[2:]
    raw_asp_data_crc = calc_crc8(raw_asp_data)
    raw_asp = raw_asp_data + raw_asp_data_crc
    return raw_asp


def get_pkg_from_raw_serial(raw):

    if ((len(raw) == SERIAL_PKG_LEN) and
        (raw[0] == START_BYTE)):

        return bytearray([raw[CAN_ID_H]]) + \
               bytearray([raw[CAN_ID_L]]) + \
               raw[CAN_DATA:CAN_DATA+CAN_DATA_SIZE+1]
    else:
        return None


def asp_data_crc_is_ok(raw_asp_data, raw_asp_crc):
    if calc_crc8(raw_asp_data) == raw_asp_crc:
        return True
    else:
        return False


# x^8 + x^2 + x^1 + x^0
def calc_crc8(data):

    crc8 = 0xFF

    for byte in data:
        crc8 ^= byte

        for _ in range(8):

            if (crc8 & 0x80):
                xor_val = 0x07
            else:
                xor_val = 0x00

            crc8 = ((crc8 << 1) & 0x00FF) ^ xor_val
    # print("crc8: " + hex(crc8))
    return bytearray([crc8])


# x^16 + x^12 + x^5 + x^0
def calc_crc16(data):

    crc16 = 0xFFFF

    for byte in data:
        crc16 ^= byte << 8

        for _ in range(8):

            if (crc16 & 0x8000):
                xor_val = 0x1021
            else:
                xor_val = 0x0000

            crc16 = ((crc16 << 1) & 0x00FFFF) ^ xor_val

    slp_crc16 = bytearray([crc16 & 0x00FF, crc16>>8])

    return slp_crc16


def print_raw(raw_data):
    print(" ".join(hex(byte) for byte in raw_data))

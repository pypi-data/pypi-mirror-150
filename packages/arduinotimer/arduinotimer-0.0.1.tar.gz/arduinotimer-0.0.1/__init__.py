#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
# ----------------------------------------------------------------------------
# Created By  : Felipe Mendoza   Line 3
# Created Date: 09/05/2022
# version ='0.0.1'
# ---------------------------------------------------------------------------
"""
This program is designed to get the better values of the Ps and cs register 
to calculate a specific frequency in the Arduino Timer
"""


# ---------------------------------------------------------------------------
# Imports Line 5
# ---------------------------------------------------------------------------


def get_values(f, fs):
    # Use a breakpoint in the code line below to debug your script.
    min_e = 1e10
    result = {'ps': 0, 'cs': 0}
    for Ps in [1024, 256, 64, 8, 1]:
        cs = round(f / (Ps * fs)) - 1
        error = abs(f / (Ps * (cs + 1)) - fs)
        if (error < min_e) and (cs < 2 ** 16):
            result = {'ps': Ps, 'cs': cs}
            min_e = error
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rs = get_values(16e6, 1)
    print('Prescaler: {} Cs: {}'.format(rs['ps'], rs['cs']))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

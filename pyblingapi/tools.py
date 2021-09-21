#*************************************************************************#
# © 2021 Alexandre Defendi, Nexuz System                                  #
#     _   __                         _____            __                  #               
#    / | / /__  _  ____  ______     / ___/__  _______/ /____  ____ ___    #
#   /  |/ / _ \| |/_/ / / /_  /     \__ \/ / / / ___/ __/ _ \/ __ `__ \   #
#  / /|  /  __/>  </ /_/ / / /_    ___/ / /_/ (__  ) /_/  __/ / / / / /   #
# /_/ |_/\___/_/|_|\__,_/ /___/   /____/\__, /____/\__/\___/_/ /_/ /_/    #
#                                     /____/                              #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).      #
#*************************************************************************#

from datetime import datetime

INTDATATYPE = 'integer'
FLOATDATATYPE = 'float'
NUMERICDATATYPE = 'numeric'
DECIMALDATATYPE = 'decimal'
DATEDATATYPE = 'date'
SELECTDATEDATATYPE = 'selectdate'

BLINGDATEFORMAT = '%d/%m/%Y'

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def checkData(datatype, data):
    res = False
    if datatype == INTDATATYPE:
        res = isinstance(data, int)
    elif datatype == FLOATDATATYPE:
        res = isinstance(data, float)
    elif datatype == NUMERICDATATYPE:
        if isinstance(data, str):
            res = data.isnumeric()
    elif datatype == DECIMALDATATYPE:
        if isinstance(data, str):
            res = data.isdecimal()
    elif datatype == DATEDATATYPE:
        if isinstance(data, str):
            try:
                res = bool(datetime.strptime(data,BLINGDATEFORMAT))
            except:
                pass
    elif datatype == SELECTDATEDATATYPE:
        if isinstance(data, list) and len(data) == 2:
            res = checkData(DATEDATATYPE, data[0]) and checkData(DATEDATATYPE, data[1])
    return res

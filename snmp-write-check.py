#!/usr/bin/env python3

import sys
import re

import shlex
import subprocess
from subprocess import PIPE

#Debug flag
debug = False

#Display help 
if len(sys.argv)==1 or sys.argv[1].lower()=="-h" or sys.argv[1].lower()=="--help":
    usage={}
    usage["desc"] = """Returns the number of writable OIDs and list them.
Parses the output of 'snmpwalk' and determines all elements that are readable. The return code of 'snmpset' is used to determine if an element's value can be written, by performing a write with the exact actual value.
"""
    usage["cmd"] = f"Syntax:\t{sys.argv[0]} [OPTIONS] AGENT [PARAMETERS] #see man snmpcmd"
    usage["example"] = f"Example: {sys.argv[0]} -v 2c -c public 192.168.0.3"
    usage["disclaimer"] = """
DISCLAIMAR: The script might change the value of the writable or cause other effects. Use with care.
""" 
    print("\n".join(usage.values()))
    sys.exit(0)

#Simply the command line options to snmpwalk and snmpset
options_agent = ' '.join(sys.argv[1:])

cmd = f"snmpwalk {options_agent}"
args = shlex.split(cmd)
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
out = proc.stdout.read().decode()

if(debug):
    print(f"{cmd}\n{out}\n\n")

#map between snmpwalk output and expected type by snmpset
type_map = {"INTEGER":'i', "unsigned INTEGER":'u', "UNSIGNED":'u', "TIMETICKS":'t', "Timeticks":'t', "IPADDRESS":'a', "OBJID":'o', "OID":'o',  "STRING":'s', "HEX STRING":'x', "Hex-STRING":'x', "DECIMAL STRING":'d', "BITS":'b', "unsigned int64":'U', "signed int64":'I', "float":'F', "double":'D', "NULLOBJ":'n'}

#count how many OIDs are writable
count=0


#Iterate and parse each OID
for line in out.splitlines():
    try:
        oid = line.split(" = ")[0]
        type_value = line.split(" = ")[1]
        type_ = type_map[ type_value.split(": ")[0] ] #ex: STRING: "abc"
        value = type_value.split(": ")[1]

        #for TIMETICKS extract only the numeric value
        if type_ == 't':
            match = re.search('\((.+?)\)', value)
            if match:
                value = match.group(1)
            else:
                continue
        #for HEX STRING put the value in quotes
        if type_ == 'x':
            value = f'"{value}"'

        #Try to write the existing value once again        
        cmd = f"snmpset {options_agent} {oid} {type_} {value}"
        args = shlex.split(cmd)
        if(debug):
            print(cmd)
            retcode = subprocess.call(args)
        else:
            retcode = subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        if retcode == 0:
            cmd_get = f"snmpget {options_agent} {oid}"
            args_get = shlex.split(cmd_get)
            oidtype = subprocess.run(args_get, stdout=subprocess.PIPE).stdout.decode('utf-8')
            m = re.search('=', oidtype)
            oidtype_s = oidtype[m.end():]
            print(f"{oid} is writable - "f"{oidtype_s}")
            count+=1
    except:
        pass

#return code is the number of found OIDs
sys.exit(count)


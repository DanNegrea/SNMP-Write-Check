#!/usr/bin/env python3

import pprint
pp = pprint.PrettyPrinter(indent=4)

import shlex
import subprocess
from subprocess import PIPE

import re

version = "-v 2C"
community = "-c public"
target = "127.0.0.1"

type_map = {"INTEGER":'i', "unsigned INTEGER":'u', "UNSIGNED":'u', "TIMETICKS":'t', "Timeticks":'t', "IPADDRESS":'a', "OBJID":'o', "OID":'o',  "STRING":'s', "HEX STRING":'x', "Hex-STRING":'x', "DECIMAL STRING":'d', "BITS":'b', "unsigned int64":'U', "signed int64":'I', "float":'F', "double":'D', "NULLOBJ":'n'}

cmd = f"snmpwalk {version} {community} {target}"
#cmd = "cat test/snmpwalk.out"

args = shlex.split(cmd)
proc = subprocess.Popen(args, stdout=subprocess.PIPE)
out = proc.stdout.read().decode()

walk = {} 
for line in out.splitlines():
    try:
        oid = line.split(" = ")[0]
        type_value = line.split(" = ")[1] #STRING: "DS1515+"
        type_ = type_map[ type_value.split(": ")[0] ]        
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
        
        #store values in a dictionary
        #walk[oid]= [type_, value]

        cmd = f"snmpset {version} {community} {target} {oid} {type_} {value}"
        args = shlex.split(cmd)
        retcode = subprocess.call(args)

        print(f"{cmd}\n{retcode}\n\n")
        
        #Example of FAIL
        #snmpset -v2c -c public 127.0.0.1 iso.3.6.1.2.1.1.1.0 s "AAA"    
        #Reason: noAccess
        #Failed object: iso.3.6.1.2.1.1.1.0
        #root@kali:~/.snmp/mibs# echo $?
        #2
        #...
        #Reason: notWritable (That object does not support modification)
        #Failed object: iso.3.6.1.2.1.1.1.0
        #root@kali:~/.snmp/mibs# echo $?
        #2


        #Example of SUCCESS
        #root@kali:~/.snmp/mibs# snmpset -v2c -c public 127.0.0.1 iso.3.6.1.2.1.1.5.0 s "AAA"
        #iso.3.6.1.2.1.1.5.0 = STRING: "AAA"
        #root@kali:~/.snmp/mibs# echo $?
        #0


    except:
        pass




#pp.pprint(walk)




#pp.pprint( str(out).split(' = ') )








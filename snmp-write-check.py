#!/usr/bin/env python3

import pprint
pp = pprint.PrettyPrinter(indent=4)

import shlex
import subprocess
from subprocess import PIPE

version = "-v 1"
community = "-c public"
target = "xx.xx.xx.xx"

type_map = {"INTEGER":'i', "unsigned INTEGER":'u', "TIMETICKS":'t', "IPADDRESS":'a', "OBJID":'o',  "STRING":'s', "HEX STRING":'x', "DECIMAL STRING":'d', "BITS":'b', "unsigned int64":'U', "signed int64":'I', "float":'F', "double":'D'}

cmd = f"snmpwalk {version} {community} {target}"
cmd = "cat test/snmpwalk.out"

args = shlex.split(cmd)
proc = subprocess.Popen(args, stdout=subprocess.PIPE)
out = proc.stdout.read().decode()

walk = {} 
for line in out.splitlines():
    oid = line.split(" = ")[0]
    type_value = line.split(" = ")[1] #STRING: "DS1515+"
    type_ = type_map[ type_value.split(": ")[0] ]
    value = type_value.split(": ")[1]

    walk[oid]= [type_, value]

    #cmd = f"snmpset {version} {community} {oid} {type_} {value} {target}"
    #args = shlex.split(cmd)
    #proc = subprocess.Popen(args, stdout=subprocess.PIPE)
	#retcode = proc.returncode
    #out = proc.stdout.read().decode()



pp.pprint(walk)




#pp.pprint( str(out).split(' = ') )








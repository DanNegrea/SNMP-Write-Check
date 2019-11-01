#!/usr/bin/env python3

import pprint
pp = pprint.PrettyPrinter(indent=4)

import shlex
import subprocess
from subprocess import PIPE

command = "cat snmpwalk.out"


args = shlex.split(command)
proc = subprocess.Popen(args, stdout=subprocess.PIPE)
out = proc.stdout.read().decode()

walk = {} 
for line in out.splitlines():
    id = line.split(" = ")[0]
    value = line.split(" = ")[1]

    walk[id]= value

    command = ""
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = proc.stdout.read().decode()



pp.pprint(walk)




#pp.pprint( str(out).split(' = ') )








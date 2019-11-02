# SNMP Write Check v0.1
[@sec3ty](https://twitter.com/sec3ty)

Returns the number of writable OIDs and list them.
Parses the output of 'snmpwalk' and determines all elements that are readable. The return code of 'snmpset' is used to determine if an element's value can be written, by performing a write with the exact actual value.

# Requirements for usage
Net-SNMP tools `snmpwalk` and `snmpset` 

# Usage
`snmp-write-check.py [OPTIONS] AGENT [PARAMETERS]`
where 
* `[OPTIONS]` include version `-v`, community string `-c` or credentials for v3
* `AGENT` IP address or hostname of device
these will be passed directly to `snmpwalk` and `snmpset`

**DISCLAIMAR** The script might change the value of the writable or cause other effects. Use with care.


#Recommandations

1. Disable SNMP v1 and v2c
Both of this versions are communicationg in plain-text.

2. Enable SNMP v3
The original SNMPv3 with USM or the newer SNMPv3 over (D)TLS are to be preffered.

3. Use 'authPriv' security level and strong algorithms
This guarantees both authentication and confidentiality for data in transit.
(see defSecurityLevel token in the snmp.conf)

4. Practice MIB whitelisting using SNMP views
Just information that is required for monitoring (read) or device configurations (write) should be exposed. 
Create roles and assign them views based on the least privilege principle.

5. Whitelist and control what machines can connect
Block unauthorized machines that try to consume or change the configuration.

6. Make use of a management network
Segregating the SNMP traffic (and other managemnet network) onto a dedicated management network.

#Reference
man snmpcmd



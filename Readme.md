# SNMP Write Check v0.1
[@sec3ty](https://twitter.com/sec3ty)

Returns the a list and the number of writable OIDs.

It works by parsing the output of 'snmpwalk', followed by determining all elements that are writable. The return code of 'snmpset' is used to determine if an element's value can be written, the check performs a write by using the current value. This way it tries to not alter the entries. Along the OID found to be writable it shows the type and current value obtained with 'snmpget'.

# Requirements for usage
Net-SNMP tools `snmpwalk`, `snmpset` and `snmpget`

# Usage
`snmp-write-check.py [OPTIONS] AGENT [PARAMETERS]`
where 
* `[OPTIONS]` includes info like version `-v`, community string `-c` or credentials for v3
* `AGENT` represents the IP address or hostname of device

these will be passed directly to `snmpwalk`, `snmpset` and `snmpget`

**DISCLAIMAR** The script might change the value of the writable OID or cause other effects. Use with care.


# SNMP Security Recommandations

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

#!/bin/bash
source /nfsexport/groups/lsst-daq/rpt-sdk/current/i86-linux-64/tools/envs-sdk.sh
# manual way
#ssh root@`atca_ip darwin/5/4/0 --ifname p1p1`
#minicom -w bay0.0
#reboot
cob_rce_reset 192.168.201.2/5/0/0
sleep 20
/nfsexport/groups/lsst-daq/daq-sdk/current/x86/bin/rms_servers


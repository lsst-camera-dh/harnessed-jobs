import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.subsystem.power.PowerControl
import org.lsst.ccs.subsystem.power.BK1696Device
import org.lsst.ccs.subsystem.power.RebPower
import org.lsst.ccs.subsystem.power.RebPsDevice
import org.lsst.ccs.subsystem.monitor.Channel
import org.lsst.ccs.subsystem.monitor.Page

CCSBuilder builder = ["ccs-rebps"]

int nreb = 3
def ps0 = "PS0"

builder.main (RebPower) {

    "$ps0" (RebPsDevice, devcId: "192.168.1.20", devcParm: 0)

//    MainPS (BK1696Device, connType: "serial", devcId: "/dev/ttyS0", baudRate: 0) {
    MainPS (BK1696Device, connType: "ftdi", devcId: "A5060GDP", baudRate: 0) {

        MainCtrl (PowerControl, desc: "Main PS control", hwChan: 0, voltage: 48.0,
                  current: 2.0, onDelay: 0.0, offDelay: 0.0)
    }

    Page4 (Page, id: 4, label: "Common")

    BoardTemp   (Channel, description: "Common\\Board temperature", units: "\u00b0C",
                 devcName: "$ps0", hwChan: 0, type: "TEMP", pageId: 4)

    MainVoltage (Channel, description: "Main PS Voltage", units: "Volts",
                 devcName: "MainPS", hwChan: 0, type: "VOLTAGE", pageId: 4)

    MainCurrent (Channel, description: "Main PS Current", format: ".1f", units: "mA",
                 devcName: "MainPS", hwChan: 0, type: "CURRENT", scale: 1000, pageId: 4)

    for (int i = 0; i < nreb; i++) {
        def reb = "REB$i"

        "Page$i" (Page, id: i, label: "REB $i")

        def psn = "digital"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "analog"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "OD"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.VaftLDO2" (Channel, description: "Voltage after LDO2", units: "Volts",
                                  devcName: "$ps0", hwChan: 5, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "clockhi"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "clocklo"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.VaftLDO2" (Channel, description: "Voltage after LDO2", units: "Volts",
                                  devcName: "$ps0", hwChan: 5, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "heater"

        "${reb}.${psn}.VbefLDO" (Channel, description: "$reb $psn PS\\Voltage before LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefLDO" (Channel, description: "Current before LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftLDO" (Channel, description: "Voltage after LDO", units: "Volts",
                                 devcName: "$ps0", hwChan: 2, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IaftLDO" (Channel, description: "Current after LDO", format: ".1f", units: "mA",
                                 devcName: "$ps0", hwChan: 3, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.${psn}.VaftSwch" (Channel, description: "Voltage after switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 4, type: "$i:$psn", pageId: i)

        psn = "hvbias"

        "${reb}.${psn}.VbefSwch" (Channel, description: "$reb $psn PS\\Voltage before switch", units: "Volts",
                                  devcName: "$ps0", hwChan: 0, type: "$i:$psn", pageId: i)

        "${reb}.${psn}.IbefSwch" (Channel, description: "Current before switch", format: ".3f", units: "mA",
                                  devcName: "$ps0", hwChan: 1, type: "$i:$psn", scale: 1000, pageId: i)

        "${reb}.Power"           (Channel, description: "$reb all PSs\\Total power", units: "Watts",
                                  devcName: "$ps0", hwChan: 0, type: "$i:POWER", pageId: i)

    }

}

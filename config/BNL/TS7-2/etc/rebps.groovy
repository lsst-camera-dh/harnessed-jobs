import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.bootstrap.BootstrapResourceUtils
import org.lsst.ccs.subsystem.power.PowerControl
import org.lsst.ccs.subsystem.power.BK1696Device
import org.lsst.ccs.subsystem.power.CpfeDevice
import org.lsst.ccs.subsystem.power.RebPower
import org.lsst.ccs.subsystem.power.SimPowerDevice
import org.lsst.ccs.subsystem.power.RebPsDevice
import org.lsst.ccs.monitor.Channel
import org.lsst.ccs.monitor.Page

taskConfig = ["monitor-update/taskPeriodMillis":1000,"monitor-publish/taskPeriodMillis":10000]

Properties props = BootstrapResourceUtils.getBootstrapSystemProperties()
def runMode = props.getProperty("org.lsst.ccs.run.mode", "normal")
if (runMode.equals("simulation")) {
    System.out.println("***** Loading simulated power devices")
    mainPsType = "sim"
    mainPsAttributes = [loads:[50] as double[]]
    isProto = true
} else {
    mainPsType = props.getProperty("org.lsst.ccs.main.ps.type", "bk1696")
//    mainPsAttributes = [connType: "serial", devcId: "/dev/ttyS0"]
    mainPsAttributes = [connType: "ftdi", devcId: "A5060GDP"]
    isProto = props.getProperty("org.lsst.ccs.ps.version", "prod").equals("proto")
}    
int nReb = isProto ? 3 : 6
int nTemp = isProto ? 1 : 7
def mainDevice = mainPsType.equals("bk1696") ? BK1696Device : mainPsType.equals("cpfe") ? CpfeDevice :
                 mainPsType.equals("sim") ? SimPowerDevice : null
boolean haveMainPs = mainDevice != null
boolean haveMainPsTemp = mainDevice == CpfeDevice

def ps0 = "PS0"

CCSBuilder builder = ["rebps"]

builder.main (RebPower, nodeTags:taskConfig) {

    "$ps0" (RebPsDevice, ipAddr: "192.168.1.20")

    Page7 (Page, id: 7, label: "Common")

    if (haveMainPs) {

        MainPS (mainDevice, mainPsAttributes) {

            MainCtrl (PowerControl, description: "Main PS control", hwChan: 0, voltage: 48.0,
                      current: 3.0, onDelay: 0.0, offDelay: 0.0)
        }

        MainVoltage (Channel, description: "Main PS Voltage", units: "Volts",
                     devcName: "MainPS", hwChan: 0, type: "VOLTAGE", pageId: 7)

        MainCurrent (Channel, description: "Main PS Current", format: ".1f", units: "mA",
                     devcName: "MainPS", hwChan: 0, type: "CURRENT", scale: 1000, pageId: 7)

        MainPower   (Channel, description: "Main PS Power", format: ".2f", units: "Watts",
                     devcName: "Calc", hwChan: 0, type: "PROD", subtype: "MainVoltage:MainCurrent", scale: 0.001, pageId: 7)

        if (haveMainPsTemp) {
            MainTemp (Channel, description: "Main PS Temperature", units: "\u00b0C",
                      devcName: "MainPS", hwChan: 0, type: "TEMP", pageId: 7)
        }
    }

    for (int i = 0; i < nTemp; i++) {
        "BoardTemp$i" (Channel, description: "Board temperature $i", units: "\u00b0C",
                       devcName: "$ps0", hwChan: i, type: "TEMP", pageId: 7)
    }

    for (int i = 0; i < nReb; i++) {
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

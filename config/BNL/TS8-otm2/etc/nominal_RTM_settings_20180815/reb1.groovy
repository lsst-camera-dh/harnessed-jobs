import org.lsst.ccs.startup.CCSBuilder
import org.lsst.ccs.subsystem.rafts.RaftsMain
import org.lsst.ccs.subsystem.rafts.REBDevice
import org.lsst.ccs.subsystem.rafts.DacControl
import org.lsst.ccs.subsystem.rafts.AspicControl
import org.lsst.ccs.subsystem.rafts.CabacControl
import org.lsst.ccs.monitor.Channel

taskConfig = ["monitor-update/taskPeriodMillis":1000,"monitor-publish/taskPeriodMillis":10000]

CCSBuilder builder = ["ccs-reb1"]

int nreb = 1

builder.main (RaftsMain, nodeTags:taskConfig) {

    for (int i = 0; i < nreb; i++) {
        def reb = "REB$i"
        def dreb = "DREB$i"

        "$reb" (REBDevice, hdwType:"daq0", id:0, ifcName:"em2", ccdMask:7) {

            "${reb}.DAC"  (DacControl)

            for (int j = 0; j < 6; j++) {
                def apc = "ASPIC$j"
                def cbc = "CABAC$j"

                "${reb}.${apc}" (AspicControl, hwChan:j)

                "${reb}.${cbc}" (CabacControl, hwChan:j)
            }
        }
        
        for (int j = 1; j <= 2; j++) {
                "${dreb}.Temp$j" (Channel, description: "${dreb} temperature $j", units: "\u00b0C",
                        devcName: "${reb}", hwChan: j - 1, type: "TEMP")
        }
                
        for (int j = 1; j <= 9; j++) {
                "${reb}.Temp$j" (Channel, description: "${reb} temperature $j", units: "\u00b0C",
                        devcName: "${reb}", hwChan: j + 1, type: "TEMP")
        }
                
        "${dreb}.6Vv"   (Channel, description: "${dreb} 6V voltage", units: "Volts",
                        devcName: "${reb}", hwChan:0, type: "POWER")
                    
        "${dreb}.6Vi"   (Channel, description: "${dreb} 6V current", units: "Amps",
                        devcName: "${reb}", hwChan:1, type: "POWER")
                    
        "${dreb}.9Vv"   (Channel, description: "${dreb} 9V voltage", units: "Volts",
                        devcName: "${reb}", hwChan:2, type: "POWER")
                    
        "${dreb}.9Vi"   (Channel, description: "${dreb} 9V current", units: "Amps",
                        devcName: "${reb}", hwChan:3, type: "POWER")
                         
        "${dreb}.24Vv"  (Channel, description: "${dreb} 24V voltage", units: "Volts",
                        devcName: "${reb}", hwChan:4, type: "POWER")

        "${dreb}.24Vi"  (Channel, description: "${dreb} 24V current", units: "Amps",
                        devcName: "${reb}", hwChan:5, type: "POWER")
                    
        "${dreb}.40Vv"  (Channel, description: "${dreb} 40V voltage", units: "Volts",
                        devcName: "${reb}", hwChan:6, type: "POWER")

        "${dreb}.40Vi"  (Channel, description: "${dreb} 40V current", units: "Amps",
                        devcName: "${reb}", hwChan:7, type: "POWER")
                    
    }

}

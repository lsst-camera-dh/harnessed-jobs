import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.subsystem.rafts.RaftsMain
import org.lsst.ccs.subsystem.rafts.REBDevice
import org.lsst.ccs.subsystem.rafts.DacControl
import org.lsst.ccs.subsystem.rafts.AspicControl
import org.lsst.ccs.subsystem.rafts.BiasControl
import org.lsst.ccs.monitor.Channel
import org.lsst.ccs.drivers.reb.SlowAdcs
import org.lsst.ccs.drivers.reb.sim.ClientFactorySimulation

taskConfig = ["monitor-update/taskPeriodMillis":1000,"monitor-publish/taskPeriodMillis":10000]

CCSBuilder builder = ["ccs-reb3"]

def runMode = System.getProperty("org.lsst.ccs.run.mode", "normal")
clientFactory = runMode.equals("simulation") ? new ClientFactorySimulation() : null

int nreb = Integer.valueOf(System.getProperty("org.lsst.ccs.rafts.nreb", "1"))

builder.main (RaftsMain, clientFactory:clientFactory, nodeTags:taskConfig) {

    for (int i = 0; i < nreb; i++) {
        def reb = "REB$i"
        def dreb = "DREB$i"

        "$reb" (REBDevice, hdwType:"daq1", id:i, ifcName:"", ccdMask:7, clientFactory:clientFactory) {

            "${reb}.DAC"  (DacControl)

            for (int j = 0; j < 6; j++) {
                def apc = "ASPIC$j"
                "${reb}.${apc}" (AspicControl, hwChan:j)
            }

            for (int j = 0; j < 3; j++) {
                def bias = "Bias$j"
                "${reb}.${bias}" (BiasControl, hwChan:j)
            }
        }

        String title = "${reb} temperatures\\"
        for (int j = 1; j <= 10; j++) {
            "${reb}.Temp$j" (Channel, description: "${title}Board temperature $j", units:"\u00b0C",
                                    devcName: "${reb}", hwChan: j - 1, type: "TEMP")                                    
            title = ""
        }

        "${reb}.Atemp0U" (Channel, description: "ASPIC 0 upper temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 0, type: "ATEMP")
                                 
        "${reb}.Atemp0L" (Channel, description: "ASPIC 0 lower temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 1, type: "ATEMP")
                                 
        "${reb}.Atemp1U" (Channel, description: "ASPIC 1 upper temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 2, type: "ATEMP")
                                 
        "${reb}.Atemp1L" (Channel, description: "ASPIC 1 lower temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 3, type: "ATEMP")
                                 
        "${reb}.Atemp2U" (Channel, description: "ASPIC 2 upper temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 4, type: "ATEMP")
                                 
        "${reb}.Atemp2L" (Channel, description: "ASPIC 2 lower temp", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 5, type: "ATEMP")
                                 
        for (int j = 0; j < 3; j++) {
            "${reb}.CCDTemp$j" (Channel, description: "CCD $j temperature", units:"\u00b0C",
                               devcName: "${reb}", hwChan: j, type: "RTD")                               
        }

        "${reb}.RTDtemp" (Channel, description: "RTD temperature", units:"\u00b0C",
                                 devcName: "${reb}", hwChan: 3, type: "RTD")
                                 
        "${reb}.DigV"    (Channel, description: "${reb} board power\\Digital PS voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: 0, type: "POWER")
                                 
        "${reb}.DigI"    (Channel, description: "Digital PS current", format:".1f", units:"mA",
                                 devcName: "${reb}", hwChan: 1, type: "POWER", scale:1000)
                                 
        "${reb}.AnaV"    (Channel, description: "Analog PS voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: 2, type: "POWER")
                                 
        "${reb}.AnaI"    (Channel, description: "Analog PS current", format:".1f", units:"mA",
                                 devcName: "${reb}", hwChan: 3, type: "POWER", scale:1000)
                                 
        "${reb}.ClkV"    (Channel, description: "Clock PS voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: 4, type: "POWER")
                                 
        "${reb}.ClkI"    (Channel, description: "Clock PS current", format:".1f", units:"mA",
                                 devcName: "${reb}", hwChan: 5, type: "POWER", scale:1000)
                                 
        "${reb}.ODV"     (Channel, description: "OD PS voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: 6, type: "POWER")
                                 
        "${reb}.ODI"     (Channel, description: "OD PS current", format:".1f", units:"mA",
                                 devcName: "${reb}", hwChan: 7, type: "POWER", scale:1000)
                                 
        "${reb}.OD0V"    (Channel, description: "${reb} bias voltages\\OD 0 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OD_0, type: "BIAS")
                                 
        "${reb}.OG0V"    (Channel, description: "OG 0 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OG_0, type: "BIAS")
                                 
        "${reb}.RD0V"    (Channel, description: "RD 0 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_RD_0, type: "BIAS")
                                 
        "${reb}.GD0V"    (Channel, description: "GD 0 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_GD_0, type: "BIAS")
                                 
        "${reb}.OD1V"    (Channel, description: "OD 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OD_1, type: "BIAS")
                                 
        "${reb}.OG1V"    (Channel, description: "OG 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OG_1, type: "BIAS")
                                 
        "${reb}.RD1V"    (Channel, description: "RD 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_RD_1, type: "BIAS")
                                 
        "${reb}.GD1V"    (Channel, description: "GD 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_GD_1, type: "BIAS")
                                 
        "${reb}.OD2V"    (Channel, description: "OD 2 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OD_2, type: "BIAS")
                                 
        "${reb}.OG2V"    (Channel, description: "OG 2 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_OG_2, type: "BIAS")
                                 
        "${reb}.RD2V"    (Channel, description: "RD 2 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_RD_2, type: "BIAS")
                                 
        "${reb}.GD2V"    (Channel, description: "GD 2 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_GD_2, type: "BIAS")
                                 
        "${reb}.Ref05V"  (Channel, description: "5V ref 0 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_VREF5_0, type: "BIAS")
                                 
        "${reb}.Ref15V"  (Channel, description: "5V ref 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_VREF5_1, type: "BIAS")
                                 
        "${reb}.Ref25V"  (Channel, description: "5V ref 2 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_VREF5_2, type: "BIAS")
                                 
        "${reb}.Ref125V" (Channel, description: "2.5V ref 1 voltage", units:"Volts",
                                 devcName: "${reb}", hwChan: SlowAdcs.CHAN_VREF25_1, type: "BIAS")
                                 
        title = "${reb} CCD currents\\"
        for (int js = 0; js < 3; js++) {
            for (int jd = 0; jd < 2; jd++) {
                String tb = jd == 0 ? "upper" : "lower"

                for (int jc = 0; jc < 8; jc++) {
                    int ch = jc + 8 * jd + 16 * js

                    "${reb}.CCDI${js}${jd}${jc}" \
                         (Channel, description: "${title}CCD ${js} ${tb} current ${jc}", format:".3f", units:"mA",
                                          devcName: "${reb}", hwChan: ch, type: "CURR", scale: 1000)
                                          
                    title = ""
                }
            }
        }

    }

}

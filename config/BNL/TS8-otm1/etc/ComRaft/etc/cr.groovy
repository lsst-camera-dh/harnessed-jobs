import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.bootstrap.BootstrapResourceUtils
import org.lsst.ccs.subsystem.rafts.RaftsMain
import org.lsst.ccs.subsystem.rafts.REBDevice
import org.lsst.ccs.subsystem.rafts.DacControl
import org.lsst.ccs.subsystem.rafts.BiasControl
import org.lsst.ccs.subsystem.rafts.AspicControl
import org.lsst.ccs.drivers.reb.PowerAdcs
import org.lsst.ccs.drivers.reb.SlowAdcs
import org.lsst.ccs.monitor.Channel
import org.lsst.ccs.monitor.Page
import org.lsst.ccs.drivers.reb.sim.ClientFactorySimulation
import org.lsst.ccs.daq.utilities.FitsService

taskConfig = ["monitor-update/taskPeriodMillis":1000,"monitor-publish/taskPeriodMillis":10000,
              "agentStatusAggregatorService/patternConfigList":[
              "[pattern:.*,predicate:[agentName:cr-raft]]",
              "[pattern:.*,predicate:[agentName:cr-rebps]]",
              "[pattern:.*,predicate:[agentName:ts7-2cr]]"]
             ]

Properties props = BootstrapResourceUtils.getBootstrapSystemProperties()
def runMode = props.getProperty("org.lsst.ccs.run.mode", "normal")
factory = runMode.equals("simulation") ? new ClientFactorySimulation() : null

int raftId = Integer.valueOf(props.getProperty("org.lsst.ccs.rafts.id", "0"))
def partition = props.getProperty("org.lsst.ccs.rafts.partition", "cr")

CCSBuilder builder = ["ccs-cr"]

builder.main (RaftsMain, nodeTags:taskConfig) {

    def wreb = "WREB"
    def greb = "GREB"


    fitsService (FitsService, 
        headerFilesList:["primary", "extended", "cr-primary:primary", "cr-reb_cond:reb_cond", "cr-test_cond:test_cond"]            
    )


    "$wreb" (REBDevice, hdwType: "daq2", id: 4 * raftId, ifcName: partition, ccdMask: 1, clientFactory:factory) {

        "${wreb}.DAC"  (DacControl)

        for (int j = 0; j < 2; j++) {
            "${wreb}.ASPIC$j" (AspicControl, hwChan: j)
        }

        for (int j = 0; j < 1; j++) {
            "${wreb}.Bias$j" (BiasControl, hwChan: j)
        }
    }

    "$greb" (REBDevice, hdwType: "daq2", id: 4 * raftId + 1, ifcName: partition, ccdMask: 3, clientFactory:factory) {

        "${greb}.DAC"  (DacControl)

        for (int j = 0; j < 4; j++) {
            "${greb}.ASPIC$j" (AspicControl, hwChan: j)
        }

        for (int j = 0; j < 2; j++) {
            "${greb}.Bias$j" (BiasControl, hwChan: j)
        }
    }

    Page1 (Page, id: 1, label: "$wreb")
    Page2 (Page, id: 2, label: "$greb")

    String title = "Temperatures\\"
    for (int j = 1; j <= 6; j++) {
        "${wreb}.Temp$j" (Channel, description: "${title}Board temperature $j", units: "\u00b0C",
                          devcName: "$wreb", hwChan: j - 1, type: "TEMP", pageId: 1)
        title = ""
    }

    "${wreb}.Atemp0U" (Channel, description: "ASPIC 0 upper temp", units: "\u00b0C",
                       devcName: "$wreb", hwChan: 0, type: "ATEMP", pageId: 1)

    "${wreb}.Atemp0L" (Channel, description: "ASPIC 0 lower temp", units: "\u00b0C",
                       devcName: "$wreb", hwChan: 1, type: "ATEMP", pageId: 1)

    "${wreb}.CCDtemp0" (Channel, description: "CCD 0 temperature", units: "\u00b0C",
                        devcName: "$wreb", hwChan: 0, type: "RTD", pageId: 1)

    "${wreb}.RTDtemp" (Channel, description: "RTD temperature", units: "\u00b0C",
                       devcName: "$wreb", hwChan: 3, type: "RTD", pageId: 1)

    "${wreb}.DigV"   (Channel, description: "Board power\\Digital PS voltage", units: "Volts",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_DIG_VOLTAGE, type: "POWER", pageId: 1)

    "${wreb}.DigI"   (Channel, description: "Digital PS current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_DIG_CURRENT, type: "POWER", scale: 1000, pageId: 1)

    "${wreb}.AnaV"   (Channel, description: "Analog PS voltage", units: "Volts",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_ANA_VOLTAGE, type: "POWER", pageId: 1)

    "${wreb}.AnaI"   (Channel, description: "Analog PS current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_ANA_CURRENT, type: "POWER", scale: 1000, pageId: 1)

    "${wreb}.ClkHV"  (Channel, description: "CLK_H PS voltage", units: "Volts",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_CLKH_VOLTAGE, type: "POWER", pageId: 1)

    "${wreb}.ClkHI"  (Channel, description: "CLK_H PS current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_CLKH_CURRENT, type: "POWER", scale: 1000, pageId: 1)

    "${wreb}.ODV"    (Channel, description: "OD PS voltage", units: "Volts",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_OD_VOLTAGE, type: "POWER", pageId: 1)

    "${wreb}.ODI"    (Channel, description: "OD PS current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_OD_CURRENT, type: "POWER", scale: 1000, pageId: 1)

    "${wreb}.HtrV"   (Channel, description: "Heater PS voltage", units: "Volts",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_HTR_VOLTAGE, type: "POWER", pageId: 1)

    "${wreb}.HtrI"   (Channel, description: "Heater PS current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: PowerAdcs.ADC_HTR_CURRENT, type: "POWER", scale: 1000, pageId: 1)

    "${wreb}.Power"  (Channel, description: "Total power", format: ".2f", units: "Watts",
                      devcName: "$wreb", hwChan: REBDevice.CHAN_TOTAL_POWER, type: "POWER", pageId: 1)

    "${wreb}.PClkSh" (Channel, description: "Clock rails\\Parallel shifted", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_CKP_SH, type: "CRVOLT", pageId: 1)

    "${wreb}.SClkU"  (Channel, description: "Serial upper", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_SCK_U, type: "CRVOLT", pageId: 1)

    "${wreb}.SClkL"  (Channel, description: "Serial lower", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_SCK_L, type: "CRVOLT", pageId: 1)

    "${wreb}.RGU"    (Channel, description: "RG upper", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_RG_U, type: "CRVOLT", pageId: 1)

    "${wreb}.RGL"    (Channel, description: "RG lower", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_RG_L, type: "CRVOLT", pageId: 1)

    "${wreb}.PClk0"  (Channel, description: "Clock states\\Parallel 0", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_CKP_0, type: "CRVOLT", pageId: 1)

    "${wreb}.SClk0"  (Channel, description: "Serial 0", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_CKS_0, type: "CRVOLT", pageId: 1)

    "${wreb}.RG0"    (Channel, description: "RG 0", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_RG_0, type: "CRVOLT", pageId: 1)

    "${wreb}.OD0V"   (Channel, description: "Bias voltages\\OD 0 voltage", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_OD_0, type: "CRVOLT", pageId: 1)

    "${wreb}.OG0V"   (Channel, description: "OG 0 voltage", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_OG_0, type: "CRVOLT", pageId: 1)

    "${wreb}.RD0V"   (Channel, description: "RD 0 voltage", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_RD_0, type: "CRVOLT", pageId: 1)

    "${wreb}.GD0V"   (Channel, description: "GD 0 voltage", format: ".2f", units: "Volts",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_GD_0, type: "CRVOLT", pageId: 1)

    "${wreb}.OD0I"   (Channel, description: "OD 0 current", format: ".1f", units: "mA",
                      devcName: "$wreb", hwChan: SlowAdcs.CHAN_ODI_0, type: "CRVOLT", scale: 1000, pageId: 1)

    title = "Temperatures\\"
    for (int j = 1; j <= 10; j++) {
        "${greb}.Temp$j" (Channel, description: "${title}Board temperature $j", units: "\u00b0C",
                          devcName: "$greb", hwChan: j - 1, type: "TEMP", pageId: 2)
        title = ""
    }

    "${greb}.Atemp0U" (Channel, description: "ASPIC 0 upper temp", units: "\u00b0C",
                       devcName: "$greb", hwChan: 0, type: "ATEMP", pageId: 2)

    "${greb}.Atemp0L" (Channel, description: "ASPIC 0 lower temp", units: "\u00b0C",
                       devcName: "$greb", hwChan: 1, type: "ATEMP", pageId: 2)

    "${greb}.Atemp1U" (Channel, description: "ASPIC 1 upper temp", units: "\u00b0C",
                       devcName: "$greb", hwChan: 2, type: "ATEMP", pageId: 2)

    "${greb}.Atemp1L" (Channel, description: "ASPIC 1 lower temp", units: "\u00b0C",
                       devcName: "$greb", hwChan: 3, type: "ATEMP", pageId: 2)

    "${greb}.CCDtemp0" (Channel, description: "CCD 0 temperature", units: "\u00b0C",
                        devcName: "$greb", hwChan: 0, type: "RTD", pageId: 2)

    "${greb}.CCDtemp1" (Channel, description: "CCD 1 temperature", units: "\u00b0C",
                        devcName: "$greb", hwChan: 1, type: "RTD", pageId: 2)

    "${greb}.RTDtemp" (Channel, description: "RTD temperature", units: "\u00b0C",
                       devcName: "$greb", hwChan: 3, type: "RTD", pageId: 2)

    "${greb}.DigV"    (Channel, description: "Board power\\Digital PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_DIG_VOLTAGE, type: "POWER", pageId: 2)

    "${greb}.DigI"    (Channel, description: "Digital PS current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_DIG_CURRENT, type: "POWER", scale: 1000, pageId: 2)

    "${greb}.AnaV"    (Channel, description: "Analog PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_ANA_VOLTAGE, type: "POWER", pageId: 2)

    "${greb}.AnaI"    (Channel, description: "Analog PS current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_ANA_CURRENT, type: "POWER", scale: 1000, pageId: 2)

    "${greb}.ClkHV"   (Channel, description: "CLK_H PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_CLKH_VOLTAGE, type: "POWER", pageId: 2)

    "${greb}.ClkHI"   (Channel, description: "CLK_H PS current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_CLKH_CURRENT, type: "POWER", scale: 1000, pageId: 2)

    "${greb}.ClkLV"   (Channel, description: "CLK_L PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_V_CLKL, type: "CRVOLT", pageId: 2)

    "${greb}.ODV"     (Channel, description: "OD PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_OD_VOLTAGE, type: "POWER", pageId: 2)

    "${greb}.ODI"     (Channel, description: "OD PS current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_OD_CURRENT, type: "POWER", scale: 1000, pageId: 2)

    "${greb}.HtrV"    (Channel, description: "Heater PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_HTR_VOLTAGE, type: "POWER", pageId: 2)

    "${greb}.HtrI"    (Channel, description: "Heater PS current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: PowerAdcs.ADC_HTR_CURRENT, type: "POWER", scale: 1000, pageId: 2)

    "${greb}.DphiV"   (Channel, description: "DPHI PS voltage", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_V_DPHI, type: "CRVOLT", pageId: 2)

    "${greb}.Power"   (Channel, description: "Total power", format: ".2f", units: "Watts",
                       devcName: "$greb", hwChan: REBDevice.CHAN_TOTAL_POWER, type: "POWER", pageId: 2)

    "${greb}.PClkSh"  (Channel, description: "Clock rails\\Parallel shifted", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_CKP_SH, type: "CRVOLT", pageId: 2)

    "${greb}.SClkU"   (Channel, description: "Serial upper", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_SCK_U, type: "CRVOLT", pageId: 2)

    "${greb}.SClkL"   (Channel, description: "Serial lower", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_SCK_L, type: "CRVOLT", pageId: 2)

    "${greb}.RGU"     (Channel, description: "RG upper", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RG_U, type: "CRVOLT", pageId: 2)

    "${greb}.RGL"     (Channel, description: "RG lower", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RG_L, type: "CRVOLT", pageId: 2)

    "${greb}.PClk0"   (Channel, description: "Clock states\\Parallel 0", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_CKP_0, type: "CRVOLT", pageId: 2)

    "${greb}.SClk0"   (Channel, description: "Serial 0", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_CKS_0, type: "CRVOLT", pageId: 2)

    "${greb}.RG0"     (Channel, description: "RG 0", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RG_0, type: "CRVOLT", pageId: 2)

    "${greb}.PClk1"   (Channel, description: "Parallel 1", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_CKP_1, type: "CRVOLT", pageId: 2)

    "${greb}.SClk1"   (Channel, description: "Serial 1", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_CKS_1, type: "CRVOLT", pageId: 2)

    "${greb}.RG1"     (Channel, description: "RG 1", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RG_1, type: "CRVOLT", pageId: 2)

    "${greb}.OD0V"    (Channel, description: "Bias voltages\\OD 0 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_OD_0, type: "CRVOLT", pageId: 2)

    "${greb}.OG0V"    (Channel, description: "OG 0 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_OG_0, type: "CRVOLT", pageId: 2)

    "${greb}.RD0V"    (Channel, description: "RD 0 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RD_0, type: "CRVOLT", pageId: 2)

    "${greb}.GD0V"    (Channel, description: "GD 0 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_GD_0, type: "CRVOLT", pageId: 2)

    "${greb}.OD0I"    (Channel, description: "OD 0 current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_ODI_0, type: "CRVOLT", scale: 1000, pageId: 2)

    "${greb}.OD1V"    (Channel, description: "OD 1 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_OD_1, type: "CRVOLT", pageId: 2)

    "${greb}.OG1V"    (Channel, description: "OG 1 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_OG_1, type: "CRVOLT", pageId: 2)

    "${greb}.RD1V"    (Channel, description: "RD 1 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_RD_1, type: "CRVOLT", pageId: 2)

    "${greb}.GD1V"    (Channel, description: "GD 1 voltage", format: ".2f", units: "Volts",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_GD_1, type: "CRVOLT", pageId: 2)

    "${greb}.OD1I"    (Channel, description: "OD 1 current", format: ".1f", units: "mA",
                       devcName: "$greb", hwChan: SlowAdcs.CHAN_ODI_1, type: "CRVOLT", scale: 1000, pageId: 2)

}

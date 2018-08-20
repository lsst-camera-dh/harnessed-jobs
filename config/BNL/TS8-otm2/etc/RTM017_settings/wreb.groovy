import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.subsystem.rafts.RaftsMain
import org.lsst.ccs.subsystem.rafts.REBDevice
import org.lsst.ccs.subsystem.rafts.DacControl
import org.lsst.ccs.subsystem.rafts.BiasControl
import org.lsst.ccs.subsystem.rafts.AspicControl
import org.lsst.ccs.drivers.reb.SlowAdcs
import org.lsst.ccs.monitor.Channel

taskConfig = ["monitor-update/taskPeriodMillis":1000,"monitor-publish/taskPeriodMillis":10000]

CCSBuilder builder = ["ccs-wreb"]

builder.main (RaftsMain, nodeTags:taskConfig) {

    def reb = "WREB"

    "$reb" (REBDevice, hdwType: "pci1", id: 0, ifcName: "pgpcard_0", ccdMask: 3) {

        "${reb}.DAC"  (DacControl)
        //"${reb}.DAC"  (DacControl, raw: true, version: 1)

        for (int j = 0; j < 2; j++) {
            "${reb}.ASPIC$j" (AspicControl, hwChan: j)
        }

        for (int j = 0; j < 1; j++) {
            "${reb}.Bias$j" (BiasControl, hwChan: j)
            //"${reb}.Bias$j" (BiasControl, hwChan: j, raw: true)
        }
    }

    String title = "${reb} temperatures\\"
    for (int j = 1; j <= 10; j++) {
        "${reb}.Temp$j" (Channel, description: "${title}Board temperature $j", units: "\u00b0C",
                         devcName: "${reb}", hwChan: j - 1, type: "TEMP")
        title = ""
    }

    "${reb}.Atemp0U" (Channel, description: "ASPIC 0 upper temp", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 0, type: "ATEMP")

    "${reb}.Atemp0L" (Channel, description: "ASPIC 0 lower temp", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 1, type: "ATEMP")

    "${reb}.Atemp1U" (Channel, description: "ASPIC 1 upper temp", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 2, type: "ATEMP")

    "${reb}.Atemp1L" (Channel, description: "ASPIC 1 lower temp", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 3, type: "ATEMP")

    "${reb}.CCDtemp0" (Channel, description: "CCD 0 temperature", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 0, type: "RTD")

    "${reb}.CCDtemp1" (Channel, description: "CCD 1 temperature", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 1, type: "RTD")

    "${reb}.RTDtemp" (Channel, description: "RTD temperature", units: "\u00b0C",
                      devcName: "${reb}", hwChan: 3, type: "RTD")

    "${reb}.DigPS_V" (Channel, description: "${reb} board power\\Digital PS voltage", units: "Volts",
                     devcName: "${reb}", hwChan: 0, type: "POWER")

    "${reb}.DigPS_I" (Channel, description: "Digital PS current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: 1, type: "POWER", scale: 1000)

    "${reb}.AnaPS_V" (Channel, description: "Analog PS voltage", units: "Volts",
                     devcName: "${reb}", hwChan: 2, type: "POWER")

    "${reb}.AnaPS_I" (Channel, description: "Analog PS current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: 3, type: "POWER", scale: 1000)

    "${reb}.ClkHPS_V" (Channel, description: "CLK_H PS voltage", units: "Volts",
                     devcName: "${reb}", hwChan: 4, type: "POWER")

    "${reb}.ClkHPS_I" (Channel, description: "CLK_H PS current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: 5, type: "POWER", scale: 1000)

    "${reb}.ODPS_V" (Channel, description: "OD PS voltage", units: "Volts",
                     devcName: "${reb}", hwChan: 6, type: "POWER")

    "${reb}.ODPS_I" (Channel, description: "OD PS current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: 7, type: "POWER", scale: 1000)

    "${reb}.HtrPS_V" (Channel, description: "Heater PS voltage", units: "Volts",
                     devcName: "${reb}", hwChan: 8, type: "POWER")

    "${reb}.HtrPS_I" (Channel, description: "Heater PS current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: 9, type: "POWER", scale: 1000)

    "${reb}.Power"   (Channel, description: "Total power", format: ".2f", units: "Watts",
                      devcName: "$reb", hwChan: REBDevice.CHAN_TOTAL_POWER, type: "POWER", pageId: i)

    "${reb}.CKPSH_V" (Channel, description: "${reb} clock rails\\CKP_SH voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_CKP_SH, type: "CRVOLT")

    "${reb}.CKS_V"  (Channel, description: "CKS voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_CKS, type: "CRVOLT")

    "${reb}.SCKU_V" (Channel, description: "SCK_U voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_SCK_U, type: "CRVOLT")

    "${reb}.SCKL_V" (Channel, description: "SCK_L voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_SCK_L, type: "CRVOLT")

    "${reb}.RG_V"   (Channel, description: "RG voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_RG, type: "CRVOLT")

    "${reb}.RGU_V"  (Channel, description: "RG_U voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_RG_U, type: "CRVOLT")

    "${reb}.RGL_V"  (Channel, description: "RG_L voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_RG_L, type: "CRVOLT")

    "${reb}.CKP0V"  (Channel, description: "CKP 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_CKP_0, type: "CRVOLT")

    "${reb}.CKS0V"  (Channel, description: "CKS 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_CKS_0, type: "CRVOLT")

    "${reb}.RG0V"   (Channel, description: "RG 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_RG_0, type: "CRVOLT")

    "${reb}.OD0V"   (Channel, description: "${reb} bias voltages\\OD 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_OD_0, type: "CRVOLT")

    "${reb}.OG0V"   (Channel, description: "OG 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_OG_0, type: "CRVOLT")

    "${reb}.RD0V"   (Channel, description: "RD 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_RD_0, type: "CRVOLT")

    "${reb}.GD0V"   (Channel, description: "GD 0 voltage", format: ".2f", units: "Volts",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_GD_0, type: "CRVOLT")

    "${reb}.OD0I"   (Channel, description: "OD 0 current", format: ".1f", units: "mA",
                     devcName: "${reb}", hwChan: SlowAdcs.CHAN_ODI_0, type: "CRVOLT", scale: 1000)

}

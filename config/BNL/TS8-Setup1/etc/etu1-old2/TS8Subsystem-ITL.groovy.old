
import static org.lsst.gruth.jutils.MapArgs.*;
import org.lsst.ccs.drivers.reb.sim.ClientFactorySimulation
import org.lsst.ccs.subsystem.rafts.RaftsMain;
import org.lsst.ccs.subsystem.rafts.REBDevice;
import org.lsst.ccs.subsystem.rafts.DacControl;
import org.lsst.ccs.subsystem.rafts.AspicControl;
import org.lsst.ccs.subsystem.rafts.CabacControl;
import org.lsst.ccs.subsystem.rafts.BiasControl;
import org.lsst.ccs.subsystem.monitor.Channel;
import org.lsst.ccs.utilities.ccd.*;
import org.lsst.ccs.utilities.image.*;
import org.lsst.ccs.subsystem.ts8.TS8Subsystem;
import org.lsst.ccs.subsystem.ts8.sim.*;
import org.lsst.ccs.subsystem.ts8.sim.TS8ClientFactorySimulation
import org.lsst.ccs.description.groovy.CCSBuilder
import org.lsst.ccs.drivers.reb.ClientFactory
import org.lsst.ccs.drivers.reb.SlowAdcs

//def raftBuilder = Class.forName("org.lsst.ccs.utilities.ccd.Raft");
//raftGeometry = raftBuilder.createRaft("R00",CCDType.E2V);
raftGeometry = new Raft("R00",CCDType.ITL);
reb0 = Reb.createReb("Reb0", 0, CCDType.ITL);
raftGeometry.addChildGeometry(reb0, 0, 0);
reb1 = Reb.createReb("Reb1", 1, CCDType.ITL);
raftGeometry.addChildGeometry(reb1, 1, 0);
reb2 = Reb.createReb("Reb2", 2, CCDType.ITL);
raftGeometry.addChildGeometry(reb2, 2, 0);

def runMode = System.getProperty("org.lsst.ccs.run.mode","normal");
System.out.println("Building TS8 subsystem in run mode: "+runMode);

ClientFactory mainClientFactory = runMode.equals("simulation") ? new ClientFactorySimulation() : new ClientFactory();


CCSBuilder builder = ["ts8"]

builder.
    "main" (TS8Subsystem, argMap("main", 1000, raftGeometry, mainClientFactory)) {
    
        for (Reb rebGeometry : raftGeometry.getChildrenList() ) {
            def rebCount = rebGeometry.getParallelPosition();
            def reb = rebGeometry.getUniqueId();
            def dreb = "D$reb"
                    

            clientFactory = runMode.equals("simulation") ? new TS8ClientFactorySimulation(rebGeometry) : null;

            "$reb" (REBDevice, argMap("DAQ1", rebCount, "", 7, clientFactory)) {

                "${reb}.DAC"  (DacControl, argMap("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

                for (int j = 0; j < 6; j++) {
                    def apc = "ASPIC$j"

                    "${reb}.${apc}" (AspicControl, argMap("", j, 0, 0, 0, 0, 0))
                }

                for (int j = 0; j < 3; j++) {
                    def bias = "Bias$j"

                    "${reb}.${bias}" (BiasControl, argMap("", j, 0, 0, 0, 0, 0, 0))
                }
            }

            "${dreb}.Temp1" (Channel,
                             argMap("${dreb} temperature 1", "\u00b0C",
                                    "${reb}", 0, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${dreb}.Temp2" (Channel,
                             argMap("${dreb} temperature 2", "\u00b0C",
                                    "${reb}", 1, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp1"  (Channel,
                             argMap("${reb} temperature 1", "\u00b0C",
                                    "${reb}", 2, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp2"  (Channel,
                             argMap("${reb} temperature 2", "\u00b0C",
                                    "${reb}", 3, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp3"  (Channel,
                             argMap("${reb} temperature 3", "\u00b0C",
                                    "${reb}", 4, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp4"  (Channel,
                             argMap("${reb} temperature 4", "\u00b0C",
                                    "${reb}", 5, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp5"  (Channel,
                             argMap("${reb} temperature 5", "\u00b0C",
                                    "${reb}", 6, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp6"  (Channel,
                             argMap("${reb} temperature 6", "\u00b0C",
                                    "${reb}", 7, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp7"  (Channel,
                             argMap("${reb} temperature 7", "\u00b0C",
                                    "${reb}", 8, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Temp8"  (Channel,
                             argMap("${reb} temperature 8", "\u00b0C",
                                    "${reb}", 9, "TEMP", "", 0, 1,
                                    "FLAG", 0, 0, null,
                                    "FLAG", 0, 0, null))

            "${reb}.Atemp0U" (Channel,
                              argMap("${reb} ASPIC 0 upper temp", "\u00b0C",
                                     "${reb}", 0, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Atemp0L" (Channel,
                              argMap("${reb} ASPIC 0 lower temp", "\u00b0C",
                                     "${reb}", 1, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Atemp1U" (Channel,
                              argMap("${reb} ASPIC 1 upper temp", "\u00b0C",
                                     "${reb}", 2, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Atemp1L" (Channel,
                              argMap("${reb} ASPIC 1 lower temp", "\u00b0C",
                                     "${reb}", 3, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Atemp2U" (Channel,
                              argMap("${reb} ASPIC 2 upper temp", "\u00b0C",
                                     "${reb}", 4, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Atemp2L" (Channel,
                              argMap("${reb} ASPIC 2 lower temp", "\u00b0C",
                                     "${reb}", 5, "ATEMP", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.DigV"    (Channel,
                              argMap("${reb} Digital PS voltage", "Volts",
                                     "${reb}", 0, "POWER", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.DigI"    (Channel,
                              argMap("${reb} Digital PS current", ".1f", "mA",
                                     "${reb}", 1, "POWER", "", 0, 1000,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.AnaV"    (Channel,
                              argMap("${reb} Analog PS voltage", "Volts",
                                     "${reb}", 2, "POWER", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))
            "${reb}.ClkV"    (Channel,
                              argMap("${reb} Clock PS voltage", "Volts",
                                     "${reb}", 4, "POWER", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.ClkI"    (Channel,
                              argMap("${reb} Clock PS current", ".1f", "mA",
                                     "${reb}", 5, "POWER", "", 0, 1000,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.ODV"     (Channel,
                              argMap("${reb} OD PS voltage", "Volts",
                                     "${reb}", 6, "POWER", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.ODI"     (Channel,
                              argMap("${reb} OD PS current", ".1f", "mA",
                                     "${reb}", 7, "POWER", "", 0, 1000,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OD0V"    (Channel,
                              argMap("${reb} OD 0 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OD_0, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OG0V"    (Channel,
                              argMap("${reb} OG 0 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OG_0, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.RD0V"    (Channel,
                              argMap("${reb} RD 0 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_RD_0, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.GD0V"    (Channel,
                              argMap("${reb} GD 0 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_GD_0, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OD1V"    (Channel,
                              argMap("${reb} OD 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OD_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OG1V"    (Channel,
                              argMap("${reb} OG 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OG_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.RD1V"    (Channel,
                              argMap("${reb} RD 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_RD_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.GD1V"    (Channel,
                              argMap("${reb} GD 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_GD_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OD2V"    (Channel,
                              argMap("${reb} OD 2 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OD_2, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.OG2V"    (Channel,
                              argMap("${reb} OG 2 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_OG_2, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.RD2V"    (Channel,
                              argMap("${reb} RD 2 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_RD_2, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.GD2V"    (Channel,
                              argMap("${reb} GD 2 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_GD_2, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Ref05V"  (Channel,
                              argMap("${reb} 5V ref 0 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_VREF5_0, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Ref15V"  (Channel,
                              argMap("${reb} 5V ref 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_VREF5_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))
             "${reb}.Ref25V"  (Channel,
                              argMap("${reb} 5V ref 2 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_VREF5_2, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            "${reb}.Ref125V" (Channel,
                              argMap("${reb} 2.5V ref 1 voltage", "Volts",
                                     "${reb}", SlowAdcs.CHAN_VREF25_1, "BIAS", "", 0, 1,
                                     "FLAG", aDbl("limitLo", 0), 0, null,
                                     "FLAG", aDbl("limitHi", 0), 0, null))

            for (int js = 0; js < 3; js++) {

                for (int jd = 0; jd < 2; jd++) {
                    String tb = jd == 0 ? "upper" : "lower"

                    for (int jc = 0; jc < 8; jc++) {
                        int ch = jc + 8 * jd + 16 * js
                        
                        "${reb}.CCDI${js}${jd}${jc}" \
                             (Channel, argMap("${reb} CCD ${js} ${tb} current ${jc}",
                                              ".3f", "mA",
                                              "${reb}", ch, "CURR", "", 0, 1000,
                                              "FLAG", aDbl("limitLo", 0), 0, null,
                                              "FLAG", aDbl("limitHi", 0), 0, null))
                    }
                }
            }

        }
         
     }
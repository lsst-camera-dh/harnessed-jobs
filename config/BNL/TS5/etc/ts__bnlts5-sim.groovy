import static org.lsst.gruth.jutils.MapArgs.*;
import org.lsst.ccs.description.groovy.CCSBuilder;
import org.lsst.ccs.subsystem.teststand.TSSubSys;
import org.lsst.ccs.subsystem.teststand.TSConfigurable;
import org.lsst.ccs.subsystem.teststand.TSSetDevTypes;
import org.lsst.ccs.subsystem.teststand.KeithleyDevice;
import org.lsst.ccs.subsystem.teststand.CryoCon24cDevice;
import org.lsst.ccs.subsystem.teststand.CryoCon24cSimDevice;
import org.lsst.ccs.subsystem.teststand.MicroIonDevice;
import org.lsst.ccs.subsystem.teststand.NewportLampDevice;
import org.lsst.ccs.subsystem.teststand.OrielShutterDevice;
import org.lsst.ccs.subsystem.teststand.Cornerstone260Device;
import org.lsst.ccs.subsystem.teststand.NetBotzDevice;
import org.lsst.ccs.subsystem.teststand.XEDDevice;
import org.lsst.ccs.subsystem.teststand.AP7900Device;
import org.lsst.ccs.subsystem.teststand.data.TSConfig;

import org.lsst.ccs.subsystem.monitor.Alarm;
import org.lsst.ccs.subsystem.monitor.Line;
import org.lsst.ccs.subsystem.monitor.Channel;


CCSBuilder builder = ["ts"]

builder.
    main (TSSubSys, argMap("main", 10000, "bnlts3setup2")) {
/*
    Bias  (KeithleyDevice, argMap(
            "AH032N9T",
            57600))

    PhotoDiode  (KeithleyDevice, argMap(
            "AH032N9V",
            57600))
*/
    Cryo   (CryoCon24cSimDevice, argMap(1,"AH032N9U",19200))
/*
  
    VacuumGauge (MicroIonDevice, argMap(1, "ZM", 19200, 1))
*/    
    Enviro (NetBotzDevice,argMap("/home/homer/bnlenviro.dat"))
/*
    Lamp (NewportLampDevice, argMap(1, "HY", 9600))
    
    Shutter (OrielShutterDevice, argMap("?", 9600, 0))
    
    PDU (AP7900Device, argMap("130.199.47.172", 23))

    Monochromator (Cornerstone260Device, argMap("AH032N9X", 9600))
    
    Fe55 (XEDDevice, argMap("HX",4800))
*/
    "TSCFG" (TSSetDevTypes, argMap(
            'empty','275CutOn','550CutOn',' ',' ',' ',
            0.0,    275.0,    560.0,    0.0,    0.0,    0.0,
            'KEITHLEY-INSTRUMENTS-INC.,MODEL-6487',
            'KEITHLEY-INSTRUMENTS-INC.,MODEL-6487',
            'Newport-Xenon-Arc-Lamp',
            'Cornerstone260'))
        
    "IDLE"(TSConfigurable, argMap('IDLE', 500.0, 0.0, 200.0, 0.0, 1000.0, -125.0) )
 
    "READY"(TSConfigurable, argMap('READY', 500.0, 198.0, 2.0, 0.0, 1.0e-3, -125.0) )
 
    "TEST"(TSConfigurable, argMap('TEST', 500.0, 0.0, 2.0, -25.0, 1.0e-5, -125.0) )
 
    "ACQ1"(TSConfigurable, argMap('ACQ1', 500.0, 198.0, 2.0, -25.0, 1.0e-5, -125.0) )
 
    "WARM"(TSConfigurable, argMap('WARM', 500.0, 0.0, 10.0, -25.0, 1000.0, 20.0) )
 
            

        
    
    //    AlarmHDW  (TSSubSys, argMap("OV", 0))
    AlarmHDW  (Alarm, argMap(null, TSConfig.EVENT_ID.BIAS.ordinal()))

    AlarmHDWC  (Alarm, argMap(null, TSConfig.EVENT_ID.CRYO.ordinal()))

    AlarmHDWV  (Alarm, argMap(null, TSConfig.EVENT_ID.VAC.ordinal()))

    AlarmHDWPD (Alarm, argMap(null, TSConfig.EVENT_ID.PD.ordinal()))

    AlarmHDWLMP (Alarm, argMap(null, TSConfig.EVENT_ID.LMP.ordinal()))


    /*
    CmpCCDBias  (MonChannel,
    argMap("CCD Bias Voltage", "V",
    "alarm", 0.0, 0.0,
    "alarm", 0.0, 0.0,
    "Bias", 0, "VOLT", "B", 0, 0.0, 1.0))
     */      
    /*
    Its name, used to identify it in databases, plots, etc.
    Its longer, more descriptive, name.
    The units the value is expressed in, e.g. "Volts".
    The device used for obtaining its value.
    The hardware channel number on the device.
    The channel type, e.g. temperature, pressure, etc, which is needed by some devices.
    The subtype, which supplies hardware configuration information.
    The offset and scale values needed for converting a raw hardware value to a physical one.
    Parameters used for checking the value against a limit.  There is one set for the low limit and one for the high one:
    The checking option: NONE, FLAG or ALARM
    The limit value.
    The alarm to be activated upon status transitions when ALARM is specified.
    The deadband value which delays a potential alarm action during a transition back to good status.
    Its id, which is its index in the list of all channels.

    The limit values are maintained by the configuration system and can be changed while running.  Any such change causes a status message to be broadcast, which can be used to update the trending database or to update any console displays.
     */
       ccdtemperature  (Channel,
                    argMap("Cryogenics temperature", "C",
                           "Cryo", 0, "TEMP", "T", 0.0, 1.0,
                           "flag", -110.0, 0.0, null,
                           "alarm", 28.0, 0.0, "AlarmHDWC"))

        ccdtempstddev  (Channel,
                    argMap("Cryogenics temperature Std Dev", "C",
                           "Cryo", 2, "TEMP", "T", 0.0, 1.0,
                           "flag", -2.0, 0.0, null,
                           "flag", 2.0, 0.0, null))

        ccdtempsetpoint  (Channel,
                    argMap("CCD temp setpoint", "C",
                           "Cryo", -1, "TEMP", "T", 0.0, 1.0,
                           "flag", -110.0, 0.0, null,
                           "flag", 28.0, 0.0, null))

        dewarpressure  (Channel,
                    argMap("Dewar Vacuum Reading", "T",
                           "VacuumGauge", 0, "PRESSURE", "T", 0.0, 1.0,
                           "flag",  0.0, 0.0, null,
                           "alarm", 1000.0, 0.0, "AlarmHDWV"))

        cleanroomhumidity  (Channel,
                    argMap("Humidity", "P",
                           "Enviro", 0, "UNKNOWN", "P", 0.0, 1.0,
                           "flag", 40.0, 0.0, null,
                           "flag", 80.0, 0.0, null))

        roomtemperature  (Channel,
                    argMap("Temperature", "C",
                           "Enviro", 1, "UNKNOWN", "C", 0.0, 1.0,
                           "flag", 65.0, 0.0, null,
                           "flag", 75.0, 0.0, null))

        dewpoint  (Channel,
                    argMap("Dew Point", "D",
                           "Enviro", 2, "UNKNOWN", "C", 0.0, 1.0,
                           "flag", 0.0, 0.0, null,
                           "flag", 1.0, 0.0, null))

        partcounter  (Channel,
                    argMap("Particle Count", "1",
                           "Enviro", 3, "UNKNOWN", "1", 0.0, 1.0,
                           "flag", 0.0, 0.0, null,
                           "flag", 10.0, 0.0, null))
}

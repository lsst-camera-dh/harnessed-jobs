import org.lsst.ccs.description.groovy.CCSBuilder;
import org.lsst.ccs.subsystem.teststand.data.TSConfig;
//import org.lsst.ccs.subsystem.teststand.TS8Bench;
import org.lsst.ccs.subsystem.teststand.TSSubSys;
import org.lsst.ccs.subsystem.teststand.KeithleyDevice;
import org.lsst.ccs.subsystem.teststand.KeithleySimDevice;
import org.lsst.ccs.subsystem.teststand.Cornerstone260Device;
import org.lsst.ccs.subsystem.teststand.NewportLampDevice;
import org.lsst.ccs.bootstrap.BootstrapResourceUtils;
import org.lsst.ccs.subsystem.teststand.TSConfigurable;
import org.lsst.ccs.subsystem.teststand.TSSetDevTypes;
import org.lsst.ccs.subsystem.teststand.CryoCon24cDevice;
import org.lsst.ccs.subsystem.teststand.GPVacMon835Device;
import org.lsst.ccs.subsystem.teststand.NetBotzDevice;
import org.lsst.ccs.subsystem.teststand.TrippLitePDUDevice;
import org.lsst.ccs.subsystem.teststand.XEDDevice;

import org.lsst.ccs.monitor.Alarm;
import org.lsst.ccs.monitor.Line;
import org.lsst.ccs.monitor.Channel;

CCSBuilder builder = ["ts"]

Properties props = BootstrapResourceUtils.getBootstrapSystemProperties()
def runMode = props.getProperty("org.lsst.ccs.run.mode","normal");

//Class keithleyClass = Class.forName("org.lsst.ccs.subsystem.teststand.Keithley" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
//Class monochromatorClass = Class.forName("org.lsst.ccs.subsystem.teststand.Cornerstone260" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
//Class lamClass = Class.forName("org.lsst.ccs.subsystem.teststand.NewportLamp" + (runMode.equals("simulation") ? "Sim" : "") + "Device");


taskConfig = ["monitor-update/taskPeriodMillis":60000,"monitor-publish/taskPeriodMillis":60000]

builder.
    main (TSSubSys, nodeTags:taskConfig) {

//    main (TSSubSys, configName:"bnlts8", broadcastMillis:10000) {

    Bias  (KeithleyDevice, devName:"PH", baudRate:57600, connType:"serial")

    PhotoDiode  (KeithleyDevice, devName:"PJ", baudRate:57600, connType:"serial")

//    PhotoDiode  (KeithleySimDevice, host:"PJ", port:57600)
//    Cryo   (CryoCon24cDevice, itype:1, host:"A103LM1Q", port:19200)
    Cryo   (CryoCon24cDevice, host:"A103LM1Q", port:19200, 
    	   maxSetPoints:[35, 35, 35, 35] as double[],
	   channelUnits:["A":"C", "B":"C", "C":"C", "D":"C"],
	   channelTypes:["A":"PTC100", "B":"PTC100", "C":"PTC100", "D":"PTC100"]
	   )
  
//    VacuumGauge (MicroIonDevice, itype:1, host:"DB93", port:19200, addr:1)
    
//    VQMonitor (GPVacMon835Device, serialdev:"/dev/ttyACM0", baud:9600)
    VQMonitor (GPVacMon835Device, serialdev:"/dev/ttyACM0")
    
    Enviro (NetBotzDevice, ef:"/home/homer/bnlenviro.dat")

    Lamp (NewportLampDevice, host:"PF", port:9600)
    
    PDU (TrippLitePDUDevice, host:"130.199.47.45", port:23)

    Monochromator (Cornerstone260Device, host:"PG", baud:9600)
    
    Fe55 (XEDDevice, host:"A603EP00", port:4800)

    "TSCFG" (TSSetDevTypes, filter1:'empty',filter2:'275CutOn',filter3:'550CutOn',filter4:' ',filter5:' ',filter6:' ',
            filteredge1:0.0, filteredge2:275.0, filteredge3:560.0, filteredge4:0.0, filteredge5:0.0, filteredge6:0.0,
            pdtype:'KEITHLEY-INSTRUMENTS-INC.,MODEL-6487',
            biastype:'KEITHLEY-INSTRUMENTS-INC.,MODEL-6487',
            srctype:'Newport-Xenon-Arc-Lamp',
            monotype:'Cornerstone260')

    "IDLE"(TSConfigurable, name:'IDLE', lambda:500.0, minlmppwr:0.0,
        cryotol:200.0, bias:0.0, vac:1000.0, cryo:-125.0)
     
    "READY"(TSConfigurable, name:'READY', lambda:500.0, minlmppwr:198.0, 
        cryotol:2.0, bias:0.0, vac:1.0e-3, cryo:-125.0)
 
    "TEST"(TSConfigurable, name:'TEST', lambda:500.0, minlmppwr:0.0, 
        cryotol:2.0, bias:-25.0, vac:1.0e-5, cryo:-125.0)
 
    "ACQ1"(TSConfigurable, name:'ACQ1', lambda:500.0, minlmppwr:198.0, 
        cryotol:2.0, bias:-25.0, vac:1.0e-5, cryo:-125.0)
 
    "WARM"(TSConfigurable, name:'WARM', lambda:500.0, minlmppwr:0.0, 
        cryotol:10.0, bias:-25.0, vac:1000.0, cryo:20.0)
    
    //    AlarmHDW  (TSSubSys, argMap("OV", 0))
    AlarmHDW  (Alarm, eventParm:TSConfig.EVENT_ID.BIAS.ordinal())

    AlarmHDWC  (Alarm, eventParm:TSConfig.EVENT_ID.CRYO.ordinal())

    AlarmHDWV  (Alarm, eventParm:TSConfig.EVENT_ID.VAC.ordinal())

    AlarmHDWPD (Alarm, eventParm:TSConfig.EVENT_ID.PD.ordinal())

    AlarmHDWLMP (Alarm, eventParm:TSConfig.EVENT_ID.LMP.ordinal())



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
        temp_a  (Channel,
                    description:"Cryogenics temperature A", units:"C",
                           devcName:"Cryo", hwChan:5, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-110.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:28.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        temp_b  (Channel,
                    description:"Cryogenics temperature B", units:"C",
                           devcName:"Cryo", hwChan:6, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-110.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:28.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        temp_c  (Channel,
                    description:"Cryogenics temperature C", units:"C",
                           devcName:"Cryo", hwChan:7, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-140.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:28.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        temp_d  (Channel,
                    description:"Cryogenics temperature D", units:"C",
                           devcName:"Cryo", hwChan:8, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-140.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:28.0, dbandHi:0.0, alarmHi:null)

        htrread1  (Channel,
                    description:"Cryogenics heater loop 1 % power", units:"C",
                           devcName:"Cryo", hwChan:3, type:"TEMP", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        htrread2  (Channel,
                    description:"Cryogenics heater loop 2 % power", units:"C",
                           devcName:"Cryo", hwChan:4, type:"TEMP", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)


        pid_p1  (Channel,
                    description:"PID_P Loop 1", units:"",
                           devcName:"Cryo", hwChan:9, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        pid_i1  (Channel,
                    description:"PID_P Loop 1", units:"",
                           devcName:"Cryo", hwChan:10, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        pid_d1  (Channel,
                    description:"PID_P Loop 1", units:"",
                           devcName:"Cryo", hwChan:11, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        pid_p2  (Channel,
                    description:"PID_P Loop 2", units:"",
                           devcName:"Cryo", hwChan:12, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        pid_i2  (Channel,
                    description:"PID_P Loop 2", units:"",
                           devcName:"Cryo", hwChan:13, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        pid_d2  (Channel,
                    description:"PID_P Loop 2", units:"",
                           devcName:"Cryo", hwChan:14, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:100.0, dbandHi:0.0, alarmHi:null)

        tempChng  (Channel,
                    description:"temperature change", units:"",
                           devcName:"Cryo", hwChan:15, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-10.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:10.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        SetPnt1  (Channel,
                    description:"setPoint Loop 1", units:"",
                           devcName:"Cryo", hwChan:16, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-135.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:27.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        SetPnt2  (Channel,
                    description:"setPoint Loop 2", units:"",
                           devcName:"Cryo", hwChan:17, type:"TEMP", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-135.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:27.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        vqmpressure  (Channel,
                    description:"VQM Pressure Reading", units:"T",
                           devcName:"VQMonitor", hwChan:0, type:"PRESSURE", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:1000.0, dbandHi:0.0, alarmHi:"AlarmHDWV")

 
        ccdtemperature  (Channel,
                    description:"Cryogenics temperature", units:"C",
                           devcName:"Cryo", hwChan:0, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-110.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:28.0, dbandHi:0.0, alarmHi:"AlarmHDWC")

        ccdtempstddev  (Channel,
                    description:"Cryogenics temperature Std Dev", units:"C",
                           devcName:"Cryo", hwChan:2, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-2.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2.0, dbandHi:0.0, alarmHi:null)

        ccdtempsetpoint  (Channel,
                    description:"CCD temp setpoint", units:"C",
                           devcName:"Cryo", hwChan:-1, type:"TEMP", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-110.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:28.0, dbandHi:0.0, alarmHi:null)
/*
        ccdbiasvoltage  (Channel,
                    description:"CCD bias supply voltage", units:"V",
                           devcName:"Bias", hwChan:0, type:"VOLTS", subtype:"V", offset:0.0, scale:1.0,
                           checkLo:"alarm", limitLo:-74.0, dbandLo:0.0, alarmLo:"AlarmHDW",
                           checkHi:"alarm", limitHi:2.0, dbandHi:0.0, alarmHi:"AlarmHDW")

        ccdbiascurrent  (Channel,
                    description:"CCD bias supply current", units:"I",
                           devcName:"Bias", hwChan:0, type:"CURR", subtype:"I", offset:0.0, scale:1.0,
                           checkLo:"alarm", limitLo:-1.0e6, dbandLo:0.0, alarmLo:"AlarmHDW",
                           checkHi:"alarm", limitHi:1.0e6, dbandHi:0.0, alarmHi:"AlarmHDW")
*/
        photodiodevoltage  (Channel,
                    description:"photodiode supply voltage", units:"V",
                           devcName:"PhotoDiode", hwChan:0, type:"VOLTS", subtype:"V", offset:0.0, scale:1.0,
                           checkLo:"alarm", limitLo:-74.0, dbandLo:0.0, alarmLo:"AlarmHDWPD",
                           checkHi:"alarm",   limitHi:2.0, dbandHi:0.0, alarmHi:"AlarmHDWPD")

        photodiodecurrent  (Channel,
                    description:"photodiode supply current", units:"I",
                           devcName:"PhotoDiode", hwChan:0, type:"CURR", subtype:"I", offset:0.0, scale:1.0,
                           checkLo:"alarm", limitLo:-1.0e6, dbandLo:0.0, alarmLo:"AlarmHDWPD",
                           checkHi:"alarm",  limitHi:1.0e6, dbandHi:0.0, alarmHi:"AlarmHDWPD")
/*
        dewarpressure  (Channel,
                    description:"Dewar Vacuum Reading", units:"T",
                           devcName:"VacuumGauge", hwChan:0, type:"PRESSURE", subtype:"T", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:1000.0, dbandHi:0.0, alarmHi:"AlarmHDWV")
*/

        lamppower  (Channel,
                    description:"Xenon Lamp Power", units:"W",
                           devcName:"Lamp", hwChan:0, type:"Watts", subtype:"W", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"alarm", limitHi:300.0, dbandHi:0.0, alarmHi:"AlarmHDWLMP")

        monochromatordefaultwavelength  (Channel,
                    description:"Wavelength", units:"A",
                           devcName:"Monochromator", hwChan:-1, type:"UNKNOWN", subtype:"A", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        monochromatorwavelength  (Channel,
                    description:"Wavelength", units:"A",
                           devcName:"Monochromator", hwChan:0, type:"UNKNOWN", subtype:"A", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        monochromatorslit1  (Channel,
                    description:"slit 1 width", units:"nm",
                           devcName:"Monochromator", hwChan:3, type:"UNKNOWN", subtype:"nm", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        monochromatorslit2  (Channel,
                    description:"slit 2 width", units:"nm",
                           devcName:"Monochromator", hwChan:4, type:"UNKNOWN", subtype:"nm", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        monochromgrating  (Channel,
                    description:"Grating Position", units:"1",
                           devcName:"Monochromator", hwChan:5, type:"UNKNOWN", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:4.0, dbandHi:0.0, alarmHi:null)

        monochromstep  (Channel,
                    description:"Grating Steps", units:"1",
                           devcName:"Monochromator", hwChan:7, type:"UNKNOWN", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        monochromband  (Channel,
                    description:"bandwidth", units:"1",
                           devcName:"Monochromator", hwChan:6, type:"UNKNOWN", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)

        shutteropen  (Channel,
                    description:"Shutter Open/Closed", units:"S",
                           devcName:"Monochromator", hwChan:1, type:"UNKNOWN", subtype:"S", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:2.0, dbandHi:0.0, alarmHi:null)

        filter1position  (Channel,
                    description:"Filter Position", units:"F",
                           devcName:"Monochromator", hwChan:2, type:"UNKNOWN", subtype:"F", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:7.0, dbandHi:0.0, alarmHi:null)

        cleanroomhumidity  (Channel,
                    description:"Humidity", units:"P",
                           devcName:"Enviro", hwChan:0, type:"UNKNOWN", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:40.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:80.0, dbandHi:0.0, alarmHi:null)

        roomtemperature  (Channel,
                    description:"Temperature", units:"C",
                           devcName:"Enviro", hwChan:1, type:"UNKNOWN", subtype:"C", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:65.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:75.0, dbandHi:0.0, alarmHi:null)

        dewpoint  (Channel,
                    description:"Dew Point", units:"D",
                           devcName:"Enviro", hwChan:2, type:"UNKNOWN", subtype:"C", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:1.0, dbandHi:0.0, alarmHi:null)

        partcounter  (Channel,
                    description:"Particle Count", units:"1",
                           devcName:"Enviro", hwChan:3, type:"UNKNOWN", subtype:"1", offset:0.0, scale:1.0,
                           checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:10.0, dbandHi:0.0, alarmHi:null)
}

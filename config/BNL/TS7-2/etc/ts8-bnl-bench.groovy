import org.lsst.ccs.description.groovy.CCSBuilder;
import org.lsst.ccs.subsystem.teststand.data.TSConfig;
import org.lsst.ccs.subsystem.teststand.TS8Bench;
import org.lsst.ccs.subsystem.teststand.KeithleyDevice;
import org.lsst.ccs.subsystem.teststand.KeithleySimDevice;
import org.lsst.ccs.subsystem.teststand.Cornerstone260Device;
import org.lsst.ccs.subsystem.teststand.Cornerstone260SimDevice;
import org.lsst.ccs.subsystem.teststand.NewportLampDevice;
import org.lsst.ccs.subsystem.teststand.NewportLampSimDevice;
import org.lsst.ccs.subsystem.teststand.ThorlabsFWDevice;
import org.lsst.ccs.subsystem.teststand.ThorlabsSC10Device;
import org.lsst.ccs.subsystem.teststand.alerts.TS7Alerts;
import org.lsst.ccs.bootstrap.BootstrapResourceUtils;

import org.lsst.ccs.monitor.Alarm;
import org.lsst.ccs.monitor.Line;
import org.lsst.ccs.monitor.Channel;

CCSBuilder builder = ["ts"]

Properties props = BootstrapResourceUtils.getBootstrapSystemProperties()
def runMode = props.getProperty("org.lsst.ccs.run.mode","normal");

Class keithleyClass = Class.forName("org.lsst.ccs.subsystem.teststand.Keithley" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
Class monochromatorClass = Class.forName("org.lsst.ccs.subsystem.teststand.Cornerstone260" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
Class lamClass = Class.forName("org.lsst.ccs.subsystem.teststand.NewportLamp" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
Class thorlabsFWClass = Class.forName("org.lsst.ccs.subsystem.teststand.ThorlabsFWDevice");
Class thorlabsSC10Class = Class.forName("org.lsst.ccs.subsystem.teststand.ThorlabsSC10Device");
Class cryoClass = Class.forName("org.lsst.ccs.subsystem.teststand.CryoCon24c" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
//Class pduClass = Class.forName("org.lsst.ccs.subsystem.common.devices.power.distribution.APC7900" + (runMode.equals("simulation") ? "Sim" : "") + "Device");
Class turboClass = Class.forName("org.lsst.ccs.subsystem.common.devices.turbopump.TwisTorr84" + "Device");


taskConfig = ["monitor-update/taskPeriodMillis":60000,"monitor-publish/taskPeriodMillis":60000]

builder.
    main (TSSubSys, nodeTags:taskConfig) {

    Lamp  (lamClass, host:"PF", port:9600) {       
        lamppower  (Channel, description:"Lamp Power", units:"W",devcName:"Lamp", hwChan:0, type:"Watts")
        lampcurrent  (Channel, description:"Lamp Current", units:"A",devcName:"Lamp", hwChan:1, type:"Amps")
    }    
    
    PhotoDiode  (keithleyClass, devName:"PJ", baudRate:57600, connType:"ftdi")
    /*
    {
        mon_voltage  (Channel,
            description:"photodiode supply voltage", units:"V",
            devcName:"Monitor", hwChan:KeithleyDevice.CHAN_VOLTAGE, offset:0.0, scale:1.0,
            checkLo:"alarm", limitLo:-74.0, dbandLo:0.0, alarmLo:"AlarmHDWPD",
            checkHi:"alarm",   limitHi:2.0, dbandHi:0.0, alarmHi:"AlarmHDWPD")
        
        mon_current  (Channel,
            description:"photodiode supply current", units:"I",
            devcName:"Monitor", hwChan:KeithleyDevice.CHAN_CURRENT, offset:0.0, scale:1.0,
            checkLo:"alarm", limitLo:-1.0e6, dbandLo:0.0, alarmLo:"AlarmHDWPD",
            checkHi:"alarm",  limitHi:1.0e6, dbandHi:0.0, alarmHi:"AlarmHDWPD")
    }
            */

    Bias  (keithleyClass, devName:"PH", baudRate:57600, connType:"ftdi")
     /*
    {
        cal_voltage  (Channel,
            description:"photodiode supply voltage", units:"V",
            devcName:"Calibration", hwChan:KeithleyDevice.CHAN_VOLTAGE, offset:0.0, scale:1.0,
            checkLo:"alarm", limitLo:-74.0, dbandLo:0.0, alarmLo:"AlarmHDWPD",
            checkHi:"alarm",   limitHi:2.0, dbandHi:0.0, alarmHi:"AlarmHDWPD")
        
        cal_current  (Channel,
            description:"Calibration supply current", units:"I",
            devcName:"Calibration", hwChan:KeithleyDevice.CHAN_CURRENT, offset:0.0, scale:1.0,
            checkLo:"alarm", limitLo:-1.0e6, dbandLo:0.0, alarmLo:"AlarmHDWPD",
            checkHi:"alarm",  limitHi:1.0e6, dbandHi:0.0, alarmHi:"AlarmHDWPD")        
    }
            */

    Cryo   (cryoClass, host:"A103LM1Q", maxSetPoints:[35, 35, 35, 35] as double[],
            channelTypes:["A":"PTC100", "B":"PTC100", "C":"NONE", "D":"PTC100"],
            channelUnits:["A":"C", "B":"C", "C":"C", "D":"C"], 
            p_gainLoop1:12.0, i_gainLoop1:440.0, d_gainLoop1:63.0, 
            p_gainLoop2:2.5, i_gainLoop2:220.0, d_gainLoop2:31.0)
    
    TS7AlertHandler (TS7AlertHandler)

    Turbo  (turboClass, devcId:"", lowSpeedMode:false, waterCooling:false,
            ventValveByCmnd:true, interlockType:true, softStartMode:true,
            activeStopMode:true, model304:false)

    VQMonitor (GPVacMon835Device, serialdev:"/dev/ttyACM0")

//    PDU15 (pduClass, node:"",outlets:["VQM Controller","CRYO-CON 24C","REB-PS 48V","OTM-PS 5V","ROUGH-PUMP","TURBO-PUMP","NET-SWITCH (ON)","VATvalve"])

//    PDU20 (pduClass, node:"",outlets:["NF-55-1","NF-55-2","PT-30","XED-POWER","XED-CONTROL","ALWAYS-6 ON","ALWAYS-7 ON","ESD-ON"])


    Monochromator (monochromatorClass, host:"PG", baud:9600, connType:"ftdi",
        filter_edges:[0.0,1.0,335.0,525.0,620.0,790.0], filter_label:['empty1','empty2','Edge305','Edge495','Edge590','Edge760'])

    {
     /*
 monochromatordefaultwavelength  (Channel,
            description:"Wavelength", units:"A",
            devcName:"Monochromator", hwChan:-1, type:"UNKNOWN", subtype:"A", offset:0.0, scale:1.0,
            checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
            checkHi:"flag", limitHi:2000.0, dbandHi:0.0, alarmHi:null)
*/
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
/*
        shutteropen  (Channel,
            description:"Shutter Open/Closed", units:"S",
            devcName:"Monochromator", hwChan:1, type:"UNKNOWN", subtype:"S", offset:0.0, scale:1.0,
            checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
            checkHi:"flag", limitHi:2.0, dbandHi:0.0, alarmHi:null)
*/
        filter1position  (Channel,
            description:"Filter Position", units:"F",
            devcName:"Monochromator", hwChan:2, type:"UNKNOWN", subtype:"F", offset:0.0, scale:1.0,
            checkLo:"flag",limitLo:0.0, dbandLo:0.0, alarmLo:null,
            checkHi:"flag", limitHi:7.0, dbandHi:0.0, alarmHi:null)

    }

    SpotProjFWheel (thorlabsFWClass, devcId:"",
        //devcId:"/dev/serial/by-id/usb-FTDI_USB__-__Serial_Cable_FT1RAJQE-if00-port0", 
        fwsize:12, speedMode:true, sensorMode:false,
        filterNames:["Mask_grid","Mask_spot","empty3","empty4","empty5","empty6"])
    {
        SpotProjFWheelPos (Channel, 
                           description:"Spot projector filter wheel position",
                           devcName:"SpotProjFWheel", type:"POSITION",
                           format:"%.0f", checkLo:"none", checkHi:"none")
    }

    ProjectorShutter (thorlabsSC10Class, devcId:"",
       //devcId:"/dev/serial/by-id/usb-FTDI_USB__-__Serial_Cable_FT1RAJQE-if01-port0", 
       outputMode:false)
    {
    }

//    AlarmHDWPD (Alarm, eventParm:TSConfig.EVENT_ID.PD.ordinal())

    AlarmCryoHighTempLimit  (Alarm, description:"Cryo Plate high temperature alarm", eventParm:TS7Alerts.CRYO_PLATE_TEMPERATURE_TOO_HIGH.ordinal())

    AlarmCryoLowTempLimit   (Alarm, description:"Cryo Plate low temperature alarm", eventParm:TS7Alerts.CRYO_PLATE_TEMPERATURE_TOO_LOW.ordinal())
    
    AlarmColdHighTempLimit  (Alarm, description:"Cold Plate high temperature alarm", eventParm:TS7Alerts.COLD_PLATE_TEMPERATURE_TOO_HIGH.ordinal())

    AlarmColdLowTempLimit   (Alarm, description:"Cold Plate low temperature alarm", eventParm:TS7Alerts.COLD_PLATE_TEMPERATURE_TOO_LOW.ordinal())

    AlarmPressureHighLimit  (Alarm, description:"Pressure too high alarm", eventParm:TS7Alerts.PRESSURE_TOO_HIGH.ordinal())

    AlarmPressureLowLimit   (Alarm, description:"Pressure too low alarm", eventParm:TS7Alerts.PRESSURE_TOO_LOW.ordinal())

    AlarmTurboStatusFail    (Alarm, description:"Turbo Pump Status = Fail", eventParm:TS7Alerts.TURBO_PUMP_FAIL.ordinal())

    AlarmTurboStatusSlow    (Alarm, description:"Turbo Pump Status below Normal", eventParm:TS7Alerts.TURBO_PUMP_SLOW.ordinal())

    AlarmTurboTempHighLimit (Alarm, description:"Turbo Pump Temp too high", eventParm:TS7Alerts.TURBO_PUMP_OVERTEMP.ordinal())

    AlarmGeneric  (Alarm, description:"Generic alarm", eventParm:TS7Alerts.GENERIC.ordinal())



        ColdPlate  (Channel, description:"Cryogenics temperature A", units:"\u00b0C",
                 devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_TEMP_A,
                 checkLo:"alarm", limitLo:-135, dbandLo:35.0, alarmLo:"AlarmColdLowTempLimit",
                 checkHi:"alarm", limitHi:30, dbandHi:35.0, alarmHi:"AlarmColdHighTempLimit")

        CryoPlate  (Channel, description:"Cryogenics temperature B", units:"\u00b0C",
                 devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_TEMP_B,
                 limitLo:-135.0, dbandLo:35.0, checkLo:"alarm", alarmLo:"AlarmCryoLowTempLimit",
                 checkHi:"alarm", limitHi:30.0, dbandHi:35.0, alarmHi:"AlarmCryoHighTempLimit")


    htrread1  (Channel, description:"Cryogenics heater loop 1 % power", units:"%",
               devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_HTR_1, limitLo:0.0, limitHi:100.0)

    htrread2  (Channel, description:"Cryogenics heater loop 2 % power", units:"%",
               devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_HTR_2, limitLo:0.0, limitHi:100.0)

    tempChng  (Channel, description:"Temperature change rate", units:"\u00b0C/min",
               devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_TEMP_CHNG,
               checkLo:"alarm", limitLo:-10.0, alarmLo:"AlarmGeneric",
               checkHi:"alarm", limitHi:10.0, alarmHi:"AlarmGeneric")

    SetPnt1  (Channel, description:"setPoint Loop 1", units:"",
              devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_SETPOINT_1,
              limitLo:-135.0, checkHi:"alarm", limitHi:27.0, alarmHi:"AlarmGeneric")

    SetPnt2  (Channel, description:"setPoint Loop 2", units:"",
              devcName:"Cryo", hwChan:CryoCon24cDevice.CHAN_SETPOINT_2,
              limitLo:-135.0, checkHi:"alarm", limitHi:27.0, alarmHi:"AlarmGeneric")

    vqmpressure  (Channel, description:"VQM Pressure Reading", units:"Torr", format:".3G",
                  devcName:"VQMonitor", hwChan:0,
                limitLo:750.0, dbandLo:5.0, checkLo:"alarm", alarmLo:"AlarmPressureLowLimit",
                checkHi:"alarm", limitHi:810.0, dbandHi:20.0, alarmHi:"AlarmPressureHighLimit")
/*
    PDU15Current  (Channel, description:"PDU15 current", units:"Amps",
                   devcName:"PDU15", hwChan:APC7900Device.CHAN_CURRENT, type:"POWER",
                   limitHi:12.0)

    PDU15Power    (Channel, description:"PDU15 power", units:"Watts",
                   devcName:"PDU15", hwChan:APC7900Device.CHAN_POWER, type:"POWER",
                   limitHi:1320.0)

    PDU20Current  (Channel, description:"PDU20 current", units:"Amps",
                   devcName:"PDU20", hwChan:APC7900Device.CHAN_CURRENT, type:"POWER",
                   limitHi:16.0)

    PDU20Power    (Channel, description:"PDU20 power", units:"Watts",
                   devcName:"PDU20", hwChan:APC7900Device.CHAN_POWER, type:"POWER",
                   limitHi:1760.0)

    TurboCurrent      (Channel, description:"TurboPump current", units:"mA dc",
                       devcName:"Turbo", type:"Numeric", subtype:"CURRENT",
                       checkLo:"none", checkHi:"none", format:"%.0f")

    TurboVoltage      (Channel, description:"TurboPump voltage", units:"V dc",
                       devcName:"Turbo", type:"Numeric", subtype:"VOLTAGE",
                       checkLo:"none", checkHi:"none", format:"%.0f")

    TurboPower        (Channel, description:"TurboPump power", units:"W",
                       devcName:"Turbo", type:"Numeric", subtype:"POWER",
                       checkLo:"none", checkHi:"alarm", format:"%.0f",
                       limitHi:71.0, dbandHi:31.0, alarmHi:"AlarmGeneric")

    TurboDriveFreq    (Channel, description:"TurboPump drive freq.", units:"Hz",
                       devcName:"Turbo", type:"Numeric", subtype:"DRIVEFREQ",
                       checkLo:"none", checkHi:"none", format:"%.0f")

    TurboPumpTemp     (Channel, description:"TurboPump pump temperature", 
                       units:"deg C", devcName:"Turbo", 
                       type:"Numeric", subtype:"PUMP_TEMP", format:"%.0f",
                       limitLo:0.0, checkLo:"flag", dbandLo:5.0, 
                       limitHi:35.0, checkHi:"alarm", dbandHi:5.0, 
                       alarmHi:"AlarmTurboTempHighLimit")

    TurboContTempSink (Channel, description:"TurboPump controller sink temp.", 
                       units:"deg C", devcName:"Turbo", 
                       type:"Numeric", subtype:"CONT_TEMP_SINK", format:"%.0f",
                       limitLo:0.0, checkLo:"flag", dbandLo:5.0, 
                       limitHi:35.0, checkHi:"alarm", dbandHi:5.0, 
                       alarmHi:"AlarmTurboTempHighLimit")

    TurboContTempAir  (Channel, description:"TurboPump controller air temp.", 
                       units:"deg C", devcName:"Turbo", 
                       type:"Numeric", subtype:"CONT_TEMP_AIR", format:"%.0f",
                       limitLo:0.0, checkLo:"flag", dbandLo:5.0, 
                       limitHi:35.0, checkHi:"alarm", dbandHi:5.0, 
                       alarmHi:"AlarmTurboTempHighLimit")

    TurboRPM          (Channel, description:"TurboPump speed", units:"RPM",
                       devcName:"Turbo", type:"Numeric", subtype:"RPM",
                       checkLo:"none", checkHi:"none", format:"%.0f")

    TurboStatus       (Channel, description:"TurboPump status: 5=normal, 6=fail", 
                       devcName:"Turbo", type:"Numeric", subtype:"STATUS", 
                       format:"%.0f", limitLo:-0.5,  dbandLo:5.0, limitHi:5.5,
                       checkLo:"alarm", alarmLo:"AlarmTurboStatusSlow",
                       checkHi:"alarm", alarmHi:"AlarmTurboStatusFail")

    UPS_Status    (Channel, description:"UPS status", format:".0f",
                   devcName:"UPS", hwChan:AP9630UPSDevice.CHAN_STATUS)
               
    UPS_Current   (Channel, description:"UPS output current", units:"Amps", format:".2f",
                   devcName:"UPS", hwChan:AP9630UPSDevice.CHAN_OUT_CURRENT)
               
    UPS_Charge    (Channel, description:"UPS battery charge", units:"%", format:".2f",
                   devcName:"UPS", hwChan:AP9630UPSDevice.CHAN_BATT_CHARGE)
               
    UPS_RemTime   (Channel, description:"UPS remaining time", units:"secs", format:".0f",
                   devcName:"UPS", hwChan:AP9630UPSDevice.CHAN_REM_TIME)
    ThermalConfiguration(ThermalConfiguration, coldSetPoint: Double.NaN, cryoSetPoint: Double.NaN, 
        coldMonitoringLimitAlgorithm: 'NONE', cryoMonitoringLimitAlgorithm: 'NONE',
        coldMonitoringLimitAlgorithmParameters: [],   cryoMonitoringLimitAlgorithmParameters: [])
    
    VacuumConfiguration(VacuumConfiguration, pressureSetPoint: Double.NaN, 
        pressureMonitoringLimitAlgorithm: 'NONE', pressureMonitoringLimitAlgorithmParameters: [], 
        pressureMonitoringTransitionAlgorithm: 'NONE', pressureMonitoringTransitionAlgorithmParameters: [])  
*/               

}

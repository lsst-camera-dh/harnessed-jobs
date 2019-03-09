import org.lsst.ccs.description.groovy.CCSBuilder;
import org.lsst.ccs.subsystem.metrology.MetrologySubSys;
import org.lsst.ccs.subsystem.metrology.MetrologyConfigurable;
import org.lsst.ccs.subsystem.metrology.PointListConfigurable;

import org.lsst.ccs.subsystem.metrology.AerotechP165Device;
import org.lsst.ccs.subsystem.metrology.KeyenceG5001Device;
import org.lsst.ccs.subsystem.metrology.data.MetrologyConfig;

import org.lsst.ccs.monitor.Alarm;
import org.lsst.ccs.monitor.Line;
import org.lsst.ccs.monitor.Channel;


String limitLo = "limitLo"
String limitHi = "limitHi"

CCSBuilder builder = ["ts5"]

taskConfig = ["monitor-update/taskPeriodMillis":5000,"monitor-publish/taskPeriodMillis":5000]

builder.
    main (MetrologySubSys, nodeTags:taskConfig) {

//builder.
//    main (MetrologySubSys,
//        broadcastMillis:5000, configName:"metrology") {

    Measurer (KeyenceG5001Device, devcName:"/dev/ttyS1", baudRate:38400)
    
    Positioner (AerotechP165Device, host:"130.199.47.32", port:8000, xOffset:-300.0, yOffset:-200.0, zOffset:-100.0)

    //    AlarmHDW  (TSSubSys, argMap("OV", 0))
    AlarmLo  (Alarm, eventParm:MetrologyConfig.EVENT_ID.POSX.ordinal())
    AlarmHi  (Alarm, eventParm:MetrologyConfig.EVENT_ID.POSX.ordinal())

    for (int j = 0; j < 150; j++) {
        def apc = "ASPIC$j"

        "Point$j" (PointListConfigurable,
            PointX:-999.0,
            PointY:-999.0,
            PointZ:-999.0)  
    }

    "RTM" (MetrologyConfigurable,
	name:'RTM',
        startx:22.0,
        stopx:107.0,
        dx:4.0,
        starty:52.0,
        stopy:159.0,
        dy:4.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples:6,
        measmode:0,
        acceleration:1.0,
        speed:2.5)

    "RTM_Explore"(MetrologyConfigurable,
        name:'RTM_Explore',
        startx:22.0,
        stopx:42.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "RTM_calib"(MetrologyConfigurable,
        name:'RTM_calib',
        startx:22.0,
        stopx:107.0,
        dx: 4.0,
        starty:52.0,
        stopy:159.0,
        dy: 4.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "SCAN3"(MetrologyConfigurable,
        name:'SCAN3',
        startx:22.0,
        stopx:42.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "SCAN4"(MetrologyConfigurable,
        name:'SCAN4',
        startx:22.0,
        stopx:42.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD00"(MetrologyConfigurable,
        name:'CCD00',
        startx:0.0,
        stopx:20.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD01"(MetrologyConfigurable,
        name:'CCD01',
        startx:20.0,
        stopx:40.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        z:58.0,
        dy: 2.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD02"(MetrologyConfigurable,
        name:'CCD02',
        startx:40.0,
        stopx:60.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD10"(MetrologyConfigurable,
        name:'CCD10',
        startx:0.0,
        stopx:20.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD11"(MetrologyConfigurable,
        name:'CCD11',
        startx:20.0,
        stopx:40.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD12"(MetrologyConfigurable,
        name:'CCD12',
        startx:40.0,
        stopx:60.0,
        dx: 2.0,
        starty:55.0,
        stopy:159.0,
        dy: 2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples: 6,
        measmode: 0,
        acceleration:1.0,
        speed:2.5)

    "CCD20"(MetrologyConfigurable,
        name:'CCD20',
        startx:0.0,
        stopx:20.0,
        dx:2.0,
        starty:55.0,
        stopy:159.0,
        dy:2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples:6,
        measmode:0,
        acceleration:1.0,
        speed:2.5)

    "CCD21"(MetrologyConfigurable,
        name:'CCD21',
        startx:20.0,
        stopx:40.0,
        dx:2.0,
        starty:55.0,
        stopy:159.0,
        dy:2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples:6,
        measmode:0,
        acceleration:1.0,
        speed:2.5)

    "CCD22"(MetrologyConfigurable,
        name:'CCD22',
        startx:40.0,
        stopx:60.0,
        dx:2.0,
        starty:55.0,
        stopy:159.0,
        dy:2.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples:6,
        measmode:0,
        acceleration:1.0,
        speed:2.5)

    "BASEPLATE"(MetrologyConfigurable,
        name:'BASEPLATE',
        startx:0.0,
        stopx:20.0,
        dx:4.0,
        starty:44.0,
        stopy:142.0,
        dy:4.0,
        z:58.0,
        rotation:0.0,
        cornerang:89.5,
        nsamples:6,
        measmode:0,
        acceleration:1.0,
        speed:2.5)


    /*
    CmpCCDBias  (MonChannel,
   "CCD Bias Voltage", "V",
    "alarm", aDbl(limitLo, 0.0, 0.0,
    "alarm", aDbl(limitHi, 0.0, 0.0,
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
    The checking option:NONE, FLAG or ALARM
    The limit value.
    The alarm to be activated upon status transitions when ALARM is specified.
    The deadband value which delays a potential alarm action during a transition back to good status.
    Its id, which is its index in the list of all channels.

    The limit values are maintained by the configuration system and can be changed while running.  Any such change causes a status message to be broadcast, which can be used to update the trending database or to update any console displays.
     */
    posX  (Channel,
                   description:"posX", units:"mm",
                           devcName:"Positioner", hwChan:0, type:"POSITION", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-1.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:301.0, dbandHi:0.0, alarmHi:null)

    posY  (Channel,
                   description:"posY", units:"mm",
                           devcName:"Positioner", hwChan:1, type:"POSITION", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-1.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:301.0, dbandHi:0.0, alarmHi:null)

    posZ  (Channel,
                   description:"posZ", units:"mm",
                           devcName:"Positioner", hwChan:2, type:"POSITION", subtype:"P", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-1.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:201.0, dbandHi:0.0, alarmHi:null)
    displacement  (Channel,
                   description:"displacement", units:"mm",
                           devcName:"Measurer", hwChan:0, type:"POSITION", subtype:"A", offset:0.0, scale:1.0,
                           checkLo:"flag", limitLo:-1000.0, dbandLo:0.0, alarmLo:null,
                           checkHi:"flag", limitHi:1000.0, dbandHi:0.0, alarmHi:null)

}

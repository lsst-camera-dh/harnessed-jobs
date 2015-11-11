import static org.lsst.gruth.jutils.MapArgs.*;
import org.lsst.ccs.startup.CCSBuilder;
import org.lsst.ccs.subsystem.archon.Archon

CCSBuilder builder = ["archon"]

builder.
    main(ArchonTS, argMap("main", 1000, null))

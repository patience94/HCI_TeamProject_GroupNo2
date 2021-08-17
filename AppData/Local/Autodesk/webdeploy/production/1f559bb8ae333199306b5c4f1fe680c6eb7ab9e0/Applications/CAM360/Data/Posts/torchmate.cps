/**
  Copyright (C) 2012-2017 by Autodesk, Inc.
  All rights reserved.

  Torchmate Mill/Plasma post processor configuration.

  $Revision: 42473 905303e8374380273c82d214b32b7e80091ba92e $
  $Date: 2019-09-04 00:46:02 $
  
  FORKID {7B91741C-EF71-49D7-9E87-E53C2C071888}
*/

/* additional commands
M100 Wait for input line (normal state)
M101 Wait for input line (tripped state)
*/

description = "Torchmate 3.0 Mill/Plasma";
vendor = "Torchmate";
vendorUrl = "http://torchmate.com";
legal = "Copyright (C) 2012-2017 by Autodesk, Inc.";
certificationLevel = 2;
minimumRevision = 40783;

longDescription = "Generic post for Torchmate 3.0 Mill/Plasma. Enable property 'useZ' to output Z moves. Turn off property 'useWorkOffsets' if G54, G55, ... work offsets are not used. Disable property 'useM30' to avoid M30 at end of program. Disable property 'useCoolant' to avoid coolant M-codes. Disable property 'useTool' if tool calls should not be output.";

extension = "fgc";
setCodePage("ascii");

capabilities = CAPABILITY_MILLING | CAPABILITY_JET;
tolerance = spatial(0.002, MM);

minimumChordLength = spatial(0.25, MM);
minimumCircularRadius = spatial(0.01, MM);
maximumCircularRadius = spatial(1000, MM);
minimumCircularSweep = toRad(0.01);
maximumCircularSweep = toRad(180);
allowHelicalMoves = true; // for milling
allowedCircularPlanes = undefined; // allow any circular motion

// user-defined properties
properties = {
  writeMachine: true, // write machine.
  showSequenceNumbers: true, // show sequence numbers.
  sequenceNumberStart: 10, // first sequence number.
  sequenceNumberIncrement: 1, // increment for sequence numbers.
  separateWordsWithSpace: true, // specifies that the words should be separated with a white space.
  useRadius: false, // specifies that arcs should be output using the radius (R word) instead of the I, J, and K words.
  dwellInSeconds: true, // specifies the dwell unit - use true:seconds and false:milliseconds.
  useZ: false, // disable to output only XY motion.
  useWorkOffsets: true, // enable to output G54, ... work offsets.
  useCoolant: true, // enable to output coolant M-codes. E.g. M9.
  useTool: true, // enable to output tool calls. E.g. T1.
  useM30: true // enable to output M30 for program end.
};

// user-defined property definitions
propertyDefinitions = {
  writeMachine: {title:"Write machine", description:"Output the machine settings in the header of the code.", group:0, type:"boolean"},
  showSequenceNumbers: {title:"Use sequence numbers", description:"Use sequence numbers for each block of outputted code.", group:1, type:"boolean"},
  sequenceNumberStart: {title:"Start sequence number", description:"The number at which to start the sequence numbers.", group:1, type:"integer"},
  sequenceNumberIncrement: {title:"Sequence number increment", description:"The amount by which the sequence number is incremented by in each block.", group:1, type:"integer"},
  separateWordsWithSpace: {title:"Separate words with space", description:"Adds spaces between words if 'yes' is selected.", type:"boolean"},
  useRadius: {title:"Radius arcs", description:"If yes is selected, arcs are outputted using radius values rather than IJK.", type:"boolean"},
  dwellInSeconds: {title:"Dwell in seconds", description:"Specifies the unit for dwelling, set to 'Yes' for seconds and 'No' for milliseconds.", type:"boolean"},
  useZ: {title:"Use Z Values", description:"If disabled, all Z values are ommited.", type:"boolean"},
  useWorkOffsets: {title:"Use work offsets", description:"Enable to allow the use of work offsets.", type:"boolean"},
  useCoolant: {title:"Use coolant", description:"Enable to ouput coolant commands.", type:"boolean"},
  useTool: {title:"Use tool", description:"Enable to ouptut tool calls. E.g. T1.", type:"boolean"},
  useM30: {title:"Use M30", description:"Enable to output M30 for program end.", type:"boolean"}
};

var mapCoolantTable = new Table(
  [9, 8, 7],
  {initial:COOLANT_OFF, force:true},
  "Invalid coolant mode"
);

var gFormat = createFormat({prefix:"G", decimals:1});
var mFormat = createFormat({prefix:"M", decimals:0});
var hFormat = createFormat({prefix:"H", decimals:0});
var dFormat = createFormat({prefix:"D", decimals:0});

var xyzFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true, force:false});
var rFormat = xyzFormat; // radius
var feedFormat = createFormat({decimals:(unit == MM ? 1 : 2), forceDecimal:true});
var toolFormat = createFormat({decimals:0});
var rpmFormat = createFormat({decimals:0});
var secFormat = createFormat({decimals:3, forceDecimal:true}); // seconds - range 0.001-99999.999
var milliFormat = createFormat({decimals:0}); // milliseconds // range 1-9999

var xOutput = createVariable({prefix:"X", force:false}, xyzFormat);
var yOutput = createVariable({prefix:"Y", force:false}, xyzFormat);
var zOutput = createVariable({prefix:"Z", force:false}, xyzFormat);

var feedOutput = createVariable({prefix:"F"}, feedFormat);
var sOutput = createVariable({prefix:"S", force:true}, rpmFormat);

// circular output
var iOutput = createReferenceVariable({prefix:"I", force:true}, xyzFormat);
var jOutput = createReferenceVariable({prefix:"J", force:true}, xyzFormat);
var kOutput = createReferenceVariable({prefix:"K", force:true}, xyzFormat);

var gMotionModal = createModal({force:false}, gFormat); // modal group 1 // G0-G3
var gPlaneModal = createModal({onchange:function () {gMotionModal.reset();}}, gFormat); // modal group 2 // G17-19
var gAbsIncModal = createModal({}, gFormat); // modal group 3 // G90-91
var gUnitModal = createModal({}, gFormat); // modal group 6 // G20-21 or G70-71
var gCycleModal = createModal({}, gFormat); // modal group 9 // G81, ...
var gRetractModal = createModal({}, gFormat); // modal group 10 // G98-99

var WARNING_WORK_OFFSET = 0;

// collected state
var sequenceNumber;
var currentWorkOffset;

/**
  Writes the specified block.
*/
function writeBlock() {
  if (properties.showSequenceNumbers) {
    writeWords2("N" + (sequenceNumber % 100000), arguments);
    sequenceNumber += properties.sequenceNumberIncrement;
  } else {
    writeWords(arguments);
  }
}

/**
  Writes the specified optional block.
*/
function writeOptionalBlock() {
  if (properties.showSequenceNumbers) {
    var words = formatWords(arguments);
    if (words) {
      writeWords("/", "N" + (sequenceNumber % 10000), words);
      sequenceNumber += properties.sequenceNumberIncrement;
      if (sequenceNumber >= 10000) {
        sequenceNumber = properties.sequenceNumberStart;
      }
    }
  } else {
    writeWords2("/", arguments);
  }
}

function formatComment(text) {
  return "(" + String(text).replace(/[()]/g, "") + ")";
}

/**
  Output a comment.
*/
function writeComment(text) {
  writeln(formatComment(text));
}

function onOpen() {
  if (properties.useRadius) {
    maximumCircularSweep = toRad(90); // avoid potential center calculation errors for CNC
  }

  if (!properties.useZ) {
    zOutput.disable();
  }
  
  if (!properties.separateWordsWithSpace) {
    setWordSeparator("");
  }

  sequenceNumber = properties.sequenceNumberStart;

  if (programComment) {
    writeComment(programComment);
  }

  // dump machine configuration
  var vendor = machineConfiguration.getVendor();
  var model = machineConfiguration.getModel();
  var description = machineConfiguration.getDescription();

  if (properties.writeMachine && (vendor || model || description)) {
    writeComment(localize("Machine"));
    if (vendor) {
      writeComment("  " + localize("vendor") + ": " + vendor);
    }
    if (model) {
      writeComment("  " + localize("model") + ": " + model);
    }
    if (description) {
      writeComment("  " + localize("description") + ": "  + description);
    }
  }

  switch (unit) {
  case IN:
    writeBlock(gUnitModal.format(70)); // or use M20
    break;
  case MM:
    writeBlock(gUnitModal.format(71)); // or use M21
    break;
  }

  if ((getNumberOfSections() > 0) && (getSection(0).workOffset == 0)) {
    for (var i = 0; i < getNumberOfSections(); ++i) {
      if (getSection(i).workOffset > 0) {
        error(localize("Using multiple work offsets is not possible if the initial work offset is 0."));
        return;
      }
    }
  }

  // absolute coordinates
  if (properties.useZ) {
    writeBlock(gAbsIncModal.format(90), conditional(properties.useZ, gPlaneModal.format(17)));
  } else {
    writeBlock(gAbsIncModal.format(90));
  }
}

function onComment(message) {
  writeComment(message);
}

/** Force output of X, Y, and Z. */
function forceXYZ() {
  xOutput.reset();
  yOutput.reset();
}

/** Force output of X, Y, Z, and F on next output. */
function forceAny() {
  forceXYZ();
  feedOutput.reset();
}

function onSection() {
  var insertToolCall = isFirstSection() ||
    currentSection.getForceToolChange && currentSection.getForceToolChange() ||
    (tool.number != getPreviousSection().getTool().number);
  
  var retracted = false; // specifies that the tool has been retracted to the safe plane
  var newWorkOffset = isFirstSection() ||
    (getPreviousSection().workOffset != currentSection.workOffset); // work offset changes
  var newWorkPlane = isFirstSection() ||
    !isSameDirection(getPreviousSection().getGlobalFinalToolAxis(), currentSection.getGlobalInitialToolAxis());
  if (insertToolCall || newWorkOffset || newWorkPlane) {
    
    // stop spindle before retract during tool change
    if (insertToolCall && !isFirstSection()) {
      onCommand(COMMAND_STOP_SPINDLE);
    }

    // retract to safe plane
    if (properties.useZ) {
      retracted = true;
      writeBlock(gFormat.format(28), gAbsIncModal.format(91), "Z" + xyzFormat.format(0)); // retract
      writeBlock(gAbsIncModal.format(90));
      zOutput.reset();
    }
  }

  writeln("");
  
  if (hasParameter("operation-comment")) {
    var comment = getParameter("operation-comment");
    if (comment) {
      writeComment(comment);
    }
  }

  if (properties.useTool) {
    if (currentSection.type == TYPE_JET) {
      switch (tool.type) {
      case TOOL_PLASMA_CUTTER:
        break;
      /*
      case TOOL_MARKER:
        break;
      */
      default:
        error(localize("The CNC does not support the required tool/process. Only plasma cutting is supported."));
        return;
      }

      switch (currentSection.jetMode) {
      case JET_MODE_THROUGH:
        break;
      case JET_MODE_ETCHING:
        break;
      case JET_MODE_VAPORIZE:
        error(localize("Vaporize cutting mode is not supported."));
        break;
      default:
        error(localize("Unsupported cutting mode."));
        return;
      }

      var toolNumber = 1; // plasma
      if (currentSection.jetMode == JET_MODE_ETCHING) {
        toolNumber = 2; // marker
      }
      writeBlock(mFormat.format(6), "T" + toolFormat.format(toolNumber));
    } else {
      writeBlock(mFormat.format(6), "T" + toolFormat.format(tool.number));
    }
  }
  if (tool.comment) {
    writeComment(tool.comment);
  }
  
  if ((currentSection.type == TYPE_MILLING) &&
      (insertToolCall ||
       isFirstSection() ||
       (rpmFormat.areDifferent(spindleSpeed, sOutput.getCurrent())) ||
       (tool.clockwise != getPreviousSection().getTool().clockwise))) {
    if (spindleSpeed < 1) {
      error(localize("Spindle speed out of range."));
    }
    if (spindleSpeed > 99999) {
      warning(localize("Spindle speed exceeds maximum value."));
    }
    writeBlock(
      sOutput.format(spindleSpeed), mFormat.format(tool.clockwise ? 3 : 4)
    );
  }

  // wcs
  if (properties.useWorkOffsets) {
    if (insertToolCall) { // force work offset when changing tool
      currentWorkOffset = undefined;
    }
    var workOffset = currentSection.workOffset;
    if (workOffset == 0) {
      warningOnce(localize("Work offset has not been specified. Using G54 as WCS."), WARNING_WORK_OFFSET);
      workOffset = 1;
    }
    if (workOffset > 0) {
      if (workOffset > 6) {
        var p = workOffset - 6; // 1->...
        if (p > 100) {
          error(localize("Work offset out of range."));
        } else {
          if (workOffset != currentWorkOffset) {
            writeBlock(gFormat.format(54.1), "P" + p); // G54.1P
            currentWorkOffset = workOffset;
          }
        }
      } else {
        if (workOffset != currentWorkOffset) {
          writeBlock(gFormat.format(53 + workOffset)); // G54->G59
          currentWorkOffset = workOffset;
        }
      }
    }
  }

  { // pure 3D
    var remaining = currentSection.workPlane;
    if (!isSameDirection(remaining.forward, new Vector(0, 0, 1))) {
      error(localize("Tool orientation is not supported."));
      return;
    }
    setRotation(remaining);
  }

  // set coolant after we have positioned at Z
  if (properties.useCoolant) {
    var c = mapCoolantTable.lookup(tool.coolant);
    if (c) {
      writeBlock(mFormat.format(c));
    } else {
      warning(localize("Coolant not supported."));
    }
  }

  forceAny();

  var initialPosition = getFramePosition(currentSection.getInitialPosition());
  if (!retracted && properties.useZ && !insertToolCall) {
    if (getCurrentPosition().z < initialPosition.z) {
      writeBlock(gMotionModal.format(0), zOutput.format(initialPosition.z));
    }
  }

  gMotionModal.reset();

  if (true) {
    gMotionModal.reset();
    writeBlock(conditional(properties.useZ, gPlaneModal.format(17)));

    if (properties.useZ) {
      writeBlock(
        gAbsIncModal.format(90),
        gMotionModal.format(0), gFormat.format(43),
        xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z),
        hFormat.format(tool.lengthOffset)
      );
    } else {
      writeBlock(
        gAbsIncModal.format(90),
        gMotionModal.format(0),
        xOutput.format(initialPosition.x), yOutput.format(initialPosition.y)
      );
    }
  } else {
    writeBlock(
      gAbsIncModal.format(90),
      gMotionModal.format(0),
      xOutput.format(initialPosition.x),
      yOutput.format(initialPosition.y),
      zOutput.format(initialPosition.z)
    );
  }

  writeBlock(
    gAbsIncModal.format(90),
    gMotionModal.format(0),
    xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z)
  );

  // could use G31 Zz Ii Ss Cc Ff for seek sensing
}

function onDwell(seconds) {
  if (seconds > 99999.999) {
    warning(localize("Dwelling time is out of range."));
  }
  if (properties.dwellInSeconds) {
    writeBlock(gFormat.format(4), "X" + secFormat.format(seconds));
  } else {
    // P unit is setting in control!
    var milliseconds = clamp(1, seconds * 1000, 99999999);
    writeBlock(gFormat.format(4), "P" + milliFormat.format(milliseconds));
  }
}

function onSpindleSpeed(spindleSpeed) {
  writeBlock(sOutput.format(spindleSpeed));
}

function onCycle() {
  writeBlock(conditional(properties.useZ, gPlaneModal.format(17)));
}

function getCommonCycle(x, y, z, r) {
  forceXYZ();
  return [xOutput.format(x), yOutput.format(y),
    zOutput.format(z),
    "R" + xyzFormat.format(r)];
}

function onCyclePoint(x, y, z) {
  if (!properties.useZ) {
    error(localize("Z must be enabled by setting the 'useZ' property to use drilling cycles."));
    return;
  }
  if (!isSameDirection(getRotation().forward, new Vector(0, 0, 1))) {
    expandCyclePoint(x, y, z);
    return;
  }

  if (isFirstCyclePoint()) {
    repositionToCycleClearance(cycle, x, y, z);
    
    // return to initial Z which is clearance plane and set absolute mode

    var F = cycle.feedrate;
    var P = !cycle.dwell ? 0 : clamp(1, cycle.dwell * 1000, 99999); // in milliseconds

    switch (cycleType) {
    case "drilling":
      writeBlock(
        gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
        getCommonCycle(x, y, z, cycle.retract),
        feedOutput.format(F)
      );
      break;
    case "counter-boring":
      if (P > 0) {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(82),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + milliFormat.format(P),
          feedOutput.format(F)
        );
      } else {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
          getCommonCycle(x, y, z, cycle.retract),
          feedOutput.format(F)
        );
      }
      break;
    case "chip-breaking":
      expandCyclePoint(x, y, z);
      break;
    case "deep-drilling":
      if (P > 0) {
        expandCyclePoint(x, y, z);
      } else {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(83),
          getCommonCycle(x, y, z, cycle.retract),
          "Q" + xyzFormat.format(cycle.incrementalDepth),
          feedOutput.format(F)
        );
      }
      break;
    case "fine-boring": // not supported
      expandCyclePoint(x, y, z);
      break;
    case "reaming":
      writeBlock(
        gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(85),
        getCommonCycle(x, y, z, cycle.retract),
        feedOutput.format(F)
      );
      break;

    case "boring":
      if (P > 0) {
        expandCyclePoint(x, y, z);
      } else {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(85),
          getCommonCycle(x, y, z, cycle.retract),
          feedOutput.format(F)
        );
      }
      break;
    default:
      expandCyclePoint(x, y, z);
    }
  } else {
    if (cycleExpanded) {
      expandCyclePoint(x, y, z);
    } else {
      var _x = xOutput.format(x);
      var _y = yOutput.format(y);
      if (!_x && !_y) {
        xOutput.reset(); // at least one axis is required
        _x = xOutput.format(x);
      }
      writeBlock(_x, _y);
    }
  }
}

function onCycleEnd() {
  if (!cycleExpanded) {
    writeBlock(gCycleModal.format(80));
    zOutput.reset();
  }
}

var pendingRadiusCompensation = -1;

function onRadiusCompensation() {
  pendingRadiusCompensation = radiusCompensation;
}

var shapeArea = 0;
var shapePerimeter = 0;
var shapeSide = "inner";
var cuttingSequence = "";

function onParameter(name, value) {
  if ((name == "action") && (value == "pierce")) {
    // add delay if desired
  } else if (name == "shapeArea") {
    shapeArea = value;
  } else if (name == "shapePerimeter") {
    shapePerimeter = value;
  } else if (name == "shapeSide") {
    shapeSide = value;
  } else if (name == "beginSequence") {
    if (value == "piercing") {
      if (cuttingSequence != "piercing") {
        if (properties.allowHeadSwitches) {
          // Allow head to be switched here
          // writeBlock(mFormat.format(0), '"Switch head for piercing."');
        }
      }
    } else if (value == "cutting") {
      if (cuttingSequence == "piercing") {
        if (properties.allowHeadSwitches) {
          // Allow head to be switched here
          // writeBlock(mFormat.format(0), '"Switch head for cutting."');
        }
      }
    }
    cuttingSequence = value;
  }
}

function onPower(power) {
  writeBlock(mFormat.format(power ? 50 : 51)); // plasma on/off
}

function onRapid(_x, _y, _z) {
  // manual states linear interpolation - so not dog-leg motion expected
  // at least one axis is required
  if (pendingRadiusCompensation >= 0) {
    // ensure that we end at desired position when compensation is turned off
    xOutput.reset();
    yOutput.reset();
  }
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      var toolNumber = tool.number;
      if (currentSection.type == TYPE_JET) {
        toolNumber = 1; // plasma
        if (currentSection.jetMode == JET_MODE_ETCHING) {
          toolNumber = 2; // marker
        }
      }
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gFormat.format(41), dFormat.format(toolNumber));
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gFormat.format(42), dFormat.format(toolNumber));
        break;
      default:
        writeBlock(gFormat.format(40));
      }
    }
    writeBlock(gMotionModal.format(0), x, y, z);
    feedOutput.reset();
  }
}

function onLinear(_x, _y, _z, feed) {
  // at least one axis is required
  if (pendingRadiusCompensation >= 0) {
    // ensure that we end at desired position when compensation is turned off
    xOutput.reset();
    yOutput.reset();
  }
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  var f = feedOutput.format(feed);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      var toolNumber = tool.number;
      if (currentSection.type == TYPE_JET) {
        toolNumber = 1; // plasma
        if (currentSection.jetMode == JET_MODE_ETCHING) {
          toolNumber = 2; // marker
        }
      }
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gFormat.format(41), dFormat.format(toolNumber));
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gFormat.format(42), dFormat.format(toolNumber));
        break;
      default:
      }
    }
    writeBlock(gMotionModal.format(1), x, y, z, f);
  } else if (f) {
    if (getNextRecord().isMotion()) { // try not to output feed without motion
      feedOutput.reset(); // force feed on next line
    } else {
      writeBlock(gMotionModal.format(1), f);
    }
  }
}

function onRapid5D(_x, _y, _z, _a, _b, _c) {
  error(localize("The CNC does not support 5-axis simultaneous toolpath."));
}

function onLinear5D(_x, _y, _z, _a, _b, _c, feed) {
  error(localize("The CNC does not support 5-axis simultaneous toolpath."));
}

function onCircular(clockwise, cx, cy, cz, x, y, z, feed) {
  // one of X/Y and I/J are required and likewise
  
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation cannot be activated/deactivated for a circular move."));
    return;
  }

  var start = getCurrentPosition();

  if (isFullCircle()) {
    if (properties.useRadius || isHelical()) { // radius mode does not support full arcs
      linearize(tolerance);
      return;
    }
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(conditional(properties.useZ, gPlaneModal.format(17)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), feedOutput.format(feed));
      break;
    case PLANE_ZX:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(18)), gMotionModal.format(clockwise ? 2 : 3), zOutput.format(z), iOutput.format(cx - start.x, 0), kOutput.format(cz - start.z, 0), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    case PLANE_YZ:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(19)), gMotionModal.format(clockwise ? 2 : 3), yOutput.format(y), jOutput.format(cy - start.y, 0), kOutput.format(cz - start.z, 0), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    default:
      linearize(tolerance);
    }
  } else if (!properties.useRadius) {
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(conditional(properties.useZ, gPlaneModal.format(17)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), feedOutput.format(feed));
      break;
    case PLANE_ZX:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(18)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx - start.x, 0), kOutput.format(cz - start.z, 0), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    case PLANE_YZ:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(19)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), jOutput.format(cy - start.y, 0), kOutput.format(cz - start.z, 0), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    default:
      linearize(tolerance);
    }
  } else { // use radius mode
    var r = getCircularRadius();
    if (toDeg(getCircularSweep()) > 180) {
      r = -r; // allow up to <360 deg arcs
    }
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(conditional(properties.useZ, gPlaneModal.format(17)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), "R" + rFormat.format(r), feedOutput.format(feed));
      break;
    case PLANE_ZX:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(18)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), "R" + rFormat.format(r), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    case PLANE_YZ:
      if (properties.useZ) {
        writeBlock(conditional(properties.useZ, gPlaneModal.format(19)), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), "R" + rFormat.format(r), feedOutput.format(feed));
      } else {
        linearize(tolerance);
      }
      break;
    default:
      linearize(tolerance);
    }
  }
}

var mapCommand = {
  COMMAND_STOP:0,
  COMMAND_OPTIONAL_STOP:1,
  COMMAND_SPINDLE_CLOCKWISE:3,
  COMMAND_SPINDLE_COUNTERCLOCKWISE:4,
  COMMAND_STOP_SPINDLE:5,
  COMMAND_COOLANT_ON:8,
  COMMAND_COOLANT_OFF:9
};

function onCommand(command) {
  switch (command) {
  case COMMAND_START_SPINDLE:
    onCommand(tool.clockwise ? COMMAND_SPINDLE_CLOCKWISE : COMMAND_SPINDLE_COUNTERCLOCKWISE);
    return;
  case COMMAND_POWER_ON:
    return;
  case COMMAND_POWER_OFF:
    return;
  case COMMAND_LOCK_MULTI_AXIS:
    return;
  case COMMAND_UNLOCK_MULTI_AXIS:
    return;
  case COMMAND_BREAK_CONTROL:
    return;
  case COMMAND_TOOL_MEASURE:
    return;
  }

  var stringId = getCommandStringId(command);
  var mcode = mapCommand[stringId];
  if (mcode != undefined) {
    writeBlock(mFormat.format(mcode));
  } else {
    onUnsupportedCommand(command);
  }
}

function onSectionEnd() {
  writeBlock(conditional(properties.useZ, gPlaneModal.format(17)));
  forceAny();
}

function onClose() {
  if (properties.useZ || properties.useM30) {
    writeln("");
  }

  if (properties.useZ) {
    writeBlock(gFormat.format(28), gAbsIncModal.format(91), "Z" + xyzFormat.format(0)); // retract
    writeBlock(gAbsIncModal.format(90));
    zOutput.reset();
  }

  if (properties.useZ) {
    writeBlock(gFormat.format(28)); // move to reference point #1 - tool change position by default
  }

  if (properties.useM30) {
    writeBlock(mFormat.format(30));
  }
}

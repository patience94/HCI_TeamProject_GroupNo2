/**
  Copyright (C) 2012-2016 by Autodesk, Inc.
  All rights reserved.

  Burny Plasma post processor configuration.

  $Revision: 42473 905303e8374380273c82d214b32b7e80091ba92e $
  $Date: 2019-09-04 00:46:02 $
  
  FORKID {E49EFDF4-0C61-4E7B-A77A-686311BCCC19}
*/

description = "Burny Plasma (WADR)";
vendor = "Lincoln Electric";
vendorUrl = "http://www.burny.com";
legal = "Copyright (C) 2012-2016 by Autodesk, Inc.";
certificationLevel = 2;
minimumRevision = 39000;

longDescription = "Generic post for the Burny plasma cutters.";

extension = "cnc";
programNameIsInteger = true;
setCodePage("ascii");

capabilities = CAPABILITY_JET;
tolerance = spatial(0.002, MM);

minimumChordLength = spatial(0.25, MM);
minimumCircularRadius = spatial(0.01, MM);
maximumCircularRadius = spatial(4000, MM);
minimumCircularSweep = toRad(0.01);
maximumCircularSweep = toRad(360);
allowHelicalMoves = false;
allowedCircularPlanes = 1 << PLANE_XY; // only XY

// user-defined properties
properties = {
  writeMachine: true, // write machine
  showSequenceNumbers: true, // show sequence numbers
  sequenceNumberStart: 10, // first sequence number
  sequenceNumberIncrement: 1, // increment for sequence numbers
  separateWordsWithSpace: false, // specifies that the words should be separated with a white space
  useAbsoluteIJ: true, // IJ for G2/G3 is assumed to be absolute - make sure SD51-PRGM FORMAT is set accordingly
  useHeightSensor: false, // use height sensor M14/M15
  overlayTable: -1, // use 0-4 for G46
  useRepeat: false // use G97/G98 to repeat program
};

// user-defined property definitions
propertyDefinitions = {
  writeMachine: {title:"Write machine", description:"Output the machine settings in the header of the code.", group:0, type:"boolean"},
  showSequenceNumbers: {title:"Use sequence numbers", description:"Use sequence numbers for each block of outputted code.", group:1, type:"boolean"},
  sequenceNumberStart: {title:"Start sequence number", description:"The number at which to start the sequence numbers.", group:1, type:"integer"},
  sequenceNumberIncrement: {title:"Sequence number increment", description:"The amount by which the sequence number is incremented by in each block.", group:1, type:"integer"},
  separateWordsWithSpace: {title:"Separate words with space", description:"Adds spaces between words if 'yes' is selected.", type:"boolean"},
  useAbsoluteIJ: {title:"Absolute IJ", description:"IJ for G2/G3 is assumed to be absolute, ensure SD51-PRGM FORMAT is set accordingly.", type:"boolean"},
  useHeightSensor: {title:"Use height sensor", description:"Use height sensor M14/M15.", type:"boolean"},
  overlayTable: {title:"Overlay table", description:"Use 0-4 for G46.", type:"integer"},
  useRepeat: {title:"Use repeat", description:"Use G97/G98 to repeat the program.", type:"boolean"}
};

var gFormat = createFormat({prefix:"G", decimals:0, width:2, zeropad:true});
var mFormat = createFormat({prefix:"M", decimals:0, width:2, zeropad:true});

var xyzFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var feedFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var secFormat = createFormat({decimals:3, forceDecimal:true}); // seconds - range 0.001-1000

var xOutput = createVariable({prefix:"X"}, xyzFormat);
var yOutput = createVariable({prefix:"Y"}, xyzFormat);
var feedOutput = createVariable({prefix:"F"}, feedFormat);

// circular output
var iOutput;
var jOutput;

var gMotionModal = createModal({force:true}, gFormat); // modal group 1 // G2-G3 - linear moves do not use G-word
var gAbsIncModal = createModal({}, gFormat); // modal group 3 // G90-91
var gUnitModal = createModal({}, gFormat); // modal group 6 // G70-71

// collected state
var sequenceNumber;
var currentWorkOffset;

/**
  Writes the specified block.
*/
function writeBlock() {
  if (properties.showSequenceNumbers) {
    writeWords2("N" + sequenceNumber, arguments);
    sequenceNumber += properties.sequenceNumberIncrement;
  } else {
    writeWords(arguments);
  }
}

function formatComment(text) {
  return "(" + String(text).replace(/[()]/g, "") + ")";
}

/**
  Output a comment.
*/
function writeComment(text) {
  // not supported writeln(formatComment(text));
}

function onOpen() {

  // only one of I or J are required
  if (properties.useAbsoluteIJ) {
    iOutput = createVariable({prefix:"I", force:true}, xyzFormat);
    jOutput = createVariable({prefix:"J", force:true}, xyzFormat);
  } else {
    iOutput = createReferenceVariable({prefix:"I", force:true}, xyzFormat);
    jOutput = createReferenceVariable({prefix:"J", force:true}, xyzFormat);
  }

  if (!properties.separateWordsWithSpace) {
    setWordSeparator("");
  }

  sequenceNumber = properties.sequenceNumberStart;
  writeln("%"); // required

  if (programName) {
    var programNumber;
    try {
      programNumber = getAsInt(programName);
    } catch (e) {
      error(localize("Program name must be a number."));
      return;
    }
    if (!((programNumber >= 1) && (programNumber <= 99999999))) {
      error(localize("Program number is out of range."));
    }

    var oFormat = createFormat({width:8, zeropad:true, decimals:0});
    writeBlock("P" + oFormat.format(programNumber)); // max 8 digits
  }
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
    writeBlock(gUnitModal.format(70));
    break;
  case MM:
    writeBlock(gUnitModal.format(71));
    break;
  }

  // absolute coordinates
  writeBlock(gAbsIncModal.format(90));

  if (properties.overlayTable >= 0) {
    writeBlock(gFormat.format(46), "T" + properties.overlayTable); // select overlay
  }

  if (properties.useRepeat) {
    writeBlock(gFormat.format(97)); // restart here / add Txxxx for counter
  }

  if (properties.useHeightSensor) {
    writeBlock(mFormat.format(15)); // turn on height sensor
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

  switch (tool.type) {
  case TOOL_PLASMA_CUTTER:
    break;
  default:
    error(localize("The CNC does not support the required tool/process. Only plasma cutting is supported."));
    return;
  }

  switch (currentSection.jetMode) {
  case JET_MODE_THROUGH:
    break;
  case JET_MODE_ETCHING:
    error(localize("Etch cutting mode is not supported."));
    break;
  case JET_MODE_VAPORIZE:
    error(localize("Vaporize cutting mode is not supported."));
    break;
  default:
    error(localize("Unsupported cutting mode."));
    return;
  }

  { // pure 3D
    var remaining = currentSection.workPlane;
    if (!isSameDirection(remaining.forward, new Vector(0, 0, 1))) {
      error(localize("Tool orientation is not supported."));
      return;
    }
    setRotation(remaining);
  }

  forceAny();

  var initialPosition = getFramePosition(currentSection.getInitialPosition());
  gMotionModal.reset();
  writeBlock(
    gAbsIncModal.format(90),
    xOutput.format(initialPosition.x), yOutput.format(initialPosition.y)
  );
}

function onDwell(seconds) {
  if (seconds > 99999.999) {
    warning(localize("Dwelling time is out of range."));
  }
  seconds = clamp(0.001, seconds, 99999.999);
  writeBlock(gFormat.format(4), "F" + secFormat.format(seconds));
}

function onCycle() {
  error(localize("Canned cycles are not supported by CNC."));
}

function onCyclePoint(x, y, z) {
}

function onCycleEnd() {
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
          // onCommand(COMMAND_STOP);
        }
      }
    } else if (value == "cutting") {
      if (cuttingSequence == "piercing") {
        if (properties.allowHeadSwitches) {
          // Allow head to be switched here
          // onCommand(COMMAND_STOP);
        }
      }
    }
    cuttingSequence = value;
  }
}

function onPower(power) {
  writeBlock(mFormat.format(power ? 4 : 3)); // or M21/M20
}

function onRapid(_x, _y, _z) {
  // at least one axis is required
  if (pendingRadiusCompensation >= 0) {
    // ensure that we end at desired position when compensation is turned off
    xOutput.reset();
    yOutput.reset();
  }
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  if (x || y) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gFormat.format(41));
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gFormat.format(42));
        break;
      default:
        writeBlock(gFormat.format(40));
      }
    }
    writeBlock(x, y); // fast linear move
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
  var f = feedOutput.format(feed);
  if (x || y) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gFormat.format(41));
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gFormat.format(42));
        break;
      default:
        writeBlock(gFormat.format(40));
      }
    }
    writeBlock(x, y, f); // linear without G-word
  } else if (f) {
    if (getNextRecord().isMotion()) { // try not to output feed without motion
      feedOutput.reset(); // force feed on next line
    } else {
      writeBlock(f);
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
  
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation cannot be activated/deactivated for a circular move."));
    return;
  }

  var start = getCurrentPosition();

  if (isFullCircle()) {
    switch (getCircularPlane()) {
    case PLANE_XY:
      if (properties.useAbsoluteIJ) {
        writeBlock(gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), iOutput.format(cx), jOutput.format(cy));
      } else {
        writeBlock(gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), feedOutput.format(feed));
      }
      break;
    default:
      linearize(tolerance);
    }
  } else {
    switch (getCircularPlane()) {
    case PLANE_XY:
      if (properties.useAbsoluteIJ) {
        writeBlock(gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), iOutput.format(cx), jOutput.format(cy));
      } else {
        writeBlock(gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), feedOutput.format(feed));
      }
      break;
    default:
      linearize(tolerance);
    }
  }
}

var mapCommand = {
  COMMAND_STOP:0,
  COMMAND_OPTIONAL_STOP:1
};

function onCommand(command) {
  switch (command) {
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
  forceAny();
}

function onClose() {
  if (properties.useRepeat) {
    writeBlock(gFormat.format(98)); // restart from G97
  }
  
  var homeOffset = 1; // 1-4
  writeBlock(mFormat.format(79), "T" + homeOffset); // go home

  if (properties.useHeightSensor) {
    writeBlock(mFormat.format(14)); // turn off height sensor
  }

  writeBlock(mFormat.format(30)); // stop program - rewind
}

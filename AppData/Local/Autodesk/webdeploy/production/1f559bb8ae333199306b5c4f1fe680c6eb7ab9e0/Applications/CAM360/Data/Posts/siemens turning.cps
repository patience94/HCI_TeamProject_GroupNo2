/**
  Copyright (C) 2012-2018 by Autodesk, Inc.
  All rights reserved.

  Siemens Lathe post processor configuration.

  $Revision: 42631 621a6aaa12feb9f27eb24e2b06cf85758a41d354 $
  $Date: 2020-01-21 06:14:08 $
  
  FORKID {3505AD38-4010-4F6B-8F14-9CE36B9375F7}
*/

description = "Siemens Turning";
vendor = "Siemens";
vendorUrl = "http://www.siemens.com";
legal = "Copyright (C) 2012-2018 by Autodesk, Inc.";
certificationLevel = 2;
minimumRevision = 40783;

longDescription = "Generic lathe post for Siemens. Use Turret 0 for Positional Turret, Turret 101 for QCTP on X- Post, Turret 102 for QCTP on X+ Post, Turret 103 for Gang Tooling on X- Post, Turret 104 for Gang Tooling on X+ Tool Post.";

extension = "mpf";
setCodePage("ascii");

capabilities = CAPABILITY_TURNING;
tolerance = spatial(0.002, MM);

minimumChordLength = spatial(0.25, MM);
minimumCircularRadius = spatial(0.01, MM);
maximumCircularRadius = spatial(1000, MM);
minimumCircularSweep = toRad(0.01);
maximumCircularSweep = toRad(179);
allowHelicalMoves = true;
allowedCircularPlanes = undefined; // allow any circular motion

// user-defined properties
properties = {
  writeMachine: false, // write machine
  writeTools: false, // writes the tools
  /*preloadTool: false,*/ // preloads next tool on tool change if any
  showSequenceNumbers: true, // show sequence numbers
  sequenceNumberStart: 10, // first sequence number
  sequenceNumberIncrement: 1, // increment for sequence numbers
  optionalStop: true, // optional stop
  separateWordsWithSpace: true, // specifies that the words should be separated with a white space
  useRadius: false, // specifies that arcs should be output using the radius (R word) instead of the I, J, and K words.
  maximumSpindleSpeed: 100 * 60, // specifies the maximum spindle speed
  useParametricFeed: false, // specifies that feed should be output using R parameters
  showNotes: false, // specifies that operation notes should be output
  g53HomePositionX: 0, // home position for X-axis
  g53HomePositionZ: 0 // home position for Z-axis
};

// user-defined property definitions
propertyDefinitions = {
  writeMachine: {title:"Write machine", description:"Output the machine settings in the header of the code.", group:0, type:"boolean"},
  writeTools: {title:"Write tool list", description:"Output a tool list in the header of the code.", group:0, type:"boolean"},
  //preloadTool: {title:"Preload tool", description:"Preloads the next tool at a tool change (if any).", type:"boolean"},
  showSequenceNumbers: {title:"Use sequence numbers", description:"Use sequence numbers for each block of outputted code.", group:1, type:"boolean"},
  sequenceNumberStart: {title:"Start sequence number", description:"The number at which to start the sequence numbers.", group:1, type:"integer"},
  sequenceNumberIncrement: {title:"Sequence number increment", description:"The amount by which the sequence number is incremented by in each block.", group:1, type:"integer"},
  optionalStop: {title:"Optional stop", description:"Outputs optional stop code during when necessary in the code.", type:"boolean"},
  separateWordsWithSpace: {title:"Separate words with space", description:"Adds spaces between words if 'yes' is selected.", type:"boolean"},
  useRadius: {title:"Radius arcs", description:"If yes is selected, arcs are outputted using radius values rather than IJK.", type:"boolean"},
  maximumSpindleSpeed: {title:"Max spindle speed", description:"Defines the maximum spindle speed allowed by your machines.", type:"integer", range:[0, 999999999]},
  useParametricFeed:  {title:"Parametric feed", description:"Specifies the feed value that should be output using a Q value.", type:"boolean"},
  showNotes: {title:"Show notes", description:"Writes operation notes as comments in the outputted code.", type:"boolean"},
  g53HomePositionX: {title:"G53 home position X", description:"G53 X-axis home position.", type:"number"},
  g53HomePositionZ: {title:"G53 home position Z", description:"G53 Z-axis home position.", type:"number"}
};

var gFormat = createFormat({prefix:"G", decimals:1});
var mFormat = createFormat({prefix:"M", decimals:1});
var dFormat = createFormat({prefix:"D", decimals:0});

var spatialFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var xFormat = createFormat({decimals:(unit == MM ? 3 : 4), scale:2}); // diameter mode
var yFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var zFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var rFormat = createFormat({decimals:(unit == MM ? 3 : 4)}); // radius
var feedFormat = createFormat({decimals:(unit == MM ? 4 : 5)});
var pitchFormat = createFormat({decimals:(unit == MM ? 3 : 4)});
var toolFormat = createFormat({decimals:0});
var rpmFormat = createFormat({decimals:0});
var secFormat = createFormat({decimals:3}); // seconds - range 0.001-99999.999
var taperFormat = createFormat({decimals:1, scale:DEG});
var integerFormat = createFormat({decimals:0});

var xOutput = createVariable({prefix:"X"}, xFormat);
var yOutput = createVariable({prefix:"Y"}, yFormat);
var zOutput = createVariable({prefix:"Z"}, zFormat);
var feedOutput = createVariable({prefix:"F"}, feedFormat);
var pitchOutput = createVariable({prefix:"K", force:true}, pitchFormat);
var sOutput = createVariable({prefix:"S", force:true}, rpmFormat);

// circular output
var kOutput = createReferenceVariable({prefix:"K"}, spatialFormat);
var iOutput = createReferenceVariable({prefix:"I"}, spatialFormat); // no scaling

var gMotionModal = createModal({}, gFormat); // modal group 1 // G0-G3, ...
var gPlaneModal = createModal({onchange:function () {gMotionModal.reset();}}, gFormat); // modal group 2 // G17-19
var gAbsIncModal = createModal({}, gFormat); // modal group 3 // G90-91 // only for B and C mode
var gFeedModeModal = createModal({}, gFormat); // modal group 5 // G94-95
var gSpindleModeModal = createModal({}, gFormat); // modal group 5 // G96-97
var gUnitModal = createModal({}, gFormat); // modal group 6 // G70-71
var gCycleModal = createModal({}, gFormat); // modal group 9 // G81, ...
var gRetractModal = createModal({}, gFormat); // modal group 10 // G98-99

// fixed settings
var firstFeedParameter = 1;
var gotSecondarySpindle = false;
var gotDoorControl = false;
var gotTailStock = false;
var gotBarFeeder = false;

var WARNING_WORK_OFFSET = 0;

var QCTP = 0;
var TURRET = 1;
var GANG = 2;

var FRONT = -1;
var REAR = 1;

// collected state
var sequenceNumber;
var currentWorkOffset;
var optionalSection = false;
var forceSpindleSpeed = false;
var activeMovements; // do not use by default
var currentFeedId;
var toolingData;
var previousToolingData;

function getCode(code) {
  switch (code) {
  // case "PART_CATCHER_ON":
  // return mFormat.format(SPECIFY YOUR CODE HERE);
  // case "PART_CATCHER_OFF":
  // return mFormat.format(SPECIFY YOUR CODE HERE);
  // case "TAILSTOCK_ON":
  // return mFormat.format(SPECIFY YOUR CODE HERE);
  // case "TAILSTOCK_OFF":
  // return mFormat.format(SPECIFY YOUR CODE HERE);
  // case "ENGAGE_C_AXIS":
  // machineState.cAxisIsEngaged = true;
  // return cAxisEngageModal.format(UNSUPPORTED);
  // case "DISENGAGE_C_AXIS":
  // machineState.cAxisIsEngaged = false;
  // return cAxisEngageModal.format(UNSUPPORTED);
  // case "POLAR_INTERPOLATION_ON":
  // return gPolarModal.format(UNSUPPORTED);
  // case "POLAR_INTERPOLATION_OFF":
  // return gPolarModal.format(UNSUPPORTED);
  // case "STOP_LIVE_TOOL":
  // machineState.liveToolIsActive = false;
  // return mFormat.format(UNSUPPORTED);
  // case "STOP_MAIN_SPINDLE":
  // machineState.mainSpindleIsActive = false;
  // return mFormat.format(UNSUPPORTED);
  // case "STOP_SUB_SPINDLE":
  // machineState.subSpindleIsActive = false;
  // return mFormat.format(UNSUPPORTED);
  // case "START_LIVE_TOOL_CW":
  // machineState.liveToolIsActive = true;
  // return mFormat.format(UNSUPPORTED);
  // case "START_LIVE_TOOL_CCW":
  // machineState.liveToolIsActive = true;
  // return mFormat.format(UNSUPPORTED);
  case "START_MAIN_SPINDLE_CW":
    // machineState.mainSpindleIsActive = true;
    return mFormat.format(3);
  case "START_MAIN_SPINDLE_CCW":
    // machineState.mainSpindleIsActive = true;
    return mFormat.format(4);
  // case "START_SUB_SPINDLE_CW":
    // machineState.subSpindleIsActive = true;
    // return mFormat.format(UNSUPPORTED);
  // case "START_SUB_SPINDLE_CCW":
    // machineState.subSpindleIsActive = true;
    // return mFormat.format(UNSUPPORTED);
  // case "MAIN_SPINDLE_BRAKE_ON":
    // machineState.mainSpindleBrakeIsActive = true;
    // return cAxisBrakeModal.format(UNSUPPORTED);
  // case "MAIN_SPINDLE_BRAKE_OFF":
    // machineState.mainSpindleBrakeIsActive = false;
    // return cAxisBrakeModal.format(UNSUPPORTED);
  // case "SUB_SPINDLE_BRAKE_ON":
    // machineState.subSpindleBrakeIsActive = true;
    // return cAxisBrakeModal.format(UNSUPPORTED);
  // case "SUB_SPINDLE_BRAKE_OFF":
    // machineState.subSpindleBrakeIsActive = false;
    // return cAxisBrakeModal.format(UNSUPPORTED);
  case "FEED_MODE_UNIT_REV":
    return gFeedModeModal.format(95);
  case "FEED_MODE_UNIT_MIN":
    return gFeedModeModal.format(94);
  case "CONSTANT_SURFACE_SPEED_ON":
    return gSpindleModeModal.format(96);
  case "CONSTANT_SURFACE_SPEED_OFF":
    return gSpindleModeModal.format(97);
  // case "MAINSPINDLE_AIR_BLAST_ON":
    // return mFormat.format(UNSUPPORTED);
  // case "MAINSPINDLE_AIR_BLAST_OFF":
    // return mFormat.format(UNSUPPORTED);
  // case "SUBSPINDLE_AIR_BLAST_ON":
    // return mFormat.format(UNSUPPORTED);
  // case "SUBSPINDLE_AIR_BLAST_OFF":
    // return mFormat.format(UNSUPPORTED);
  // case "CLAMP_PRIMARY_CHUCK":
    // return mFormat.format(UNSUPPORTED);
  // case "UNCLAMP_PRIMARY_CHUCK":
    // return mFormat.format(UNSUPPORTED);
  // case "CLAMP_SECONDARY_CHUCK":
    // return mFormat.format(UNSUPPORTED);
  // case "UNCLAMP_SECONDARY_CHUCK":
    // return mFormat.format(UNSUPPORTED);
  // case "SPINDLE_SYNCHRONIZATION_ON":
    // machineState.spindleSynchronizationIsActive = true;
    // return gSynchronizedSpindleModal.format(UNSUPPORTED);
  // case "SPINDLE_SYNCHRONIZATION_OFF":
    // machineState.spindleSynchronizationIsActive = false;
    // return gSynchronizedSpindleModal.format(UNSUPPORTED);
  // case "START_CHIP_TRANSPORT":
    // return mFormat.format(UNSUPPORTED);
  // case "STOP_CHIP_TRANSPORT":
    // return mFormat.format(UNSUPPORTED);
  // case "OPEN_DOOR":
    // return mFormat.format(UNSUPPORTED);
  // case "CLOSE_DOOR":
    // return mFormat.format(UNSUPPORTED);
  case "COOLANT_FLOOD_ON":
    return mFormat.format(8);
  case "COOLANT_FLOOD_OFF":
    return mFormat.format(9);
  // case "COOLANT_AIR_ON":
    // return mFormat.format(UNSUPPORTED);
  // case "COOLANT_AIR_OFF":
    // return mFormat.format(UNSUPPORTED);
  // case "COOLANT_THROUGH_TOOL_ON":
    // return mFormat.format(UNSUPPORTED);
  // case "COOLANT_THROUGH_TOOL_OFF":
    // return mFormat.format(UNSUPPORTED);
  case "COOLANT_OFF":
    return mFormat.format(9);
  default:
    error(localize("Command " + code + " is not defined."));
    return 0;
  }
}

/**
  Writes the specified block.
*/
function writeBlock() {
  var text = formatWords(arguments);
  if (!text) {
    return;
  }
  if (properties.showSequenceNumbers) {
    if (optionalSection) {
      if (text) {
        writeWords("/", "N" + sequenceNumber, text);
      }
    } else {
      writeWords2("N" + sequenceNumber, arguments);
    }
    sequenceNumber += properties.sequenceNumberIncrement;
  } else {
    if (optionalSection) {
      writeWords2("/", arguments);
    } else {
      writeWords(arguments);
    }
  }
}

/**
  Writes the specified optional block.
*/
function writeOptionalBlock() {
  if (properties.showSequenceNumbers) {
    var words = formatWords(arguments);
    if (words) {
      writeWords("/", "N" + sequenceNumber, words);
      sequenceNumber += properties.sequenceNumberIncrement;
    }
  } else {
    writeWords2("/", arguments);
  }
}

function formatComment(text) {
  return "; " + String(text);
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

  yOutput.disable();
 
  if (!properties.separateWordsWithSpace) {
    setWordSeparator("");
  }

  sequenceNumber = properties.sequenceNumberStart;

  // if (!((programName.length >= 2) && (isAlpha(programName[0]) || (programName[0] == "_")) && isAlpha(programName[1]))) {
  //   error(localize("Program name must begin with 2 letters."));
  // }
  writeln("; %_N_" + translateText(String(programName).toUpperCase(), " ", "_") + "_MPF");
  
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

  if ((getNumberOfSections() > 0) && (getSection(0).workOffset == 0)) {
    for (var i = 0; i < getNumberOfSections(); ++i) {
      if (getSection(i).workOffset > 0) {
        error(localize("Using multiple work offsets is not possible if the initial work offset is 0."));
        return;
      }
    }
  }

  // dump tool information
  if (properties.writeTools) {
    var zRanges = {};
    if (is3D()) {
      var numberOfSections = getNumberOfSections();
      for (var i = 0; i < numberOfSections; ++i) {
        var section = getSection(i);
        var zRange = section.getGlobalZRange();
        var tool = section.getTool();
        if (zRanges[tool.number]) {
          zRanges[tool.number].expandToRange(zRange);
        } else {
          zRanges[tool.number] = zRange;
        }
      }
    }

    var tools = getToolTable();
    if (tools.getNumberOfTools() > 0) {
      for (var i = 0; i < tools.getNumberOfTools(); ++i) {
        var tool = tools.getTool(i);
        var comment = "T" + toolFormat.format(tool.number) + " " +
          (tool.diameter != 0 ? "D=" + spatialFormat.format(tool.diameter) + " " : "") +
          (tool.isTurningTool() ? localize("NR") + "=" + spatialFormat.format(tool.noseRadius) : localize("CR") + "=" + spatialFormat.format(tool.cornerRadius)) +
          (tool.taperAngle > 0 && (tool.taperAngle < Math.PI) ? " " + localize("TAPER") + "=" + taperFormat.format(tool.taperAngle) + localize("deg") : "") +
          (zRanges[tool.number] ? " - " + localize("ZMIN") + "=" + spatialFormat.format(zRanges[tool.number].getMinimum()) : "") +
          " - " + localize(getToolTypeName(tool.type));
        writeComment(comment);
      }
    }
  }

  // absolute coordinates and feed per min
  writeBlock(gAbsIncModal.format(90), getCode("FEED_MODE_UNIT_MIN"), gPlaneModal.format(18));

  switch (unit) {
  case IN:
    writeBlock(gUnitModal.format(70));
    break;
  case MM:
    writeBlock(gUnitModal.format(71));
    break;
  }

  if (properties.maximumSpindleSpeed > 0) {
    writeBlock("LIMS=" + rpmFormat.format(properties.maximumSpindleSpeed));
  }

  onCommand(COMMAND_START_CHIP_TRANSPORT);
}

function onComment(message) {
  writeComment(message);
}

/** Force output of X, Y, and Z. */
function forceXYZ() {
  xOutput.reset();
  yOutput.reset();
  zOutput.reset();
}

function forceFeed() {
  currentFeedId = undefined;
  feedOutput.reset();
}

/** Force output of X, Y, Z, and F on next output. */
function forceAny() {
  forceXYZ();
  forceFeed();
}

function FeedContext(id, description, feed) {
  this.id = id;
  this.description = description;
  this.feed = feed;
}

function getFeed(f) {
  if (activeMovements) {
    var feedContext = activeMovements[movement];
    if (feedContext != undefined) {
      if (!feedFormat.areDifferent(feedContext.feed, f)) {
        if (feedContext.id == currentFeedId) {
          return ""; // nothing has changed
        }
        forceFeed();
        currentFeedId = feedContext.id;
        return "F=R" + (firstFeedParameter + feedContext.id);
      }
    }
    currentFeedId = undefined; // force Q feed next time
  }
  return feedOutput.format(f); // use feed value
}

function initializeActiveFeeds() {
  activeMovements = new Array();
  var movements = currentSection.getMovements();
  var feedPerRev = currentSection.feedMode == FEED_PER_REVOLUTION;
  
  var id = 0;
  var activeFeeds = new Array();
  if (hasParameter("operation:tool_feedCutting")) {
    if (movements & ((1 << MOVEMENT_CUTTING) | (1 << MOVEMENT_LINK_TRANSITION) | (1 << MOVEMENT_EXTENDED))) {
      var feedContext = new FeedContext(id, localize("Cutting"), feedPerRev ? getParameter("operation:tool_feedCuttingRel") : getParameter("operation:tool_feedCutting"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_CUTTING] = feedContext;
      activeMovements[MOVEMENT_LINK_TRANSITION] = feedContext;
      activeMovements[MOVEMENT_EXTENDED] = feedContext;
    }
    ++id;
    if (movements & (1 << MOVEMENT_PREDRILL)) {
      feedContext = new FeedContext(id, localize("Predrilling"), feedPerRev ? getParameter("operation:tool_feedCuttingRel") : getParameter("operation:tool_feedCutting"));
      activeMovements[MOVEMENT_PREDRILL] = feedContext;
      activeFeeds.push(feedContext);
    }
    ++id;
  }
  
  if (hasParameter("operation:finishFeedrate")) {
    if (movements & (1 << MOVEMENT_FINISH_CUTTING)) {
      var finishFeedrateRel;
      if (hasParameter("operation:finishFeedrateRel")) {
        finishFeedrateRel = getParameter("operation:finishFeedrateRel");
      } else if (hasParameter("operation:finishFeedratePerRevolution")) {
        finishFeedrateRel = getParameter("operation:finishFeedratePerRevolution");
      }
      var feedContext = new FeedContext(id, localize("Finish"), feedPerRev ? finishFeedrateRel : getParameter("operation:finishFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_FINISH_CUTTING] = feedContext;
    }
    ++id;
  } else if (hasParameter("operation:tool_feedCutting")) {
    if (movements & (1 << MOVEMENT_FINISH_CUTTING)) {
      var feedContext = new FeedContext(id, localize("Finish"), feedPerRev ? getParameter("operation:tool_feedCuttingRel") : getParameter("operation:tool_feedCutting"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_FINISH_CUTTING] = feedContext;
    }
    ++id;
  }
  
  if (hasParameter("operation:tool_feedEntry")) {
    if (movements & (1 << MOVEMENT_LEAD_IN)) {
      var feedContext = new FeedContext(id, localize("Entry"), feedPerRev ? getParameter("operation:tool_feedEntryRel") : getParameter("operation:tool_feedEntry"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LEAD_IN] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:tool_feedExit")) {
    if (movements & (1 << MOVEMENT_LEAD_OUT)) {
      var feedContext = new FeedContext(id, localize("Exit"), feedPerRev ? getParameter("operation:tool_feedExitRel") : getParameter("operation:tool_feedExit"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LEAD_OUT] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:noEngagementFeedrate")) {
    if (movements & (1 << MOVEMENT_LINK_DIRECT)) {
      var feedContext = new FeedContext(id, localize("Direct"), feedPerRev ? getParameter("operation:noEngagementFeedrateRel") : getParameter("operation:noEngagementFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LINK_DIRECT] = feedContext;
    }
    ++id;
  } else if (hasParameter("operation:tool_feedCutting") &&
             hasParameter("operation:tool_feedEntry") &&
             hasParameter("operation:tool_feedExit")) {
    if (movements & (1 << MOVEMENT_LINK_DIRECT)) {
      var feedContext = new FeedContext(
        id,
        localize("Direct"),
        Math.max(
          feedPerRev ? getParameter("operation:tool_feedCuttingRel") : getParameter("operation:tool_feedCutting"),
          feedPerRev ? getParameter("operation:tool_feedEntryRel") : getParameter("operation:tool_feedEntry"),
          feedPerRev ? getParameter("operation:tool_feedExitRel") : getParameter("operation:tool_feedExit")
        )
      );
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LINK_DIRECT] = feedContext;
    }
    ++id;
  }
  
  if (hasParameter("operation:reducedFeedrate")) {
    if (movements & (1 << MOVEMENT_REDUCED)) {
      var feedContext = new FeedContext(id, localize("Reduced"), feedPerRev ? getParameter("operation:reducedFeedrateRel") : getParameter("operation:reducedFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_REDUCED] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:tool_feedRamp")) {
    if (movements & ((1 << MOVEMENT_RAMP) | (1 << MOVEMENT_RAMP_HELIX) | (1 << MOVEMENT_RAMP_PROFILE) | (1 << MOVEMENT_RAMP_ZIG_ZAG))) {
      var feedContext = new FeedContext(id, localize("Ramping"), feedPerRev ? getParameter("operation:tool_feedRampRel") : getParameter("operation:tool_feedRamp"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_RAMP] = feedContext;
      activeMovements[MOVEMENT_RAMP_HELIX] = feedContext;
      activeMovements[MOVEMENT_RAMP_PROFILE] = feedContext;
      activeMovements[MOVEMENT_RAMP_ZIG_ZAG] = feedContext;
    }
    ++id;
  }
  if (hasParameter("operation:tool_feedPlunge")) {
    if (movements & (1 << MOVEMENT_PLUNGE)) {
      var feedContext = new FeedContext(id, localize("Plunge"), feedPerRev ? getParameter("operation:tool_feedPlungeRel") : getParameter("operation:tool_feedPlunge"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_PLUNGE] = feedContext;
    }
    ++id;
  }
  if (true) { // high feed
    if (movements & (1 << MOVEMENT_HIGH_FEED)) {
      var feedContext = new FeedContext(id, localize("High Feed"), this.highFeedrate);
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_HIGH_FEED] = feedContext;
    }
    ++id;
  }
  
  for (var i = 0; i < activeFeeds.length; ++i) {
    var feedContext = activeFeeds[i];
    writeBlock("R" + (firstFeedParameter + feedContext.id) + "=" + feedFormat.format(feedContext.feed), formatComment(feedContext.description));
  }
}

function getSpindle() {
  if (getNumberOfSections() == 0) {
    return SPINDLE_PRIMARY;
  }
  if (getCurrentSectionId() < 0) {
    return getSection(getNumberOfSections() - 1).spindle == 0;
  }
  if (currentSection.getType() == TYPE_TURNING) {
    return currentSection.spindle;
  } else {
    if (isSameDirection(currentSection.workPlane.forward, new Vector(0, 0, 1))) {
      return SPINDLE_PRIMARY;
    } else if (isSameDirection(currentSection.workPlane.forward, new Vector(0, 0, -1))) {
      if (!gotSecondarySpindle) {
        error(localize("Secondary spindle is not available."));
      }
      return SPINDLE_SECONDARY;
    } else {
      return SPINDLE_PRIMARY;
    }
  }
}

function ToolingData(_tool) {
  switch (_tool.turret) {
  // Positional Turret
  case 0:
    this.tooling = TURRET;
    this.toolPost = REAR;
    break;
  // QCTP X-
  case 101:
    this.tooling = QCTP;
    this.toolPost = FRONT;
    break;
  // QCTP X+
  case 102:
    this.tooling = QCTP;
    this.toolPost = REAR;
    break;
  // Gang Tooling X-
  case 103:
    this.tooling = GANG;
    this.toolPost = FRONT;
    break;
  // Gang Tooling X+
  case 104:
    this.tooling = GANG;
    this.toolPost = REAR;
    break;
  default:
    error(localize("Turret number must be 0 (main turret), 101 (QCTP X-), 102 (QCTP X+, 103 (gang tooling X-), or 104 (gang tooling X+)."));
    break;
  }
  this.number = _tool.number;
  this.comment = _tool.comment;
  this.toolLength = _tool.bodyLength;
  // HSMWorks returns 0 in tool.bodyLength
  if ((tool.bodyLength == 0) && hasParameter("operation:tool_bodyLength")) {
    this.toolLength = getParameter("operation:tool_bodyLength");
  }
}

function onSection() {
  if (currentSection.getType() != TYPE_TURNING) {
    if (!hasParameter("operation-strategy") || (getParameter("operation-strategy") != "drill")) {
      if (currentSection.getType() == TYPE_MILLING) {
        error(localize("Milling toolpath is not supported."));
      } else {
        error(localize("Non-turning toolpath is not supported."));
      }
      return;
    }
  }

  var forceToolAndRetract = optionalSection && !currentSection.isOptional();
  optionalSection = currentSection.isOptional();

  var turning = (currentSection.getType() == TYPE_TURNING);
  
  var insertToolCall = forceToolAndRetract || isFirstSection() ||
    currentSection.getForceToolChange && currentSection.getForceToolChange() ||
    (tool.number != getPreviousSection().getTool().number) ||
    (tool.compensationOffset != getPreviousSection().getTool().compensationOffset) ||
    (tool.diameterOffset != getPreviousSection().getTool().diameterOffset) ||
    (tool.lengthOffset != getPreviousSection().getTool().lengthOffset);
  
  var retracted = false; // specifies that the tool has been retracted to the safe plane
  var newSpindle = isFirstSection() ||
    (getPreviousSection().spindle != currentSection.spindle);
  var newWorkOffset = isFirstSection() ||
    (getPreviousSection().workOffset != currentSection.workOffset); // work offset changes

  // determine which tooling holder is used
  if (!isFirstSection()) {
    previousToolingData = toolingData;
  }
  toolingData = new ToolingData(tool);
  toolingData.operationComment = "";
  if (hasParameter("operation-comment")) {
    toolingData.operationComment = getParameter("operation-comment");
  }
  toolingData.toolChange = insertToolCall;
  if (isFirstSection()) {
    previousToolingData = toolingData;
  }

  // turning using front tool post
  if (toolingData.toolPost == FRONT) {
    xFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true, scale:-2});
    xOutput = createVariable({prefix:"X"}, xFormat);
    iFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true, scale:-1}); // radius mode
    iOutput = createReferenceVariable({prefix:"I"}, iFormat);

  // turning using rear tool post
  } else {
    xFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true, scale:2});
    xOutput = createVariable({prefix:"X"}, xFormat);
    iFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true, scale:1}); // radius mode
    iOutput = createReferenceVariable({prefix:"I"}, iFormat);
  }

  if (insertToolCall || newSpindle || newWorkOffset) {
    // retract to safe plane
    retracted = true;
    if (!isFirstSection() && insertToolCall) {
      onCommand(COMMAND_COOLANT_OFF);
    }
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), "X" + xFormat.format(properties.g53HomePositionX)); // retract
    // writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), "Z" + zFormat.format(properties.g53HomePositionZ)); // retract, optional
    forceXYZ();
  }

  writeln("");

  if (hasParameter("operation-comment")) {
    var comment = getParameter("operation-comment");
    if (comment) {
      writeComment(comment);
    }
  }
  
  if (properties.showNotes && hasParameter("notes")) {
    var notes = getParameter("notes");
    if (notes) {
      var lines = String(notes).split("\n");
      var r1 = new RegExp("^[\\s]+", "g");
      var r2 = new RegExp("[\\s]+$", "g");
      for (line in lines) {
        var comment = lines[line].replace(r1, "").replace(r2, "");
        if (comment) {
          writeComment(comment);
        }
      }
    }
  }
  
  if (insertToolCall) {
    retracted = true;
  
    if (!isFirstSection() && properties.optionalStop) {
      onCommand(COMMAND_OPTIONAL_STOP);
    }

    if (tool.number > 99) {
      warning(localize("Tool number exceeds maximum value."));
    }

    if ((toolingData.tooling == QCTP) || tool.getManualToolChange()) {
      var comment = formatComment(localize("CHANGE TO T") + tool.number + " " + localize("ON") + " " +
        localize((toolingData.toolPost == REAR) ? "REAR TOOL POST" : "FRONT TOOL POST"));
      writeBlock(mFormat.format(0), comment);
    }

    var compensationOffset = 1; // optional, use tool.isTurningTool() ? tool.compensationOffset : tool.lengthOffset
    if (compensationOffset > 99) {
      error(localize("Compensation offset is out of range."));
      return;
    }
    writeBlock("T" + toolFormat.format(tool.number), dFormat.format(compensationOffset));
    if (tool.comment) {
      writeComment(tool.comment);
    }

    /*
    if (properties.preloadTool) {
      var nextTool = getNextTool(tool.number);
      if (nextTool) {
        var compensationOffset = nextTool.isTurningTool() ? nextTool.compensationOffset : nextTool.lengthOffset;
        if (compensationOffset > 99) {
          error(localize("Compensation offset is out of range."));
          return;
        }
        writeBlock("T" + toolFormat.format(nextTool.number * 100 + compensationOffset));
      } else {
        // preload first tool
        var section = getSection(0);
        var firstTool = section.getTool().number;
        if (tool.number != firstTool.number) {
          var compensationOffset = firstTool.isTurningTool() ? firstTool.compensationOffset : firstTool.lengthOffset;
          if (compensationOffset > 99) {
            error(localize("Compensation offset is out of range."));
            return;
          }
          writeBlock("T" + toolFormat.format(firstTool.number * 100 + compensationOffset));
        }
      }
    }
*/
  }

  // wcs
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
      error(localize("Work offset out of range."));
      return;
    } else {
      if (workOffset != currentWorkOffset) {
        writeBlock(gFormat.format(53 + workOffset)); // G54->G59
        currentWorkOffset = workOffset;
      }
    }
  }

  // set coolant after we have positioned at Z
  setCoolant(tool.coolant);

  forceAny();
  gMotionModal.reset();

  gFeedModeModal.reset();
  if (currentSection.feedMode == FEED_PER_REVOLUTION) {
    writeBlock(getCode("FEED_MODE_UNIT_REV"));
  } else {
    writeBlock(getCode("FEED_MODE_UNIT_MIN"));
  }

  if (gotTailStock) {
    writeBlock(getCode(currentSection.tailstock ? "TAILSTOCK_ON" : "TAILSTOCK_OFF"));
  }

  // writeBlock(mFormat.format(clampPrimaryChuck ? x : x));
  // writeBlock(mFormat.format(clampSecondaryChuck ? x : x));

  var initialPosition = getFramePosition(currentSection.getInitialPosition());
  startSpindle(false, true, initialPosition);
  
  setRotation(currentSection.workPlane);
  
  if (currentSection.partCatcher) {
    engagePartCatcher(true);
  }

  if (!retracted) {
    // TAG: need to retract along X or Z
    if (getCurrentPosition().z < initialPosition.z) {
      writeBlock(gMotionModal.format(0), zOutput.format(initialPosition.z));
    }
  }

  if (insertToolCall || tool.getSpindleMode() == SPINDLE_CONSTANT_SURFACE_SPEED) {
    gMotionModal.reset();
    
    writeBlock(
      gAbsIncModal.format(90),
      gMotionModal.format(0), xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z)
    );

    gMotionModal.reset();
  }

  // enable SFM spindle speed
  if (tool.getSpindleMode() == SPINDLE_CONSTANT_SURFACE_SPEED) {
    startSpindle(false, false);
  }

  if (properties.useParametricFeed &&
      hasParameter("operation-strategy") &&
      (getParameter("operation-strategy") != "drill") && // legacy
      !(currentSection.hasAnyCycle && currentSection.hasAnyCycle())) {
    if (!insertToolCall &&
        activeMovements &&
        (getCurrentSectionId() > 0) &&
        ((getPreviousSection().getPatternId() == currentSection.getPatternId()) && (currentSection.getPatternId() != 0))) {
      // use the current feeds
    } else {
      initializeActiveFeeds();
    }
  } else {
    activeMovements = undefined;
  }

  if (insertToolCall || retracted) {
    gPlaneModal.reset();
  }
}

function onDwell(seconds) {
  if (seconds > 99999.999) {
    warning(localize("Dwelling time is out of range."));
  }
  writeBlock(gFormat.format(4), "F" + secFormat.format(seconds));
}

var pendingRadiusCompensation = -1;

function onRadiusCompensation() {
  pendingRadiusCompensation = radiusCompensation;
}

var resetFeed = false;

function onRapid(_x, _y, _z) {
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gMotionModal.format(0), gFormat.format(41), x, y, z);
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gMotionModal.format(0), gFormat.format(42), x, y, z);
        break;
      default:
        writeBlock(gMotionModal.format(0), gFormat.format(40), x, y, z);
      }
    } else {
      writeBlock(gMotionModal.format(0), x, y, z);
    }
    forceFeed();
  }
}

function onLinear(_x, _y, _z, feed) {
  if (isSpeedFeedSynchronizationActive()) {
    resetFeed = true;
    var threadPitch = getParameter("operation:threadPitch");
    var threadsPerInch = 1.0 / threadPitch; // per mm for metric
    writeBlock(gMotionModal.format(33), xOutput.format(_x), yOutput.format(_y), zOutput.format(_z), pitchOutput.format(1 / threadsPerInch));
    return;
  }
  if (resetFeed) {
    resetFeed = false;
    forceFeed();
  }
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  var f = getFeed(feed);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      writeBlock(gPlaneModal.format(18));
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        writeBlock(gMotionModal.format(isSpeedFeedSynchronizationActive() ? 32 : 1), gFormat.format(41), x, y, z, f);
        break;
      case RADIUS_COMPENSATION_RIGHT:
        writeBlock(gMotionModal.format(isSpeedFeedSynchronizationActive() ? 32 : 1), gFormat.format(42), x, y, z, f);
        break;
      default:
        writeBlock(gMotionModal.format(isSpeedFeedSynchronizationActive() ? 32 : 1), gFormat.format(40), x, y, z, f);
      }
    } else {
      writeBlock(gMotionModal.format(isSpeedFeedSynchronizationActive() ? 32 : 1), x, y, z, f);
    }
  } else if (f) {
    if (getNextRecord().isMotion()) { // try not to output feed without motion
      forceFeed(); // force feed on next line
    } else {
      writeBlock(gMotionModal.format(isSpeedFeedSynchronizationActive() ? 32 : 1), f);
    }
  }
}

function onCircular(clockwise, cx, cy, cz, x, y, z, feed) {
  if (isSpeedFeedSynchronizationActive()) {
    error(localize("Speed-feed synchronization is not supported for circular moves."));
    return;
  }
  
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation cannot be activated/deactivated for a circular move."));
    return;
  }

  var start = getCurrentPosition();
  var directionCode = (toolingData.toolPost == REAR) ? (clockwise ? 2 : 3) : (clockwise ? 3 : 2);

  if (isFullCircle()) {
    if (properties.useRadius || isHelical()) { // radius mode does not support full arcs
      linearize(tolerance);
      return;
    }
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(directionCode), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), getFeed(feed));
      break;
    case PLANE_ZX:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(directionCode), iOutput.format(cx - start.x, 0), kOutput.format(cz - start.z, 0), getFeed(feed));
      break;
    case PLANE_YZ:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(directionCode), jOutput.format(cy - start.y, 0), kOutput.format(cz - start.z, 0), getFeed(feed));
      break;
    default:
      linearize(tolerance);
    }
  } else if (!properties.useRadius) {
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx - start.x, 0), jOutput.format(cy - start.y, 0), getFeed(feed));
      break;
    case PLANE_ZX:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx - start.x, 0), kOutput.format(cz - start.z, 0), getFeed(feed));
      break;
    case PLANE_YZ:
      writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), jOutput.format(cy - start.y, 0), kOutput.format(cz - start.z, 0), getFeed(feed));
      break;
    default:
      linearize(tolerance);
    }
  } else { // use radius mode
    var r = getCircularRadius();
    if (toDeg(getCircularSweep()) > (180 + 1e-9)) {
      r = -r; // allow up to <360 deg arcs
    }
    switch (getCircularPlane()) {
    case PLANE_XY:
      writeBlock(gPlaneModal.format(17), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), "CR=" + rFormat.format(r), getFeed(feed));
      break;
    case PLANE_ZX:
      writeBlock(gPlaneModal.format(18), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), "CR=" + rFormat.format(r), getFeed(feed));
      break;
    case PLANE_YZ:
      writeBlock(gPlaneModal.format(19), gMotionModal.format(directionCode), xOutput.format(x), yOutput.format(y), zOutput.format(z), "CR=" + rFormat.format(r), getFeed(feed));
      break;
    default:
      linearize(tolerance);
    }
  }
}

var expandCurrentCycle = false;

function onCycle() {
  
  expandCurrentCycle = false;

  if ((cycleType != "tapping") &&
      (cycleType != "right-tapping") &&
      (cycleType != "left-tapping") &&
      (cycleType != "turning-canned-rough")) {
    writeBlock(feedOutput.format(cycle.feedrate));
  }

  var RTP = cycle.clearance; // return plane (absolute)
  var RFP = cycle.stock; // reference plane (absolute)
  var SDIS = cycle.retract - cycle.stock; // safety distance
  var DP = cycle.bottom; // depth (absolute)
  // var DPR = RFP - cycle.bottom; // depth (relative to reference plane)
  var DTB = cycle.dwell;
  var SDIR = tool.clockwise ? 3 : 4; // direction of rotation: M3:3 and M4:4

  switch (cycleType) {
  case "drilling":
    writeBlock(
      "CYCLE81(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ + ")"
    );
    break;
  case "counter-boring":
    writeBlock(
      "CYCLE82(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + conditional(DTB > 0, secFormat.format(DTB)) + ")"
    );
    break;
  case "chip-breaking":
    if (cycle.accumulatedDepth < cycle.depth) {
      expandCurrentCycle = true;
    } else {
      var FDEP = cycle.stock - cycle.incrementalDepth;
      var FDPR = cycle.incrementalDepth; // relative to reference plane (unsigned)
      var DAM = 0; // degression (unsigned)
      var DTS = 0; // dwell time at start
      var FRF = 1; // feedrate factor (unsigned)
      var VARI = 0; // chip breaking
      var _AXN = 3; // tool axis
      var _MDEP = cycle.incrementalDepth; // minimum drilling depth
      var _VRT = 0; // retraction distance
      var _DTD = (cycle.dwell != undefined) ? cycle.dwell : 0;
      var _DIS1 = 0; // limit distance

      writeBlock(
        "CYCLE83(" + zFormat.format(RTP) +
        ", " + zFormat.format(RFP) +
        ", " + zFormat.format(SDIS) +
        ", " + zFormat.format(DP) +
        ", " /*+ zFormat.format(DPR)*/ +
        ", " + zFormat.format(FDEP) +
        ", " /*+ zFormat.format(FDPR)*/ +
        ", " + zFormat.format(DAM) +
        ", " + /*conditional(DTB > 0, secFormat.format(DTB))*/ // only dwell at bottom
        ", " + conditional(DTS > 0, secFormat.format(DTS)) +
        ", " + zFormat.format(FRF) +
        ", " + zFormat.format(VARI) +
        ", " + /*_AXN +*/
        ", " + zFormat.format(_MDEP) +
        ", " + zFormat.format(_VRT) +
        ", " + secFormat.format(_DTD) +
        ", 0" + /*zFormat.format(_DIS1) +*/
        ")"
      );
    }
    break;
  case "deep-drilling":
    var FDEP = cycle.stock - cycle.incrementalDepth;
    var FDPR = cycle.incrementalDepth; // relative to reference plane (unsigned)
    var DAM = 0; // degression (unsigned)
    var DTS = 0; // dwell time at start
    var FRF = 1; // feedrate factor (unsigned)
    var VARI = 1; // full retract
    var _MDEP = cycle.incrementalDepth; // minimum drilling depth
    var _VRT = 0; // retraction distance
    var _DTD = (cycle.dwell != undefined) ? cycle.dwell : 0;
    var _DIS1 = 0; // limit distance

    writeBlock(
      "CYCLE83(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + zFormat.format(FDEP) +
      ", " /*+ zFormat.format(FDPR)*/ +
      ", " + zFormat.format(DAM) +
      ", " + /*conditional(DTB > 0, secFormat.format(DTB)) +*/ // only dwell at bottom
      ", " + conditional(DTS > 0, secFormat.format(DTS)) +
      ", " + zFormat.format(FRF) +
      ", " + zFormat.format(VARI) +
      ", " + /*_AXN +*/
      ", " + zFormat.format(_MDEP) +
      ", " + zFormat.format(_VRT) +
      ", " + secFormat.format(_DTD) +
      ", 0" + /*zFormat.format(_DIS1) +*/
      ")"
    );
    break;
  case "tapping":
  case "left-tapping":
  case "right-tapping":
    var SDAC = SDIR; // direction of rotation after end of cycle
    var MPIT = 0; // thread pitch as thread size
    var PIT = ((tool.type == TOOL_TAP_LEFT_HAND) ? -1 : 1) * tool.threadPitch; // thread pitch
    var POSS = 0; // spindle position for oriented spindle stop in cycle (in degrees)
    var SST = spindleSpeed; // speed for tapping
    var SST1 = spindleSpeed; // speed for return
    writeBlock(
      "CYCLE84(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + conditional(DTB > 0, secFormat.format(DTB)) +
      ", " + zFormat.format(SDAC) +
      ", " /*+ zFormat.format(MPIT)*/ +
      ", " + zFormat.format(PIT) +
      ", " + zFormat.format(POSS) +
      ", " + zFormat.format(SST) +
      ", " + zFormat.format(SST1) + ")"
    );
    break;
  case "reaming":
    var FFR = cycle.feedrate;
    var RFF = cycle.retractFeedrate;
    writeBlock(
      "CYCLE85(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + conditional(DTB > 0, secFormat.format(DTB)) +
      ", " + zFormat.format(FFR) +
      ", " + zFormat.format(RFF) + ")"
    );
    break;
  case "stop-boring":
    if (cycle.dwell > 0) {
      expandCurrentCycle = true;
    } else {
      writeBlock(
        "CYCLE87(" + zFormat.format(RTP) +
        ", " + zFormat.format(RFP) +
        ", " + zFormat.format(SDIS) +
        ", " + zFormat.format(DP) +
        ", " /*+ zFormat.format(DPR)*/ +
        ", " + SDIR + ")"
      );
    }
    break;
  case "fine-boring":
    var RPA = 0; // return path in abscissa of the active plane (enter incrementally with)
    var RPO = 0; // return path in the ordinate of the active plane (enter incrementally sign)
    var RPAP = 0; // return plane in the applicate (enter incrementally with sign)
    var POSS = 0; // spindle position for oriented spindle stop in cycle (in degrees)
    writeBlock(
      "CYCLE86(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + conditional(DTB > 0, secFormat.format(DTB)) +
      ", " + SDIR +
      ", " + zFormat.format(RPA) +
      ", " + zFormat.format(RPO) +
      ", " + zFormat.format(RPAP) +
      ", " + zFormat.format(POSS) + ")"
    );
    break;
  case "boring":
    // retract feed is ignored
    writeBlock(
      "CYCLE89(" + zFormat.format(RTP) +
      ", " + zFormat.format(RFP) +
      ", " + zFormat.format(SDIS) +
      ", " + zFormat.format(DP) +
      ", " /*+ zFormat.format(DPR)*/ +
      ", " + conditional(DTB > 0, secFormat.format(DTB)) + ")"
    );
    break;
  default:
    expandCurrentCycle = true;
  }
  if (!expandCurrentCycle) {
    xOutput.reset();
    yOutput.reset();
  }
}

function onCyclePoint(x, y, z) {
  if (!expandCurrentCycle) {
    var _x = xOutput.format(x);
    var _y = yOutput.format(y);
    /*zOutput.format(z)*/
    if (_x || _y) {
      writeBlock(_x, _y);
    }
  } else {
    expandCyclePoint(x, y, z);
  }
}

function onCycleEnd() {
  if (!expandCurrentCycle) {
    // end modal cycle
  }
  zOutput.reset();
}

var saveShowSequenceNumbers = true;
var xyzFormat = createFormat({decimals:(unit == MM ? 4 : 5), forceDecimal:true});
var pathBlockNumber = {start: 0, end: 0};

function onCyclePath() {
  saveShowSequenceNumbers = properties.showSequenceNumbers;

  // buffer all paths and stop feeds being output
  feedOutput.disable();
  properties.showSequenceNumbers = false;
  redirectToBuffer();
  //Adding indice in cases of multiple canned cycles calls
  writeBlock("START" + integerFormat.format(currentSection.getId()) + ":");
  gMotionModal.reset();
  forceXYZ();
}

function onCyclePathEnd() {
  writeBlock("END" + integerFormat.format(currentSection.getId()) + ":");
  properties.showSequenceNumbers = saveShowSequenceNumbers; // reset property to initial state
  feedOutput.enable();
  var cyclePath = String(getRedirectionBuffer()).split(EOL); // get cycle path from buffer
  closeRedirection();
  for (line in cyclePath) { // remove empty elements
    if (cyclePath[line] == "") {
      cyclePath.splice(line);
    }
  }

  var outsideProfiling = cycle.turningMode == 0;
  var verticalPasses;
  if (cycle.profileRoughingCycle == 0) {
    verticalPasses = false;
  } else if (cycle.profileRoughingCycle == 1) {
    verticalPasses = true;
  } else {
    error(localize("Unsupported passes type."));
    return;
  }

  // output cycle data
  switch (cycleType) {
  case "turning-canned-rough":
    var NPP = "\"" + "START" + integerFormat.format(currentSection.getId()) + ":END" + integerFormat.format(currentSection.getId()) + "\""; // Name of contour subroutine
    var MID = xyzFormat.format(cycle.depthOfCut); // Infeed depth (enter without sign)
    //Siemens doesn't use sign for allowance
    var FALZ = Math.abs(xyzFormat.format(cycle.zStockToLeave)); // Finishing allowance in the longitudinal axis (enter without sign)
    var FALX = Math.abs(xFormat.format(cycle.xStockToLeave)); // Finishing allowance in the transverse axis (enter without sign)
    var FAL = 0; // Finishing allowance suitable for contour (enter without sign)
    var FF1 = feedFormat.format(cycle.cutfeedrate); // Feedrate for roughing without relief cut
    var FF2 = feedFormat.format(cycle.cutfeedrate); //Feedrate for plunging into relief cut element
    var FF3 = feedFormat.format(cycle.cutfeedrate); // Feedrate for finishing cut
    var VARI = outsideProfiling ? (verticalPasses ? 2 : 1) : (verticalPasses ? 4 : 3); // Machining typeRange of values: 1 ... 12
    var DT = 0; // Dwell time fore chip breaking when roughing
    var DAM = 0; // Path length after which each roughing step is interrupted for chip breaking
    var _VRT = xyzFormat.format(cycle.retractLength); // Lift-off distance from contour when roughing, incremental (to be entered without sign)

    writeBlock(
      "CYCLE95(" + NPP + ", " + MID + ", " + FALZ + ", " + FALX + ", " + FAL + ", " + FF1 + ", " + FF2 +
        ", " + FF3 + ", " + VARI + ", " + DT + ", " + DAM + ", " + _VRT + ")"
    );
    break;
  default:
    error(localize("Unsupported turning canned cycle."));
  }
  
  for (var i = 0; i < cyclePath.length; ++i) {
    /*
    if (i == 0 || i == (cyclePath.length - 1)) { // write sequence number on first and last line of the cycle path
      properties.showSequenceNumbers = true;
      if ((i == 0 && pathBlockNumber.start != sequenceNumber) || (i == (cyclePath.length - 1) && pathBlockNumber.end != sequenceNumber)) {
        error(localize("Mismatch of start/end block number in turning canned cycle."));
        return;
      }
    }
    */
    writeBlock(cyclePath[i]); // output cycle path
    properties.showSequenceNumbers = saveShowSequenceNumbers; // reset property to initial state
  }
}

var currentCoolantMode = COOLANT_OFF;

function setCoolant(coolant) {
  if (coolant == currentCoolantMode) {
    return; // coolant is already active
  }

  var m = undefined;
  if (coolant == COOLANT_OFF) {
    writeBlock(getCode("COOLANT_OFF"));
    currentCoolantMode = COOLANT_OFF;
    return;
  }

  switch (coolant) {
  case COOLANT_FLOOD:
    m = getCode("COOLANT_FLOOD_ON");
    break;
  default:
    onUnsupportedCoolant(coolant);
    m = getCode("COOLANT_OFF");
  }
  
  if (m) {
    writeBlock(m);
    currentCoolantMode = coolant;
  }
}

function onSpindleSpeed(spindleSpeed) {
  if (rpmFormat.areDifferent(spindleSpeed, sOutput.getCurrent())) {
    startSpindle(false, false, getFramePosition(currentSection.getInitialPosition()), spindleSpeed);
  }
}

function startSpindle(tappingMode, forceRPMMode, initialPosition, rpm) {
  var spindleDir;
  var spindleMode;
  var _spindleSpeed = spindleSpeed;
  if (rpm !== undefined) {
    _spindleSpeed = rpm;
  }
  var maxSpeed = "";
  gSpindleModeModal.reset();
  
  if ((getSpindle() == SPINDLE_SECONDARY) && !gotSecondarySpindle) {
    error(localize("Secondary spindle is not available."));
    return;
  }
 
  if (false /*tappingMode*/) {
    spindleDir = getCode("RIGID_TAPPING");
  } else {
    if (getSpindle() == SPINDLE_SECONDARY) {
      spindleDir = tool.clockwise ? getCode("START_SUB_SPINDLE_CW") : getCode("START_SUB_SPINDLE_CCW");
    } else {
      spindleDir = tool.clockwise ? getCode("START_MAIN_SPINDLE_CW") : getCode("START_MAIN_SPINDLE_CCW");
    }
  }

  var maximumSpindleSpeed = (tool.maximumSpindleSpeed > 0) ? Math.min(tool.maximumSpindleSpeed, properties.maximumSpindleSpeed) : properties.maximumSpindleSpeed;
  if (tool.getSpindleMode() == SPINDLE_CONSTANT_SURFACE_SPEED) {
    _spindleSpeed = tool.surfaceSpeed * ((unit == MM) ? 1 / 1000.0 : 1 / 12.0);
    if (forceRPMMode) { // RPM mode is forced until move to initial position
      if (xFormat.getResultingValue(initialPosition.x) == 0) {
        _spindleSpeed = maximumSpindleSpeed;
      } else {
        _spindleSpeed = Math.min((_spindleSpeed * ((unit == MM) ? 1000.0 : 12.0) / (Math.PI * Math.abs(initialPosition.x * 2))), maximumSpindleSpeed);
      }
      spindleMode = getCode("CONSTANT_SURFACE_SPEED_OFF");
    } else {
      spindleMode = getCode("CONSTANT_SURFACE_SPEED_ON");
    }
  } else {
    spindleMode = getCode("CONSTANT_SURFACE_SPEED_OFF");
  }
  if (getSpindle(true) == SPINDLE_SECONDARY) {
    writeBlock(
      spindleMode,
      sOutput.format(_spindleSpeed),
      spindleDir
    );
  } else {
    writeBlock(
      spindleMode,
      sOutput.format(_spindleSpeed),
      spindleDir
    );
  }

  if (currentSection.getTool().getSpindleMode() == SPINDLE_CONSTANT_SURFACE_SPEED && !forceRPMMode) {
    if (maximumSpindleSpeed > 0) {
      writeBlock("LIMS=" + rpmFormat.format(maximumSpindleSpeed));
    }
  }
  // wait for spindle here if required
}

function onCommand(command) {
  switch (command) {
  case COMMAND_COOLANT_OFF:
    setCoolant(COOLANT_OFF);
    return;
  case COMMAND_COOLANT_ON:
    setCoolant(COOLANT_FLOOD);
    return;
  case COMMAND_LOCK_MULTI_AXIS:
    return;
  case COMMAND_UNLOCK_MULTI_AXIS:
    return;
  case COMMAND_START_CHIP_TRANSPORT:
    return;
  case COMMAND_STOP_CHIP_TRANSPORT:
    return;
  case COMMAND_BREAK_CONTROL:
    return;
  case COMMAND_TOOL_MEASURE:
    return;
  case COMMAND_ACTIVATE_SPEED_FEED_SYNCHRONIZATION:
    return;
  case COMMAND_DEACTIVATE_SPEED_FEED_SYNCHRONIZATION:
    return;

  case COMMAND_STOP:
    writeBlock(mFormat.format(0));
    forceSpindleSpeed = true;
    return;
  case COMMAND_OPTIONAL_STOP:
    writeBlock(mFormat.format(1));
    break;
  case COMMAND_END:
    writeBlock(mFormat.format(2));
    break;
  case COMMAND_SPINDLE_CLOCKWISE:
    switch (currentSection.spindle) {
    case SPINDLE_PRIMARY:
      writeBlock(mFormat.format(3));
      break;
    case SPINDLE_SECONDARY:
      break;
    }
    // writeBlock("M2=3"); // live spindle
    break;
  case COMMAND_SPINDLE_COUNTERCLOCKWISE:
    switch (currentSection.spindle) {
    case SPINDLE_PRIMARY:
      writeBlock(mFormat.format(4));
      break;
    case SPINDLE_SECONDARY:
      break;
    }
    // writeBlock("M2=4"); // live spindle
    break;
  case COMMAND_START_SPINDLE:
    onCommand(tool.clockwise ? COMMAND_SPINDLE_CLOCKWISE : COMMAND_SPINDLE_COUNTERCLOCKWISE);
    return;
  case COMMAND_STOP_SPINDLE:
    switch (currentSection.spindle) {
    case SPINDLE_PRIMARY:
      writeBlock(mFormat.format(5));
      break;
    case SPINDLE_SECONDARY:
      break;
    }
    // writeBlock("M2=5"); // live spindle
    break;
  //case COMMAND_ORIENTATE_SPINDLE:
  //case COMMAND_CLAMP: // TAG: add support for clamping
  //case COMMAND_UNCLAMP: // TAG: add support for clamping
  default:
    onUnsupportedCommand(command);
  }
}

function engagePartCatcher(engage) {
  if (engage) {
    // catch part here
    writeBlock(getCode("PART_CATCHER_ON"), formatComment(localize("PART CATCHER ON")));
  } else {
    onCommand(COMMAND_COOLANT_OFF);
    writeBlock(gFormat.format(53), gMotionModal.format(0), "X" + xFormat.format(properties.g53HomePositionX)); // retract
    writeBlock(gFormat.format(53), gMotionModal.format(0), "Z" + zFormat.format(properties.g53HomePositionZ)); // retract
    writeBlock(getCode("PART_CATCHER_OFF"), formatComment(localize("PART CATCHER OFF")));
    forceXYZ();
  }
}

function onSectionEnd() {

  // cancel SFM mode to preserve spindle speed
  if (tool.getSpindleMode() == SPINDLE_CONSTANT_SURFACE_SPEED) {
    startSpindle(false, true, getFramePosition(currentSection.getFinalPosition()));
  }

  if (currentSection.partCatcher) {
    engagePartCatcher(false);
  }

  forceAny();
}

function onClose() {
  writeln("");

  optionalSection = false;

  onCommand(COMMAND_COOLANT_OFF);

  // we might want to retract in Z before X
  // writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), "X" + xFormat.format(0)); // retract

  forceXYZ();
  if (!machineConfiguration.hasHomePositionX() && !machineConfiguration.hasHomePositionY()) {
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), "X" + xFormat.format(properties.g53HomePositionX), conditional(yOutput.isEnabled(), "Y" + yFormat.format(0))); // return to home
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), "Z" + zFormat.format(properties.g53HomePositionZ)); // return to home
  } else {
    var homeX;
    if (machineConfiguration.hasHomePositionX()) {
      homeX = xOutput.format(machineConfiguration.getHomePositionX());
    }
    var homeY;
    if (yOutput.isEnabled() && machineConfiguration.hasHomePositionY()) {
      homeY = yOutput.format(machineConfiguration.getHomePositionY());
    }
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), homeX, homeY, zOutput.format(machineConfiguration.getRetractPlane()));
  }

  onImpliedCommand(COMMAND_END);
  onImpliedCommand(COMMAND_STOP_SPINDLE);
  writeBlock(mFormat.format(30)); // stop program, spindle stop, coolant off
}

/**
  Copyright (C) 2012-2018 by Autodesk, Inc.
  All rights reserved.

  HURCO post processor configuration.

  $Revision: 42602 ab32647ea0af02682e27dce3d6352deb199564d5 $
  $Date: 2019-12-04 06:18:00 $
  
  FORKID {1B14E478-26FE-4db2-A3E7-FB814E8C0B4E}
*/

description = "HURCO";
vendor = "HURCO";
vendorUrl = "http://www.hurco.com";
legal = "Copyright (C) 2012-2017 by Autodesk, Inc.";
certificationLevel = 2;
minimumRevision = 40783;

longDescription = "Generic post for HURCO. Note that this post supports both ISNC (ISO NC mode) and BNC (Basic NC mode). By default ISNC mode is used but you can switch to BNC mode by disabling the 'isnc' property. Also note that you can turn on 3D arcs by enabling the 'allow3DArcs' property so you will get arcs in any plane instead of only in the primary planes G17/G18/G19. Note that the HURCO CNC cannot guarantee that no gouging will happen at rewinds when using vector output for multi-axis simultaneous machining as vector does not provide enough information. You need to define the machine in the post to be safe.";

extension = "hnc";
programNameIsInteger = true;
setCodePage("ascii");

capabilities = CAPABILITY_MILLING;
tolerance = spatial(0.002, MM);

minimumChordLength = spatial(0.25, MM);
minimumCircularRadius = spatial(0.01, MM);
maximumCircularRadius = spatial(1000, MM);
minimumCircularSweep = toRad(0.01);
maximumCircularSweep = toRad(180);
allowHelicalMoves = true;
allowedCircularPlanes = undefined; // allow any circular motion
highFeedrate = (unit == IN) ? 100 : 5000;

// user-defined properties
properties = {
  writeMachine: true, // write machine
  writeTools: true, // writes the tools
  preloadTool: true, // preloads next tool on tool change if any
  showSequenceNumbers: true, // show sequence numbers
  sequenceNumberStart: 1, // first sequence number
  sequenceNumberIncrement: 1, // increment for sequence numbers
  optionalStop: true, // optional stop
  isnc: true, // specifies the mode ISNC (ISO NC mode) or BNC (Basic NC mode)
  separateWordsWithSpace: true, // specifies that the words should be separated with a white space
  allow3DArcs: false, // specifies that 3D circular moves are allowed
  useParametricFeed: false, // specifies that feed should be output using Q values
  showNotes: false, // specifies that operation notes should be output.
  preferPositiveTilt: false, // prefer positive/negative tilt
  safeToolChangePositionX: false, // safe tool change position in X
  safeToolChangePositionY: false, // safe tool change position in Y
  machineAxisABC: "ABC" // specify your machine axes here for use with vectors output only.
};

// user-defined property definitions
propertyDefinitions = {
  writeMachine: {title:"Write machine", description:"Output the machine settings in the header of the code.", group:0, type:"boolean"},
  writeTools: {title:"Write tool list", description:"Output a tool list in the header of the code.", group:0, type:"boolean"},
  preloadTool: {title:"Preload tool", description:"Preloads the next tool at a tool change (if any).", type:"boolean"},
  showSequenceNumbers: {title:"Use sequence numbers", description:"Use sequence numbers for each block of outputted code.", group:1, type:"boolean"},
  sequenceNumberStart: {title:"Start sequence number", description:"The number at which to start the sequence numbers.", group:1, type:"integer"},
  sequenceNumberIncrement: {title:"Sequence number increment", description:"The amount by which the sequence number is incremented by in each block.", group:1, type:"integer"},
  optionalStop: {title:"Optional stop", description:"Outputs optional stop code during when necessary in the code.", type:"boolean"},
  isnc:{title: "Use ISNC or BNC mode", description: "Selects between ISNC (ISO NC mode) and BNC (Basic NC mode).", type: "boolean", values: ["Basic NC mode", "ISO NC mode"]},
  separateWordsWithSpace: {title:"Separate words with space", description:"Adds spaces between words if 'yes' is selected.", type:"boolean"},
  allow3DArcs: {title:"Allow 3D arcs", description:"Specifies whether 3D circular arcs are allowed.", type:"boolean"},
  useParametricFeed:  {title:"Parametric feed", description:"Specifies the feed value that should be output using a Q value.", type:"boolean"},
  showNotes: {title:"Show notes", description:"Writes operation notes as comments in the outputted code.", type:"boolean"},
  preferPositiveTilt: {title:"Prefer positive tilt", description:"Specifies whether to prefer positive or negative tilt angles.", type:"boolean"},
  safeToolChangePositionX: {title:"Safe tool change position X", description:"Specify whether to use a safe tool change position in the X axis.", type:"boolean"},
  safeToolChangePositionY: {title:"Safe tool change position Y", description:"Specify whether to use a safe tool change position in the X axis.", type:"boolean"},
  machineAxisABC: {title:"Machine axes", description:"Specify your machine axes here, for use with vector output only.", type:"string"}
};

var singleLineCoolant = false; // specifies to output multiple coolant codes in one line rather than in separate lines
// samples:
// {id: COOLANT_THROUGH_TOOL, on: 88, off: 89}
// {id: COOLANT_THROUGH_TOOL, on: [8, 88], off: [9, 89]}
var coolants = [
  {id: COOLANT_FLOOD, on: 8},
  {id: COOLANT_MIST},
  {id: COOLANT_THROUGH_TOOL, on: 88},
  {id: COOLANT_AIR},
  {id: COOLANT_AIR_THROUGH_TOOL},
  {id: COOLANT_SUCTION},
  {id: COOLANT_FLOOD_MIST},
  {id: COOLANT_FLOOD_THROUGH_TOOL},
  {id: COOLANT_OFF, off: 9}
];

var gFormat = createFormat({prefix:"G", decimals:1});
var mFormat = createFormat({prefix:"M", decimals:0});
var hFormat = createFormat({prefix:"H", decimals:0});
var dFormat = createFormat({prefix:"D", decimals:0});
var probe100Format = createFormat({decimals:3, zeropad:true, width:3, forceDecimal:true});

var xyzFormat = createFormat({decimals:(unit == MM ? 3 : 4), forceDecimal:true});
var ijkFormat = createFormat({decimals:6, forceDecimal:true});
var abcFormat = createFormat({decimals:3, forceDecimal:true, scale:DEG});
var feedFormat = createFormat({decimals:(unit == MM ? 1 : 2), forceDecimal:true});
var toolFormat = createFormat({decimals:0});
var rpmFormat = createFormat({decimals:0});
var secFormat = createFormat({decimals:3, forceDecimal:true}); // seconds - range 0.001-9999.999
var taperFormat = createFormat({decimals:1, scale:DEG});

var xOutput = createVariable({prefix:"X"}, xyzFormat);
var yOutput = createVariable({prefix:"Y"}, xyzFormat);
var zOutput = createVariable({onchange:function () {retracted = false;}, prefix:"Z"}, xyzFormat);
var aOutput = createVariable({prefix:"A"}, abcFormat);
var bOutput = createVariable({prefix:"B"}, abcFormat);
var cOutput = createVariable({prefix:"C"}, abcFormat);
var feedOutput = createVariable({prefix:"F"}, feedFormat);
var sOutput = createVariable({prefix:"S", force:true}, rpmFormat);
var dOutput = createVariable({}, dFormat);

// circular output
var iOutput = createVariable({prefix:"I", force:true}, xyzFormat);
var jOutput = createVariable({prefix:"J", force:true}, xyzFormat);
var kOutput = createVariable({prefix:"K", force:true}, xyzFormat);
var irOutput = createReferenceVariable({prefix:"I", force:true}, xyzFormat);
var jrOutput = createReferenceVariable({prefix:"J", force:true}, xyzFormat);
var krOutput = createReferenceVariable({prefix:"K", force:true}, xyzFormat);

var gMotionModal = createModal({}, gFormat); // modal group 1 // G0-G3, ...
var gPlaneModal = createModal({onchange:function () {gMotionModal.reset();}}, gFormat); // modal group 2 // G17-19
var gAbsIncModal = createModal({}, gFormat); // modal group 3 // G90-91
var gUnitModal = createModal({}, gFormat); // modal group 6 // G20-21 or G70-71
var gCycleModal = createModal({}, gFormat); // modal group 9 // G81, ...
var gRetractModal = createModal({}, gFormat); // modal group 10 // G98-99
var gRotationModal = createModal({}, gFormat); // modal group 16 // G68-G69

// fixed settings
var firstFeedParameter = 1;
var useMultiAxisFeatures = true;
var forceMultiAxisIndexing = false; // force multi-axis indexing for 3D programs

var ANGLE_PROBE_NOT_SUPPORTED = 0;
var ANGLE_PROBE_USE_ROTATION = 1;
var ANGLE_PROBE_USE_CAXIS = 2;

var WARNING_WORK_OFFSET = 0;

// collected state
var sequenceNumber;
var currentWorkOffset;
var forceSpindleSpeed = false;
var activeMovements; // do not use by default
var currentFeedId;
var g68RotationMode = 0;
var angularProbingMode;
var retracted = false; // specifies that the tool has been retracted to the safe plane
probeMultipleFeatures = true;

/** Returns true if the given ABC axis is available for use with vector output. */
function hasABCAxis(name) {
  return String(properties.machineAxisABC).toUpperCase().indexOf(name) != -1;
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
    if (text) {
      if (sequenceNumber > 9999999) {
        sequenceNumber = properties.sequenceNumberStart;
      }
      writeWords2("N" + sequenceNumber, text);
      sequenceNumber += properties.sequenceNumberIncrement;
    }
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
  writeln(formatComment(text));
}

function onOpen() {

  if (properties.isnc && (highFeedrate <= 0)) {
    error(localize("You must set 'highFeedrate' because axes are not synchronized in HURCO ISO NC mode."));
    return;
  }

  if (false) { // note: setup your machine here
    var aAxis = createAxis({coordinate:0, table:false, axis:[1, 0, 0], range:[-360, 360], preference:1});
    var cAxis = createAxis({coordinate:2, table:false, axis:[0, 0, 1], range:[-360, 360], preference:1});
    machineConfiguration = new MachineConfiguration(aAxis, cAxis);

    setMachineConfiguration(machineConfiguration);
    optimizeMachineAngles2(0); // TCP mode
  }

  if (!machineConfiguration.isMachineCoordinate(0)) {
    aOutput.disable();
  }
  if (!machineConfiguration.isMachineCoordinate(1)) {
    bOutput.disable();
  }
  if (!machineConfiguration.isMachineCoordinate(2)) {
    cOutput.disable();
  }
  
  if (useMultiAxisFeatures && !machineConfiguration.isMultiAxisConfiguration()) {
    var text = String(properties.machineAxisABC).toUpperCase();
    for (var i = 0; i < text.length; ++i) {
      if ("ABC".indexOf(text.charAt(i)) == -1) {
        error(localize("Property 'machineAxisABC' must be A, B, C or any combination of these axes!"));
        return;
      }
    }
  }
  
  if (!properties.separateWordsWithSpace) {
    setWordSeparator("");
  }

  sequenceNumber = properties.sequenceNumberStart;
  writeln("%");

  if (programName) {
    var programId;
    try {
      programId = getAsInt(programName);
    } catch (e) {
      error(localize("Program name must be a number."));
      return;
    }
    if (!((programId >= 1) && (programId <= 9999))) {
      error(localize("Program number is out of range."));
    }
    var oFormat = createFormat({width:4, zeropad:true, decimals:0});
    writeln(
      "O" + oFormat.format(programId) +
      conditional(programComment, " " + formatComment(programComment))
    );
  } else {
    error(localize("Program name has not been specified."));
    return;
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

  //Probing Surface Inspection
  if (typeof inspectionWriteVariables == "function") {
    inspectionWriteVariables();
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
          "D=" + xyzFormat.format(tool.diameter) + " " +
          localize("CR") + "=" + xyzFormat.format(tool.cornerRadius);
        if ((tool.taperAngle > 0) && (tool.taperAngle < Math.PI)) {
          comment += " " + localize("TAPER") + "=" + taperFormat.format(tool.taperAngle) + localize("deg");
        }
        if (zRanges[tool.number]) {
          comment += " - " + localize("ZMIN") + "=" + xyzFormat.format(zRanges[tool.number].getMinimum());
        }
        comment += " - " + getToolTypeName(tool.type);
        writeComment(comment);
      }
    }
  }
  
  if (false) {
    // check for duplicate tool number
    for (var i = 0; i < getNumberOfSections(); ++i) {
      var sectioni = getSection(i);
      var tooli = sectioni.getTool();
      for (var j = i + 1; j < getNumberOfSections(); ++j) {
        var sectionj = getSection(j);
        var toolj = sectionj.getTool();
        if (tooli.number == toolj.number) {
          if (xyzFormat.areDifferent(tooli.diameter, toolj.diameter) ||
              xyzFormat.areDifferent(tooli.cornerRadius, toolj.cornerRadius) ||
              abcFormat.areDifferent(tooli.taperAngle, toolj.taperAngle) ||
              (tooli.numberOfFlutes != toolj.numberOfFlutes)) {
            error(
              subst(
                localize("Using the same tool number for different cutter geometry for operation '%1' and '%2'."),
                sectioni.hasParameter("operation-comment") ? sectioni.getParameter("operation-comment") : ("#" + (i + 1)),
                sectionj.hasParameter("operation-comment") ? sectionj.getParameter("operation-comment") : ("#" + (j + 1))
              )
            );
            return;
          }
        }
      }
    }
  }
  
  if (useMultiAxisFeatures && !machineConfiguration.isMultiAxisConfiguration() && isMultiAxis()) {
    onCommand(COMMAND_STOP);
    onComment("We cannot guarantee that the CNC will not have to do a rewind during cutting when using vector output.");
    onComment("Machine needs to be defined in post to use ABC output and hence avoid risk of gouges during rewind. Please be careful.");
  }

  if ((getNumberOfSections() > 0) && (getSection(0).workOffset == 0)) {
    for (var i = 0; i < getNumberOfSections(); ++i) {
      if (getSection(i).workOffset > 0) {
        error(localize("Using multiple work offsets is not possible if the initial work offset is 0."));
        return;
      }
    }
  }

  // absolute coordinates and feed per min
  writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17));
  if (!properties.isnc) {
    writeBlock(gAbsIncModal.format(75)); // multi-quadrant arc interpolation mode
  }

  switch (unit) {
  case IN:
    writeBlock(gUnitModal.format(properties.isnc ? 20 : 70));
    break;
  case MM:
    writeBlock(gUnitModal.format(properties.isnc ? 21 : 71));
    break;
  }
  onCommand(COMMAND_START_CHIP_TRANSPORT);
  
  if (useMultiAxisFeatures && (forceMultiAxisIndexing || !is3D() || machineConfiguration.isMultiAxisConfiguration())) {
    writeBlock(mFormat.format(31)); // rotary axes encoder reset
    writeBlock(mFormat.format(126)); // shortest path traverse
  }
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

/** Force output of A, B, and C. */
function forceABC() {
  aOutput.reset();
  bOutput.reset();
  cOutput.reset();
}

function forceFeed() {
  currentFeedId = undefined;
  feedOutput.reset();
}

/** Force output of X, Y, Z, A, B, C, and F on next output. */
function forceAny() {
  forceXYZ();
  forceABC();
  forceFeed();
}

function isProbeOperation() {
  return hasParameter("operation-strategy") && ((getParameter("operation-strategy") == "probe" || getParameter("operation-strategy") == "probe_geometry"));
}

function isInspectionOperation(section) {
  return section.hasParameter("operation-strategy") && (section.getParameter("operation-strategy") == "inspectSurface");
}

var probeOutputWorkOffset = 1;

function onParameter(name, value) {
  if (name == "probe-output-work-offset") {
    probeOutputWorkOffset = (value > 0) ? value : 1;
  }
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
        return "F#" + (firstFeedParameter + feedContext.id);
      }
    }
    currentFeedId = undefined; // force Q feed next time
  }
  return feedOutput.format(f); // use feed value
}

function initializeActiveFeeds() {
  activeMovements = new Array();
  var movements = currentSection.getMovements();
  
  var id = 0;
  var activeFeeds = new Array();
  if (hasParameter("operation:tool_feedCutting")) {
    if (movements & ((1 << MOVEMENT_CUTTING) | (1 << MOVEMENT_LINK_TRANSITION) | (1 << MOVEMENT_EXTENDED))) {
      var feedContext = new FeedContext(id, localize("Cutting"), getParameter("operation:tool_feedCutting"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_CUTTING] = feedContext;
      activeMovements[MOVEMENT_LINK_TRANSITION] = feedContext;
      activeMovements[MOVEMENT_EXTENDED] = feedContext;
    }
    ++id;
    if (movements & (1 << MOVEMENT_PREDRILL)) {
      feedContext = new FeedContext(id, localize("Predrilling"), getParameter("operation:tool_feedCutting"));
      activeMovements[MOVEMENT_PREDRILL] = feedContext;
      activeFeeds.push(feedContext);
    }
    ++id;
  }
  
  if (hasParameter("operation:finishFeedrate")) {
    if (movements & (1 << MOVEMENT_FINISH_CUTTING)) {
      var feedContext = new FeedContext(id, localize("Finish"), getParameter("operation:finishFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_FINISH_CUTTING] = feedContext;
    }
    ++id;
  } else if (hasParameter("operation:tool_feedCutting")) {
    if (movements & (1 << MOVEMENT_FINISH_CUTTING)) {
      var feedContext = new FeedContext(id, localize("Finish"), getParameter("operation:tool_feedCutting"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_FINISH_CUTTING] = feedContext;
    }
    ++id;
  }
  
  if (hasParameter("operation:tool_feedEntry")) {
    if (movements & (1 << MOVEMENT_LEAD_IN)) {
      var feedContext = new FeedContext(id, localize("Entry"), getParameter("operation:tool_feedEntry"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LEAD_IN] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:tool_feedExit")) {
    if (movements & (1 << MOVEMENT_LEAD_OUT)) {
      var feedContext = new FeedContext(id, localize("Exit"), getParameter("operation:tool_feedExit"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LEAD_OUT] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:noEngagementFeedrate")) {
    if (movements & (1 << MOVEMENT_LINK_DIRECT)) {
      var feedContext = new FeedContext(id, localize("Direct"), getParameter("operation:noEngagementFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LINK_DIRECT] = feedContext;
    }
    ++id;
  } else if (hasParameter("operation:tool_feedCutting") &&
             hasParameter("operation:tool_feedEntry") &&
             hasParameter("operation:tool_feedExit")) {
    if (movements & (1 << MOVEMENT_LINK_DIRECT)) {
      var feedContext = new FeedContext(id, localize("Direct"), Math.max(getParameter("operation:tool_feedCutting"), getParameter("operation:tool_feedEntry"), getParameter("operation:tool_feedExit")));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_LINK_DIRECT] = feedContext;
    }
    ++id;
  }
  
  if (hasParameter("operation:reducedFeedrate")) {
    if (movements & (1 << MOVEMENT_REDUCED)) {
      var feedContext = new FeedContext(id, localize("Reduced"), getParameter("operation:reducedFeedrate"));
      activeFeeds.push(feedContext);
      activeMovements[MOVEMENT_REDUCED] = feedContext;
    }
    ++id;
  }

  if (hasParameter("operation:tool_feedRamp")) {
    if (movements & ((1 << MOVEMENT_RAMP) | (1 << MOVEMENT_RAMP_HELIX) | (1 << MOVEMENT_RAMP_PROFILE) | (1 << MOVEMENT_RAMP_ZIG_ZAG))) {
      var feedContext = new FeedContext(id, localize("Ramping"), getParameter("operation:tool_feedRamp"));
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
      var feedContext = new FeedContext(id, localize("Plunge"), getParameter("operation:tool_feedPlunge"));
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
    writeBlock("#" + (firstFeedParameter + feedContext.id) + "=" + feedFormat.format(feedContext.feed), formatComment(feedContext.description));
  }
}

var currentWorkPlaneABC = undefined;

function forceWorkPlane() {
  currentWorkPlaneABC = undefined;
}

function setWorkPlane(abc) {
  if (!forceMultiAxisIndexing && is3D() && !machineConfiguration.isMultiAxisConfiguration()) {
    return; // ignore
  }
  if (forceMultiAxisIndexing) {
    forceWorkPlane();
  }
  
  if (!((currentWorkPlaneABC == undefined) ||
        (machineConfiguration.isMultiAxisConfiguration() ? abcFormat.areDifferent(abc.x, currentWorkPlaneABC.x) : ijkFormat.areDifferent(abc.x, currentWorkPlaneABC.x)) ||
        (machineConfiguration.isMultiAxisConfiguration() ? abcFormat.areDifferent(abc.y, currentWorkPlaneABC.y) : ijkFormat.areDifferent(abc.y, currentWorkPlaneABC.y)) ||
        (machineConfiguration.isMultiAxisConfiguration() ? abcFormat.areDifferent(abc.z, currentWorkPlaneABC.z) : ijkFormat.areDifferent(abc.z, currentWorkPlaneABC.z)))) {
    return; // no change
  }
  
  onCommand(COMMAND_UNLOCK_MULTI_AXIS);

  if (useMultiAxisFeatures) {
    if (true) { // we don't want to use G69 for reset alone
      writeBlock(gFormat.format(0), mFormat.format(140)); // retract along tool vector
      writeBlock(gFormat.format(69)); // cancel frame
      gMotionModal.reset();
      var initialPosition = getFramePosition(currentSection.getInitialPosition()); // TAG
      var W = currentSection.workPlane;
      if (!machineConfiguration.isMultiAxisConfiguration()) {
        writeBlock(
          gFormat.format(68.2),
          "X" + xyzFormat.format(currentSection.workOrigin.x),
          "Y" + xyzFormat.format(currentSection.workOrigin.y),
          "Z" + xyzFormat.format(currentSection.workOrigin.z),
          "I" + ijkFormat.format(W.right.x), "J" + ijkFormat.format(W.right.y), "K" + ijkFormat.format(W.right.z),
          "U" + ijkFormat.format(W.up.x), "V" + ijkFormat.format(W.up.y), "W" + ijkFormat.format(W.up.z)
        ); // set frame
        var d = currentSection.getInitialToolAxis();
        writeBlock(
          gMotionModal.format(0), gFormat.format(8.2),
          xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z),
          "I" + ijkFormat.format(d.x), "J" + ijkFormat.format(d.y), "K" + ijkFormat.format(d.z)
        );
      } else {
        writeBlock(
          gMotionModal.format(0),
          conditional(machineConfiguration.isMachineCoordinate(0), "A" + abcFormat.format(abc.x)),
          conditional(machineConfiguration.isMachineCoordinate(1), "B" + abcFormat.format(abc.y)),
          conditional(machineConfiguration.isMachineCoordinate(2), "C" + abcFormat.format(abc.z))
        );
        writeBlock(
          gFormat.format(68.2),
          "X" + xyzFormat.format(currentSection.workOrigin.x),
          "Y" + xyzFormat.format(currentSection.workOrigin.y),
          "Z" + xyzFormat.format(currentSection.workOrigin.z),
          conditional(machineConfiguration.isMachineCoordinate(0), "A" + abcFormat.format(abc.x)),
          conditional(machineConfiguration.isMachineCoordinate(1), "B" + abcFormat.format(abc.y)),
          conditional(machineConfiguration.isMachineCoordinate(2), "C" + abcFormat.format(abc.z))
        ); // set frame
        writeBlock(
          gMotionModal.format(0), gFormat.format(8.2),
          xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z)
        );
      }
      // writeBlock(mFormat.format(141));
    } else {
      writeBlock(gFormat.format(69)); // cancel frame
    }
  } else {
    gMotionModal.reset();
    writeBlock(
      gMotionModal.format(0),
      conditional(machineConfiguration.isMachineCoordinate(0), "A" + abcFormat.format(abc.x)),
      conditional(machineConfiguration.isMachineCoordinate(1), "B" + abcFormat.format(abc.y)),
      conditional(machineConfiguration.isMachineCoordinate(2), "C" + abcFormat.format(abc.z))
    );
  }
  
  onCommand(COMMAND_LOCK_MULTI_AXIS);

  currentWorkPlaneABC = abc;
}

var closestABC = false; // choose closest machine angles
var currentMachineABC;

function getWorkPlaneMachineABC(workPlane) {
  var W = workPlane; // map to global frame

  var abc = machineConfiguration.getABC(W);
  if (closestABC) {
    if (currentMachineABC) {
      abc = machineConfiguration.remapToABC(abc, currentMachineABC);
    } else {
      abc = machineConfiguration.getPreferredABC(abc);
    }
  } else {
    abc = machineConfiguration.getPreferredABC(abc);
  }
  
  try {
    abc = machineConfiguration.remapABC(abc);
    currentMachineABC = abc;
  } catch (e) {
    error(
      localize("Machine angles not supported") + ":"
      + conditional(machineConfiguration.isMachineCoordinate(0), " A" + abcFormat.format(abc.x))
      + conditional(machineConfiguration.isMachineCoordinate(1), " B" + abcFormat.format(abc.y))
      + conditional(machineConfiguration.isMachineCoordinate(2), " C" + abcFormat.format(abc.z))
    );
  }
  
  var direction = machineConfiguration.getDirection(abc);
  if (!isSameDirection(direction, W.forward)) {
    error(localize("Orientation not supported."));
  }
  
  if (!machineConfiguration.isABCSupported(abc)) {
    error(
      localize("Work plane is not supported") + ":"
      + conditional(machineConfiguration.isMachineCoordinate(0), " A" + abcFormat.format(abc.x))
      + conditional(machineConfiguration.isMachineCoordinate(1), " B" + abcFormat.format(abc.y))
      + conditional(machineConfiguration.isMachineCoordinate(2), " C" + abcFormat.format(abc.z))
    );
  }

  var tcp = false;
  if (tcp) {
    setRotation(W); // TCP mode
  } else {
    var O = machineConfiguration.getOrientation(abc);
    var R = machineConfiguration.getRemainingOrientation(abc, W);
    setRotation(R);
  }
  
  return abc;
}

function onSection() {
  var insertToolCall = isFirstSection() ||
    currentSection.getForceToolChange && currentSection.getForceToolChange() ||
    (tool.number != getPreviousSection().getTool().number);
  
  retracted = false; // specifies that the tool has been retracted to the safe plane
  var newWorkOffset = isFirstSection() ||
    (getPreviousSection().workOffset != currentSection.workOffset); // work offset changes
  var newWorkPlane = isFirstSection() ||
    !isSameDirection(getPreviousSection().getGlobalFinalToolAxis(), currentSection.getGlobalInitialToolAxis()) ||
    (currentSection.isOptimizedForMachine() && getPreviousSection().isOptimizedForMachine() &&
      Vector.diff(getPreviousSection().getFinalToolAxisABC(), currentSection.getInitialToolAxisABC()).length > 1e-4) ||
    (!machineConfiguration.isMultiAxisConfiguration() && currentSection.isMultiAxis()) ||
    (!getPreviousSection().isMultiAxis() && currentSection.isMultiAxis() ||
      getPreviousSection().isMultiAxis() && !currentSection.isMultiAxis()); // force newWorkPlane between indexing and simultaneous operations
  if (insertToolCall || newWorkOffset || newWorkPlane) {
    
    // stop spindle before retract during tool change
    if (insertToolCall && !isFirstSection()) {
      onCommand(COMMAND_STOP_SPINDLE);
    }
    
    // retract to safe plane
    writeRetract(Z);
    forceXYZ();
    
    // save tool change position
    if (insertToolCall && !isFirstSection()) {
      if (properties.safeToolChangePositionX || properties.safeToolChangePositionY) {
        writeBlock(gFormat.format(53), conditional(properties.safeToolChangePositionX, "X" + xyzFormat.format(0)), conditional(properties.safeToolChangePositionY, "Y" + xyzFormat.format(0)));
      }
    }
  }

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
    forceWorkPlane();
  
    if (!isFirstSection()) {
      setCoolant(COOLANT_OFF);
      if (properties.optionalStop) {
        onCommand(COMMAND_OPTIONAL_STOP);
      }
    }

    if (tool.number > 99) {
      warning(localize("Tool number exceeds maximum value."));
    }

    writeBlock("T" + toolFormat.format(tool.number), mFormat.format(6));
    if (tool.comment) {
      writeComment(tool.comment);
    }
    var showToolZMin = false;
    if (showToolZMin) {
      if (is3D()) {
        var numberOfSections = getNumberOfSections();
        var zRange = currentSection.getGlobalZRange();
        var number = tool.number;
        for (var i = currentSection.getId() + 1; i < numberOfSections; ++i) {
          var section = getSection(i);
          if (section.getTool().number != number) {
            break;
          }
          zRange.expandToRange(section.getGlobalZRange());
        }
        writeComment(localize("ZMIN") + "=" + zRange.getMinimum());
      }
    }

    if (properties.preloadTool) {
      var nextTool = getNextTool(tool.number);
      if (nextTool) {
        writeBlock("T" + toolFormat.format(nextTool.number));
      } else {
        // preload first tool
        var section = getSection(0);
        var firstToolNumber = section.getTool().number;
        if (tool.number != firstToolNumber) {
          writeBlock("T" + toolFormat.format(firstToolNumber));
        }
      }
    }
    if (isProbeOperation() || isInspectionOperation(currentSection)) {
      if (properties.isnc) {
        writeBlock(mFormat.format(19)); // spindle orientation
        writeBlock(mFormat.format(26)); // select the part probe, M27 is selecting the tool probe
        writeBlock(mFormat.format(41)); // Single touch probing, M42 is 2 touch probing
      } else {
        error(localize("Probing or surface inspection is only allowed in ISNC mode!"));
      }
    }
  }
  
  if (!isProbeOperation() &&
      !isInspectionOperation(currentSection) && (insertToolCall ||
      forceSpindleSpeed ||
      isFirstSection() ||
      (rpmFormat.areDifferent(spindleSpeed, sOutput.getCurrent())) ||
      (tool.clockwise != getPreviousSection().getTool().clockwise))) {
    forceSpindleSpeed = false;
    
    if (spindleSpeed < 1) {
      error(localize("Spindle speed out of range."));
      return;
    }
    if (spindleSpeed > 65535) {
      warning(localize("Spindle speed exceeds maximum value."));
    }
    writeBlock(
      sOutput.format(spindleSpeed), mFormat.format(tool.clockwise ? 3 : 4)
    );
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

  forceXYZ();

  if (forceMultiAxisIndexing || !is3D() || machineConfiguration.isMultiAxisConfiguration()) { // use 5-axis indexing for multi-axis mode
    // set working plane after datum shift

    if (currentSection.isMultiAxis()) {
      forceWorkPlane();
      cancelTransformation();
    } else {
      var abc = new Vector(0, 0, 0);
      if (useMultiAxisFeatures && !machineConfiguration.isMultiAxisConfiguration()) {
        // writeln("VECTOR")
        abc = currentSection.getGlobalInitialToolAxis(); // using vectors
      } else {
        // writeln("MACHINE ANGLES")
        abc = getWorkPlaneMachineABC(currentSection.workPlane);
      }
      setWorkPlane(abc);
    }
  } else { // pure 3D
    var remaining = currentSection.workPlane;
    if (!isSameDirection(remaining.forward, new Vector(0, 0, 1))) {
      error(localize("Tool orientation is not supported."));
      return;
    }
    setRotation(remaining);
  }

  // set coolant after we have positioned at Z
  setCoolant(tool.coolant);

  forceAny();

  if (currentSection.isMultiAxis()) {
    onCommand(COMMAND_UNLOCK_MULTI_AXIS);

    writeBlock(gFormat.format(69));
    writeBlock(mFormat.format(128)); // only after we are at initial position

    // turn
    var abc;
    var d = currentSection.getGlobalInitialToolAxis();
    var initialPosition = getFramePosition(currentSection.getInitialPosition());
    if (currentSection.isOptimizedForMachine()) {
      abc = currentSection.getInitialToolAxisABC();
      writeBlock(
        gMotionModal.format(0), gFormat.format(8.2),
        xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z),
        aOutput.format(abc.x), bOutput.format(abc.y), cOutput.format(abc.z)
      );
    } else {
      gMotionModal.reset();
      writeBlock(
        gMotionModal.format(0), gFormat.format(8.2),
        xOutput.format(initialPosition.x), yOutput.format(initialPosition.y), zOutput.format(initialPosition.z),
        "I" + ijkFormat.format(d.x), "J" + ijkFormat.format(d.y), "K" + ijkFormat.format(d.z)
      );
    }
    writeBlock(gFormat.format(43.4));
    writeBlock(mFormat.format(200), "P" + (properties.preferPositiveTilt ? 1 : 2)); // prefer positive/negative tilt
  } else {
    var initialPosition = getFramePosition(currentSection.getInitialPosition());
    if (!retracted && !insertToolCall) {
      if (getCurrentPosition().z < initialPosition.z) {
        writeBlock(gMotionModal.format(0), zOutput.format(initialPosition.z));
      }
    }
  
    if (insertToolCall || retracted) {
      var lengthOffset = tool.lengthOffset;
      if (lengthOffset > 200) {
        warning(localize("The length offset exceeds the maximum value."));
      }

      gMotionModal.reset();
      writeBlock(gPlaneModal.format(17));

      if (!machineConfiguration.isHeadConfiguration()) {
        writeBlock(
          gAbsIncModal.format(90),
          gMotionModal.format(0), xOutput.format(initialPosition.x), yOutput.format(initialPosition.y)
        );
        if (!useMultiAxisFeatures || currentSection.isZOriented()) {
          writeBlock(gMotionModal.format(0), gFormat.format(43), zOutput.format(initialPosition.z), hFormat.format(lengthOffset));
        } else {
          writeBlock(gMotionModal.format(0), zOutput.format(initialPosition.z));
        }
      } else {
        if (!useMultiAxisFeatures || currentSection.isZOriented()) {
          writeBlock(
            gAbsIncModal.format(90),
            gMotionModal.format(0),
            gFormat.format(43), xOutput.format(initialPosition.x),
            yOutput.format(initialPosition.y),
            zOutput.format(initialPosition.z), hFormat.format(lengthOffset)
          );
        } else {
          writeBlock(
            gAbsIncModal.format(90),
            gMotionModal.format(0),
            xOutput.format(initialPosition.x),
            yOutput.format(initialPosition.y),
            zOutput.format(initialPosition.z)
          );
        }
      }
    } else {
      writeBlock(
        gAbsIncModal.format(90),
        gMotionModal.format(0),
        xOutput.format(initialPosition.x),
        yOutput.format(initialPosition.y)
      );
    }
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
  
  if (isProbeOperation()) {
    if (g68RotationMode != 0) {
      error(localize("You cannot probe while G68 Rotation is in effect."));
      return;
    }
    angularProbingMode = getAngularProbingMode();
    writeBlock(gFormat.format(65), "P" + 9832); // spin the probe on
  }

  // surface Inspection
  if (isInspectionOperation(currentSection) && (typeof inspectionProcessSectionStart == "function")) {
    inspectionProcessSectionStart();
  }

/*
  if (properties.smoothingTolerance > 0) {
    writeBlock(gFormat.format(5.2), "P1", "Q" + xyzFormat.format(properties.smoothingTolerance));
  }
*/
}

function onDwell(seconds) {
  if (seconds > 9999.999) {
    warning(localize("Dwelling time is out of range."));
  }
  seconds = clamp(0.001, seconds, 9999.999);
  writeBlock(gFormat.format(4), "P" + secFormat.format(seconds));
}

function onSpindleSpeed(spindleSpeed) {
  writeBlock(sOutput.format(spindleSpeed));
}

function onCycle() {
  writeBlock(gPlaneModal.format(17));
}

function getCommonCycle(x, y, z, r) {
  forceXYZ();
  if (properties.isnc) {
    return [xOutput.format(x), yOutput.format(y),
      zOutput.format(z),
      "R" + xyzFormat.format(r)];
  } else {
    return [xOutput.format(x), yOutput.format(y),
      "Z" + xyzFormat.format(z),
      "R" + xyzFormat.format(r)];
  }
}

/** Convert approach to sign. */
function approach(value) {
  validate((value == "positive") || (value == "negative"), "Invalid approach.");
  return (value == "positive") ? 1 : -1;
}

/**
  Determine if angular probing is supported
*/
function getAngularProbingMode() {
  if (machineConfiguration.isMultiAxisConfiguration()) {
    if (machineConfiguration.isMachineCoordinate(2)) {
      return ANGLE_PROBE_USE_CAXIS;
    } else {
      return ANGLE_PROBE_NOT_SUPPORTED;
    }
  } else {
    return ANGLE_PROBE_USE_ROTATION;
  }
}

/**
  Output rotation offset based on angular probing cycle.
*/
function setProbingAngle() {
  if ((g68RotationMode == 1) || (g68RotationMode == 2)) { // Rotate coordinate system for Angle Probing
    gRotationModal.reset();
    gAbsIncModal.reset();
    writeBlock(
      gRotationModal.format(68), gAbsIncModal.format(90),
      (g68RotationMode == 1) ? "X0" : "X[#135]",
      (g68RotationMode == 1) ? "Y0" : "Y[#136]",
      "R[#139]"
    );
    g68RotationMode = 3;
  }
}

function protectedProbeMove(_cycle, x, y, z) {
  var _x = xOutput.format(x);
  var _y = yOutput.format(y);
  var _z = zOutput.format(z);
  if (_z && z >= getCurrentPosition().z) {
    writeBlock(gFormat.format(65), "P" + 9810, _z, getFeed(cycle.feedrate)); // protected positioning move
  }
  if (_x || _y) {
    writeBlock(gFormat.format(65), "P" + 9810, _x, _y, getFeed(highFeedrate)); // protected positioning move
  }
  if (_z && z < getCurrentPosition().z) {
    writeBlock(gFormat.format(65), "P" + 9810, _z, getFeed(cycle.feedrate)); // protected positioning move
  }
}

function onCyclePoint(x, y, z) {
  if (cycleType == "inspect") {
    if (typeof inspectionCycleInspect == "function") {
      inspectionCycleInspect(cycle, x, y, z);
      return;
    } else {
      cycleNotSupported();
    }
  }
  if (!isSameDirection(getRotation().forward, new Vector(0, 0, 1))) {
    expandCyclePoint(x, y, z);
    return;
  }
  var probeWorkOffsetCode;
  if (isProbeOperation()) {
    if (!useMultiAxisFeatures && !isSameDirection(currentSection.workPlane.forward, new Vector(0, 0, 1)) && (!cycle.probeMode || (cycle.probeMode == 0))) {
      error(localize("Updating WCS / work offset using probing is only supported by the CNC in the WCS frame."));
      return;
    }
    protectedProbeMove(cycle, x, y, z);

    var workOffset = probeOutputWorkOffset ? probeOutputWorkOffset : currentWorkOffset;
    if (workOffset > 99) {
      error(localize("Work offset is out of range."));
      return;
    } else if (workOffset > 6) {
      probeWorkOffsetCode = probe100Format.format(workOffset - 6 + 100);
    } else {
      probeWorkOffsetCode = workOffset + "."; // G54->G59
    }
  }

  if (isFirstCyclePoint() || isProbeOperation()) {
    if (!isProbeOperation()) {
      // return to initial Z which is clearance plane and set absolute mode
      repositionToCycleClearance(cycle, x, y, z);
    }
    // R is only used in G99 mode for BNC

    var F = cycle.feedrate;
    var P = !cycle.dwell ? 0 : clamp(1, cycle.dwell, 9999.999); // in seconds
    
    switch (cycleType) {
    case "drilling":
      if (properties.isnc) {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
          getCommonCycle(x, y, z, cycle.retract),
          feedOutput.format(F)
        );
      } else { // BNC mode
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
          getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
          feedOutput.format(F)
        );
      }
      break;
    case "counter-boring":
      if (P > 0) {
        if (properties.isnc) {
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(82),
            getCommonCycle(x, y, z, cycle.retract),
            "P" + secFormat.format(P), // not optional
            feedOutput.format(F)
          );
        } else { // BNC mode
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(82),
            getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
            "P" + secFormat.format(P), // not optional
            feedOutput.format(F)
          );
        }
      } else {
        if (properties.isnc) {
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
            getCommonCycle(x, y, z, cycle.retract),
            feedOutput.format(F)
          );
        } else { // BNC mode
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(81),
            getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
            feedOutput.format(F)
          );
        }
      }
      break;
    case "chip-breaking":
      if ((cycle.accumulatedDepth < cycle.depth) || (P > 0)) {
        expandCyclePoint(x, y, z);
      } else {
        if (properties.isnc) {
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(73),
            getCommonCycle(x, y, z, cycle.retract),
            "Q" + xyzFormat.format(cycle.incrementalDepth),
            feedOutput.format(F)
          );
        } else { // BNC mode
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(73),
            getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
            "Q" + xyzFormat.format(cycle.incrementalDepth),
            feedOutput.format(F)
          );
        }
      }
      break;
    case "deep-drilling":
      if (P > 0) {
        expandCyclePoint(x, y, z);
      } else {
        if (properties.isnc) {
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(83),
            getCommonCycle(x, y, z, cycle.retract),
            "Q" + xyzFormat.format(cycle.incrementalDepth),
            feedOutput.format(F)
          );
        } else { // BNC mode
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(83),
            xOutput.format(x),
            yOutput.format(y),
            "Z" + xyzFormat.format(cycle.clearance - cycle.bottom),
            "Z" + xyzFormat.format(cycle.incrementalDepth), // first peck
            conditional((cycle.minimumIncrementalDepth != undefined) && (cycle.minimumIncrementalDepth < cycle.incrementalDepth), "Z" + xyzFormat.format(cycle.minimumIncrementalDepth)), // remaining pecks
            "R" + xyzFormat.format(zOutput.getCurrent() - cycle.retract),
            feedOutput.format(F)
          );
        }
      }
      break;
    case "tapping":
      if (true || !F) {
        F = tool.getTappingFeedrate();
      }
      if (properties.isnc) {
        writeBlock(mFormat.format(29)); // rigid
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format((tool.type == TOOL_TAP_LEFT_HAND) ? 74 : 84),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
      } else { // BNC mode
        if (tool.type != TOOL_TAP_LEFT_HAND) { // right hand
          writeBlock(mFormat.format(3)); // cw
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(88), // rigid
            xOutput.format(x),
            yOutput.format(y),
            "Z" + xyzFormat.format(cycle.clearance - cycle.bottom),
            //"Z" + xyzFormat.format(cycle.incrementalDepth),
            "R" + xyzFormat.format(zOutput.getCurrent() - cycle.retract),
            "P" + secFormat.format(P), // not optional
            feedOutput.format(F)
          );
          if (!tool.clockwise) {
            writeBlock(mFormat.format(tool.clockwise ? 3 : 4));
          }
        } else { // left hand
          // warning: not rigid

          writeBlock(mFormat.format((tool.type == TOOL_TAP_LEFT_HAND) ? 4 : 3));
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(84),
            getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
            feedOutput.format(F)
          );
          if ((tool.type == TOOL_TAP_LEFT_HAND) != !tool.clockwise) {
            writeBlock(mFormat.format(tool.clockwise ? 3 : 4));
          }
        }
      }
      break;
    case "left-tapping":
      if (true || !F) {
        F = tool.getTappingFeedrate();
      }
      if (properties.isnc) {
        writeBlock(mFormat.format(29)); // rigid
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(74),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
      } else { // BNC mode
        // warning: not rigid
        writeBlock(mFormat.format(4)); // ccw
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(84),
          getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
          feedOutput.format(F)
        );
        if (tool.clockwise) {
          writeBlock(mFormat.format(tool.clockwise ? 3 : 4));
        }
      }
      break;
    case "right-tapping":
      if (true || !F) {
        F = tool.getTappingFeedrate();
      }
      if (properties.isnc) {
        writeBlock(mFormat.format(29)); // rigid
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(84),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
      } else { // BNC mode
        writeBlock(mFormat.format(3)); // cw
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(88), // rigid
          xOutput.format(x),
          yOutput.format(y),
          "Z" + xyzFormat.format(cycle.clearance - cycle.bottom),
          "R" + xyzFormat.format(zOutput.getCurrent() - cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
        if (!tool.clockwise) {
          writeBlock(mFormat.format(tool.clockwise ? 3 : 4));
        }
      }
      break;
    case "tapping-with-chip-breaking":
    case "left-tapping-with-chip-breaking":
    case "right-tapping-with-chip-breaking":
      if (cycle.accumulatedDepth < cycle.depth) {
        error(localize("Accumulated pecking depth is not supported for canned tapping cycles with chip breaking."));
        return;
      }
      if (true || !F) {
        F = tool.getTappingFeedrate();
      }
      if (properties.isnc) {
        forceXYZ();
        writeBlock(mFormat.format(29)); // rigid
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format((tool.type == TOOL_TAP_LEFT_HAND) ? 84.3 : 84.2),
          // getCommonCycle(x, y, z, cycle.retract),
          xOutput.format(x),
          yOutput.format(y),
          "Z" + xyzFormat.format(z),
          "Z" + xyzFormat.format(cycle.incrementalDepth),
          "R" + xyzFormat.format(cycle.retract),
          "P" + secFormat.format(P), // not optional
          conditional(cycle.minimumIncrementalDepth < cycle.depth, "Q" + xyzFormat.format(cycle.minimumIncrementalDepth)), // optional
          feedOutput.format(F)
        );
        zOutput.reset();
      } else { // BNC mode
        if (tool.type != TOOL_TAP_LEFT_HAND) { // right hand
          writeBlock(mFormat.format(3)); // cw
          writeBlock(
            gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(88), // rigid
            xOutput.format(x),
            yOutput.format(y),
            "Z" + xyzFormat.format(cycle.clearance - cycle.bottom),
            "Z" + xyzFormat.format(cycle.incrementalDepth),
            "R" + xyzFormat.format(zOutput.getCurrent() - cycle.retract),
            "P" + secFormat.format(P), // not optional
            feedOutput.format(F)
          );
          if (!tool.clockwise) {
            writeBlock(mFormat.format(tool.clockwise ? 3 : 4));
          }
        } else {
          error(localize("Left-tapping with chip breaking is not supported."));
        }
      }
      break;
    case "fine-boring":
      if (properties.isnc) {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(76),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + secFormat.format(P), // not optional
          "Q" + xyzFormat.format(cycle.shift),
          feedOutput.format(F)
        );
      } else { // BNC mode
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(76),
          getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
          "P" + secFormat.format(P), // not optional
          "Q" + xyzFormat.format(cycle.shift),
          feedOutput.format(F)
        );
      }
      break;
    case "back-boring":
      if (!properties.isnc) {
        error(localize("Back boring is not supported."));
      }
      var dx = (gPlaneModal.getCurrent() == 19) ? cycle.backBoreDistance : 0;
      var dy = (gPlaneModal.getCurrent() == 18) ? cycle.backBoreDistance : 0;
      var dz = (gPlaneModal.getCurrent() == 17) ? cycle.backBoreDistance : 0;
      writeBlock(
        gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(87),
        getCommonCycle(x - dx, y - dy, z - dz, cycle.bottom),
        "Q" + xyzFormat.format(cycle.shift),
        "P" + secFormat.format(P), // not optional
        feedOutput.format(F)
      );
      break;
    case "reaming":
      if (properties.isnc) {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(85),
          getCommonCycle(x, y, z, cycle.retract),
          feedOutput.format(F)
        );
      } else { // BNC mode
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(85),
          getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
          feedOutput.format(F)
        );
      }
      break;
    case "stop-boring":
      if ((P > 0) || !properties.isnc) {
        expandCyclePoint(x, y, z);
      } else {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(86),
          getCommonCycle(x, y, z, cycle.retract),
          feedOutput.format(F)
        );
      }
      break;
    case "manual-boring":
      if (!properties.isnc) {
        error(localize("Manual boring is not supported."));
      }
      writeBlock(
        gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(88),
        getCommonCycle(x, y, z, cycle.retract),
        "P" + secFormat.format(P), // not optional
        feedOutput.format(F)
      );
      break;
    case "boring":
      if (properties.isnc) {
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(89),
          getCommonCycle(x, y, z, cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
      } else { // BNC
        writeBlock(
          gRetractModal.format(98), gAbsIncModal.format(90), gCycleModal.format(89),
          getCommonCycle(x, y, cycle.clearance - cycle.bottom, zOutput.getCurrent() - cycle.retract),
          "P" + secFormat.format(P), // not optional
          feedOutput.format(F)
        );
      }
      break;
    case "probing-x":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9811,
        "X" + xyzFormat.format(x + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2)),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-y":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9811,
        "Y" + xyzFormat.format(y + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2)),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-z":
      protectedProbeMove(cycle, x, y, Math.min(z - cycle.depth + cycle.probeClearance, cycle.retract));
      writeBlock(
        gFormat.format(65), "P" + 9811,
        "Z" + xyzFormat.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-x-wall":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "X" + xyzFormat.format(cycle.width1),
        zOutput.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-y-wall":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Y" + xyzFormat.format(cycle.width1),
        zOutput.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-x-channel":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "X" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        // not required "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-x-channel-with-island":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "X" + xyzFormat.format(cycle.width1),
        zOutput.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-y-channel":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Y" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        // not required "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-y-channel-with-island":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Y" + xyzFormat.format(cycle.width1),
        zOutput.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-circular-boss":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9814,
        "D" + xyzFormat.format(cycle.width1),
        "Z" + xyzFormat.format(z - cycle.depth),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-circular-hole":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9814,
        "D" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        // not required "R" + xyzFormat.format(cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-circular-hole-with-island":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9814,
        "Z" + xyzFormat.format(z - cycle.depth),
        "D" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-rectangular-hole":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "X" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        // not required "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Y" + xyzFormat.format(cycle.width2),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        // not required "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-rectangular-boss":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Z" + xyzFormat.format(z - cycle.depth),
        "X" + xyzFormat.format(cycle.width1),
        "R" + xyzFormat.format(cycle.probeClearance),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Z" + xyzFormat.format(z - cycle.depth),
        "Y" + xyzFormat.format(cycle.width2),
        "R" + xyzFormat.format(cycle.probeClearance),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
    case "probing-xy-rectangular-hole-with-island":
      protectedProbeMove(cycle, x, y, z);
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Z" + xyzFormat.format(z - cycle.depth),
        "X" + xyzFormat.format(cycle.width1),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      writeBlock(
        gFormat.format(65), "P" + 9812,
        "Z" + xyzFormat.format(z - cycle.depth),
        "Y" + xyzFormat.format(cycle.width2),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        "R" + xyzFormat.format(-cycle.probeClearance),
        getProbingArguments(cycle, probeWorkOffsetCode)
      );
      break;
  
    case "probing-xy-inner-corner":
      var cornerX = x + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2);
      var cornerY = y + approach(cycle.approach2) * (cycle.probeClearance + tool.diameter / 2);
      var cornerI = 0;
      var cornerJ = 0;
      if (cycle.probeSpacing !== undefined) {
        cornerI = cycle.probeSpacing;
        cornerJ = cycle.probeSpacing;
      }
      if ((cornerI != 0) && (cornerJ != 0)) {
        g68RotationMode = 2;
      }
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9815, xOutput.format(cornerX), yOutput.format(cornerY),
        conditional(cornerI != 0, "I" + xyzFormat.format(cornerI)),
        conditional(cornerJ != 0, "J" + xyzFormat.format(cornerJ)),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        conditional((g68RotationMode == 0) || (angularProbingMode == ANGLE_PROBE_USE_CAXIS), getProbingArguments(cycle, probeWorkOffsetCode))
      );
      break;
    case "probing-xy-outer-corner":
      var cornerX = x + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2);
      var cornerY = y + approach(cycle.approach2) * (cycle.probeClearance + tool.diameter / 2);
      var cornerI = 0;
      var cornerJ = 0;
      if (cycle.probeSpacing !== undefined) {
        cornerI = cycle.probeSpacing;
        cornerJ = cycle.probeSpacing;
      }
      if ((cornerI != 0) && (cornerJ != 0)) {
        g68RotationMode = 2;
      }
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9816, xOutput.format(cornerX), yOutput.format(cornerY),
        conditional(cornerI != 0, "I" + xyzFormat.format(cornerI)),
        conditional(cornerJ != 0, "J" + xyzFormat.format(cornerJ)),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        conditional((g68RotationMode == 0) || (angularProbingMode == ANGLE_PROBE_USE_CAXIS), getProbingArguments(cycle, probeWorkOffsetCode))
      );
      break;
    case "probing-x-plane-angle":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9843,
        "X" + xyzFormat.format(x + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2)),
        "D" + xyzFormat.format(cycle.probeSpacing),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, false)
      );
      g68RotationMode = 1;
      break;
    case "probing-y-plane-angle":
      protectedProbeMove(cycle, x, y, z - cycle.depth);
      writeBlock(
        gFormat.format(65), "P" + 9843,
        "Y" + xyzFormat.format(y + approach(cycle.approach1) * (cycle.probeClearance + tool.diameter / 2)),
        "D" + xyzFormat.format(cycle.probeSpacing),
        "Q" + xyzFormat.format(cycle.probeOvertravel),
        getProbingArguments(cycle, false)
      );
      g68RotationMode = 1;
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

function getProbingArguments(cycle, probeWorkOffsetCode) {
  var probeWCS = hasParameter("operation-strategy") && (getParameter("operation-strategy") == "probe");
  return [
    (cycle.angleAskewAction == "stop-message" ? "B" + xyzFormat.format(cycle.toleranceAngle ? cycle.toleranceAngle : 0) : undefined),
    ((cycle.updateToolWear && cycle.toolWearErrorCorrection < 100) ? "F" + xyzFormat.format(cycle.toolWearErrorCorrection ? cycle.toolWearErrorCorrection / 100 : 100) : undefined),
    (cycle.wrongSizeAction == "stop-message" ? "H" + xyzFormat.format(cycle.toleranceSize ? cycle.toleranceSize : 0) : undefined),
    (cycle.outOfPositionAction == "stop-message" ? "M" + xyzFormat.format(cycle.tolerancePosition ? cycle.tolerancePosition : 0) : undefined),
    ((cycle.updateToolWear && cycleType == "probing-z") ? "T" + xyzFormat.format(cycle.toolLengthOffset) : undefined),
    ((cycle.updateToolWear && cycleType !== "probing-z") ? "T" + xyzFormat.format(cycle.toolDiameterOffset) : undefined),
    (cycle.updateToolWear ? "V" + xyzFormat.format(cycle.toolWearUpdateThreshold ? cycle.toolWearUpdateThreshold : 0) : undefined),
    (cycle.printResults ? "W" + xyzFormat.format(1 + cycle.incrementComponent) : undefined), // 1 for advance feature, 2 for reset feature count and advance component number. first reported result in a program should use W2.
    conditional(probeWorkOffsetCode && probeWCS, "S" + probeWorkOffsetCode)
  ];
}

function onCycleEnd() {
  if (isProbeOperation()) {
    zOutput.reset();
    gMotionModal.reset();
    writeBlock(gFormat.format(65), "P" + 9810, zOutput.format(cycle.retract)); // protected retract move
  } else {
    if (!cycleExpanded) {
      writeBlock(gCycleModal.format(80));
      zOutput.reset();
    }
  }
}

var pendingRadiusCompensation = -1;

function onRadiusCompensation() {
  pendingRadiusCompensation = radiusCompensation;
}

function onRapid(_x, _y, _z) {
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      error(localize("Radius compensation mode cannot be changed at rapid traversal."));
      return;
    }
    if (properties.isnc && (((x ? 1 : 0) + (y ? 1 : 0) + (z ? 1 : 0)) > 1)) {
      // axes are not synchronized
      writeBlock(gMotionModal.format(1), x, y, z, feedOutput.format(highFeedrate));
    } else {
      writeBlock(gMotionModal.format(0), x, y, z);
      forceFeed();
    }
  }
}

function onLinear(_x, _y, _z, feed) {
  if (pendingRadiusCompensation >= 0) {
    // ensure that we end at desired position when compensation is turned off
    xOutput.reset();
    yOutput.reset();
  }
  var x = xOutput.format(_x);
  var y = yOutput.format(_y);
  var z = zOutput.format(_z);
  var f = getFeed(feed);
  if (x || y || z) {
    if (pendingRadiusCompensation >= 0) {
      pendingRadiusCompensation = -1;
      var d = tool.diameterOffset;
      if (d > 200) {
        warning(localize("The diameter offset exceeds the maximum value."));
      }
      writeBlock(gPlaneModal.format(17));
      switch (radiusCompensation) {
      case RADIUS_COMPENSATION_LEFT:
        dOutput.reset();
        writeBlock(gMotionModal.format(1), gFormat.format(41), x, y, z, dOutput.format(d), f);
        break;
      case RADIUS_COMPENSATION_RIGHT:
        dOutput.reset();
        writeBlock(gMotionModal.format(1), gFormat.format(42), x, y, z, dOutput.format(d), f);
        break;
      default:
        writeBlock(gMotionModal.format(1), gFormat.format(40), x, y, z, f);
      }
    } else {
      writeBlock(gMotionModal.format(1), x, y, z, f);
    }
  } else if (f) {
    if (getNextRecord().isMotion()) { // try not to output feed without motion
      forceFeed(); // force feed on next line
    } else {
      writeBlock(gMotionModal.format(1), f);
    }
  }
}

function onRapid5D(_x, _y, _z, _a, _b, _c) {
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation mode cannot be changed at rapid traversal."));
    return;
  }
  if (currentSection.isOptimizedForMachine()) {
    var x = xOutput.format(_x);
    var y = yOutput.format(_y);
    var z = zOutput.format(_z);
    var a = aOutput.format(_a);
    var b = bOutput.format(_b);
    var c = cOutput.format(_c);
    if (properties.isnc) {
      // axes are not synchronized
      writeBlock(gMotionModal.format(1), x, y, z, a, b, c, feedOutput.format(highFeedrate));
    } else {
      writeBlock(gMotionModal.format(0), x, y, z, a, b, c);
      forceFeed();
    }
  } else {
    forceXYZ();
    var x = xOutput.format(_x);
    var y = yOutput.format(_y);
    var z = zOutput.format(_z);
    var i = ijkFormat.format(_a);
    var j = ijkFormat.format(_b);
    var k = ijkFormat.format(_c);
    if (x || y || z || i || j || k) {
      if (properties.isnc) {
        // axes are not synchronized
        writeBlock(gMotionModal.format(1), x, y, z, "I" + i, "J" + j, "K" + k, feedOutput.format(highFeedrate));
      } else {
        writeBlock(gMotionModal.format(0), x, y, z, "I" + i, "J" + j, "K" + k);
        forceFeed();
      }
    }
  }
}

function onLinear5D(_x, _y, _z, _a, _b, _c, feed) {
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation cannot be activated/deactivated for 5-axis move."));
    return;
  }

  if (currentSection.isOptimizedForMachine()) {
    var x = xOutput.format(_x);
    var y = yOutput.format(_y);
    var z = zOutput.format(_z);
    var a = aOutput.format(_a);
    var b = bOutput.format(_b);
    var c = cOutput.format(_c);
    var f = getFeed(feed);
    if (x || y || z || a || b || c) {
      writeBlock(gMotionModal.format(1), x, y, z, a, b, c, f);
    } else if (f) {
      if (getNextRecord().isMotion()) { // try not to output feed without motion
        forceFeed(); // force feed on next line
      } else {
        writeBlock(gMotionModal.format(1), f);
      }
    }
  } else {
    forceXYZ();
    var x = xOutput.format(_x);
    var y = yOutput.format(_y);
    var z = zOutput.format(_z);
    var i = ijkFormat.format(_a);
    var j = ijkFormat.format(_b);
    var k = ijkFormat.format(_c);
    var f = getFeed(feed);
    if (x || y || z || i || j || k) {
      writeBlock(gMotionModal.format(1), x, y, z, "I" + i, "J" + j, "K" + k, f);
    } else if (f) {
      if (getNextRecord().isMotion()) { // try not to output feed without motion
        forceFeed(); // force feed on next line
      } else {
        writeBlock(gMotionModal.format(1), f);
      }
    }
  }
}

function onCircular(clockwise, cx, cy, cz, x, y, z, feed) {
  if (pendingRadiusCompensation >= 0) {
    error(localize("Radius compensation cannot be activated/deactivated for a circular move."));
    return;
  }

  var start = getCurrentPosition();

  if (isFullCircle()) {
    if (isHelical()) {
      linearize(tolerance);
      return;
    }
    switch (getCircularPlane()) {
    case PLANE_XY:
      if (properties.isnc) {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(clockwise ? 2 : 3), irOutput.format(cx - start.x, 0), jrOutput.format(cy - start.y, 0), getFeed(feed));
      } else {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(clockwise ? 2 : 3), iOutput.format(cx), jOutput.format(cy), getFeed(feed));
      }
      break;
    case PLANE_ZX:
      if (properties.isnc) {
        // right-handed
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(clockwise ? 2 : 3), irOutput.format(cx - start.x, 0), krOutput.format(cz - start.z, 0), getFeed(feed));
      } else {
        // note: left hand coordinate system
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(clockwise ? 3 : 2), iOutput.format(cx), kOutput.format(cz), getFeed(feed));
      }
      break;
    case PLANE_YZ:
      if (properties.isnc) {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(clockwise ? 2 : 3), jrOutput.format(cy - start.y, 0), krOutput.format(cz - start.z, 0), getFeed(feed));
      } else {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(clockwise ? 2 : 3), jOutput.format(cy), kOutput.format(cz), getFeed(feed));
      }
      break;
    default:
      linearize(tolerance);
    }
  } else {
    switch (getCircularPlane()) {
    case PLANE_XY:
      if (properties.isnc) {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), irOutput.format(cx - start.x, 0), jrOutput.format(cy - start.y, 0), getFeed(feed));
      } else {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(17), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx), jOutput.format(cy), getFeed(feed));
      }
      break;
    case PLANE_ZX:
      if (isHelical()) {
        linearize(tolerance);
        return;
      }

      if (properties.isnc) {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), irOutput.format(cx - start.x, 0), krOutput.format(cz - start.z, 0), getFeed(feed));
      } else {
        // note: left hand coordinate system
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(18), gMotionModal.format(clockwise ? 3 : 2), xOutput.format(x), yOutput.format(y), zOutput.format(z), iOutput.format(cx), kOutput.format(cz), getFeed(feed));
      }
      break;
    case PLANE_YZ:
      if (isHelical()) {
        linearize(tolerance);
        return;
      }

      if (properties.isnc) {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), jrOutput.format(cy - start.y, 0), krOutput.format(cz - start.z, 0), getFeed(feed));
      } else {
        writeBlock(gAbsIncModal.format(90), gPlaneModal.format(19), gMotionModal.format(clockwise ? 2 : 3), xOutput.format(x), yOutput.format(y), zOutput.format(z), jOutput.format(cy), kOutput.format(cz), getFeed(feed));
      }
      break;
    default:
      if (properties.allow3DArcs) {
        // make sure maximumCircularSweep is well below 360deg
        // we could use G2.4 or G3.4 - direction is calculated
        var ip = getPositionU(0.5);
        writeBlock(gAbsIncModal.format(90), gMotionModal.format(clockwise ? 2.4 : 3.4), xOutput.format(ip.x), yOutput.format(ip.y), zOutput.format(ip.z));
        writeBlock(xOutput.format(x), yOutput.format(y), zOutput.format(z), getFeed(feed));
      } else {
        linearize(tolerance);
      }
    }
  }
}

var currentCoolantMode = COOLANT_OFF;
var coolantOff = undefined;

function setCoolant(coolant) {
  var coolantCodes = getCoolantCodes(coolant);
  if (Array.isArray(coolantCodes)) {
    if (singleLineCoolant) {
      writeBlock(coolantCodes.join(getWordSeparator()));
    } else {
      for (var c in coolantCodes) {
        writeBlock(coolantCodes[c]);
      }
    }
    return undefined;
  }
  return coolantCodes;
}

function getCoolantCodes(coolant) {
  var multipleCoolantBlocks = new Array(); // create a formatted array to be passed into the outputted line
  if (!coolants) {
    error(localize("Coolants have not been defined."));
  }
  if (isProbeOperation()) { // avoid coolant output for probing
    coolant = COOLANT_OFF;
  }
  if (coolant == currentCoolantMode) {
    return undefined; // coolant is already active
  }
  if ((coolant != COOLANT_OFF) && (currentCoolantMode != COOLANT_OFF) && (coolantOff != undefined)) {
    if (Array.isArray(coolantOff)) {
      for (var i in coolantOff) {
        multipleCoolantBlocks.push(mFormat.format(coolantOff[i]));
      }
    } else {
      multipleCoolantBlocks.push(mFormat.format(coolantOff));
    }
  }

  var m;
  var coolantCodes = {};
  for (var c in coolants) { // find required coolant codes into the coolants array
    if (coolants[c].id == coolant) {
      coolantCodes.on = coolants[c].on;
      if (coolants[c].off != undefined) {
        coolantCodes.off = coolants[c].off;
        break;
      } else {
        for (var i in coolants) {
          if (coolants[i].id == COOLANT_OFF) {
            coolantCodes.off = coolants[i].off;
            break;
          }
        }
      }
    }
  }
  if (coolant == COOLANT_OFF) {
    m = !coolantOff ? coolantCodes.off : coolantOff; // use the default coolant off command when an 'off' value is not specified
  } else {
    coolantOff = coolantCodes.off;
    m = coolantCodes.on;
  }

  if (!m) {
    onUnsupportedCoolant(coolant);
    m = 9;
  } else {
    if (Array.isArray(m)) {
      for (var i in m) {
        multipleCoolantBlocks.push(mFormat.format(m[i]));
      }
    } else {
      multipleCoolantBlocks.push(mFormat.format(m));
    }
    currentCoolantMode = coolant;
    return multipleCoolantBlocks; // return the single formatted coolant value
  }
  return undefined;
}

var mapCommand = {
  COMMAND_STOP:0,
  COMMAND_OPTIONAL_STOP:1,
  COMMAND_END:2,
  COMMAND_SPINDLE_CLOCKWISE:3,
  COMMAND_SPINDLE_COUNTERCLOCKWISE:4,
  COMMAND_STOP_SPINDLE:5,
  COMMAND_ORIENTATE_SPINDLE:19,
  COMMAND_LOAD_TOOL:6
};

function onCommand(command) {
  switch (command) {
  case COMMAND_STOP:
    writeBlock(mFormat.format(0));
    forceSpindleSpeed = true;
    return;
  case COMMAND_START_SPINDLE:
    onCommand(tool.clockwise ? COMMAND_SPINDLE_CLOCKWISE : COMMAND_SPINDLE_COUNTERCLOCKWISE);
    return;
  case COMMAND_LOCK_MULTI_AXIS:
    if (useMultiAxisFeatures && !machineConfiguration.isMultiAxisConfiguration()) {
      if (hasABCAxis("A")) {
        writeBlock(mFormat.format(32));
      }
      if (hasABCAxis("B")) {
        writeBlock(mFormat.format(34));
      }
      if (hasABCAxis("C")) {
        writeBlock(mFormat.format(12));
      }
    } else {
      if (aOutput.isEnabled()) {
        writeBlock(mFormat.format(32));
      }
      if (bOutput.isEnabled()) {
        writeBlock(mFormat.format(34));
      }
      if (cOutput.isEnabled()) {
        writeBlock(mFormat.format(12));
      }
    }
    return;
  case COMMAND_UNLOCK_MULTI_AXIS:
    if (useMultiAxisFeatures && !machineConfiguration.isMultiAxisConfiguration()) {
      if (hasABCAxis("A")) {
        writeBlock(mFormat.format(33));
      }
      if (hasABCAxis("B")) {
        writeBlock(mFormat.format(35));
      }
      if (hasABCAxis("C")) {
        writeBlock(mFormat.format(13));
      }
    } else {
      if (aOutput.isEnabled()) {
        writeBlock(mFormat.format(33));
      }
      if (bOutput.isEnabled()) {
        writeBlock(mFormat.format(35));
      }
      if (cOutput.isEnabled()) {
        writeBlock(mFormat.format(13));
      }
    }
    return;
  case COMMAND_START_CHIP_TRANSPORT:
    writeBlock(mFormat.format(59));
    return;
  case COMMAND_STOP_CHIP_TRANSPORT:
    writeBlock(mFormat.format(61));
    return;
  case COMMAND_BREAK_CONTROL:
    return;
  case COMMAND_TOOL_MEASURE:
    return;
  case COMMAND_PROBE_ON:
    return;
  case COMMAND_PROBE_OFF:
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
  if (typeof inspectionProcessSectionEnd == "function") {
    inspectionProcessSectionEnd();
  }
  if (currentSection.isMultiAxis()) {
    writeBlock(mFormat.format(129));
    if (!isLastSection()) {
      writeBlock(mFormat.format(31)); // rotary axes encoder reset
    }
  }
  writeBlock(gPlaneModal.format(17));
  if (!isLastSection() && (getNextSection().getTool().coolant != tool.coolant)) {
    setCoolant(COOLANT_OFF);
  }
  if (((getCurrentSectionId() + 1) >= getNumberOfSections()) ||
      (tool.number != getNextSection().getTool().number)) {
    onCommand(COMMAND_BREAK_CONTROL);
  }

  if (isProbeOperation()) {
    writeBlock(gFormat.format(65), "P" + 9833); // spin the probe off
    setProbingAngle(); // define rotation of part
  }
  forceAny();
}

/** Output block to do safe retract and/or move to home position. */
function writeRetract() {
  if (arguments.length == 0) {
    error(localize("No axis specified for writeRetract()."));
    return;
  }
  var words = []; // store all retracted axes in an array
  for (var i = 0; i < arguments.length; ++i) {
    let instances = 0; // checks for duplicate retract calls
    for (var j = 0; j < arguments.length; ++j) {
      if (arguments[i] == arguments[j]) {
        ++instances;
      }
    }
    if (instances > 1) { // error if there are multiple retract calls for the same axis
      error(localize("Cannot retract the same axis twice in one line"));
      return;
    }
    switch (arguments[i]) {
    case X:
      words.push("X" + xyzFormat.format(machineConfiguration.hasHomePositionX() ? machineConfiguration.getHomePositionX() : 0));
      break;
    case Y:
      words.push("Y" + xyzFormat.format(machineConfiguration.hasHomePositionY() ? machineConfiguration.getHomePositionY() : 0));
      break;
    case Z:
      if (useMultiAxisFeatures) {
        writeBlock(gFormat.format(0), mFormat.format(140));
      } else {
        words.push("Z" + xyzFormat.format(machineConfiguration.getRetractPlane()));
      }
      zOutput.reset();
      retracted = true; // specifies that the tool has been retracted to the safe plane
      break;
    default:
      error(localize("Bad axis specified for writeRetract()."));
      return;
    }
  }
  if (words.length > 0) {
    gMotionModal.reset();
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), gMotionModal.format(0), words); // retract
  }
}

function onClose() {
  setCoolant(COOLANT_OFF);

  /*
  if (useMultiAxisFeatures && !is3D()) {
    writeBlock(gFormat.format(0), mFormat.format(140)); // retract
    writeBlock(
      gFormat.format(68.2),
      xOutput.format(0), yOutput.format(0), zOutput.format(0),
      "I" + ijkFormat.format(1), "J" + ijkFormat.format(0), "K" + ijkFormat.format(0),
      "U" + ijkFormat.format(0), "V" + ijkFormat.format(1), "W" + ijkFormat.format(0)
    );
    forceXYZ();
    gMotionModal.reset();
    writeBlock(
      gMotionModal.format(0), gFormat.format(8.2),
      xOutput.format(0), yOutput.format(0), zOutput.format(0),
      "I" + ijkFormat.format(0), "J" + ijkFormat.format(0), "K" + ijkFormat.format(1)
    );
  } else {
    writeBlock(gAbsIncModal.format(90), gFormat.format(53), "Z" + xyzFormat.format(0)); // retract
  }
*/

  writeRetract(Z);
  zOutput.reset();

  writeRetract(X, Y);
  
  onCommand(COMMAND_UNLOCK_MULTI_AXIS);
  writeBlock(gFormat.format(69)); // cancel frame
  writeBlock(mFormat.format(31)); // rotary axes encoder reset
  
  writeBlock(
    gMotionModal.format(0),
    conditional(machineConfiguration.isMachineCoordinate(0), "A" + abcFormat.format(0)),
    conditional(machineConfiguration.isMachineCoordinate(1), "B" + abcFormat.format(0)),
    conditional(machineConfiguration.isMachineCoordinate(2), "C" + abcFormat.format(0))
  );

  onCommand(COMMAND_LOCK_MULTI_AXIS);

  if (forceMultiAxisIndexing || !is3D() || machineConfiguration.isMultiAxisConfiguration()) {
    writeBlock(mFormat.format(127)); // cancel shortest path traverse
  }

  onCommand(COMMAND_STOP_CHIP_TRANSPORT);
  onImpliedCommand(COMMAND_END);
  onImpliedCommand(COMMAND_STOP_SPINDLE);
  writeBlock(mFormat.format(2)); // end of program, stop spindle, coolant off
  writeln("E");
}

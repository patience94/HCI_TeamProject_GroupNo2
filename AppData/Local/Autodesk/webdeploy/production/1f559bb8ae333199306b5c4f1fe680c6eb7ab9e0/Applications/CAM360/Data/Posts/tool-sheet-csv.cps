/**
  Copyright (C) 2012-2018 by Autodesk, Inc.
  All rights reserved.

  Tool sheet CSV configuration.

  $Revision: 42473 905303e8374380273c82d214b32b7e80091ba92e $
  $Date: 2019-09-04 00:46:02 $
  
  FORKID {BEBD3A50-28C9-4d8f-B6BE-9AE2EC3214D9}
*/

description = "Tool Sheet CSV";
vendor = "Autodesk";
vendorUrl = "http://www.autodesk.com";
legal = "Copyright (C) 2012-2018 by Autodesk, Inc.";
certificationLevel = 2;

longDescription = "Setup sheet for exporting relevant info for each tool to an CSV file which can be imported easily into other applications like a spreadsheet.";

capabilities = CAPABILITY_SETUP_SHEET;
extension = "csv";
mimetype = "plain/csv";
setCodePage("ascii");

allowMachineChangeOnSection = true;

properties = {
  decimal: ".", // decimal symbol
  separator: ";", // field separator
  rapidFeed: 5000 // the rapid traversal feed
};

// user-defined property definitions
propertyDefinitions = {
  decimal: {title:"Decimal symbol", description:"Defines the decimal symbol.", type:"string"},
  separator: {title:"Separator symbol", description:"Defines the field separator.", type:"string"},
  rapidFeed: {title:"Rapid feed", description:"Specifies the rapid traversal feed.", type:"number"}
};

var feedFormat = createFormat({decimals:(unit == MM ? 0 : 2)});
var toolFormat = createFormat({decimals:0});
var rpmFormat = createFormat({decimals:0});
var secFormat = createFormat({decimals:3});
var angleFormat = createFormat({decimals:0, scale:DEG});
var pitchFormat = createFormat({decimals:3});
var spatialFormat = createFormat({decimals:3});
var taperFormat = angleFormat; // share format

function quote(text) {
  var result = "";
  for (var i = 0; i < text.length; ++i) {
    var ch = text.charAt(i);
    switch (ch) {
    case "\\":
    case "\"":
      result += "\\";
    }
    result += ch;
  }
  return "\"" + result + "\"";
}

function formatCycleTime(cycleTime) {
  cycleTime += 0.5; // round up
  var seconds = cycleTime % 60 | 0;
  var minutes = ((cycleTime - seconds) / 60 | 0) % 60;
  var hours = (cycleTime - minutes * 60 - seconds) / (60 * 60) | 0;
  return subst("%1:%2:%3", hours, minutes, seconds);
}

function onSection() {
  skipRemainingSection();
}

function onClose() {
  feedFormat.setDecimalSymbol(properties.decimal);
  secFormat.setDecimalSymbol(properties.decimal);
  angleFormat.setDecimalSymbol(properties.decimal);
  pitchFormat.setDecimalSymbol(properties.decimal);
  spatialFormat.setDecimalSymbol(properties.decimal);

  var s = properties.separator;
  writeln(["TOOL #", "DIAMETER #", "LENGTH #", "TYPE", "COMMENT", "DIAMETER", "CORNER RADIUS", "ANGLE", "BODY LENGTH", "FLUTE #", "MAXIMUM FEED", "MAXIMUM SPINDLE SPEED", "FEED DISTANCE", "RAPID DISTANCE", "CYCLE TIME"].join(s));
  
  var tools = getToolTable();
  if (tools.getNumberOfTools() > 0) {
    for (var i = 0; i < tools.getNumberOfTools(); ++i) {
      var tool = tools.getTool(i);

      var record = "T" + toolFormat.format(tool.number);
      record += s + "D" + toolFormat.format(tool.diameterOffset);
      record += s + "L" + toolFormat.format(tool.lengthOffset);
      record += s + quote(getToolTypeName(tool.type));
      if (tool.comment) {
        record += s + quote(tool.comment);
      } else {
        record += s;
      }
      record += s + spatialFormat.format(tool.diameter);
      if (tool.cornerRadius) {
        record += s + spatialFormat.format(tool.cornerRadius);
      } else {
        record += s;
      }
      if ((tool.taperAngle > 0) && (tool.taperAngle < Math.PI)) {
        record += s + taperFormat.format(tool.taperAngle);
      } else {
        record += s;
      }
      record += s + spatialFormat.format(tool.bodyLength);
      record += s + spatialFormat.format(tool.numberOfFlutes);

      if (tool.type != TOOL_PROBE) {
        var maximumFeed = 0;
        var maximumSpindleSpeed = 0;
        var cuttingDistance = 0;
        var rapidDistance = 0;
        var cycleTime = 0;
        for (var j = 0; j < getNumberOfSections(); ++j) {
          var section = getSection(j);
          if (section.getTool().number == tool.number) {
            maximumFeed = Math.max(maximumFeed, section.getMaximumFeedrate());
            maximumSpindleSpeed = Math.max(maximumSpindleSpeed, section.getMaximumSpindleSpeed());
            cuttingDistance += section.getCuttingDistance();
            rapidDistance += section.getRapidDistance();
            cycleTime += section.getCycleTime();
          }
        }
        if (properties.rapidFeed > 0) {
          cycleTime += rapidDistance / properties.rapidFeed * 60;
        }
        
        record += s + feedFormat.format(maximumFeed);
        record += s + maximumSpindleSpeed;
        record += s + spatialFormat.format(cuttingDistance);
        record += s + spatialFormat.format(rapidDistance);
        record += s + formatCycleTime(cycleTime);
      }

      writeln(record);
    }
  }
}

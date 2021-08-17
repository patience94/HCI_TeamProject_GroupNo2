import adsk.core
import math
import os
from xml.etree import ElementTree as et

# config for footprint sketch
sketchNameForFootprintPads = 'Pad'
sketchNameForFootprintSilkscreen = 'Silkscreen'
sketchNameForFootprintText = 'Text'
TEXT_ALIGNMENT = {
    "TOP_CENTER": "top-center",
    "BOTTOM_CENTER": "bottom-center",
}

drawLayers = ['1', '21', '25', '27']

isConstructionPadOutlines = True
isFixedPadOutlines = True

def convertMMtoCM(val, design):
    assert design, "Design is not found. Unit conversion cannot be performed."
    return design.unitsManager.convert(val, 'mm', 'cm')

def getRotationMatrix(angle, axis, origin):
    mat = adsk.core.Matrix3D.create()
    mat.setToRotation(math.radians(angle), axis, origin)
    return mat

def makeFixedSketchOutlines(sketchObjs):
    for sketchObj in sketchObjs:
        sketchObj.isFixed = True

def makeConstructionSketchOutlines(sketchObjs):
    for sketchObj in sketchObjs:
        sketchObj.isConstruction = True

def drawTwoPointRectangle(sketch, x, y, w, h, angle, isConstruction = False, isFixed = False):
    topLeftCorner = adsk.core.Point3D.create(x - w / 2, y - h / 2, 0)
    bottomRightCorner = adsk.core.Point3D.create(x + w / 2, y + h / 2, 0)

    if angle != None:
        rotMat = getRotationMatrix(float(angle[1:]), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(x, y, 0))
        topLeftCorner.transformBy(rotMat)
        bottomRightCorner.transformBy(rotMat)

    sketchLines = sketch.sketchCurves.sketchLines
    sketchLines.addTwoPointRectangle(topLeftCorner, bottomRightCorner)
    
    if isConstruction:
        makeConstructionSketchOutlines(sketchLines)

    if isFixed:
        makeFixedSketchOutlines(sketchLines)

def drawCircleByCenterRadius(sketch, center, radius, isConstruction = False, isFixed = False):
    sketchCircles = sketch.sketchCurves.sketchCircles
    sketchCircles.addByCenterRadius(center, radius)

    if isConstruction:
        makeConstructionSketchOutlines(sketchCircles)

    if isFixed:
        makeFixedSketchOutlines(sketchCircles)

def drawPadWithRoundCorner(sketch, x, y, w, h, roundness, angle, isConstruction = False, isFixed = False):
    topLeftCorner = adsk.core.Point3D.create(x - w / 2, y - h / 2, 0)
    topRightCorner = adsk.core.Point3D.create(x + w / 2, y - h / 2, 0)
    bottomRightCorner = adsk.core.Point3D.create(x + w / 2, y + h / 2, 0)
    bottomLeftCorner = adsk.core.Point3D.create(x - w / 2, y + h / 2, 0)

    if angle != None:
        rotMat = getRotationMatrix(float(angle[1:]), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(x, y, 0))
        topLeftCorner.transformBy(rotMat)
        topRightCorner.transformBy(rotMat)
        bottomRightCorner.transformBy(rotMat)
        bottomLeftCorner.transformBy(rotMat)

    sketchLines = sketch.sketchCurves.sketchLines
    topLine = sketchLines.addByTwoPoints(topLeftCorner, topRightCorner)
    rightLine = sketchLines.addByTwoPoints(topRightCorner, bottomRightCorner)
    bottomLine = sketchLines.addByTwoPoints(bottomRightCorner, bottomLeftCorner)
    leftLine = sketchLines.addByTwoPoints(bottomLeftCorner, topLeftCorner)

    lines = []
    lines.append(topLine)
    lines.append(rightLine)
    lines.append(bottomLine)
    lines.append(leftLine)

    filletRadius = min(w / 2, h / 2) * roundness / 100
    sketchArcs = sketch.sketchCurves.sketchArcs
    
    arcs = []
    arcs.append(sketchArcs.addFillet(topLine, topLine.endSketchPoint.geometry, rightLine, rightLine.startSketchPoint.geometry, filletRadius))
    arcs.append(sketchArcs.addFillet(rightLine, rightLine.endSketchPoint.geometry, bottomLine, bottomLine.startSketchPoint.geometry, filletRadius))
    arcs.append(sketchArcs.addFillet(bottomLine, bottomLine.endSketchPoint.geometry, leftLine, leftLine.startSketchPoint.geometry, filletRadius))
    arcs.append(sketchArcs.addFillet(leftLine, leftLine.endSketchPoint.geometry, topLine, topLine.startSketchPoint.geometry, filletRadius))

    if isConstruction:
        makeConstructionSketchOutlines(lines)
        makeConstructionSketchOutlines(arcs)

    if isFixed:
        makeFixedSketchOutlines(lines)
        makeFixedSketchOutlines(arcs)

def drawSmdPad(smd, sketch, design):
    x = convertMMtoCM(float(smd['x']), design)
    y = convertMMtoCM(float(smd['y']), design)
    w = convertMMtoCM(float(smd['dx']), design)
    h = convertMMtoCM(float(smd['dy']), design)
    angle = smd.get('rot')
    roundness = smd.get('roundness')
    
    if roundness != None:
        roundness = int(roundness)

        # Circular pad (Eagle uses roundness 100% for circular pad exported from cio-datamodel)
        if w == h and roundness == 100: 
            padCenter = adsk.core.Point3D.create(x, y, 0)
            drawCircleByCenterRadius(sketch, padCenter, w / 2, isConstructionPadOutlines, isFixedPadOutlines)
        # Oblong Pad    
        else:
            drawPadWithRoundCorner(sketch, x, y, w, h, roundness, angle, isConstructionPadOutlines, isFixedPadOutlines)
    else:    
        drawTwoPointRectangle(sketch, x, y, w, h, angle, isConstructionPadOutlines, isFixedPadOutlines)

def drawPthPad(pad, sketch, design):
    x = convertMMtoCM(float(pad['x']), design)
    y = convertMMtoCM(float(pad['y']), design)
    drillRadius = convertMMtoCM(float(pad['drill']), design) / 2
    padRadius = convertMMtoCM(float(pad['diameter']), design) / 2
    padShape = pad.get('shape')
    angle = pad.get('rot')
    padCenter = adsk.core.Point3D.create(x, y, 0)

    # Draw drill outlines
    if drillRadius != 0:
        drawCircleByCenterRadius(sketch, padCenter, drillRadius, isConstructionPadOutlines, isFixedPadOutlines)

    # Draw pad outlines
    # Square Pad
    if padShape != None and padShape == 'square':
        drawTwoPointRectangle(sketch, x, y, 2 * padRadius, 2 * padRadius, angle, isConstructionPadOutlines, isFixedPadOutlines)
    # Circular Pad    
    else:
        drawCircleByCenterRadius(sketch, padCenter, padRadius, isConstructionPadOutlines, isFixedPadOutlines)

def drawWire(wire, sketch, design):
    if wire['layer'] not in drawLayers:
        return

    x1 = convertMMtoCM(float(wire['x1']), design)
    y1 = convertMMtoCM(float(wire['y1']), design)
    x2 = convertMMtoCM(float(wire['x2']), design)
    y2 = convertMMtoCM(float(wire['y2']), design)
    curve = wire.get('curve')

    p1 = adsk.core.Point3D.create(x1, y1, 0)
    p2 = adsk.core.Point3D.create(x2, y2, 0)

    if curve == None:
        sketchLines = sketch.sketchCurves.sketchLines
        line = sketchLines.addByTwoPoints(p1, p2)
        line.startSketchPoint.isFixed = True
        line.endSketchPoint.isFixed = True
        line.isFixed = True
    else:
        # p2 is start point and p1 is end point
        dy = y1 - y2
        dx = x1 - x2
        chordLength = math.sqrt(dx * dx + dy * dy)
        chordAngle = math.atan2(dy, dx)
        arcAngle = float(curve) * (math.pi / 180.0)
        radius = chordLength / (2.0 * math.sin(arcAngle / 2.0))
        startAngle = math.pi / 2.0 - arcAngle / 2.0 - chordAngle
        center = adsk.core.Point3D.create(x2 + radius * math.cos(startAngle), y2 - radius * math.sin(startAngle), 0)
        
        sketchArcs = sketch.sketchCurves.sketchArcs
        arc = sketchArcs.addByCenterStartSweep(center, p2, -arcAngle)
        arc.startSketchPoint.isFixed = True
        arc.endSketchPoint.isFixed = True
        arc.isFixed = True


def drawCircle(circle, sketch, design):
    if circle['layer'] not in drawLayers:
        return

    x = convertMMtoCM(float(circle['x']), design)
    y = convertMMtoCM(float(circle['y']), design)
    center = adsk.core.Point3D.create(x, y, 0)
    radius = convertMMtoCM(float(circle['radius']), design)

    drawCircleByCenterRadius(sketch, center, radius, False, True)

def drawText(text, value, sketch, design):
    if text['layer'] not in drawLayers:
        return

    x = convertMMtoCM(float(text['x']), design)
    y = convertMMtoCM(float(text['y']), design)
    height = convertMMtoCM(float(text['size']), design)
    position = adsk.core.Point3D.create(x, y, 0)

    if text['align'] == TEXT_ALIGNMENT["TOP_CENTER"]:
        position.y -= height

    sketchTexts = sketch.sketchTexts
    sketchText = sketchTexts.add(sketchTexts.createInput(value, height, position))
    textBBox = sketchText.boundingBox
    textWidth = abs(textBBox.maxPoint.x - textBBox.minPoint.x)

    #Following does not work - FUS-62545, FUS-62548
    #sketchText.position.translateBy(translation)
    #sketchText.isFixed = True

    # Use boundary lines to translate the text
    boundaryLines = sketchText.boundaryLines
    xTranslationDone = False
    translationX = adsk.core.Vector3D.create(-textWidth / 2, 0, 0)

    cnstraints = sketch.geometricConstraints

    for i in range(boundaryLines.count):
        boundaryLine = boundaryLines.item(i)

        # Apply translation on sketch points of horizontal boundary line to shift the text along x-axis
        # No need to apply translation on other horizontal boundary line
        if not xTranslationDone:
            startSketchPoint = boundaryLine.startSketchPoint
            endSketchPoint = boundaryLine.endSketchPoint

            startSketchPointWG = startSketchPoint.worldGeometry
            endSketchPointWG = endSketchPoint.worldGeometry

            if abs(startSketchPointWG.y - endSketchPointWG.y) < 1e-2:
                # make the boundary line horizontally constraint before applying translation to sketch point
                # BUG: FUS-62496
                cnstraints.addHorizontal(boundaryLine)
                
                startSketchPoint.move(translationX)
                endSketchPoint.move(translationX)
                xTranslationDone = True

        boundaryLine.isFixed = True

# def saveFootprintXML(xmlData):
#     path, filename = os.path.split(__file__)
#     xmlFile = open(path + "/footprint.xml", "w")
#     xmlFile.write(xmlData)
#     xmlFile.close()

def removeSketchByNameFromComponent(sketchName, targetComponent):
    targetSketch = targetComponent.sketches.itemByName(sketchName)

    if targetSketch:
        targetSketch.deleteMe()

def clearSilkscreen(sketchName, targetComponent):
    targetSketch = targetComponent.sketches.itemByName(sketchName)

    if targetSketch:
        count = targetSketch.sketchCurves.count

        for i in range(count - 1, -1, -1):
            targetSketch.sketchCurves.item(i).deleteMe()

def clearText(sketchName, targetComponent):
    targetSketch = targetComponent.sketches.itemByName(sketchName)

    if targetSketch:
        count = targetSketch.sketchTexts.count

        for i in range(count - 1, -1, -1):
            targetSketch.sketchTexts.item(i).deleteMe()

#https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
def generate(design, targetComponent, xmlData):
    #saveFootprintXML(xmlData)
    
    # remove existing footprint sketches for pads
    removeSketchByNameFromComponent(sketchNameForFootprintPads, targetComponent)

    # clear existing sketches under silkscreen and text
    # silkscreen and text sketches in package cannot be deleted directly in package generator mode
    # since these are set non-modifiable in package editor
    clearSilkscreen(sketchNameForFootprintSilkscreen, targetComponent)
    clearText(sketchNameForFootprintText, targetComponent)

    # Create a new sketches on the xy plane
    sketches = targetComponent.sketches
    xyPlane = targetComponent.xYConstructionPlane
    
    padSketch = sketches.add(xyPlane)
    padSketch.name = sketchNameForFootprintPads
    
    # Use existing silkscreen sketch (always exists in package document)
    silkscreenSketch = targetComponent.sketches.itemByName(sketchNameForFootprintSilkscreen)

    # Reuse text sketch if it exists otherwise create new
    textSketch = targetComponent.sketches.itemByName(sketchNameForFootprintText)
    if textSketch == None:
        textSketch = sketches.add(xyPlane)
        textSketch.name = sketchNameForFootprintText

    # Create sketch for 
    padSketch.isComputeDeferred = True
    silkscreenSketch.isComputeDeferred = True
    textSketch.isComputeDeferred = True

    root = et.fromstring(xmlData)
    packageElem = None

    for package in root.iter('package'):
        packageElem = package

        for smd in package.iter('smd'):
            drawSmdPad(smd.attrib, padSketch, design)

        for pad in package.iter('pad'):
            drawPthPad(pad.attrib, padSketch, design)

        for wire in package.iter('wire'):
            drawWire(wire.attrib, silkscreenSketch, design)

        for circle in package.iter('circle'):
            drawCircle(circle.attrib, silkscreenSketch, design)

        for text in package.iter('text'):
            drawText(text.attrib, text.text, textSketch, design)

    padSketch.isComputeDeferred = False
    silkscreenSketch.isComputeDeferred = False
    textSketch.isComputeDeferred = False

    #attach footprint xml data as attribute to the target component
    if packageElem != None:
        #extract only footprint xml to make Eagle library happy
        packageXmlString = et.tostring(packageElem, encoding='unicode') #unicode is used to get string instead of bytestring
        footprintName = packageElem.attrib['name']

        #attach attributes for footprint (used in Electron)
        targetComponent.attributes.add('footprint', 'xml', packageXmlString)
        targetComponent.attributes.add('footprint', 'name', footprintName)
        
        return footprintName

    return None

# if any of the footprint sketches not empty return True
def footprintExists(design):
    targetComponent = design.rootComponent
    
    # check for pads
    targetSketch = targetComponent.sketches.itemByName(sketchNameForFootprintPads)
    if targetSketch and targetSketch.sketchCurves.count > 0:
        return True
    else:
        # check for silkscreens
        targetSketch = targetComponent.sketches.itemByName(sketchNameForFootprintSilkscreen)
        if targetSketch and targetSketch.sketchCurves.count > 0:
            return True
        else:
            # check for texts
            targetSketch = targetComponent.sketches.itemByName(sketchNameForFootprintText)
            if targetSketch and targetSketch.sketchTexts.count > 0:
                return True
            else:
                return False
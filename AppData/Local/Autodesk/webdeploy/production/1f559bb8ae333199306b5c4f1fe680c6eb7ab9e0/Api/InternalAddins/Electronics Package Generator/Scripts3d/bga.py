import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance" :
            if param.createdBy.name=="TopBodyOffset":
                param.expression = 'param_A'
            if param.createdBy.name=="TopBody":
                param.expression = '-(param_A - param_b/2 + ((sign(param_b - ' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.015)) +')) * 1 ) * (param_b/2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.01)) + ') ) * 1/3'
            if param.createdBy.name=="MidBodyOffset":
                param.expression = 'param_A -(param_A - param_b/2 + ((sign(param_b - ' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.015)) +')) * 1 ) * (param_b/2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.01)) + ') ) * 1/3'
            if param.createdBy.name=="MidBody":
                param.expression = '-(param_A - param_b/2 + ((sign(param_b - ' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.015)) +')) * 1 ) * (param_b/2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.01)) + ') ) * 2/3'
            if param.createdBy.name=="TerminalOffset":
                param.expression = 'param_b/2 ' 
        if param.role=="countU" :
            if param.createdBy.name=="PinPattern":
                param.expression = 'param_EPins'
        if param.role=="CountV" :
            if param.createdBy.name=="PinPattern":
                param.expression = 'param_DPins'
        if param.role=="uSpaceDistance" :
            if param.createdBy.name=="PinPattern":
                param.expression = '-param_e'
        if param.role=="vSpaceDistance" :
            if param.createdBy.name=="PinPattern":
                param.expression = '-param_d'

def bga(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    #get the default unit of the system.  need consider to set the right unit. consider if user use the imperial unit.
    #define default value of the input paramters of diode. unit is mm
    A = params.get('A') or 0.1 #Body height(A)
    b = params.get('b') or 0.03 #Ball Diameter(b)
    D = params.get('D') or 0.62 #Body length(D)
    E = params.get('E') or 0.62 #Body width(E)
    d = params.get('d') or 0.05 #Horizontal ball pitch(d)
    e = params.get('e') or 0.05 #Vertical ball pitch(d)
    DPins = params.get('DPins') or 11 #Horizontal pins amount(DPins)
    EPins = params.get('EPins') or 11 #Vertical pins amount(DPins)
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    #Bottom body length(D1)
    D1 = D - 0.01
    #Bottom body width(E1)
    E1 = E - 0.01
    #default ball offset inside body
    b1 = 0.01
    #Ball diameter threshold
    b2 = 0.015
    #Update ball height
    if(b > b2):
        A1 = b - b1
    else:
        A1 = b1 = b/2

    #Top body height
    A2 = (A - A1) * 2/3
    #Bottom body height
    A3 = 0.5 * A2

    paddingD = (DPins - 1) * d / 2
    paddingE = (EPins - 1) * e/ 2
    offset = max(D, E)/15

    if is_parametric:
        isUpdate = False
        isUpdate =model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("BallDiameter", "ball diameter"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_d', d, default_unit, _LCLZ("HorizontalBallPitch", "horizontal ball pitch"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("VerticalBallPitch", "vertical ball pitch"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("VerticalBalls", "vertical balls"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("HorizontalBalls", "horizontal balls"))
        if isUpdate: return

    #Create body
    sketches = root_comp.sketches
    top_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    top_body_offset.name = 'TopBodyOffset'
    top_body_sketch = sketches.add(top_body_offset)
    top_body_sketch.name = 'TopBodySketch'
    E_param = 'param_E -'+ str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.01))
    D_param = 'param_D -'+ str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.01))
    model_3d_sketch.create_center_point_rectangle(top_body_sketch,adsk.core.Point3D.create(0, 0, 0) , '', '', adsk.core.Point3D.create(E1/2, D1/2, 0), E_param, D_param, is_parametric)
    ext_body = top_body_sketch.profiles.item(0)
    top_body = model_3d_feature.create_extrude(root_comp,ext_body, -A3 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    top_body.name = 'TopBody'
   
    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, top_body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    #Draw pin1 mark
    lines = top_body_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-E/2 + 0.3 , 0, 0))
    constraints = top_body_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, top_body_sketch.originPoint)
    offset_str = str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.03))
    if is_parametric:
        top_body_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-E/4 + 0.3, 0, 0)).parameter.expression = 'param_E/2 -' + offset_str

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-E/2 + 0.3 , D/2 - 0.3, 0))
    if is_parametric:
        top_body_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-E/4 + 0.3 , D/4 - 0.3, 0)).parameter.expression = 'param_D/2 -' + offset_str
    line2.isConstruction = True

    constraints.addHorizontal(line1)
    constraints.addVertical(line2)

    circles = top_body_sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(line2.endSketchPoint,b/2)
    top_body_sketch.sketchDimensions.addDiameterDimension(circle, adsk.core.Point3D.create(D/4,E/4,0), True).parameter.expression = 'param_b'
    ext_pin_one = top_body_sketch.profiles.item(1)
    pin_one = model_3d_feature.create_extrude(root_comp, ext_pin_one, -0.005, adsk.fusion.FeatureOperations.CutFeatureOperation)

    #Draw mid body
    mid_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A - A3)
    mid_body_offset.name = 'MidBodyOffset'
    mid_body_sketch = sketches.add(mid_body_offset)
    model_3d_sketch.create_center_point_rectangle(mid_body_sketch,adsk.core.Point3D.create(0, 0, 0) , '', '', adsk.core.Point3D.create(E/2, D/2, 0), 'param_E ', 'param_D ', is_parametric)
    ext_body = mid_body_sketch.profiles.item(0)
    mid_body = model_3d_feature.create_extrude(root_comp,ext_body, -A2 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    mid_body.name = 'MidBody'

    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, mid_body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)
    # assign the apparance to body
    model_3d_utility.apply_rgb_appearance(app, design, mid_body.bodies.item(0), 0, 77, 26, model_3d_utility.COLOR_NAME_BGA_MID_BODY)


    #Draw balls
    terminal_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, b/2 )
    terminal_offset.name = 'TerminalOffset'
    terminal_sketch = sketches.add(terminal_offset)
    terminal_sketch.name ='TerminalSketch'
    model_3d_sketch.create_center_point_circle(terminal_sketch,adsk.core.Point3D.create(paddingE , paddingD , 0), '((param_EPins - 1) * param_e) / 2', '((param_DPins - 1) * param_d) / 2', b, 'param_b', is_parametric)
    lines = terminal_sketch.sketchCurves.sketchLines;
    constraints = terminal_sketch.geometricConstraints
    line1 = lines.addByTwoPoints( adsk.core.Point3D.create(0, 0, 0) ,adsk.core.Point3D.create(paddingE + b/2 , 0, 0))
    line1.isConstruction = True
    line1.startSketchPoint.isFixed = True
    constraints.addHorizontal(line1)
    if is_parametric:
        terminal_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(E/2, 0, 0)).parameter.expression = '(param_EPins - 1) * param_e  / 2 + param_b/2 '

    line2 = lines.addByTwoPoints( line1.endSketchPoint,adsk.core.Point3D.create(paddingE + b/2, paddingD , 0))
    line2.isConstruction = True
    constraints.addVertical(line2)
    if is_parametric:
        terminal_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = '(param_DPins - 1) * param_d  / 2'

    axisLine = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(paddingE -b/2 , paddingD , 0))
    constraints.addHorizontal(axisLine)
    if is_parametric:
        terminal_sketch.sketchDimensions.addDistanceDimension(axisLine.startSketchPoint, axisLine.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = 'param_b'

    ext_term = terminal_sketch.profiles.item(0)
    # Create an revolution input
    revolves = root_comp.features.revolveFeatures
    rev_input = revolves.createInput(ext_term, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(2 * math.pi)
    rev_input.setAngleExtent(False, angle)
    ext_rev = revolves.add(rev_input)
    # assign pysical material to terminal
    model_3d_utility.apply_material(app, design, ext_rev.bodies.item(0), model_3d_utility.MATERIAL_ID_LEAD_SOLDER)

    pattern_pins = model_3d_feature.create_two_direction_pattern(root_comp, ext_rev, -e, EPins, root_comp.xConstructionAxis, -d, DPins, root_comp.yConstructionAxis)
    pattern_pins.name = 'PinPattern'

    if is_parametric:
        map_model_parameters(root_comp)

def run(context):
    ui = app.userInterface
    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, target_comp = None):
    bga(params, design, target_comp)

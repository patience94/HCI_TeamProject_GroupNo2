import adsk.core, adsk.fusion, traceback
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyOffset":
                param.expression = 'param_A'
            if param.createdBy.name=="Body":
                param.expression = '-param_A + param_E/2 - param_E1/2'
            if param.createdBy.name=="Terminal":
                param.expression = '(param_E - param_E1)/2'
            if param.createdBy.name=="TerminalSide":
                param.expression = 'param_E/4 - param_E1/4 + param_A/2'

        if param.role=="countU":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_DPins/2'
            if param.createdBy.name=="PinPattern2":
                param.expression = 'param_DPins/2'
        if param.role=="uSpaceDistance":
            if param.createdBy.name=="PinPattern1":
                param.expression = '-param_e'
            if param.createdBy.name=="PinPattern2":
                param.expression = '-param_e'

        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A/2 - param_E/4 + param_E1/4)/2'
        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A/2 - param_E/4 + param_E1/4)'

def oscillator_l(params, design = None, target_comp = None):

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
    A = params.get('A') or 0.47 #Body height(A)
    b = params.get('b') or 0.08 #Termianl width(b)
    D = params.get('D') or 1.42 #Body length(D)
    E = params.get('E') or 0.98 #Terminal span(E)
    E1 = params.get('E1') or 0.915 #Body width(E1)
    E2 = params.get('E2') or 0.762 #Terminal center - center distance
    e = params.get('e') or 0.508 #Pin pitch(e)
    L = E - E2 #Terminal length (L)
    DPins = params.get('DPins') or 4 #pins(DPins)
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    feetThickness = (E - E1)/2 #Feet thickness
    boxHeight = A - feetThickness #Box height
    boxChamfer = boxHeight/2 #Box chamfer
    gapHori = (D - (((DPins/2 - 1) * e) + b))/2

    if is_parametric:
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("TerminalSpan", "terminal span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_E2', E2, default_unit, _LCLZ("TerminalGapDistance", "terminal center - center distance"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("Pins", "pins"))

        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    #Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(E1/2, D/2, 0), 'param_E1', 'param_D', is_parametric)
    ext_body = body_sketch.profiles.item(0)
    body = model_3d_feature.create_extrude(root_comp,ext_body, -boxHeight , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, boxChamfer/2, boxChamfer)

    #Draw pin 1 marker
    circleRadius = 1/20 * E1
    lines = body_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-E1/2 + boxChamfer + circleRadius , 0, 0))
    constraints = body_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, body_sketch.originPoint)
    if is_parametric:
        body_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-E/2, 0, 0)).parameter.expression = 'param_E1/2 - param_A/2 + param_E/4 - param_E1/4 - param_E1/20'

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-E1/2 + 2 * boxChamfer + circleRadius , D/2 - boxChamfer - circleRadius, 0))
    if is_parametric:
        body_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-E/4  , D/2 , 0)).parameter.expression = 'param_D/2 - param_A/2 + param_E/4 - param_E1/4 - param_E1/20'
    line2.isConstruction = True

    constraints.addHorizontal(line1)
    constraints.addVertical(line2)

    circles = body_sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(line2.endSketchPoint,circleRadius)
    body_sketch.sketchDimensions.addDiameterDimension(circle, adsk.core.Point3D.create(E/2,D/2,0), True).parameter.expression = 'param_E1/10'
    ext_pin_one = body_sketch.profiles.item(1)
    pin_one = model_3d_feature.create_extrude(root_comp, ext_pin_one, -0.05, adsk.fusion.FeatureOperations.CutFeatureOperation)
    pin_one.name = 'Pin1'

    #Draw terminals
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch = sketches.add(xyPlane)
    model_3d_sketch.create_center_point_rectangle(pin_sketch, adsk.core.Point3D.create(E2/2 , (DPins/2 - 1) * e/2, 0),'param_E2/2','(param_DPins/2 - 1) * param_e/2',
                                                                                         adsk.core.Point3D.create(E/2 , (DPins/2 - 1) * e/2 + b/2, 0), 'param_E - param_E2', 'param_b', is_parametric)

    lines = pin_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, (DPins/2 - 1) * e/2 + b/2, 0))
    constraints = pin_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, pin_sketch.originPoint)
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(0, D/4, 0)).parameter.expression = '(param_DPins/2 - 1) * param_e/2 + param_b/2'

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(E/2 - feetThickness, (DPins/2 - 1) * e/2 + b/2, 0))
    line2.isConstruction = True
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = 'param_E1/2'

    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(E/2 - feetThickness, (DPins/2 - 1) * e/2 - b/2, 0))
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line3.startSketchPoint, line3.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = 'param_b'
    constraints.addVertical(line1)
    constraints.addHorizontal(line2)
    constraints.addVertical(line3)

    ter_ext = pin_sketch.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp,ter_ext, feetThickness, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'Terminal'
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    ter_ext_side = pin_sketch.profiles.item(1)
    terminal_side = model_3d_feature.create_extrude(root_comp,ter_ext_side, feetThickness + boxHeight/2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal_side.name = 'TerminalSide'
    model_3d_utility.apply_material(app, design, terminal_side.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal_side.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)


    pattern_pins_1 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal, e, DPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins_1.name = 'PinPattern1'

    pattern_pins_2 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal_side, e, DPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins_2.name = 'PinPattern2'
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
    oscillator_l(params, design, target_comp)

import adsk.core,traceback, adsk.fusion, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    offset_name = str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.005))
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyOffset":
                param.expression = 'param_A'
            if param.createdBy.name=="Body":
                param.expression = '-param_A +' + offset_name #need convert the value to default unit

        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamfer":
                param.expression = '0.1 * (param_A -' + offset_name + ')' #need convert the value to default unit

        if param.role=="countU":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_DPins/2'
            if param.createdBy.name=="PinPattern2":
                param.expression = 'param_DPins/2'
            if param.createdBy.name=="PinPattern3":
                param.expression = 'param_EPins/2'
            if param.createdBy.name=="PinPattern4":
                param.expression = 'param_EPins/2'

        if param.role=="uSpaceDistance":
            if param.createdBy.name=="PinPattern1":
                param.expression = '-param_e'
            if param.createdBy.name=="PinPattern2":
                param.expression = '-param_e'
            if param.createdBy.name=="PinPattern3":
                param.expression = '-param_e'
            if param.createdBy.name=="PinPattern4":
                param.expression = '-param_e'

def create_chamfer(root_comp, ext, distance):
    edge_top = adsk.core.ObjectCollection.create()
    top_face = ext.startFaces[0];
    top_edges = top_face.edges
    for edgeI  in top_edges:
        edge_top.add(edgeI)

    chamfer_feats = root_comp.features.chamferFeatures
    chamfer_top = chamfer_feats.createInput(edge_top, True)
    chamfer_top.setToEqualDistance(adsk.core.ValueInput.createByReal(distance))
    return chamfer_feats.add(chamfer_top)

def qfn(params, design = None, target_comp = None):

    e  =params.get('e') or 0.05 # pin pitch (e)
    L = params.get('L') or 0.04 # pin length(L)
    b = params.get('b') or 0.03 # pin width (b)
    E = params.get('D') or 0.51 # body length (D)
    D = params.get('E') or 0.41 # body width (E)
    A = params.get('A') or 0.1 # body height (A)
    EPins = params.get('DPins') or 8 * 2 # pin D side (DPins)
    DPins = params.get('EPins') or 6 * 2 # pin E side (EPins)
    epins = EPins/2
    E1 = params.get('D1') or 0.32 # Thermal pad length(D1)
    D1 = params.get('E1') or 0.42 # Thermal pad width(E1)
    thermal = params['thermal'] if 'thermal' in params else 0 #thermal pad boolean
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    offset_Dpins = (DPins/2 - 1) * e/2
    offset_Epins = (EPins/2 - 1) * e/2
    terminal_thickness =  0.005

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    if is_parametric:
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("PinLength", "pin length"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("PinWidth", "pin width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("DPins", "D pins"))
        is_update = model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("EPins", "E pins"))
        is_update = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("ThermalPadLength", "thermal pad length"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("ThermalPadWidth", "thermal pad width"))
        if is_update:
            thermal_pad = root_comp.features.itemByName('ThermalPad')
            if thermal:
                thermal_pad.isSuppressed = False
            else:
                thermal_pad.isSuppressed = True

            return

    #Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(E/2, D/2, 0), 'param_E', 'param_D', is_parametric)
    ext_body = body_sketch.profiles.item(0)
    body = model_3d_feature.create_extrude(root_comp,ext_body, -A + terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)
    body_chamfer = create_chamfer(root_comp, body, 0.1 * (A - terminal_thickness) )
    body_chamfer.name = 'BodyChamfer'
    #Draw pin1 mark
    lines = body_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-E/2 + 0.03 , 0, 0))
    constraints = body_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, body_sketch.originPoint)
    offset_name = str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.03))
    if is_parametric:
        body_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-E/4 + 0.03, 0, 0)).parameter.expression = 'param_E/2 -' +  offset_name

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-E/2 + 0.03 , D/2 - 0.03, 0))
    if is_parametric:
        body_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-E/4 + 0.3 , D/4 - 0.3, 0)).parameter.expression = 'param_D/2 -'+ offset_name
    line2.isConstruction = True

    constraints.addHorizontal(line1)
    constraints.addVertical(line2)

    circles = body_sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(line2.endSketchPoint,0.015)
    body_sketch.sketchDimensions.addDiameterDimension(circle, adsk.core.Point3D.create(-E/4,D/4,0), True).parameter.value = 0.03
    ext_pin_one = body_sketch.profiles.item(1)
    pin_one = model_3d_feature.create_extrude(root_comp, ext_pin_one, -0.01, adsk.fusion.FeatureOperations.CutFeatureOperation)

    #Create terminals
    #Draw D pins
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch = sketches.add(xyPlane)
    E_param = 'param_E/2 - param_L/2 +' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.0001))
    model_3d_sketch.create_center_point_rectangle(pin_sketch, adsk.core.Point3D.create(E/2 + 0.0001 - L/2, offset_Dpins, 0), E_param, '(param_DPins/2 - 1) * param_e/2',
                                                                                         adsk.core.Point3D.create(E/2 + 0.0001, offset_Dpins + b/2, 0), 'param_L', 'param_b', is_parametric)

    lines = pin_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, offset_Dpins + b/2, 0))
    constraints = pin_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, pin_sketch.originPoint)
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(0, D/4, 0)).parameter.expression = '(param_DPins/2 - 1) * param_e/2 + param_b/2'

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(E/2, offset_Dpins + b/2, 0))
    line2.isConstruction = True
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/4, 0)).parameter.expression = 'param_E/2'

    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(E/2, offset_Dpins - b/2, 0))
    if is_parametric:
        pin_sketch.sketchDimensions.addDistanceDimension(line3.startSketchPoint, line3.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = 'param_b'
    constraints.addVertical(line1)
    constraints.addHorizontal(line2)
    constraints.addVertical(line3)


    circle = model_3d_sketch.create_center_point_circle(pin_sketch, adsk.core.Point3D.create(E/2 - L + b/2, offset_Dpins , 0),'param_E/2 - param_L + param_b/2', '(param_DPins/2 - 1) * param_e/2',
                                                                                                                             b, 'param_b', is_parametric)
    circle.trim(adsk.core.Point3D.create(E/2, D/2, 0))

    ter_ext_side = pin_sketch.profiles.item(3)
    terminal_side = model_3d_feature.create_extrude(root_comp,ter_ext_side, terminal_thickness + 0.01 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal_side.name = 'TerminalSideD'
    model_3d_utility.apply_material(app, design, terminal_side.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal_side.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)


    ter_ext = pin_sketch.profiles.item(3)
    terminal = model_3d_feature.create_extrude(root_comp,ter_ext,terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'TerminalD'
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)


    pattern_pins1 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal, e, DPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins1.name = 'PinPattern1'
    pattern_pins2 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal_side, e, DPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins2.name = 'PinPattern2'

    #Draw E pins
    sketch_pin = sketches.add(xyPlane)
    D_param = 'param_D/2 - param_L/2 +' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.0001))
    model_3d_sketch.create_center_point_rectangle(sketch_pin, adsk.core.Point3D.create(offset_Epins, D/2 + 0.0001 - L/2, 0),'(param_EPins/2 - 1) * param_e/2 ',D_param,
                                                                                         adsk.core.Point3D.create(offset_Epins + b/2, D/2 + 0.0001 , 0), 'param_b', 'param_L', is_parametric)

    lines = sketch_pin.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(offset_Epins + b/2, 0, 0))
    constraints = sketch_pin.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, sketch_pin.originPoint)
    if is_parametric:
        sketch_pin.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/4, 0, 0)).parameter.expression = '(param_EPins/2 - 1) * param_e/2 + param_b/2'

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(offset_Epins + b/2, D/2, 0))
    line2.isConstruction = True
    if is_parametric:
        sketch_pin.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/4, 0)).parameter.expression = 'param_D/2'

    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(offset_Epins - b/2, D/2, 0))
    if is_parametric:
        sketch_pin.sketchDimensions.addDistanceDimension(line3.startSketchPoint, line3.endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(E/2, D/2, 0)).parameter.expression = 'param_b'
    constraints.addHorizontal(line1)
    constraints.addVertical(line2)
    constraints.addHorizontal(line3)

    circle = model_3d_sketch.create_center_point_circle(sketch_pin, adsk.core.Point3D.create(offset_Epins, D/2 - L + b/2 , 0),'(param_EPins/2 - 1) * param_e/2', 'param_D/2 - param_L + param_b/2',
                                                                                                                             b, 'param_b', is_parametric)
    circle.trim(adsk.core.Point3D.create(E/2, D/2, 0))

    ter_ext_side = sketch_pin.profiles.item(3)
    terminal_side = model_3d_feature.create_extrude(root_comp,ter_ext_side, terminal_thickness + 0.01 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal_side.name = 'TerminalSideE'
    model_3d_utility.apply_material(app, design, terminal_side.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal_side.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)


    ter_ext = sketch_pin.profiles.item(3)
    terminal = model_3d_feature.create_extrude(root_comp,ter_ext,terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'TerminalE'
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    pattern_pins3 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal, e, EPins/2, root_comp.xConstructionAxis, root_comp.xZConstructionPlane)
    pattern_pins3.name = 'PinPattern3'
    pattern_pins4 = model_3d_feature.create_mirror_and_pattern(root_comp, terminal_side, e, EPins/2, root_comp.xConstructionAxis, root_comp.xZConstructionPlane)
    pattern_pins4.name = 'PinPattern4'
    #draw thermal pad
    model_3d_utility.create_thermal_pad(app, root_comp, 0, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(E1/2, D1/2, 0), 'param_E1', 'param_D1', terminal_thickness, thermal, is_parametric)

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
    qfn(params, design, target_comp)

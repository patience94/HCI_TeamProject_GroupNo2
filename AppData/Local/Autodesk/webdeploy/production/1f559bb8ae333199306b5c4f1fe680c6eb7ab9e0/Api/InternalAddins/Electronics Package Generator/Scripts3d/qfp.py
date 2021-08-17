import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_feature
from .Utils import model_3d_sketch
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def mapModelParameter(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneXy":
                param.expression = 'param_A1'
            if param.createdBy.name=="FrontPinPlaneXz":
                param.expression = 'param_ee1/2 * (param_DPins/2-1)'
            if param.createdBy.name=="LeftPinPlaneXz":
                param.expression = '-param_ee1/2 * (param_EPins/2-1)'
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            if param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            if param.createdBy.name=="FrontPin":
                param.expression = 'param_b'
            if param.createdBy.name=="LeftPin":
                param.expression = 'param_b'
            if param.createdBy.name=="ThermalPad":
                param.expression = 'param_A1'

        if param.role=="uSpaceDistance":
            param.expression = '-param_ee1'
        if param.role=="countU":
            if param.createdBy.name=="PinPattern":
                param.expression = 'param_DPins/2'
            else:
                param.expression = 'param_EPins/2'
        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
            else:
                param.expression = 'param_A/10'
        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
            else:
                param.expression = 'param_A/10'

def qfp(params, design = None, targetComponent = None):
    A = params.get('A') or 0.12 #body height
    A1 = params['A1'] if 'A1' in params else 0.005 #body offset
    b = params.get('b') or 0.027 #terminal width
    D = params.get('D') or 1.31 #span2
    D1 = params.get('D1') or 1.02 #body length
    E = params.get('E') or 1.31 #span1
    E1 = params.get('E1') or 1.02 #ody width
    ee1 = params.get('e') or 0.05 #lower case e in front
    #ee2 = params.get('ee2') or 0.05 #lower case e in back
    ee3 = params.get('e') or 0.05 #ower case e in left
    #ee4 = params.get('ee4') or 0.05 #lower case e in right
    L = params.get('L') or 0.103
    DPins= params.get('DPins') or 32
    EPins = params.get('EPins') or 32
    thermal = params['thermal'] if 'thermal' in params else 0 #flag
    is_parametric = params['is_parametric'] if 'is_parametric' in params else 1
    E2 = params.get('E2') or 0.7
    D2 = params.get('D2') or 0.7

    terminal_thickness = 0.02
    front_feet_num = DPins/2
    leftFeetNum = EPins/2

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

    if is_parametric:
        unitsMgr = design.unitsManager
        default_unit = unitsMgr.defaultLengthUnits
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span")+'1')
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("Span", "span")+'2')
        is_update = model_3d_utility.process_user_param(design, 'param_ee1', ee1, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalLand", "terminal land"))
        is_update = model_3d_utility.process_user_param(design, 'param_D2', D2, default_unit, _LCLZ("ThermalPadLength", "thermal pad length"))
        is_update = model_3d_utility.process_user_param(design, 'param_E2', E2, default_unit, _LCLZ("ThermalPadWidth", "thermal pad width"))
        is_update = model_3d_utility.process_user_param(design, 'param_terminalThickness', terminal_thickness, default_unit, _LCLZ("TerminalThickness", "terminal thickness"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("DSidePins", "D side pins"))
        is_update = model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("ESidePins", "E side pins"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update:
            thermal_pad = root_comp.features.itemByName('ThermalPad')
            if thermal:
                thermal_pad.isSuppressed = False
            else:
                thermal_pad.isSuppressed = True
            return

    # Create a construction plane by offset
    sketches = root_comp.sketches

    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    sketch_body = sketches.add(body_plane_xy)

    front_pin_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, ee1/2 * (front_feet_num-1))
    front_pin_plane_xz.name = 'FrontPinPlaneXz'
    sketch_front_pin = sketches.add(front_pin_plane_xz)

    left_pin_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, -ee1/2 * (leftFeetNum-1))
    left_pin_plane_xz.name = 'LeftPinPlaneXz'
    sketch_left_pin = sketches.add(left_pin_plane_xz)

    extrudes = root_comp.features.extrudeFeatures

    #create body and apply material
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(E1/2,D1/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, '', '', end_point, 'param_E1', 'param_D1', is_parametric)
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(A-A1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer
    chamfer_distance1 = (A - A1-terminal_thickness)/2
    chamfer_distance = 0.2*(A - A1-terminal_thickness)
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_distance1, chamfer_distance)

    #build pin front and back
    lead_slope =  math.tan(math.pi/15) * (A/2-terminal_thickness/2)
    body_center_z = (A+A1)/2

    model_3d_sketch.create_gull_wing_lead(sketch_front_pin, E, 'param_E/2', E1, 'param_E1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_front_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    front_pin = extrudes.add(ext_input)
    front_pin.name = 'FrontPin'
    model_3d_utility.apply_material(app, design, front_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, front_pin.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    pattern_pins = model_3d_feature.create_mirror_and_pattern(root_comp, front_pin, ee1, front_feet_num, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins.name = 'PinPattern'

    #build pin left and right
    model_3d_sketch.create_gull_wing_lead(sketch_left_pin, D, 'param_D/2', D1, 'param_D1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_left_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    left_pin = extrudes.add(ext_input)
    left_pin.name = 'LeftPin'
    model_3d_utility.apply_material(app, design, left_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, left_pin.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(left_pin.bodies.item(0))
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(math.pi/2, adsk.core.Vector3D.create(0,0,1), adsk.core.Point3D.create(0,0,0))
    # Create a move feature
    move_feats = root_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform)
    moved_pin = move_feats.add(move_feature_input)
    # Create mirror and pattern for moved pin
    mirrored_left_pin = model_3d_feature.create_mirror(root_comp, left_pin.bodies.item(0), root_comp.xZConstructionPlane)
    model_3d_feature.create_one_direction_pattern(root_comp, left_pin.bodies.item(0), -ee3, leftFeetNum, root_comp.xConstructionAxis)
    model_3d_feature.create_one_direction_pattern(root_comp, mirrored_left_pin.bodies.item(0), -ee3, leftFeetNum, root_comp.xConstructionAxis)

    #draw thermal pad
    if A1 == 0:
        A1 = terminal_thickness
    model_3d_utility.create_thermal_pad(app, root_comp, 0, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(E2/2, D2/2, 0), 'param_E2', 'param_D2', A1, thermal, is_parametric)

    #pin one body marking
    model_3d_utility.create_pin_one_mark(root_comp, A, 'param_A', D1, 'param_D1', E1, 'param_E1', is_parametric)

    #map model param to user parameters
    if is_parametric:
        mapModelParameter(root_comp)

def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, targetComponent = None):
    qfp(params, design, targetComponent)

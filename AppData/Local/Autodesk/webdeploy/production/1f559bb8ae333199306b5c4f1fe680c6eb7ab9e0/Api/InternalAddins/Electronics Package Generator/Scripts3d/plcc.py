import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_feature
from .Utils import model_3d_sketch
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameter(root_comp):
    terminal_thickness_name = str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD))

    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneXy":
                param.expression = 'param_A1'
            if param.createdBy.name=="PinPathPlaneXz":
                param.expression = '((param_DPins/2 - 1)*param_e)/2'
            if param.createdBy.name=="PinPathPlaneYz":
                param.expression = '-((param_EPins/2 - 1)*param_e)/2'
            if param.createdBy.name=="Body":
                param.expression = 'param_A-param_A1'
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            if param.createdBy.name=="DpinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="DpinBodyBottom":
                param.expression = 'param_b/2'
            if param.createdBy.name=="EpinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="EpinBodyBottom":
                param.expression = 'param_b/2'
        if param.role=="AgainstDistance":
            if param.createdBy.name=="DpinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="DpinBodyBottom":
                param.expression = 'param_b/2'
            if param.createdBy.name=="EpinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="EpinBodyBottom":
                param.expression = 'param_b/2'

        if param.role=="uSpaceDistance":
            param.expression = 'param_e'

        if param.role=="countU":
            if param.createdBy.name=="PinPatternD":
                param.expression = 'param_DPins/2'
            if param.createdBy.name=="PinPatternE":
                param.expression = 'param_EPins/2'

        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '(param_A - param_A1 -'+ terminal_thickness_name + ')/2'
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '0.2*(param_A - param_A1 -' + terminal_thickness_name + ')'

        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A - param_A1 -'+ terminal_thickness_name + ')/2'
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '0.2*(param_A - param_A1 -' + terminal_thickness_name + ')'

        if param.role == 'Diameter Dimension-3':
            if param.createdBy.name=='Dpin_path_sketch' or param.createdBy.name== 'Epin_path_sketch':
                param.expression = 'param_E - param_E2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD*2))

        if param.role == 'Linear Dimension-5':
            if param.createdBy.name=='Dpin_path_sketch' or param.createdBy.name== 'Epin_path_sketch':
                param.expression = 'param_A/2 + param_A1/2 +' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD/2))

def plcc(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits


    A = params.get('A') or 0.357    # body height(A)
    A1 = params['A1'] if 'A1' in params else 0.051  # body offset from seating plane (A1)
    b = params.get('b') or 0.043   # terminal width (b)
    e = params.get('e') or 0.127    # pin pitch (e)
    D = params.get('D') or 1.2445    # terminal span (D side)
    D1 = params.get('D1') or 1.15     # body length (D)
    D2 = params.get('D2') or 1.06   # weld space (D side)
    E = params.get('E') or 1.2445    # terminal span (E)
    E1 = params.get('E1') or 1.15  # body width (E1)
    E2 = params.get('E2') or 1.06   # weld space (E side)

    DPins = params.get('DPins') or 7*2 # Total pins amount on D side
    EPins = params.get('EPins') or 7*2 # Total pins amount on E side

    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    if is_parametric:
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("ESideSpan", "E side span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_E2', E2, default_unit, _LCLZ("ESideWeldSpace", "E side weld space"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("DSideSpan", "D side span"))
        is_update = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_D2', D2, default_unit, _LCLZ("DSideWeldSpace", "D side weld space"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("DSidePins", "D side pins"))
        is_update = model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("ESidePins", "E side pins"))

        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    sketches = root_comp.sketches

    # Step1 create D side pin plane and sketches
    pin_path_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, ((DPins/2 - 1)*e)/2 )
    pin_path_plane_xz.name = 'PinPathPlaneXz'
    Dpin_path_sketch = sketches.add(pin_path_plane_xz)
    Dpin_path_sketch.name = 'DpinPathSketch'

    #create D pins profile
    model_3d_sketch.create_j_lead(Dpin_path_sketch, E1, 'param_E1', E, 'param_E', E2, 'param_E2', A, 'param_A', A1, 'param_A1', is_parametric)
    Dpin_bottom_profile = Dpin_path_sketch.profiles.item(0)
    Dpin_side_profile = Dpin_path_sketch.profiles.item(1)

    # Step2 create the D pin body
    extrudes = root_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(Dpin_side_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    extent_distance_1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b))
    extent_distance_2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b/2))
    extrude_input.setTwoSidesExtent(extent_distance_1,extent_distance_1)
    Dpin_extru_side_body = extrudes.add(extrude_input)
    Dpin_extru_side_body.name = 'DpinBodySide'

    extrude_input = extrudes.createInput(Dpin_bottom_profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    extrude_input.setTwoSidesExtent(extent_distance_2,extent_distance_2)
    Dpin_extru_bottom_body = extrudes.add(extrude_input)
    Dpin_extru_bottom_body.name = 'DpinBodyBottom'

    #step5 move D pin to the right position.
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(Dpin_extru_bottom_body.bodies.item(0))
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(math.pi/2, adsk.core.Vector3D.create(0,0,1), adsk.core.Point3D.create(0,0,0))
    # Create a move feature
    move_feats = root_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform)
    moved_pin = move_feats.add(move_feature_input)

    #assign the material to terminal
    model_3d_utility.apply_material(app, design, Dpin_extru_bottom_body.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, Dpin_extru_bottom_body.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    # Step3 create E side pin plane and sketches
    pin_path_plane_yz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, -((EPins/2 - 1)*e)/2 )
    pin_path_plane_yz.name = 'PinPathPlaneYz'
    Epin_path_sketch = sketches.add(pin_path_plane_yz)
    Epin_path_sketch.name = 'EpinPathSketch'

    #create E pins profile
    model_3d_sketch.create_j_lead(Epin_path_sketch, D1, 'param_D1', D, 'param_D', D2, 'param_D2', A, 'param_A', A1, 'param_A1', is_parametric)
    Epin_bottom_profile = Epin_path_sketch.profiles.item(0)
    Epin_side_profile = Epin_path_sketch.profiles.item(1)

    #Step 4 create E pin body
    extrude_input = extrudes.createInput(Epin_side_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setTwoSidesExtent(extent_distance_1,extent_distance_1)
    Epin_extru_side_body = extrudes.add(extrude_input)
    Epin_extru_side_body.name = 'EpinBodySide'

    extrude_input = extrudes.createInput(Epin_bottom_profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    extrude_input.setTwoSidesExtent(extent_distance_2,extent_distance_2)
    Epin_extru_bottom_body = extrudes.add(extrude_input)
    Epin_extru_bottom_body.name = 'EpinBodyBottom'

    #assign the material to terminal
    model_3d_utility.apply_material(app, design, Epin_extru_bottom_body.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, Epin_extru_bottom_body.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)


    #step6: create construction plane to generate the body sketch
    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    body_sketch = sketches.add(body_plane_xy)
    body_sketch.name = 'BodySketch'

    #step7: create the body
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0,0,0), '', '', adsk.core.Point3D.create(E1/2,D1/2,0), 'param_D1','param_E1',  is_parametric)
    ext_body = model_3d_feature.create_extrude(root_comp,body_sketch.profiles.item(0), A-A1 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    ext_body.name = 'Body'
    model_3d_utility.apply_material(app, design, ext_body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer
    chamfer_distance = (A - A1 - model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)/2
    chamfer_distance1 = 0.2*(A - A1 - model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)
    model_3d_feature.create_start_end_face_chamfer(root_comp, ext_body, chamfer_distance1, chamfer_distance)

    # Step 8. create pin mirror and Pattern for D side pins
    pattern_pins_d = model_3d_feature.create_mirror_and_pattern(root_comp, Dpin_extru_bottom_body.bodies.item(0), e, DPins/2, root_comp.xConstructionAxis, root_comp.xZConstructionPlane)
    pattern_pins_d.name = 'PinPatternD'

    # Step 9. create pin mirror and Pattern for E side pins
    pattern_pins_e = model_3d_feature.create_mirror_and_pattern(root_comp, Epin_extru_bottom_body.bodies.item(0), e, EPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins_e.name = 'PinPatternE'

    #pin one body marking
    pin_one_mark_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    pin_one_mark_plane_xy.name = 'PinOneMarkPlaneXy'
    pin_one_mark_sketch = root_comp.sketches.add(pin_one_mark_plane_xy)

    pin_one_mark_sketch.isComputeDeferred = True
    mark_radius = E/30
    circle_origin = adsk.core.Point3D.create(-(D/2- E/10-mark_radius) ,-0.1, 0)
    sketch_point = pin_one_mark_sketch.sketchPoints.add(circle_origin)
    pin_one_mark_sketch.sketchCurves.sketchCircles.addByCenterRadius(sketch_point, mark_radius)
    if is_parametric:
        pin_one_mark_sketch.sketchDimensions.addRadialDimension(pin_one_mark_sketch.sketchCurves[0],
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_E/30'
        pin_one_mark_sketch.sketchDimensions.addDistanceDimension(sketch_point, pin_one_mark_sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = ' (1.01 + floor(param_EPins/4) - ceil(param_EPins/4))*param_e/2'
        pin_one_mark_sketch.sketchDimensions.addDistanceDimension(sketch_point, pin_one_mark_sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_D/2- param_A/10- param_E/10'

    pin_one_mark_sketch.isComputeDeferred = False
    prof = pin_one_mark_sketch.profiles[0]
    pin_one_mark = root_comp.features.extrudeFeatures.addSimple(prof, adsk.core.ValueInput.createByReal(-A*0.1), adsk.fusion.FeatureOperations.CutFeatureOperation)
    pin_one_mark.name = 'PinOneMark'
    #map model param to user parameters
    if is_parametric:
        map_model_parameter(root_comp)


def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, target_comp = None):
    plcc(params, design, target_comp)

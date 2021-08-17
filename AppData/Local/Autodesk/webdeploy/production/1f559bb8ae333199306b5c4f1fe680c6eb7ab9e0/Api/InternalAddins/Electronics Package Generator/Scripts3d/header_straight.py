import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_feature
from .Utils import model_3d_sketch
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameter(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneYz":     
                param.expression = '(-param_D+param_d*(param_DPins-1))/2'
            if param.createdBy.name=="PinPlaneXy":
                param.expression = '-param_L1'
            if param.createdBy.name=="BodySlotPlaneXy":
                param.expression = 'param_L'    
            elif param.createdBy.name=="Body":
                param.expression = 'param_D'
            elif param.createdBy.name=="Pin":
                param.expression = 'param_L+param_L1+param_L2'    
        if param.role=="countU":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_DPins'
        if param.role=="countU":
            if param.createdBy.name=="PinPattern2":
                param.expression = 'param_DPins-1' 
        if param.role=="CountV":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_EPins'
        if param.role=="vSpaceDistance":
            if param.createdBy.name=="PinPattern1":
                param.expression = '-param_e'     
        if param.role=="uSpaceDistance":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_d'
            if param.createdBy.name=="PinPattern2": 
                param.expression = 'param_d'      
        if param.role=="rightDistance":
            if param.createdBy.name=="body_chamfer_top" or param.createdBy.name=="body_chamfer_bottom" :
                param.expression = 'param_d/5'
            else:
                param.expression = 'param_b/1.5'    
        if param.role=="leftDistance":
            if param.createdBy.name=="body_chamfer_top" or param.createdBy.name=="body_chamfer_bottom" :
                param.expression = 'param_d/5'
            else:
                param.expression = 'param_b/4'      

def header_straight(params, design = None, targetComponent = None):
    b = params.get('b') or 0.064 #Terminal thickness
    D = params.get('D') or 1.016 #Lead Span
    d = params.get('d') or 0.254 #pitch along D
    E = params.get('E') or 0.556 #Body length
    e = params.get('e') or 0.254 #pitch along E
    L = params.get('L') or 0.254 #body height
    L1 = params.get('L1') or 0.3 #terminal tail length
    L2 = params.get('L2') or 0.584 #terminal post length
    DPins = params.get('DPins') or 4 #Total pins along D
    EPins = params.get('EPins') or 2 #Total pins along E

    origin_location_id = params['originLocationId'] if 'originLocationId' in params else 0
    is_parametric = params['isParametric'] if 'isParametric' in params else 1


    origin_y = -e*(EPins-1)/2
    pattern_distance_E = -e
    pattern_distance_D = d

    padding_E = (E-e*(EPins-1))     
    padding_D = (D-d*(DPins-1))/2
    chamfer_size = min(e, d, E, L)/5

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

        #Get the current transform of the occurrence
        if design.snapshots.count !=0:
            snapshot = design.snapshots.item(0)
            snapshot.deleteMe()
        component_acc = design.rootComponent.allOccurrencesByComponent(root_comp).item(0)
        transform = component_acc.transform
        # Change the transform data by moving x and y
        if origin_location_id == 1:
            transform.translation = adsk.core.Vector3D.create(-d*(DPins-1), -e*(EPins-1)/2, 0)
        elif origin_location_id == 2:
            transform.translation = adsk.core.Vector3D.create(-d*(DPins-1), e*(EPins-1)/2, 0)
        elif origin_location_id == 3:
            transform.translation = adsk.core.Vector3D.create(0, e*(EPins-1), 0)
        elif origin_location_id == 4:
            transform.translation = adsk.core.Vector3D.create(-d*(DPins-1)/2, e*(EPins-1)/2, 0)   
        else:
            transform.translation = adsk.core.Vector3D.create(0, 0, 0)         
        # Set the transform data back to the occurrence
        design.rootComponent.allOccurrencesByComponent(root_comp).item(0).transform = transform
        if design.snapshots.hasPendingSnapshot:
            design.snapshots.add()

    if is_parametric:  
        units = design.unitsManager
        mm = units.defaultLengthUnits
        is_updated = False
        is_updated = model_3d_utility.process_user_param(design, 'param_E', E, mm, _LCLZ("BodyLength", "body length"))
        is_updated = model_3d_utility.process_user_param(design, 'param_d', d, mm, _LCLZ("PitchAlongD", "pitch along D"))
        is_updated = model_3d_utility.process_user_param(design, 'param_D', D, mm, _LCLZ("LeadSpan", "lead span"))
        is_updated = model_3d_utility.process_user_param(design, 'param_e', e, mm, _LCLZ("PitchAlongE", "pitch along E"))
        is_updated = model_3d_utility.process_user_param(design, 'param_b', b, mm, _LCLZ("TerminalThickness", "terminal thickness"))
        is_updated = model_3d_utility.process_user_param(design, 'param_L', L, mm, _LCLZ("BodyHeight", "body height"))
        is_updated = model_3d_utility.process_user_param(design, 'param_L1', L1, mm, _LCLZ("TerminalTailLength", "terminal tail length"))
        is_updated = model_3d_utility.process_user_param(design, 'param_L2', L2, mm, _LCLZ("TerminalPostLength", "terminal post length"))
        is_updated = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("PinsAlongD", "pins along D"))
        is_updated = model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("PinsAlongE", "pins along E"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process. 
        if is_updated: return

    # Create a new sketch on the xy plane.
    sketches = root_comp.sketches

    body_plane_yz = model_3d_utility.create_offset_plane(root_comp,root_comp.yZConstructionPlane, 0)
    body_plane_yz.name = 'BodyPlaneYz'
    sketch_body = sketches.add(body_plane_yz)
    sketch_body.name = 'SketchBody'

    pin_plane_xy = model_3d_utility.create_offset_plane(root_comp,root_comp.xYConstructionPlane, -L1)
    pin_plane_xy.name = 'PinPlaneXy'
    sketch_pin = sketches.add(pin_plane_xy)
    sketch_pin.name = 'SketchPin'

    body_slot_plane_xy = model_3d_utility.create_offset_plane(root_comp,root_comp.xYConstructionPlane, L)
    body_slot_plane_xy.name = 'BodySlotPlaneXy'
    sketch_body_slot = sketches.add(body_slot_plane_xy)
    sketch_body_slot.name = 'SketchBodySlot'

    extrudes = root_comp.features.extrudeFeatures

    #create pin and apply material
    pinLength = L1+L+L2

    sketch_pin.isComputeDeferred = True
    lines = sketch_pin.sketchCurves.sketchLines
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(b/2,-b/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_pin, center_point, '', '', end_point, 'param_b', 'param_b', is_parametric)
    sketch_pin.isComputeDeferred = False
    prof = sketch_pin.profiles[0]
    pin = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(pinLength), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    pin.name = 'Pin'
    model_3d_utility.apply_material(app, design, pin.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    model_3d_utility.apply_appearance(app, design, pin.bodies.item(0), model_3d_utility.APPEARANCE_ID_GOLD_POLISHED)
    
    #chamfer pin
    start_face = pin.startFaces[0]
    end_face = pin.endFaces[0]
    model_3d_feature.create_face_chamfer(root_comp, start_face, b/4, b/1.5)   
    model_3d_feature.create_face_chamfer(root_comp, end_face, b/4, b/1.5) 
    pattern_pins1 = model_3d_feature.create_two_direction_pattern(root_comp, pin.bodies.item(0), pattern_distance_D, DPins, root_comp.xConstructionAxis, pattern_distance_E, EPins, root_comp.yConstructionAxis)
    pattern_pins1.name = 'PinPattern1'

    end_point = adsk.core.Point3D.create(-L, padding_E/2, 0)    
    center_point = adsk.core.Point3D.create(-L/2, origin_y, 0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, 'param_L/2', 'param_E/2-(param_E-param_e*(param_EPins-1))/2', end_point, 'param_L', 'param_E', is_parametric)
    
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(D), adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
    body.name = 'Body'
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_size, chamfer_size)
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_PBT_PLASTIC)
    model_3d_utility.apply_appearance(app, design, body.bodies.item(0), model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)

    #chamfer slots on body between pins
    sketch_body_slot.isComputeDeferred = True
    a = math.sqrt(2*chamfer_size*chamfer_size)
    lines = sketch_body_slot.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(d/2-chamfer_size, -E+padding_E/2, 0), adsk.core.Point3D.create(d/2+chamfer_size, -E+padding_E/2, 0))
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(d/2, -E+padding_E/2+chamfer_size, 0))
    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(d/2-chamfer_size, -E+padding_E/2, 0))
    if is_parametric:
        sketch_body_slot.sketchDimensions.addDistanceDimension(lines.item(2).startSketchPoint, sketch_body_slot.originPoint,
                                                            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                            adsk.core.Point3D.create(0, 1, 0)).parameter.expression = 'param_d/2'
        sketch_body_slot.sketchDimensions.addDistanceDimension(lines.item(0).startSketchPoint, sketch_body_slot.originPoint,
                                                            adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                            adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_E - (param_E-param_e*(param_EPins-1))/2'
    constraints = sketch_body_slot.geometricConstraints
    constraints.addEqual(lines.item(1), lines.item(2))
    constraints.addHorizontal(lines.item(0))
    
    sketch_body_slot.isComputeDeferred = False

    sweep_prof = sketch_body_slot.profiles[0]
    sweeps = root_comp.features.sweepFeatures
    path_data = adsk.core.ObjectCollection.create()
    #isChained i.e collection of profile path
    for index in range (sketch_body.sketchCurves.sketchLines.count-2):
        path_data.add(sketch_body.sketchCurves.sketchLines.item(index))
    path = root_comp.features.createPath(path_data)
    sweep_input = sweeps.createInput(sweep_prof, path, adsk.fusion.FeatureOperations.CutFeatureOperation)
    body_slot = sweeps.add(sweep_input)

    pattern_pins2 = model_3d_feature.create_one_direction_pattern(root_comp, body_slot, d, (DPins-1), root_comp.xConstructionAxis)
    pattern_pins2.name = 'PinPattern2'

    # move body plane to adjust as per DPins
    if not is_parametric:
        for param in root_comp.modelParameters:
            if param.role=="AlongDistance":
                if param.createdBy.name=="BodyPlaneYz":
                    param.value = -padding_D
                    
    if is_parametric:
        #map model param to user parameters
        map_model_parameter(root_comp)


def run(context):
    ui = app.userInterface
     
    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, targetComponent = None):
    header_straight(params, design, targetComponent)

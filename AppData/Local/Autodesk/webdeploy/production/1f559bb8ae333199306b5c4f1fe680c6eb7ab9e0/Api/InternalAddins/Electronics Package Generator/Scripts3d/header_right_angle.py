import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_feature
from .Utils import model_3d_sketch
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def add_fillet(root_comp, edges_collection, radius):
    fillets = root_comp.features.filletFeatures

    fillet_input = fillets.createInput()  
    fillet_input.addConstantRadiusEdgeSet(edges_collection, radius, True)
    fillet_input.isG2 = False
    fillet_input.isRollingBallCorner = True
    
    return fillets.add(fillet_input)

def add_ra_pin_fillet(root_comp, pin, terminal_thickness):
    brep = pin.bodies.item(0)
    outer_radius = adsk.core.ValueInput.createByReal(terminal_thickness*1.5)
    edges_collection1 = adsk.core.ObjectCollection.create()

    start_face = pin.startFaces[0]
    s_edges = start_face.edges

    end_face = pin.endFaces[0]
    e_edges = end_face.edges

    for edge in brep.edges:
        if edge.length == terminal_thickness and edge not in s_edges and edge not in e_edges and edge not in brep.convexEdges:
            edges_collection1.add(edge)
            fillet1 = add_fillet(root_comp, edges_collection1, outer_radius)      

    inner_radius = adsk.core.ValueInput.createByReal(terminal_thickness/2)
    edges_collection2 = adsk.core.ObjectCollection.create()
    for edge in brep.convexEdges:
        inner_edge = edge 
    edges_collection2.add(inner_edge)
    add_fillet(root_comp, edges_collection2, inner_radius)     

   
def create_ra_pin(root_comp, design, sketch_pin, path, EPins, DPins, e, d, L, b, is_parametric):
    #RA pin
    
    row = EPins + 1
    timeline = design.timeline
    pin_count = timeline.timelineGroups.count
    row = row - pin_count

    while row > 1:
        
        start_index = timeline.markerPosition
        count = sketch_pin.profiles.count
        row = row - 1
    
        sketch_pin.isComputeDeferred = True
        lines = sketch_pin.sketchCurves.sketchLines
        center_point = adsk.core.Point3D.create(0, -e*(EPins-row), 0)
        end_point = adsk.core.Point3D.create(b/2,-e*(EPins-row)-b/2,0)
        model_3d_sketch.create_center_point_rectangle(sketch_pin, center_point, '', 'param_e*'+ str(count), end_point, 'param_b', 'param_b', is_parametric)
        sketch_pin.isComputeDeferred = False

        prof = sketch_pin.profiles[count]
        sweeps = root_comp.features.sweepFeatures
        sweep_input = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        pin = sweeps.add(sweep_input)
        add_ra_pin_fillet(root_comp, pin, b)
        model_3d_utility.apply_material(app, design, pin.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
        model_3d_utility.apply_appearance(app, design, pin.bodies.item(0), model_3d_utility.APPEARANCE_ID_GOLD_POLISHED)
  
        model_3d_feature.create_face_chamfer(root_comp, pin.startFaces[0], b/4, b/1.5)
        model_3d_feature.create_face_chamfer(root_comp, pin.endFaces[0], b/4, b/1.5)
        model_3d_feature.create_one_direction_pattern(root_comp, pin.bodies.item(0), d, DPins, root_comp.xConstructionAxis)

        end_index = timeline.markerPosition
        group = timeline.timelineGroups
        group.add(start_index, end_index-1)

def map_model_parameter(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneYz":      
                param.expression = '(-param_D+param_d*(param_DPins-1))/2'
            elif param.createdBy.name=="PinPlaneXy":
                param.expression = '-param_L1'
            elif param.createdBy.name=="PinPathPlaneYz":
                param.expression = '(-param_D+param_d*(param_DPins-1))/2'    
            elif param.createdBy.name=="BodySlotPlaneXy":
                param.expression = 'param_E'
            elif param.createdBy.name=="Body":
                param.expression = 'param_D'          
        if param.role=="countU":
            if param.createdBy.name=="ChamferPattern":
                param.expression = 'param_DPins-1'
            else:
                param.expression = 'param_DPins'
        if param.role=="CountV":
            param.expression = 'param_EPins'
        if param.role=="vSpaceDistance":
            if param.createdBy.name=="CutPattern":
                param.expression = 'param_e'     
        if param.role=="uSpaceDistance":
            param.expression = 'param_d'      
        if param.role=="rightDistance":
            if param.createdBy.name!="body_chamfer_top" and param.createdBy.name!="body_chamfer_bottom":
                param.expression = 'param_b/1.5'   
        if param.role=="leftDistance":
            if param.createdBy.name!="body_chamfer_top" and param.createdBy.name!="body_chamfer_bottom":
                param.expression = 'param_b/4'


def header_right_angle(params, design = None, targetComponent = None):
    b = params.get('b') or 0.064 #Terminal thickness
    D = params.get('D') or 1.016 #Lead Span
    d = params.get('d') or 0.254 #pitch along D
    E = params.get('E') or 0.556 #Body length
    e = params.get('e') or 0.254 #pitch along E
    L = params.get('L') or 0.254 #body height
    L1 = params.get('L1') or 0.152 #terminal tail length
    L2 = params['L2'] if 'L2' in params else 0.584 #terminal post length
    L3 = params['L3'] if 'L3' in params else 0.24 #tail length below right angle body
    DPins = params['DPins'] if 'DPins' in params else 4 #Total pins along D
    EPins = params['EPins'] if 'EPins' in params else 2 #Total pins along E

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
        timeline = design.timeline
        group_count = timeline.timelineGroups.count
        sketch = root_comp.sketches.itemByName('SketchPin')
        path_sketch = root_comp.sketches.itemByName('SketchPinPath')
        
        if EPins < group_count:
            while EPins < group_count:
                
                timeline.timelineGroups[group_count-1].deleteMe(True)
                group_count = timeline.timelineGroups.count

                
                line_count = sketch.sketchCurves.sketchLines.count

                while line_count-6 < sketch.sketchCurves.sketchLines.count:
                    c = sketch.sketchCurves.sketchLines.count
                    sketch.sketchCurves.sketchLines[c-1].deleteMe()
        
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
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, mm, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_d', d, mm, _LCLZ("PitchAlongD", "pitch along D"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, mm, _LCLZ("LeadSpan", "lead span"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, mm, _LCLZ("PitchAlongE", "pitch along E"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, mm, _LCLZ("TerminalThickness", "terminal thickness"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, mm, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_L1', L1, mm, _LCLZ("TerminalTailLength", "terminal tail length"))
        is_update = model_3d_utility.process_user_param(design, 'param_L2', L2, mm, _LCLZ("TerminalPostLength", "terminal post length"))
        is_update = model_3d_utility.process_user_param(design, 'param_L3', L3, mm, _LCLZ("TailLengthBelowRightAngleBody", "tail length below right angle body"))
        
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("PinsAlongD", "pins along D"))
        is_update = model_3d_utility.process_user_param(design, 'param_EPins', EPins, '', _LCLZ("PinsAlongE", "pins along E"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process. 
        if is_update:
            if targetComponent and  EPins > group_count : 
                if sketch != None:
                   while EPins > group_count: 
                        line1 = path_sketch.sketchCurves.sketchLines[0]
                        path = root_comp.features.createPath(line1)
                        create_ra_pin(root_comp, design, sketch, path, EPins, DPins, e, d, L, b, is_parametric)
                        group_count = timeline.timelineGroups.count
                map_model_parameter(root_comp)
            return

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

    pin_path_plane_yz = model_3d_utility.create_offset_plane(root_comp,root_comp.yZConstructionPlane, -padding_D)
    pin_path_plane_yz.name = 'PinPathPlaneYz'
    sketch_pin_path = sketches.add(pin_path_plane_yz)
    sketch_pin_path.name = 'SketchPinPath'

    body_slot_plane_xy = model_3d_utility.create_offset_plane(root_comp,root_comp.xYConstructionPlane, E)
    body_slot_plane_xy.name = 'BodySlotPlaneXy'
    sketch_body_slot = sketches.add(body_slot_plane_xy)
    sketch_body_slot.name = 'SketchBodySlot'

    extrudes = root_comp.features.extrudeFeatures

    #right angle pin path
    sketch_pin_path.isComputeDeferred = True
    sketchLines = sketch_pin_path.sketchCurves.sketchLines
    line1 = sketchLines.addByTwoPoints(adsk.core.Point3D.create(L3, 0, 0), adsk.core.Point3D.create(-e*(EPins-1)-padding_E/2, 0, 0))
    line2 = sketchLines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-e*(EPins-1)-padding_E/2, -L2-L-L1-e*(EPins-1), 0))

    if is_parametric:
        constraints = sketch_pin_path.geometricConstraints
        constraints.addPerpendicular(line1, line2)
        constraints.addVertical(line2)
        constraints.addCoincident(sketch_pin_path.originPoint, line1)
        sketch_pin_path.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch_pin_path.originPoint,
                                                    adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_L3'
        sketch_pin_path.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_e*(param_EPins-1) + param_L + param_L1 + param_L2'                                         
        sketch_pin_path.sketchDimensions.addDistanceDimension( line2.endSketchPoint, sketch_pin_path.originPoint,
                                                    adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_e*(param_EPins-1) + (param_E - param_e*(param_EPins-1))/2'                                             
    sketch_pin_path.isComputeDeferred = False
    path = root_comp.features.createPath(line1)

    #RA pin
    create_ra_pin(root_comp, design, sketch_pin, path, EPins, DPins, e, d, L, b, is_parametric)

    #create body and apply material
    end_point = adsk.core.Point3D.create(-E, -L-L1-e*(EPins-1), 0)
    center_point = adsk.core.Point3D.create(-E/2, -L/2-L1-e*(EPins-1), 0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, 'param_E/2',  'param_L/2+param_L1+param_e*(param_EPins-1)', end_point, 'param_E', 'param_L', is_parametric)

    prof = sketch_body.profiles[0]

    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(D), adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
    body.name = 'Body'

    body_chamfer = model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_size, chamfer_size) 
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_PBT_PLASTIC)
    model_3d_utility.apply_appearance(app, design, body.bodies.item(0), model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)
    
    #chamfer slots on body between pins
    sketch_body_slot.isComputeDeferred = True
    a = math.sqrt(2*chamfer_size*chamfer_size)
    lines = sketch_body_slot.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(d/2-chamfer_size, -E+padding_E/2, 0), adsk.core.Point3D.create(d/2+chamfer_size, -E+padding_E/2, 0))
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(d/2, -E+padding_E/2-chamfer_size, 0))
    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(d/2-chamfer_size, -E+padding_E/2, 0))
    if is_parametric:
        sketch_body_slot.sketchDimensions.addDistanceDimension(lines.item(2).startSketchPoint, sketch_body_slot.originPoint,
                                                            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                            adsk.core.Point3D.create(0, 1, 0)).parameter.expression = 'param_d/2'
        sketch_body_slot.sketchDimensions.addDistanceDimension(lines.item(0).startSketchPoint, sketch_body_slot.originPoint,
                                                            adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                            adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_L1 + param_e*(param_EPins-1)'
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

    chamfer_pattern = model_3d_feature.create_one_direction_pattern(root_comp, body_slot, d, (DPins-1), root_comp.xConstructionAxis)
    chamfer_pattern.name = 'ChamferPattern'

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
    header_right_angle(params, design, targetComponent)
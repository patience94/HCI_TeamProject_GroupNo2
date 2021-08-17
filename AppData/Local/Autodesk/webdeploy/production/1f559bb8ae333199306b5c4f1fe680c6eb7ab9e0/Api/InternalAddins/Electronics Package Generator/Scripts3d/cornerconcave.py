import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance" :
            if param.createdBy.name=="BodyOffset":
                param.value = 0.001
            if param.createdBy.name=="Body":
                param.expression = '0.8 * param_A -'+ str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.001)) #need convert the value to default unit
            if param.createdBy.name=="TopBodyOffset":
                param.expression = 'param_A'
            if param.createdBy.name=="TopBody":
                param.expression = '-0.2 * param_A'

def cornerconcave(params, design = None, target_comp= None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    A =  params.get('A') or 0.2 #Body height(A)
    D =  params.get('D') or 0.65 #Body length(D)
    D1 =  params.get('D!') or 0.3
    E =  params.get('E') or 0.4 #Body width(E)
    E1 =  params.get('E1') or 0.15
    EPins = 4 #Total pins amt
    c = 0.001
    leftFeetNum = EPins/2
    circleRadius = (D - D1)/10
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    #Terminal thickness
    if('terminalThickness' not in params):
        terminal_thickness = c
    else:
        if(terminal_thickness < 0):
            terminal_thickness = c
        else:
            terminal_thickness = min(terminal_thickness, c)

    #Horizontal terminal width(b)
    if ('b' not in params):
        b = (D - D1 * (leftFeetNum - 1))/leftFeetNum
        #Vertical terminal width(b1)
    if ('b1' not in params):
        b1 = (E - E1 * (leftFeetNum - 1))/leftFeetNum

    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        if isUpdate: return

    # Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, terminal_thickness)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    body_sketch.name = 'BodySketch'
    model_3d_sketch.create_center_point_rectangle(body_sketch,adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(D/2, E/2, 0), 'param_D', 'param_E', is_parametric)

    circle_top = model_3d_sketch.create_center_point_circle(body_sketch, adsk.core.Point3D.create(D/2, E/2, 0),'param_D/2', 'param_E/2',  circleRadius * 2, '(param_D - param_D1)/5', is_parametric)
    circle_top.trim(adsk.core.Point3D.create(D/2, E/2, 0))

    circle_bottom = model_3d_sketch.create_center_point_circle(body_sketch, adsk.core.Point3D.create(D/2, -E/2, 0) ,'param_D/2', 'param_E/2',  circleRadius * 2, '(param_D - param_D1)/5', is_parametric)
    circle_bottom.trim(adsk.core.Point3D.create(D/2, -E/2, 0))

    circle = model_3d_sketch.create_center_point_circle(body_sketch, adsk.core.Point3D.create(-D/2, -E/2, 0) ,'param_D/2', 'param_E/2',  circleRadius * 2, '(param_D - param_D1)/5', is_parametric)
    #circle.trim(adsk.core.Point3D.create(-D/2, -E/2, 0))

    circle = model_3d_sketch.create_center_point_circle(body_sketch, adsk.core.Point3D.create(-D/2, E/2, 0) ,'param_D/2', 'param_E/2',  circleRadius * 2, '(param_D - param_D1)/5', is_parametric)
    #circle.trim(adsk.core.Point3D.create(-D/2, E/2, 0))

    ext_body = body_sketch.profiles.item(5)
    body = model_3d_feature.create_extrude(root_comp,ext_body, 0.8 * A - terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    body.name = 'Body'
    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
    # assign the apparance to body
    model_3d_utility.apply_appearance(app, design, body.bodies.item(0), model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)
    
    #rendering lower body
    body_side = body.bodies.item(0)
    for face in body_side.faces:
        if face.geometry.objectType == adsk.core.Cylinder.classType():
            model_3d_utility.apply_appearance(app, design, face, model_3d_utility.APPEARANCE_ID_GOLD_POLISHED)


    #Creating top body
    top_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    top_body_offset.name = 'TopBodyOffset'
    top_body_sketch = sketches.add(top_body_offset)
    model_3d_sketch.create_center_point_rectangle(top_body_sketch,adsk.core.Point3D.create(0, 0, 0) , '', '',  adsk.core.Point3D.create(0.9 * D/2, 0.9 * E/2, 0), 'param_D * 0.9', 'param_E *0.9', is_parametric)
    lines = top_body_sketch.sketchCurves.sketchLines
    top_body_sketch.sketchCurves.sketchArcs.addFillet(lines.item(0), lines.item(0).endSketchPoint.geometry, lines.item(1), lines.item(1).startSketchPoint.geometry, 0.02 )
    top_body_sketch.sketchCurves.sketchArcs.addFillet(lines.item(1), lines.item(1).endSketchPoint.geometry, lines.item(2), lines.item(2).startSketchPoint.geometry, 0.02 )
    top_body_sketch.sketchCurves.sketchArcs.addFillet(lines.item(2), lines.item(2).endSketchPoint.geometry, lines.item(3), lines.item(3).startSketchPoint.geometry, 0.02 )
    top_body_sketch.sketchCurves.sketchArcs.addFillet(lines.item(3), lines.item(3).endSketchPoint.geometry, lines.item(0), lines.item(0).startSketchPoint.geometry, 0.02 )

    top_body = top_body_sketch.profiles.item(0)
    ext_top_body = model_3d_feature.create_extrude(root_comp,top_body, -0.2 * A  , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    ext_top_body.name = 'TopBody'
    #assign material to top body
    model_3d_utility.apply_material(app, design, ext_top_body.bodies.item(0),model_3d_utility.MATERIAL_ID_ALUMINUM)

    #Creating terminals
    xyPlane = root_comp.xYConstructionPlane
    sketch_terminal = sketches.add(xyPlane)
    sketch_terminal.name = 'TerminalSketch'
    model_3d_sketch.create_center_point_rectangle(sketch_terminal,adsk.core.Point3D.create(D1/2 + (D - D1)/4, E1/2 + (E - E1)/4, 0), 'param_D1/2 + (param_D - param_D1)/4', 'param_E1/2 + (param_E - param_E1)/4', adsk.core.Point3D.create(D/2, E/2, 0), '(param_D - param_D1)/2', '(param_E - param_E1)/2', is_parametric)
    circle = model_3d_sketch.create_center_point_circle(sketch_terminal, adsk.core.Point3D.create(D/2, E/2, 0), 'param_D/2', 'param_E/2', circleRadius * 2, '(param_D - param_D1)/5', is_parametric)
    circle.trim(adsk.core.Point3D.create(D/2, E/2, 0))
    terminal = sketch_terminal.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp,terminal, terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'Terminal'
    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_GOLD_POLISHED)
    
    #pin
    pin = model_3d_feature.create_mirror(root_comp, terminal, root_comp.yZConstructionPlane)
    model_3d_feature.create_mirror(root_comp, terminal, root_comp.xZConstructionPlane)
    model_3d_feature.create_mirror(root_comp, pin, root_comp.xZConstructionPlane)

    #Draw pin 1 marker
    if(D > E):
        max = D
    else:
        max = E
    circleRadius = max/50
    lines = top_body_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-D/2 + 0.1 * D + 2 * circleRadius , 0, 0))
    constraints = top_body_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, top_body_sketch.originPoint)
    if is_parametric:
        top_body_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-D/2, 0, 0)).parameter.expression = 'param_D/2 - 0.1 * param_D - 2 * param_D/50'

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-D/2 + 0.1 * D + 2 * circleRadius , -E/2 + 0.1 * E + 2 * circleRadius, 0))
    if is_parametric:
        top_body_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-E/2, 0, 0)).parameter.expression = 'param_E/2 - 0.1 * param_E - 2 * param_E/50'
    line2.isConstruction = True

    constraints.addHorizontal(line1)
    constraints.addVertical(line2)

    circles = top_body_sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(line2.endSketchPoint,circleRadius)
    top_body_sketch.sketchDimensions.addDiameterDimension(circle, adsk.core.Point3D.create(D/4,E/4,0), True).parameter.expression = 'param_D/25'
    ext_pin_one = top_body_sketch.profiles.item(1)
    pin_one = model_3d_feature.create_extrude(root_comp, ext_pin_one, -0.01, adsk.fusion.FeatureOperations.CutFeatureOperation)

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
    cornerconcave(params, design, target_comp)

import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            param.expression = 'param_A'

def create_fillet(root_comp, ext, distance):
    fillets = root_comp.features.filletFeatures
    edgeBottom = adsk.core.ObjectCollection.create()
    bottomEdges = ext.bodies.item(0).faces.item(0).edges
    for edgeI  in bottomEdges:
         edgeBottom.add(edgeI)
    bottomEdges = ext.bodies.item(0).faces.item(1).edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)
    bottomEdges = ext.bodies.item(0).faces.item(2).edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)
    bottomEdges = ext.bodies.item(0).faces.item(3).edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)

    radius1 = adsk.core.ValueInput.createByReal(distance)
    input2 = fillets.createInput()
    input2.addConstantRadiusEdgeSet(edgeBottom, radius1, True)
    input2.isG2 = False
    input2.isRollingBallCorner = True
    fillet2 = fillets.add(input2)

def chip(params, design = None, target_comp = None):

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
    E = params.get('E') or 0.18 #Body Width
    D = params.get('D') or 0.34 #Body Length
    A = params.get('A') or 0.07 #Body Height
    L = params.get('L') or 0.075 #Normal terminal width(L)
    L1 = params.get('L1') or 0.075 #Odd terminal width(B1)
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    if D < L + L1:
        D = L + L1 + 0.01

    filletRadius = 0.08 * L
    if(filletRadius > 0.004):
        filletRadius = 0.004

    c = A
    if('terminalThickness' not in params):
        terminal_thickness = c
    else:
        if(params['terminalThickness']<0):
            terminal_thickness = c
        else:
            terminal_thickness = min(params['terminalThickness'],c)

    color_r = params.get('color_r')
    if color_r == None: color_r = 10
    color_g = params.get('color_g')
    if color_g == None: color_g = 10
    color_b = params.get('color_b')
    if color_b == None: color_b = 10
    
    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("NormalTerminalWidth", "normal terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L1', L1, default_unit, _LCLZ("OddTerminalWidth", "odd terminal width"))
        if isUpdate:
            rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
            body_color = model_3d_utility.get_appearance(app, design, model_3d_utility.COLOR_NAME_CHIP_BODY)
            color_prop = adsk.core.ColorProperty.cast(body_color.appearanceProperties.itemById(model_3d_utility.COLOR_PROP_ID_DEFAULT))
            color_prop.value = rgb
            return

    # Create a new sketch.
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    sketch_body = sketches.add(xyPlane)
    #Create body
    body = model_3d_sketch.create_center_point_rectangle(sketch_body, adsk.core.Point3D.create(0, 0, 0), '', '',  adsk.core.Point3D.create(D/2, E/2, 0) , 'param_D', 'param_E', is_parametric)
    lines = sketch_body.sketchCurves.sketchLines;
    constraints = sketch_body.geometricConstraints
    line_odd = lines.addByTwoPoints(adsk.core.Point3D.create(D/2 - L1, E/2, 0), adsk.core.Point3D.create(D/2 - L1, -E/2, 0))
    constraints.addVertical(line_odd)
    line_even = lines.addByTwoPoints(adsk.core.Point3D.create(-D/2 + L, E/2, 0), adsk.core.Point3D.create(-D/2 + L, -E/2, 0))
    constraints.addVertical(line_even)
    constraints.addCoincident(line_even.startSketchPoint, body.item(0))
    constraints.addCoincident(line_odd.startSketchPoint, body.item(0))
    if is_parametric:
        sketch_body.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, line_odd.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(D/2 - L1, 0, 0)).parameter.expression = 'param_E'
        sketch_body.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, body.item(0).startSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/2 - L1, E/2, 0)).parameter.expression = 'param_L1'

        sketch_body.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, line_even.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-D/2 + L, 0, 0)).parameter.expression = 'param_E'
        sketch_body.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, body.item(0).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-D/2 + L, E/2, 0)).parameter.expression = 'param_L'

    #Extrude bodies
    ext_odd = model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(0), A, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_even =model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(2), A, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_body =model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(1), A, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    create_fillet(root_comp, ext_odd, filletRadius)
    create_fillet(root_comp, ext_even, filletRadius)
    body = ext_body.bodies.item(0)
    body.name = 'ChipBody'

    #Assign materials to body and terminals
    model_3d_utility.apply_material(app, design, ext_odd.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    model_3d_utility.apply_material(app, design, ext_even.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    model_3d_utility.apply_material(app, design, ext_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
    #assign appearance to body and terminals
    model_3d_utility.apply_rgb_appearance(app, design, ext_body.bodies.item(0),color_r, color_g, color_b, model_3d_utility.COLOR_NAME_CHIP_BODY)

    #Map the features parameters
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
    chip(params, design, target_comp)

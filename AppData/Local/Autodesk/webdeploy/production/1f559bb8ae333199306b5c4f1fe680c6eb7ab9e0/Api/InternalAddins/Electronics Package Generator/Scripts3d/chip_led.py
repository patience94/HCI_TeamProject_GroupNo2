import adsk.core, adsk.fusion, traceback, math

from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

paramDict = {"OddPin" :" param_A1","EvenPin": "param_A1", "ChipBody" : "param_A1", "LedOffset" : "param_A",
                 "LightOffset" : "param_A1" , "LedLight" : "param_A1/10" }

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            param.expression = paramDict[param.createdBy.name]

def create_fillet(root_comp, params, ext):
    distance = 0.08 * get_param(params, 'L')
    if(distance > 0.004):
        distance = 0.004
    fillets = root_comp.features.filletFeatures
    edgeBottom = adsk.core.ObjectCollection.create()
    bottomEdges = ext.bodies[0].faces[0].edges
    for edgeI  in bottomEdges:
         edgeBottom.add(edgeI)
    bottomEdges = ext.bodies[0].faces[1].edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)
    bottomEdges = ext.bodies[0].faces[2].edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)
    bottomEdges = ext.bodies[0].faces[3].edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)

    radius1 = adsk.core.ValueInput.createByReal(distance)
    input2 = fillets.createInput()
    input2.addConstantRadiusEdgeSet(edgeBottom, radius1, True)
    input2.isG2 = False
    input2.isRollingBallCorner = True
    fillet2 = fillets.add(input2)

def get_param(params, name):
    if name in params:
        if name == 'color_r' and params[name] == None:
            return 220
        if name == 'color_g' and params[name] == None:
            return 0
        if name == 'color_b' and params[name] == None:
            return 0
        else:
            return params[name]
    else:
        if (name == 'E'):
            return 0.18 #Body Width
        if (name == 'D'):
            return 0.34 #Body Length
        if (name == 'A'):
            return 0.07 #Body Height
        if (name == 'A1'):
            return 0.035 #Chip Height
        if (name == 'L'):
            return 0.075 #Normal Terminal Width
        if (name == 'L1'):
            return 0.34 #Odd Terminal Width
        if (name == 'is_parametric'):
            return 1
        if (name == 'color_r'):
            return 220
        if (name == 'color_g'):
            return 0
        if (name == 'color_b'):
            return 0

def create_chip_sketch(root_comp, params):
    # Create a new sketch.
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    sketch_body = sketches.add(xyPlane)
    #Create mid body
    body = model_3d_sketch.create_center_point_rectangle(sketch_body, adsk.core.Point3D.create(0, 0, 0), '0', '0',
                 adsk.core.Point3D.create((get_param(params, 'D'))/2, (get_param(params, 'E'))/2, 0) , 'param_D', 'param_E', get_param(params, 'is_parametric'))
    #Create side terminals
    lines = sketch_body.sketchCurves.sketchLines;
    constraints = sketch_body.geometricConstraints
    line_odd = lines.addByTwoPoints(adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), (get_param(params, 'E'))/2, 0),
                                    adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), -(get_param(params, 'E'))/2, 0))
    constraints.addVertical(line_odd)
    line_even = lines.addByTwoPoints(adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), (get_param(params, 'E'))/2, 0),
                                    adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), -(get_param(params, 'E'))/2, 0))
    constraints.addVertical(line_even)
    constraints.addCoincident(line_even.startSketchPoint, body.item(0))
    constraints.addCoincident(line_odd.startSketchPoint, body.item(0))
    if get_param(params, 'is_parametric'):
        sketch_body.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, line_odd.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), 0, 0)).parameter.expression = 'param_E'
        sketch_body.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, body.item(0).startSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), get_param(params, 'E')/2, 0)).parameter.expression = 'param_L1'

        sketch_body.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, line_even.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), 0, 0)).parameter.expression = 'param_E'
        sketch_body.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, body.item(0).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), get_param(params, 'E')/2, 0)).parameter.expression = 'param_L'

    return sketch_body

def create_chip_body(root_comp, params, design, sketch_body):
    #Extrude bodies
    ext_odd = model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(0), get_param(params, 'A1'), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_odd.name = 'OddPin'
    ext_even = model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(2), get_param(params, 'A1'), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_even.name = 'EvenPin'
    ext_body = model_3d_feature.create_extrude(root_comp, sketch_body.profiles.item(1), get_param(params, 'A1'), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_body.name = 'ChipBody'
    create_fillet(root_comp, params, ext_odd)
    create_fillet(root_comp, params, ext_even)
    body = ext_body.bodies.item(0)

    #Assign materials to body and terminals
    model_3d_utility.apply_material(app, design, ext_odd.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    model_3d_utility.apply_material(app, design, ext_even.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    model_3d_utility.apply_material(app, design, ext_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
    return body

def create_led_case(root_comp, params, design, body):
    #Create top cap
    led_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, get_param(params, 'A'))
    led_offset.name = 'LedOffset'
    sketches = root_comp.sketches
    led_sketch = sketches.add(led_offset)
    led_sketch.isLightBulbOn = False
    case = model_3d_sketch.create_center_point_rectangle(led_sketch, adsk.core.Point3D.create(0, 0, 0), '0', '0',
                        adsk.core.Point3D.create((get_param(params, 'D')) * 0.9, (get_param(params, 'E'))/2 * 0.9, 0),
                        'param_D * 0.9', 'param_E * 0.85', get_param(params, 'is_parametric'))
    
    #Create side terminals for cut
    lines = led_sketch.sketchCurves.sketchLines;
    constraints = led_sketch.geometricConstraints
    line_odd = lines.addByTwoPoints(adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), (get_param(params, 'E'))/2 * 0.05, 0),
                                    adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), -(get_param(params, 'E'))/2 * 0.05, 0))
    constraints.addVertical(line_odd)
    line_even = lines.addByTwoPoints(adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), (get_param(params, 'E'))/2 * 0.05, 0),
                                    adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), -(get_param(params, 'E'))/2 * 0.05, 0))
    constraints.addVertical(line_even)
    constraints.addCoincident(line_even.startSketchPoint, case.item(0))
    constraints.addCoincident(line_odd.startSketchPoint, case.item(0))
    if get_param(params, 'is_parametric'):
        led_sketch.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, line_odd.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), 0, 0)).parameter.expression = 'param_E * 0.9'
        led_sketch.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, case.item(0).startSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create((get_param(params, 'D')/2 - get_param(params, 'L1')), get_param(params, 'E')/2, 0)).parameter.expression = 'param_L1'

        led_sketch.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, line_even.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), 0, 0)).parameter.expression = 'param_E * 0.9'
        led_sketch.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, case.item(0).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create((-(get_param(params, 'D'))/2 + get_param(params, 'L')), get_param(params, 'E')/2, 0)).parameter.expression = 'param_L'

    led_prof = led_sketch.profiles.item(1)
    # Create loft feature
    loftFeats = root_comp.features.loftFeatures
    loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftSectionsObj = loftInput.loftSections
    loftSectionsObj.add(body.faces.item(4))
    loftSectionsObj.add(led_prof)
    loftInput.isSolid = True
    led = loftFeats.add(loftInput)
    led.name = 'LedGlassCase'
    led_case = led.bodies.item(0)

    #Apply material and appearance to led case
    model_3d_utility.apply_material(app, design, led_case,model_3d_utility.MATERIAL_ID_PLASTIC_TRANSP)
    model_3d_utility.apply_rgb_appearance(app, design, led_case,get_param(params, 'color_r'),
                    get_param(params, 'color_g'), get_param(params, 'color_b'), model_3d_utility.COLOR_NAME_CHIP_LED_CASE)


    return led_case

def create_led_light(root_comp, params, design):
    #Create light
    light_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, get_param(params, 'A1'))
    light_offset.name = 'LightOffset'
    sketches = root_comp.sketches
    light_sketch = sketches.add(light_offset)
    model_3d_sketch.create_center_point_rectangle(light_sketch, adsk.core.Point3D.create((get_param(params, 'L') - get_param(params, 'L1'))/2, 0, 0), '(param_L - param_L1)/2', '0',
                    adsk.core.Point3D.create((get_param(params, 'D'))/10, (get_param(params, 'E'))/10, 0), 'param_D/10', 'param_E/10', get_param(params, 'is_parametric'))
    light_prof = light_sketch.profiles.item(0)
    ext_light = model_3d_feature.create_extrude(root_comp, light_prof,(get_param(params, 'A1'))/10, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_light.name = 'LedLight'
    led_light = ext_light.bodies.item(0)

    #Apply material and appearance to led light source
    model_3d_utility.apply_material(app, design, led_light,model_3d_utility.MATERIAL_ID_CERAMIC)
    model_3d_utility.apply_emissive_appearance(app, design, led_light, 50000.0,
                    get_param(params, 'color_r'), get_param(params, 'color_g'), get_param(params, 'color_b'), model_3d_utility.COLOR_NAME_CHIP_LED_LIGHT)

    return led_light

def user_param(design, params, default_unit):
    if get_param(params, 'is_parametric'):
        isUpdate = False
        res_1 = model_3d_utility.process_user_param(design, 'param_A', get_param(params, 'A'), default_unit, _LCLZ("BodyHeight", "body height"))
        res_2 = model_3d_utility.process_user_param(design, 'param_A1', get_param(params, 'A1'), default_unit, _LCLZ("ChipHeight", "chip height"))
        res_3 = model_3d_utility.process_user_param(design, 'param_E', get_param(params, 'E'), default_unit, _LCLZ("BodyWidth", "body width"))
        res_4 = model_3d_utility.process_user_param(design, 'param_D', get_param(params, 'D'), default_unit, _LCLZ("BodyLength", "body length"))
        res_5 = model_3d_utility.process_user_param(design, 'param_L', get_param(params, 'L'), default_unit, _LCLZ("NormalTerminalWidth", "normal terminal width"))
        res_6 = model_3d_utility.process_user_param(design, 'param_L1', get_param(params, 'L1'), default_unit, _LCLZ("OddTerminalWidth", "odd terminal width"))
        isUpdate = res_1  or res_2 or res_3 or res_4 or res_5 or res_6
        if isUpdate:
            #update the color and luminance value
            model_3d_utility.update_emissive_appearance(app, design, 50000.0, get_param(params, 'color_r'), get_param(params, 'color_g'), get_param(params, 'color_b'), model_3d_utility.COLOR_NAME_CHIP_LED_LIGHT)
            model_3d_utility.update_rgb_appearance(app, design, get_param(params, 'color_r'), get_param(params, 'color_g'), get_param(params, 'color_b'), model_3d_utility.COLOR_NAME_CHIP_LED_CASE, model_3d_utility.COLOR_PROP_ID_SURFACE)
            model_3d_utility.update_rgb_appearance(app, design, get_param(params, 'color_r'), get_param(params, 'color_g'), get_param(params, 'color_b'), model_3d_utility.COLOR_NAME_CHIP_LED_CASE, model_3d_utility.COLOR_PROP_ID_TRANSPARENT)
            return True
        else:
            return False
    else :
        return False

def chip_led(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp
    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    #param creation and updation
    param_updated = user_param(design, params, default_unit)
    if param_updated == True:
        return

    #Create chip sketch
    chip_sketch = create_chip_sketch(root_comp,params)
    #Create chip body
    body_face = create_chip_body(root_comp, params, design, chip_sketch)
    #Create top case
    create_led_case(root_comp, params, design, body_face)
    #Create LED light
    create_led_light(root_comp, params, design)

    #Map the features parameters
    if get_param(params, 'is_parametric'):
        map_model_parameters(root_comp)

def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, target_comp = None):
    chip_led(params, design, target_comp)

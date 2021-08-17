import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance" :
            if param.createdBy.name=="Body":
                param.expression = 'param_A -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.001))  #need convert the value to default unit
            if param.createdBy.name=="EndTerminal":
                param.expression = 'param_A'
            if param.createdBy.name=="MidTerminal":
                param.expression = 'param_A'
        if param.role=="uSpaceDistance":
            if param.createdBy.name=="PinPatternEnd":
                param.expression = '-param_E + param_L'
            if param.createdBy.name=="PinPatternMid":
                param.expression = '-param_e'
        if param.role=="countU":
            if param.createdBy.name=="PinPatternMid":
                param.expression = 'param_pins/2 - 2'


def chiparray2sideconvex(params, design = None, target_comp = None):

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
    e = params.get('e') or 0.064 #Pin pitch
    pins = params.get('DPins') or 10 #Total pins
    A = params.get('A') or 0.07 #Body Height
    b = params.get('b') or 0.04 #Terminal Width
    b1 = params.get('b1') or 0.055 #End terminal width
    D = params.get('D') or 0.34 #Body length
    E = params.get('E') or 0.24 #Body Width
    L = params.get('L') or 0.055 #Terminal length
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    EE = E - 2 * L #Real Body width(EE)

    offsetValue = 0.001
    gapVertical = ((pins/2 -1) * e + b1)/2
    
    color_r = params.get('color_r')
    if color_r == None: color_r = 10
    color_g = params.get('color_g')
    if color_g == None: color_g = 10
    color_b = params.get('color_b')
    if color_b == None: color_b = 10

    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_pins', pins, '', _LCLZ("TotalPins", "total pins"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_b1', b1, default_unit, _LCLZ("EndTerminalWidth", "end terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalLength", "terminal length"))
        if isUpdate:
            rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
            body_color = model_3d_utility.get_appearance(app, design, model_3d_utility.COLOR_NAME_CHIP_BODY)
            color_prop = adsk.core.ColorProperty.cast(body_color.appearanceProperties.itemById(model_3d_utility.COLOR_PROP_ID_DEFAULT))
            color_prop.value = rgb
            return

    # Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, offsetValue/2)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    model_3d_sketch.create_center_point_rectangle(body_sketch,adsk.core.Point3D.create(0, 0, 0) , '', '',  adsk.core.Point3D.create(E/2 - L, D/2, 0),'param_E - 2 * param_L', 'param_D', is_parametric)
    extBody = body_sketch.profiles.item(0)
    ext_body = model_3d_feature.create_extrude(root_comp,extBody, A - offsetValue , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    ext_body.name = 'Body'
    chip_body = ext_body.bodies.item(0)
    chip_body.name = 'ChipBody'

    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, chip_body, model_3d_utility.MATERIAL_ID_CERAMIC)
    # assign the apparance to body
    model_3d_utility.apply_rgb_appearance(app, design, chip_body, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_CHIP_BODY)

    #Create end Terminals
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch = sketches.add(xyPlane)
    pin_sketch.name = 'SketchPin'
    centerPoint = adsk.core.Point3D.create(E/2 - L/2, (pins/2 - 1) * e/2, 0)
    endPoint = adsk.core.Point3D.create(E/2 , (pins/2 - 1) * e/2 + b1/2, 0)
    model_3d_sketch.create_center_point_rectangle(pin_sketch, centerPoint, 'param_E/2 -param_L/2' , '(param_pins/2 - 1) * param_e/2'  ,endPoint, 'param_L', 'param_b1', is_parametric)
    ext_term = pin_sketch.profiles.item(0)
    term = model_3d_feature.create_extrude(root_comp,ext_term, A , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    term.name = 'EndTerminal'
    # assign pysical material to terminal
    model_3d_utility.apply_material(app, design, term.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    pattern_pin_end = model_3d_feature.create_mirror_and_pattern(root_comp, term, E - L, 2, root_comp.xConstructionAxis, root_comp.xZConstructionPlane)
    pattern_pin_end.name = 'PinPatternEnd'

    #Create middle terminals
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch_mid = sketches.add(xyPlane)
    pin_sketch_mid.name = 'SketchPinMid'
    centerPoint = adsk.core.Point3D.create(E/2 - L/2, (pins/2 - 3) * e/2, 0)
    endPoint = adsk.core.Point3D.create(E/2 , (pins/2 - 3) * e/2 + b/2, 0)
    model_3d_sketch.create_center_point_rectangle(pin_sketch_mid, centerPoint, 'param_E/2 -param_L/2'  , '(param_pins/2 - 3) * param_e/2'  ,endPoint, 'param_L', 'param_b', is_parametric)
    ext_term_mid = pin_sketch_mid.profiles.item(0)
    term = model_3d_feature.create_extrude(root_comp,ext_term_mid, A , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    term.name = 'MidTerminal'
    # assign pysical material to terminal
    model_3d_utility.apply_material(app, design, term.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    
    pattern_pin_mid = model_3d_feature.create_mirror_and_pattern(root_comp, term, e, pins/2 - 2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pin_mid.name = 'PinPatternMid'
    
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
    chiparray2sideconvex(params, design, target_comp)

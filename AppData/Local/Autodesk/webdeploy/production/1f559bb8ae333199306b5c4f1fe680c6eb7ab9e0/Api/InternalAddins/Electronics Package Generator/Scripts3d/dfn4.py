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
                param.expression = 'param_A'

        if param.role=="uSpaceDistance":
            param.expression = '-param_d'

def dfn4(params, design = None, target_comp = None):

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
    e = params.get('e') or 0.045 #Vertical pin pitch(e)
    d =params.get('d') or 0.075 #Horizontal pin pitch(d)
    b = params.get('b') or 0.028 #Normal terminal width(b)
    L = params.get('L') or 0.04 #Normal terminal length(L)
    E = params.get('E') or 0.08 #Body width(E)
    D = params.get('D') or 0.125 #Body length(D)
    A = params.get('A') or 0.04 #Body height(A)
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    thick = model_3d_utility.get_dfn_terminal_thickness(root_comp, A)

    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("VerticalPinPitch", "vertical pin pitch"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("NormalTerminalWidth", "normal terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("NormalTerminalLength", "normal terminal length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_d', d, default_unit, _LCLZ("HorizontalPinPitch", "horizontal pin pitch"))
        if isUpdate:
            terminal = root_comp.features.itemByName('Terminal')
            terminal.timelineObject.rollTo(True)
            dist_def = adsk.fusion.DistanceExtentDefinition.cast(terminal.extentOne)
            dist = adsk.fusion.ModelParameter.cast(dist_def.distance)
            dist.value = thick
            design.timeline.moveToEnd()
            return

    # Create terminals
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch = sketches.add(xyPlane)
    model_3d_sketch.create_center_point_rectangle(pin_sketch, adsk.core.Point3D.create(d/2, e/2, 0),'param_d/2', 'param_e/2', adsk.core.Point3D.create(d/2 + L/2, e/2 + b/2, 0), 'param_L', 'param_b', is_parametric)
    ext_ter = pin_sketch.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp,ext_ter, thick , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'Terminal'
     # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    model_3d_feature.create_mirror_and_pattern(root_comp, terminal, d, 2, root_comp.xConstructionAxis, root_comp.xZConstructionPlane)

    #Create body
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(D/2, E/2, 0), 'param_D', 'param_E', is_parametric)
    body_profile = body_sketch.profiles.item(0)

    extrudes = root_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(body_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    isChained = False
    extent_to_entity = adsk.fusion.ToEntityExtentDefinition.create(terminal.endFaces[0], isChained)
    extrude_input.setOneSideExtent(extent_to_entity, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    extrude_body = extrudes.add(extrude_input)
    extrude_body.name = 'Body'
    model_3d_utility.apply_material(app, design, extrude_body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

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
    dfn4(params, design, target_comp)

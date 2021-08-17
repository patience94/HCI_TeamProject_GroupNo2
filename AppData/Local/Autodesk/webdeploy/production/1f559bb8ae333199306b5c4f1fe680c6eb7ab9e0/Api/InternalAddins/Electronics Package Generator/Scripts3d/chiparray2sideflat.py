import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance" :
            if param.createdBy.name =="Body":
                param.expression = 'param_A -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.001)) #need convert the value to default unit
            if param.createdBy.name =="GapVert":
                param.expression = 'param_A'
            if param.createdBy.name =="LeadVertJoin":
                param.expression = 'param_A'

        if param.role=="countU" :
            if param.createdBy.name =="GapMirrorVert":
                param.expression = 'param_pins/2'
            if param.createdBy.name =="MirrorVert":
                param.expression = 'param_pins/2'

        if param.role=="uSpaceDistance" :
            if param.createdBy.name =="GapMirrorVert":
                param.expression = '-param_e'
            if param.createdBy.name =="MirrorVert":
                param.expression = '-param_e'


def chiparray2sideflat(params, design = None, target_comp = None):

    e = params.get('e') or 0.127 #Pin pitch(e)
    pins = params.get('DPins') or 8 #Pins
    A = params.get('A') or 0.07 #Body height(A)
    b = params.get('b') or 0.095 #Terminal width(b)
    D = params.get('D') or 0.538 #Body length(D)
    E = params.get('E') or 0.24 #Body width(E)
    L = params.get('L') or 0.055 #Terminal length(L)

    offsetValue = 0.001
    br = (b - 0.02 )/2 #Terminal hole radius(br)
    isFlatLead = params['isFlatLead'] if 'isFlatLead' in params else 0
    is_parametric = params['isParametric'] if 'isParametric' in params else 1
    gapVertical = (pins/2 - 1) * e + b

    color_r = params.get('color_r')
    if color_r == None: color_r = 10
    color_g = params.get('color_g')
    if color_g == None: color_g = 10
    color_b = params.get('color_b')
    if color_b == None: color_b = 10

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
        isUpdate = False
        isUpdate =model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_pins', pins, '', _LCLZ("TotalPins", "total pins"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalLength", "terminal length"))
        if isUpdate:
            rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
            body_color = model_3d_utility.get_appearance(app, design, model_3d_utility.COLOR_NAME_CHIP_BODY)
            color_prop = adsk.core.ColorProperty.cast(body_color.appearanceProperties.itemById(model_3d_utility.COLOR_PROP_ID_DEFAULT))
            color_prop.value = rgb

            lead_vert = root_comp.features.itemByName('LeadVertJoin')
            sketch_vert = root_comp.sketches.itemByName('PinSketchVert')

            entity = adsk.core.ObjectCollection.create()
            entity.add(sketch_vert.profiles.item(1))
            entity.add(sketch_vert.profiles.item(0))

            lead_vert.timelineObject.rollTo(True)
            if isFlatLead:
                lead_vert.profile = entity
            else:
                lead_vert.profile = sketch_vert.profiles.item(1)

            dist_def_vert = adsk.fusion.DistanceExtentDefinition.cast(lead_vert.extentOne)
            vert_dist = adsk.fusion.ModelParameter.cast(dist_def_vert.distance)
            vert_dist.expression = 'param_A'
            design.timeline.moveToEnd()

            return

    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    pin_sketch_vert = sketches.add(xyPlane)
    pin_sketch_vert.name = 'PinSketchVert'

    #Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, offsetValue/2)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    E_param = 'param_E -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.005))
    model_3d_sketch.create_center_point_rectangle(body_sketch,adsk.core.Point3D.create(0, 0, 0) , '', '',  adsk.core.Point3D.create(E/2 - offsetValue/2, D/2, 0), E_param, 'param_D', is_parametric)
    ext_body = body_sketch.profiles.item(0)
    body = model_3d_feature.create_extrude(root_comp,ext_body, A - offsetValue , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    body.name = 'Body'
    mid_body = body.bodies.item(0)
    mid_body.name = 'ChipBody'

    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, mid_body, model_3d_utility.MATERIAL_ID_CERAMIC)
    # assign the apparance to body
    model_3d_utility.apply_rgb_appearance(app, design, mid_body, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_CHIP_BODY)


    #Draw terminals
    model_3d_sketch.create_center_point_rectangle(pin_sketch_vert, adsk.core.Point3D.create(E/2 - L/2, (pins/2 - 1) * e/2, 0) , 'param_E/2 - param_L/2' , '((param_pins/2) - 1) * param_e/2',
                                                         adsk.core.Point3D.create(E/2 , (pins/2 - 1) * e/2 + b/2, 0), 'param_L', 'param_b', is_parametric)
    b_param = 'param_b -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.02))
    circle = model_3d_sketch.create_center_point_circle(pin_sketch_vert, adsk.core.Point3D.create(E/2 , (pins/2 - 1) * e/2, 0), 'param_E/2', '((param_pins/2) - 1) * param_e/2',
                                                        b - 0.02, b_param, is_parametric)
    circle.trim(adsk.core.Point3D.create(E, 0, 0))

    entities = adsk.core.ObjectCollection.create()
    entities.add(pin_sketch_vert.profiles.item(1))
    entities.add(pin_sketch_vert.profiles.item(2))
    gap = model_3d_feature.create_extrude(root_comp, entities, A , adsk.fusion.FeatureOperations.CutFeatureOperation )
    gap.name = 'GapVert'
    mirror = model_3d_feature.create_mirror_and_pattern(root_comp, gap,  e,  pins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    mirror.name = 'GapMirrorVert'

    if isFlatLead:
        profile = adsk.core.ObjectCollection.create()
        profile.add(pin_sketch_vert.profiles.item(1))
        profile.add(pin_sketch_vert.profiles.item(0))
    else:
        profile = pin_sketch_vert.profiles.item(1)

    ext_terminal = model_3d_feature.create_extrude(root_comp, profile, A , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )

    # assign pysical material to terminal
    model_3d_utility.apply_material(app, design, ext_terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    ext_terminal.name = 'LeadVertJoin'
    mirror_vert = model_3d_feature.create_mirror_and_pattern(root_comp, ext_terminal,  e,  pins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    mirror_vert.name = 'MirrorVert'

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
    chiparray2sideflat(params, design, target_comp)

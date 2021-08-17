from ..Scripts3d import soic, bga, qfp, qfn, sod, sodfl, sotfl, sot23, sot223, sot143, dpak, dfn2, dfn3, dfn4, crystal, chip, melf,\
molded, axial_resistor, axial_polarized_capacitor, axial_diode, axial_fuse, dip, header_straight, header_right_angle, header_straight_socket,\
header_right_angle_socket, son, hc49, oscillator_l, oscillator_j, chiparray2sideconvex, chiparray2sideflat, chiparray4sideflat, radial_inductor, radial_round_led, cornerconcave,\
plcc, soj, radial_ecap, ecap, female_standoff, male_female_standoff, snap_lock, chip_led


# define the package type as constant. so they can be used in different places. 
PKG_TYPE_SOIC   = 'soic'
PKG_TYPE_BGA    = 'bga'
PKG_TYPE_QFP    = 'qfp'
PKG_TYPE_QFN    = 'qfn'
PKG_TYPE_SOD    = 'sod'
PKG_TYPE_SODFL  = 'sodfl'
PKG_TYPE_SOTFL  = 'sotfl'
PKG_TYPE_SOT23  = 'sot23'
PKG_TYPE_SOT223 = 'sot223'
PKG_TYPE_SOT143 = 'sot143'
PKG_TYPE_DPAK   = 'dpak'
PKG_TYPE_DFN2   = 'dfn2'
PKG_TYPE_DFN3   = 'dfn3'
PKG_TYPE_DFN4   = 'dfn4'
PKG_TYPE_CRYSTAL = 'crystal'
PKG_TYPE_CHIP   = 'chip'
PKG_TYPE_MELF   = 'melf'
PKG_TYPE_MOLDEDBODY = 'moldedbody'
PKG_TYPE_AXIAL_RESISTOR = 'axial_resistor'
PKG_TYPE_AXIAL_POLARIZED_CAPACITOR = 'axial_polarized_capacitor'
PKG_TYPE_AXIAL_DIODE = 'axial_diode'
PKG_TYPE_AXIAL_FUSE = 'axial_fuse'
PKG_TYPE_DIP    = 'dip'
PKG_TYPE_HEADER_STRAIGHT = 'header_straight'
PKG_TYPE_HEADER_RIGHT_ANGLE = 'header_right_angle'
PKG_TYPE_HEADER_STRAIGHT_SOCKET = 'header_straight_socket'
PKG_TYPE_HEADER_RIGHT_ANGLE_SOCKET = 'header_right_angle_socket'
PKG_TYPE_SON = 'son'
PKG_TYPE_CRYSTAL_HC49 = 'crystal_hc49'
PKG_TYPE_OSCILLATOR_L = 'oscillator_l'
PKG_TYPE_OSCILLATOR_J = 'oscillator_j'
PKG_TYPE_CHIPARRAY2SIDECONVEX = 'chiparray2sideconvex'
PKG_TYPE_CHIPARRAY2SIDEFLAT = 'chiparray2sideflat'
PKG_TYPE_CHIPARRAY4SIDEFLAT = 'chiparray4sideflat'
PKG_TYPE_RADIAL_INDUCTOR = 'radial_inductor'
PKG_TYPE_RADIAL_ROUND_LED = 'radial_round_led'
PKG_TYPE_PLCC = 'plcc'
PKG_TYPE_CORNERCONCAVE = 'cornerconcave'
PKG_TYPE_SOJ = 'soj'
PKG_TYPE_RADIAL_ECAP = 'radial_ecap'
PKG_TYPE_ECAP = 'ecap'
PKG_TYPE_FEMALE_STANDOFF = 'female_standoff'
PKG_TYPE_MALE_FEMALE_STANDOFF = 'male_female_standoff'
PKG_TYPE_SNAP_LOCK = 'snap_lock'
PKG_TYPE_CHIP_LED = 'chip_led'

def runScript(params, packageType, design, targetComponent):
    #print(params)
    if packageType == PKG_TYPE_SOIC:
        soic.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_BGA:
        bga.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_QFP:
        qfp.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_QFN:
        qfn.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOD:
        sod.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SODFL:
        sodfl.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOTFL:
        sotfl.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOT23:
        sot23.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOT223:
        sot223.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOT143:
        sot143.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_DPAK:
        dpak.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_DFN2:
        dfn2.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_DFN3:
        dfn3.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_DFN4:
        dfn4.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CRYSTAL:
        crystal.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CHIP:
        chip.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_MELF:
        melf.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_MOLDEDBODY:
        molded.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_AXIAL_RESISTOR:
        axial_resistor.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_AXIAL_POLARIZED_CAPACITOR:
        axial_polarized_capacitor.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_AXIAL_DIODE:
        axial_diode.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_AXIAL_FUSE:
        axial_fuse.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_DIP:
        dip.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_HEADER_STRAIGHT:
        header_straight.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_HEADER_RIGHT_ANGLE:
        header_right_angle.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_HEADER_STRAIGHT_SOCKET:
        header_straight_socket.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_HEADER_RIGHT_ANGLE_SOCKET:
        header_right_angle_socket.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SON:
        son.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CRYSTAL_HC49:
        hc49.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_OSCILLATOR_L:
        oscillator_l.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_OSCILLATOR_J:
        oscillator_j.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CHIPARRAY2SIDECONVEX:
        chiparray2sideconvex.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CHIPARRAY2SIDEFLAT:
        chiparray2sideflat.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CHIPARRAY4SIDEFLAT:
        chiparray4sideflat.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_RADIAL_INDUCTOR:
        radial_inductor.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_RADIAL_ROUND_LED:
        radial_round_led.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_PLCC:
        plcc.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CORNERCONCAVE:
        cornerconcave.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SOJ:
        soj.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_RADIAL_ECAP:
        radial_ecap.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_ECAP:
        ecap.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_FEMALE_STANDOFF:
        female_standoff.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_MALE_FEMALE_STANDOFF:
        male_female_standoff.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_SNAP_LOCK:
        snap_lock.runWithInput(params, design, targetComponent)
    elif packageType == PKG_TYPE_CHIP_LED:
        chip_led.runWithInput(params, design, targetComponent)
    else:
        return False

    return True

def generate(design, targetComponent, modelInfo):
    return runScript(modelInfo['parameters'], modelInfo['type'], design, targetComponent)